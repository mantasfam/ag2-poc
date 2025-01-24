"""Test the Captain Agent system."""
from src.agents.captain import CaptainAgent

def test_captain_agent():
    """Test the Captain Agent's ability to answer questions with experts."""
    captain = CaptainAgent()
    
    # Test questions that require different experts
    questions = [
        "How do I get more reputation and what are its benefits?",  # Game Mechanic
        "What's the best way to make money through farming?",      # Economy Expert
        "Where can I find the bat pet and how do I train it?",    # Pet Master
        "What's the best weapon for PvP combat?",                 # Combat Expert
        "How do I join a guild and what are the benefits?",       # Social Guide
    ]
    
    print("\nTesting Captain Agent:")
    print("-" * 80)
    
    for question in questions:
        print(f"\nQuestion: {question}")
        print("-" * 40)
        
        response = captain.get_response(question)
        
        print("Context Used:")
        print(response["context_used"])
        print("\nAnswer:")
        print(response["answer"])
        print("\nChat History:")
        for msg in response["chat_history"]:
            print(f"{msg['role']}: {msg['content'][:100]}...")
        print("-" * 40)

if __name__ == "__main__":
    test_captain_agent() 