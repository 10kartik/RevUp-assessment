import logging
from fastapi import APIRouter, HTTPException
from langchain_fireworks import Fireworks
from schemas.chat import ChatRequest, ChatResponse
from services.context_manager import SessionManager
from agents import (
    IntentClassifier,
    SentimentAnalysisAgent,
    TaskPlannerAgent,
    KnowledgeAgent,
    SummarizationAgent
)
import os
from dotenv import load_dotenv

# Initialize logging
logger = logging.getLogger()

# Load environment variables
load_dotenv()
API_KEY = os.getenv("FIREWORKS_API_KEY")

# Initialize FastAPI router
router = APIRouter()

# Initialize the Fireworks LLM with specific parameters
llm = Fireworks(
    model="accounts/fireworks/models/deepseek-v3",
    api_key=API_KEY,
    temperature=0.4,  # Adjust temperature
    max_tokens=16000,  # Adjust max tokens
    top_k=30,  # Adjust top_k
    top_p=1  # Adjust top_p
)

# Initialize session manager
session_manager = SessionManager()

# Initialize agents
intent_classifier = IntentClassifier(llm)
sentiment_analyzer = SentimentAnalysisAgent(llm)
task_planner = TaskPlannerAgent(llm)
knowledge_agent = KnowledgeAgent(llm)
summarization_agent = SummarizationAgent(llm)

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Chat endpoint to handle user queries and route them to appropriate agents.

    Args:
        request (ChatRequest): The request object containing user query and session ID.

    Returns:
        ChatResponse: The response object containing sentiment, response, session ID, and agents used.
    """
    try:
        logger.info(f"Invoking /chat endpoint with query: {request.user_query}")
        
        # Get session history
        history = session_manager.get_history(request.session_id)
        logger.info(f"Session {request.session_id} history length: {len(history)}")
        print(f"Session {request.session_id} history length: {len(history)}")

        # Step 1: Intent classification
        agents_to_prompt = intent_classifier.generate(request.user_query)
        logger.info(f"Classified intent: {agents_to_prompt}")
        print(f"Classified intent: {agents_to_prompt}")

        agent_used = []
        
        # Step 2: Always run sentiment analysis
        sentiment_response = sentiment_analyzer.generate(request.user_query)
        sentiment_response = sentiment_response.upper().strip()
        logger.info(f"Sentiment response: {sentiment_response}")
        print(f"Sentiment response: {sentiment_response}")
        agent_used.append("sentiment_analysis")
        
        logger.info(f"Agents to prompt: {agents_to_prompt.keys()}")
        # Step 3: Route to appropriate agents
        primary_response = ""
        for agent in agents_to_prompt:
            if "task_planning" == agent:
                print("Routing to Task Planner agent")
                logger.info(f"Routing to *Task Planner* agent with query: {request.user_query}")
                primary_response += task_planner.generate(agents_to_prompt["task_planning"], history)
                agent_used.append("task_planner")
            elif "knowledge" == agent:
                print("Routing to Knowledge agent")
                logger.info(f"Routing to *Knowledge agent* with query: {request.user_query}")
                primary_response += knowledge_agent.generate(agents_to_prompt["knowledge"], history)
                agent_used.append("knowledge")
            elif "summarization" == agent:
                print("Routing to Summarization agent")
                logger.info(f"Routing to *Summarization agent* with history length: {history}")
                primary_response += summarization_agent.generate(history)
                agent_used.append("summarization")
            else:
                print("No specific agent matched, using general response")
                logger.info("No specific agent matched, using general response")
                primary_response += "I'll need more information to help with that."

        primary_response = primary_response.strip()

        # Step 4: Combine responses
        logger.info(f"Combined response: {primary_response[:100]}...")

        # Step 5: Update context
        session_manager.update_history(
            request.session_id,
            request.user_query,
            primary_response
        )

        logger.info(f"Session {request.session_id} updated successfully.")

        return ChatResponse(
            sentiment=sentiment_response.upper(),
            response=primary_response,
            session_id=request.session_id,
            agent_used=agent_used
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset")
async def reset_endpoint():
    """
    Reset endpoint to clear all session histories.

    Returns:
        dict: A message indicating that the session history has been reset.
    """
    session_manager.sessions = {}
    return {"message": "Session history reset successfully."}