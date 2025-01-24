"""Captain agent coordinates expert knowledge."""
import os
import autogen
from src.rag.knowledge_base import KnowledgeBase
from typing import Dict

class CaptainAgent:
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        
        config = {
            "model": "gpt-4-turbo-preview",
            "api_key": os.getenv("OPENAI_API_KEY"),
            "temperature": 0.3,        # Lower = more focused answers
            "top_p": 0.9,             # Slightly focused token selection
            "presence_penalty": 0.2,   # Avoid repetitive answers
            "frequency_penalty": 0.1   # Slightly prefer unique words
        }
        
        self.expert = autogen.AssistantAgent(
            name="GameExpert",
            system_message="""You are an expert on the Pixels game. 
            ONLY use the provided context to answer questions.
            If the context doesn't contain enough information, say so.
            Keep responses informal and brief.
            Never make assumptions or provide information not found in the context.""",
            llm_config={"config_list": [config]}
        )
        
        self.user = autogen.UserProxyAgent(
            name="User",
            human_input_mode="NEVER",
            code_execution_config={"use_docker": False},
            max_consecutive_auto_reply=0  # Prevent endless loops
        )

    def get_response(self, question: str) -> Dict:
        # Get context from database
        context = self.knowledge_base.get_context(question)
        
        # Create prompt with context
        prompt = f"""Use this context (but don't mention it): {context}
Question: {question}"""
        
        # Get single response without any follow-up
        self.user.initiate_chat(self.expert, message=prompt, clear_history=True)
        
        return {"answer": self.expert.last_message()["content"]} 