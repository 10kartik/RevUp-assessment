import logging
logger = logging.getLogger()
from typing import List, Dict
from agents.base import BaseAgent
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class KnowledgeAgent(BaseAgent):
    def __init__(self, llm):
        self.chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate.from_template(
                """You are an AI assistant specialized in Answering the factual question and have access to a vast amount of General knowledge.
                Use previous messages in the conversation to provide coherent responses. Previous conversation: {history}. {history}
                Always prioritize answering the question in the most recent message and do not rely on previous context unless explicitly referenced.
                (most recent) Question: {query}
                Provide a concise, accurate, and relevant answer. Do not provide unnecessary information and avoid overly complex or verbose responses.
                If the user’s request is unclear, ask clarifying questions
                Do not repeat the same information unless specifically requested or necessary for clarity.
                Answer:"""
            )
        )
    
    def generate(self, query: str, history: List[Dict]) -> str:
        print(f"Answering knowledge question: {query}")
        return self.chain.run(query=query, history=history)