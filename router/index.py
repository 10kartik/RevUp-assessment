import logging
logger = logging.getLogger()

from fastapi import APIRouter, HTTPException
from langchain_fireworks import Fireworks
from schemas.chat import ChatRequest, ChatResponse
from services.context_manager import SessionManager
from agents import (
    IntentClassifier,
    SentimentAnalysisAgent,
    TaskPlannerAgent,
    KnowledgeAgent
)

router = APIRouter()

import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("FIREWORKS_API_KEY")
# Initialize components
llm = Fireworks(model="accounts/fireworks/models/llama-v3p1-8b-instruct",
                api_key=API_KEY,
                temperature=0.4,  # Adjust temperature
                max_tokens=10000,   # Adjust max tokens
                top_k=30,         # Adjust top_k
                top_p=1,        # Adjust top_p
                frequency_penalty=0.5,  # Adjust frequency penalty
                presence_penalty=0.2)

session_manager = SessionManager()

# Initialize agents
intent_classifier = IntentClassifier(llm)
sentiment_analyzer = SentimentAnalysisAgent(llm)
task_planner = TaskPlannerAgent(llm)
knowledge_agent = KnowledgeAgent(llm)

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Get session history
        history = session_manager.get_history(request.session_id)
        logger.info(f"Session {request.session_id} history length: {len(history)}")

        # Step 1: Intent classification
        intent = intent_classifier.generate(request.user_query, history)
        logger.info(f"Classified intent: {intent}")

        # Step 2: Always run sentiment analysis
        sentiment_response = sentiment_analyzer.generate(request.user_query, history)
        
        # Step 3: Route to appropriate agent
        if "task_planning" in intent:
            print("Routing to Task Planner agent")
            primary_response = task_planner.generate(request.user_query, history)
            agent_used = "task_planner"
        elif "knowledge" in intent:
            print("Routing to Knowledge agent")
            primary_response = knowledge_agent.generate(request.user_query, history)
            agent_used = "knowledge"
        else:
            print("No specific agent matched, using general response")
            primary_response = "I'll need more information to help with that."
            agent_used = "general"

        # Step 4: Combine responses
        combined_response = f"""
                            Sentiment: {sentiment_response}
                            Response: {primary_response}
                            """
        
        logger.info(f"Combined response: {combined_response[:100]}...")

        # Step 5: Update context
        session_manager.update_history(
            request.session_id,
            request.user_query,
            combined_response
        )

        return ChatResponse(
            response=combined_response,
            session_id=request.session_id,
            agent_used=agent_used
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))