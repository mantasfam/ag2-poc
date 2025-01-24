"""Knowledge base for retrieving and formatting context."""
from typing import List, Dict
from src.db.connection import search_similar_messages

class KnowledgeBase:
    """Manages knowledge retrieval and context building."""
    
    def get_context(self, query: str) -> str:
        """Get formatted context for a query."""
        # Get relevant messages from database only
        messages = search_similar_messages(query, limit=5)
        
        # Format them into context string
        context = "Here are some relevant past messages:\n\n"
        for msg in messages:
            context += f"User {msg['author']} said: {msg['content']}\n"
            context += f"(Posted at: {msg['timestamp']}, Relevance: {1-msg['distance']:.4f})\n\n"
            if msg['knowledge']:
                context += f"Additional info: {msg['knowledge']}\n\n"
        
        return context

    def get_structured_context(self, query: str) -> List[Dict]:
        """
        Get context as structured data for more complex processing.
        
        Args:
            query: User's question or input
            
        Returns:
            List of message dictionaries with metadata
        """
        return self.db.get_relevant_messages(query) 