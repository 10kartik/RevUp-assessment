import logging
logger = logging.getLogger()
from typing import List, Dict
from agents.base import BaseAgent
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class SentimentAnalysisAgent(BaseAgent):
    def __init__(self, llm):
        self.chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate.from_template(
                """You are an AI assistant specialized in Analysing the sentiments of the user based on the provided query. Classify the sentiment as 'positive', 'negative', or 'neutral'.
                Query: {query}
                Response:"""
            )
        )
    
    def generate(self, query: str, history: List[Dict]) -> str:
        print(f"Analyzing sentiment for query: {query}")
        response = self.chain.run(query=query)
        logger.info(f"Sentiment response: {response}")
        return response