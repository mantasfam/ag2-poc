"""Test database connection and queries."""
from src.db.connection import get_db_engine
from sqlalchemy import text

def test_db_connection():
    """Test database connection and sample data."""
    engine = get_db_engine()
    
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT author_name, timestamp, content 
            FROM discord_messages 
            LIMIT 5
        """))
        
        print("\nSuccessfully connected to database!")
        print("\nSample messages:")
        print("-" * 80)
        
        for row in result:
            print(f"User: {row.author_name}")
            print(f"Time: {row.timestamp}")
            print(f"Message: {row.content}")
            print("-" * 80)

if __name__ == "__main__":
    test_db_connection() 