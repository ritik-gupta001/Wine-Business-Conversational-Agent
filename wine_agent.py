import os
from typing import Dict, Any, List, TypedDict, Literal
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain.tools import tool
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
import json
from tools import WeatherTool, WebSearchTool, WineKnowledgeBase

# Define the state of our agent
class AgentState(TypedDict):
    messages: List[dict]
    user_input: str
    next_action: str

# Create tool functions using @tool decorator
@tool
def get_weather_info(city: str = "Napa, CA") -> str:
    """Get current weather information for a location."""
    weather_tool = WeatherTool()
    return weather_tool.get_weather(city)

@tool
def search_web_info(query: str) -> str:
    """Search the web for current information."""
    search_tool = WebSearchTool()
    return search_tool.search_web(query)

@tool
def get_wine_knowledge(query: str = "") -> str:
    """Get information about the wine business, wines, tasting room, events, etc."""
    kb = WineKnowledgeBase()
    if query:
        return kb.search_knowledge(query)
    return kb.get_business_info()

class WineConciergeAgent:
    def __init__(self):
        # Initialize the language model
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # System prompt for the wine concierge
        self.system_prompt = """You are a knowledgeable and friendly wine concierge for Napa Valley Premium Winery. 
        Your role is to help customers with information about:
        1. Our wines, prices, and tasting notes
        2. Tasting room hours and reservations
        3. Events and experiences
        4. Current weather in Napa Valley
        5. General wine knowledge and recommendations
        6. Any current wine-related news or information through web search
        
        Always be helpful, professional, and enthusiastic about wine. Be conversational and engaging, 
        as if you're a sommelier helping customers in person.
        
        When you need information, I'll provide it through tools. Just focus on giving great responses."""

    def classify_and_respond(self, user_input: str) -> str:
        """Simple classification and response method"""
        user_input_lower = user_input.lower()
        
        # Get context based on user input
        context = ""
        
        try:
            # Check for wine business questions
            if any(word in user_input_lower for word in ["wine", "tasting", "vineyard", "bottle", "price", "hours", "reservation", "event", "cabernet", "chardonnay", "merlot", "pinot"]):
                wine_info = get_wine_knowledge(user_input)
                context = f"Wine Business Information: {wine_info}"
            
            # Check for weather questions
            elif any(word in user_input_lower for word in ["weather", "temperature", "rain", "sunny", "climate"]):
                weather_info = get_weather_info("Napa, CA")
                context = f"Weather Information: {weather_info}"
            
            # Check for web search questions
            elif any(word in user_input_lower for word in ["news", "latest", "recent", "current", "search", "find", "trend"]):
                search_info = search_web_info(user_input)
                context = f"Web Search Results: {search_info}"
            
            # For general wine questions, also include wine knowledge
            else:
                wine_info = get_wine_knowledge(user_input)
                context = f"Wine Business Information: {wine_info}"
        
        except Exception as e:
            print(f"Error getting context: {e}")
            context = "I'm having trouble accessing some information right now."
        
        # Create the prompt
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=f"""User question: {user_input}
            
            Available Information:
            {context}
            
            Please provide a helpful, engaging response as a wine concierge. Use the information above if relevant.
            Keep your response conversational and friendly.""")
        ]
        
        try:
            # Get LLM response
            response = self.llm.invoke(messages)
            return response.content
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request right now. Please try again. Error: {str(e)}"

    def chat(self, user_input: str) -> str:
        """Main chat interface"""
        return self.classify_and_respond(user_input)

# Example usage
if __name__ == "__main__":
    print("Testing Wine Concierge Agent...")
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("Please set your OPENAI_API_KEY in the .env file")
        exit(1)
    
    agent = WineConciergeAgent()
    
    # Test the agent
    test_questions = [
        "What wines do you have available?",
        "What's the weather like today?",
        "What are the latest wine trends in Napa Valley?",
        "Tell me about your tasting room hours",
    ]
    
    for question in test_questions:
        print(f"\n🍷 Q: {question}")
        try:
            response = agent.chat(question)
            print(f"A: {response}")
        except Exception as e:
            print(f"Error: {e}")
        print("-" * 80)