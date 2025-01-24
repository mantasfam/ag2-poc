"""Test the RAG-powered assistant."""
from src.rag.assistant import GameAssistant

def test_rag_assistant():
    """Test the assistant's ability to answer questions with context."""
    assistant = GameAssistant()
    
    # Test questions
    questions = [
        "How do I increase my reputation in the game?",
        "Where can I find rare pets?",
        "What are the best farming strategies?"
    ]
    
    print("\nTesting RAG Assistant:")
    print("-" * 80)
    
    for question in questions:
        print(f"\nQuestion: {question}")
        print("-" * 40)
        
        response = assistant.answer_question(question, analyze_context=True)
        
        print("Context Used:")
        print(response["context_used"])
        print("\nAnswer:")
        print(response["answer"])
        if "context_analysis" in response:
            print("\nContext Analysis:")
            print(response["context_analysis"])
        print("-" * 40)

if __name__ == "__main__":
    test_rag_assistant() 