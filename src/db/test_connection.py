"""Test database connection and queries."""
from connection import get_db_engine
from sqlalchemy import text

def test_db_connection():
    """Test database connection and print some messages."""
    try:
        engine = get_db_engine()
        with engine.connect() as conn:
            # Simple SELECT query to get 5 messages
            result = conn.execute(
                text("""
                    SELECT content, username, timestamp
                    FROM messages
                    LIMIT 5
                """)
            )
            
            print("\nSuccessfully connected to database!")
            print("\nSample messages:")
            print("-" * 80)
            
            for row in result:
                print(f"User: {row.username}")
                print(f"Time: {row.timestamp}")
                print(f"Message: {row.content}")
                print("-" * 80)
                
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")

if __name__ == "__main__":
    test_db_connection() 