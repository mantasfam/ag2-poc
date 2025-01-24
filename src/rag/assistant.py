"""Main RAG-powered assistant interface."""
from typing import Dict
from .knowledge_base import KnowledgeBase
from .prompts import ANSWER_TEMPLATE, CONTEXT_ANALYSIS_TEMPLATE

class GameAssistant:
    """RAG-powered game assistant."""
    
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        
    def answer_question(self, question: str, analyze_context: bool = False) -> Dict:
        """
        Answer a question using RAG.
        
        Args:
            question: User's question
            analyze_context: Whether to include context analysis
            
        Returns:
            Dictionary containing answer and optional analysis
        """
        # Get relevant context
        context = self.knowledge_base.get_context(question)
        
        # Format prompt for the main answer
        prompt = ANSWER_TEMPLATE.format(
            context=context,
            question=question
        )
        
        # TODO: Send to LLM for completion
        answer = "TODO: Implement LLM call"
        
        response = {
            "answer": answer,
            "context_used": context
        }
        
        # Optional context analysis
        if analyze_context:
            analysis_prompt = CONTEXT_ANALYSIS_TEMPLATE.format(context=context)
            # TODO: Send to LLM for analysis
            response["context_analysis"] = "TODO: Implement analysis"
            
        return response 