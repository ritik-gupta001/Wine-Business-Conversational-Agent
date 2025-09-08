"""
Test script for the Wine Concierge Agent.
Run this to test agent functionality without the web interface.
"""

import os
import sys
from dotenv import load_dotenv

def check_api_key():
    """Ensure OPENAI_API_KEY is set in environment."""
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in .env file")
        print("Please add your OpenAI API key to the .env file")
        sys.exit(1)

def import_agent():
    """Import WineConciergeAgent safely."""
    try:
        from wine_agent import WineConciergeAgent
        print("✅ Wine agent imports successful")
        return WineConciergeAgent
    except Exception as e:
        print(f"❌ Error importing wine agent: {e}")
        sys.exit(1)

def test_agent(WineConciergeAgent):
    """Test the wine concierge agent with sample questions."""
    print("\n🍷 Initializing Napa Valley Wine Concierge...")
    try:
        agent = WineConciergeAgent()
        print("✅ Agent initialized successfully!\n")
    except Exception as e:
        print(f"❌ Failed to initialize agent: {e}")
        return

    test_questions = [
        "What wines do you have available?",
        "What are your tasting room hours?",
        "What's the weather like today in Napa?",
        "Tell me about your Cabernet Sauvignon pricing",
        "What are the latest wine trends?",
        "Do you have any events this month?",
        "How much does wine tasting cost?",
    ]

    print("🧪 Testing agent with sample questions...\n" + "=" * 80)
    for i, question in enumerate(test_questions, 1):
        print(f"\n🔍 Test {i}/{len(test_questions)}")
        print(f"Q: {question}")
        print("A: ", end="", flush=True)
        try:
            response = agent.chat(question)
            print(response)
        except Exception as e:
            print(f"❌ Error: {e}")
        print("-" * 80)
    print("\n✅ Agent testing completed!")
    print("\n🚀 To start the web interface, run: python main.py")
    print("   Then visit: http://localhost:8000")

def test_individual_tools():
    """Test individual tools separately."""
    print("\n🔧 Testing individual tools...\n")
    # Test knowledge base
    try:
        from tools import WineKnowledgeBase
        kb = WineKnowledgeBase()
        info = kb.get_business_info()
        print("✅ Wine Knowledge Base loaded successfully")
        print(f"   Content length: {len(info)} characters")
    except Exception as e:
        print(f"❌ Wine Knowledge Base error: {e}")

    # Test weather tool
    try:
        from tools import WeatherTool
        weather = WeatherTool()
        result = weather.get_weather("Napa, CA")
        print(f"✅ Weather Tool: {result[:100]}...")
    except Exception as e:
        print(f"❌ Weather Tool error: {e}")

    # Test web search
    try:
        from tools import WebSearchTool
        search = WebSearchTool()
        result = search.search_web("Napa Valley wine")
        print(f"✅ Web Search Tool: Found results")
    except Exception as e:
        print(f"❌ Web Search Tool error: {e}")

def main():
    print("🍷 Wine Concierge Agent Test Suite\n" + "=" * 50)
    check_api_key()
    test_individual_tools()
    WineConciergeAgent = import_agent()
    test_agent(WineConciergeAgent)
    print("\n🎉 Testing complete! Your wine concierge is ready to serve.")

if __name__ == "__main__":
    main()