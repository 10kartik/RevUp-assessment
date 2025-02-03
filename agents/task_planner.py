import logging
logger = logging.getLogger()
from typing import List, Dict
from agents.base import BaseAgent
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class TaskPlannerAgent(BaseAgent):
    def __init__(self, llm):
        self.chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate.from_template(
                """You are an AI assistant specialized in task planning, management, and organization.
                Help break down and prioritize tasks. Provide short, relevant, bullet-pointed task plans and instructions relevant to the query.
                Use previous messages in the conversation to provide coherent responses. Previous conversation: {history}.
                Always prioritize answering the query in the most recent message and do not rely on previous context unless explicitly referenced.
                (most recent) Query: {query}
                Respond in a friendly and professional manner.
                If the user’s request is unclear, ask clarifying questions
                Do not repeat the same information unless specifically requested or necessary for clarity.
                Response:"""
            )
        )
    
    def generate(self, query: str, history: List[Dict]) -> str:
        print(f"Generating task plan for: {query}")
        return self.chain.run(query=query, history=history)