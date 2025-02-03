import logging
logger = logging.getLogger()
from typing import List, Dict
from agents.base import BaseAgent
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class SummarizationAgent(BaseAgent):
    def __init__(self, llm):
        self.chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate.from_template(
                """You are an AI assistant specialized in summarizing the conversation. Summarize the conversation history and provide a concise summary of the key points discussed.
                Previous conversation: {history}.
                Response:"""
            )
        )
    
    def generate(self, history: List[Dict]) -> str:
        print(f"Analyzing Summarization for history: {history}")
        response = self.chain.run(history=history)
        logger.info(f"Summarization response: {response}")
        return response