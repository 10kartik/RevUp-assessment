import logging
import json
from typing import Dict
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.base import BaseAgent

logger = logging.getLogger()

class IntentClassifier(BaseAgent):
    def __init__(self, llm):
        self.chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate(
                input_variables=["query"],  # ✅ Explicitly declare input variables
                template="""You are an AI assistant expert in classifying the intent of the query. 
                Analyze the query and identify components for different agents. 

                **Output dictonary format:**
                - `"knowledge"`: Sub-query for knowledge agent (if applicable)
                - `"task_planning"`: Sub-query for task planning agent (if applicable)
                - `"summarization"`: Sub-query for summarization agent (if applicable)

                **Example:**
                **Input:** "Which country won the 2014 FIFA World Cup? Can you help plan my hiking trip to the Grand Canyon?"
                **Output:** {{"knowledge": "Who won 2014 FIFA World Cup", "task_planning": "Help plan my hiking trip"}}

                **Return valid dictonary format only**.

                Query: {query}
                Response:
                """
            )
        )
    
    def generate(self, query: str) -> Dict:
        print(f"Classifying intent for query: {query}")
        
        # Call the LLM with the correct input
        result = self.chain.run(query=query)
        
        logger.info(f"Intent classification result: {result}")

        # Debugging: Print raw response
        print(f"Raw LLM output: {result}")

        # Ensure the output is a valid JSON object
        try:
            parsed_result = json.loads(result)
            print(f"Intent classification parsed result: {parsed_result}")
        except json.JSONDecodeError:
            logger.error(f"Failed to parse intent classification result: {result}")
            return {}

        return parsed_result