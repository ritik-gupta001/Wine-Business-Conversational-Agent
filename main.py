from fastapi import FastAPI, Request, Form, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
try:
    from wine_agent import WineConciergeAgent
except ImportError:
    from wine_agent import SimpleWineConcierge as WineConciergeAgent
import uvicorn
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Napa Valley Wine Concierge", description="AI-powered wine business assistant")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Initialize the wine concierge agent
try:
    wine_agent = WineConciergeAgent()
    logger.info("Wine Concierge Agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Wine Concierge Agent: {e}")
    wine_agent = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main chat interface"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "agent_ready": wine_agent is not None}

@app.post("/chat")
async def chat_endpoint(request: Request, message: str = Form(...)):
    """Chat endpoint for the wine concierge"""
    try:
        if not wine_agent:
            return JSONResponse(
                content={"error": "Wine concierge agent not available"}, 
                status_code=503
            )
        
        if not message.strip():
            return JSONResponse(
                content={"error": "Please provide a message"}, 
                status_code=400
            )
        
        # Get response from the agent
        response = wine_agent.chat(message)
        
        return JSONResponse(content={
            "user_message": message,
            "bot_response": response,
            "status": "success"
        })
    
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        return JSONResponse(
            content={
                "error": "Sorry, I encountered an error processing your request. Please try again.",
                "details": str(e)
            }, 
            status_code=500
        )

@app.get("/api/chat/{message}")
async def chat_api(message: str):
    """GET endpoint for chat (for testing)"""
    try:
        if not wine_agent:
            return JSONResponse(
                content={"error": "Wine concierge agent not available"}, 
                status_code=503
            )
        
        response = wine_agent.chat(message)
        
        return JSONResponse(content={
            "user_message": message,
            "bot_response": response,
            "status": "success"
        })
    
    except Exception as e:
        logger.error(f"Error processing API chat request: {e}")
        return JSONResponse(
            content={
                "error": "Sorry, I encountered an error processing your request.",
                "details": str(e)
            }, 
            status_code=500
        )

@app.post("/api/weather")
async def weather_api(data: dict = Body(...)):
    """POST endpoint to get weather by lat/lon"""
    try:
        lat = data.get("lat")
        lon = data.get("lon")
        if lat is None or lon is None:
            return JSONResponse(content={"error": "Latitude and longitude required"}, status_code=400)
        from tools import WeatherTool
        weather_tool = WeatherTool()
        result = weather_tool.get_weather(lat, lon)
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Error in weather API: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        logger.warning("OpenAI API key not found. Please set OPENAI_API_KEY in .env file")
    
    # Get host and port from environment variables
    host = os.getenv("APP_HOST", "localhost")
    port = int(os.getenv("APP_PORT", 8000))
    
    logger.info(f"Starting Wine Concierge server on {host}:{port}")
    uvicorn.run(
        "main:app", 
        host=host, 
        port=port, 
        reload=True,
        log_level="info"

    )
