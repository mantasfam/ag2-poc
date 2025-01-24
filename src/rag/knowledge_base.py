"""Knowledge base for retrieving and formatting context."""
from typing import List, Dict
from src.db.connection import search_similar_messages

class KnowledgeBase:
    """Manages knowledge retrieval and context building."""
    
    def get_context(self, query: str) -> str:
        """Get formatted context for a query."""
        messages = search_similar_messages(query)
        
        # Sort by relevance
        messages.sort(key=lambda x: x['distance'])
        
        context = "Recent information about this topic:\n\n"
        for msg in messages:
            # Only include highly relevant knowledge (adjust threshold if needed)
            if 1-msg['distance'] > 0.5:  
                context += f"• {msg['content']}\n"
                if msg.get('source_ids'):
                    context += f"(Reference IDs: {msg['source_ids']})\n"
                context += "\n"
        
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