"""Test knowledge lookup functionality."""
from src.db.connection import get_db_engine, get_related_knowledge
from sqlalchemy import text

def test_knowledge_lookup():
    """Test finding related knowledge for messages."""
    engine = get_db_engine()
    
    with engine.connect() as conn:
        # Test specific message ID
        message_id = "1232784999812698168"
        knowledge = get_related_knowledge(conn, message_id)
        
        print("\nTesting knowledge lookup:")
        print("-" * 80)
        print(f"Message ID: {message_id}")
        print(f"Related Knowledge: {knowledge}")
        
        # Also show the raw message data
        message = conn.execute(
            text("""
                SELECT content, author_name, timestamp 
                FROM discord_messages 
                WHERE message_id = :msg_id
            """),
            {"msg_id": message_id}
        ).first()
        
        if message:
            print("\nOriginal Message:")
            print(f"Content: {message.content}")
            print(f"Author: {message.author_name}")
            print(f"Time: {message.timestamp}")

if __name__ == "__main__":
    test_knowledge_lookup() 