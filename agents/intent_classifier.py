import logging
logger = logging.getLogger()
from typing import List, Dict
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from agents.base import BaseAgent

class IntentClassifier(BaseAgent):
    def __init__(self, llm):
        self.chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate.from_template(
                """You are an AI assistant expert in Classifying the intent of the query.
                Choices: task_planning, knowledge, other.
                Query: {query}
                Intent:"""
            )
        )
    
    def generate(self, query: str, history: List[Dict]) -> str:
        print(f"Classifying intent for query: {query}")
        result = self.chain.run(query=query)
        logger.info(f"Intent classification result: {result}")
        return result.strip().lower()