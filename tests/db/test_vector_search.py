"""Test vector similarity search functionality."""
from src.db.connection import search_similar_messages

def test_vector_search():
    """Test searching for similar messages."""
    # Test queries
    queries = [
        "How do I get reputation in the game?",
        "Where can I find the bat pet?",
        "What are the best farming locations?"
    ]
    
    print("\nTesting vector similarity search:")
    print("-" * 80)
    
    for query in queries:
        print(f"\nQuery: {query}")
        print("-" * 40)
        
        results = search_similar_messages(query, limit=3)
        
        for result in results:
            print(f"\nUser: {result['username']}")
            print(f"Time: {result['timestamp']}")
            print(f"Message: {result['content']}")
            print(f"Distance: {result['distance']:.4f}")
            print("-" * 40)

if __name__ == "__main__":
    test_vector_search() 