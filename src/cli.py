"""Command line interface for the Captain Agent."""
from src.agents.captain import CaptainAgent

def main():
    expert = CaptainAgent()  # Enable debug mode to see context
    
    print("\nPixels Game Assistant 🎮")
    print("Ask me anything! (type 'exit' to quit)")
    print("-" * 40)
    
    while True:
        question = input("\n> ")
        if question.lower() in ['exit', 'quit', 'q']:
            break
            
        response = expert.get_response(question)
        print(f"\n{response['answer']}")

if __name__ == "__main__":
    main() 