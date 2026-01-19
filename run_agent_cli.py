import asyncio
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Ensure the current directory is in the Python path
sys.path.append(os.getcwd())

try:
    from backend.api.agent.core import process_request
except ImportError as e:
    print(f"Error importing backend: {e}")
    print("Make sure you are running this script from the project root directory.")
    sys.exit(1)

async def main():
    print("=============================================")
    print("🤖 Tickwen AI Agent CLI")
    print("   Type 'exit' or 'quit' to stop.")
    print("=============================================")
    
    # Check for API Keys
    if not os.getenv("GEMINI_API_KEY"):
        print("\n⚠️  WARNING: GEMINI_API_KEY is not set.")
        print("   Set GEMINI_API_KEY to your Gemini Key in your environment or .env file.")
        print("---------------------------------------------\n")

    history = []
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye! 👋")
                break
            
            if not user_input.strip():
                continue

            print("Agent is thinking...", end="\r")
            
            # Call the agent
            response_text = await process_request(user_input, history)
            
            # Clear loading text
            print(" " * 20, end="\r")
            print(f"Agent: {response_text}")
            
            # Update history manually for this simple CLI
            # (The Runner.run handles context within a session if we used SQLiteSession,
            # but since we are stateless in core.py, we manage list manually here)
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": response_text})
            
        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
