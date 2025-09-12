from fastapi import FastAPI, Request, Body
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from dotenv import load_dotenv
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

# Dummy Wine Agent (replace with your real agent later)
class SimpleWineConcierge:
    def chat(self, message: str) -> str:
        return f"You said: {message}. I'm your wine concierge 🍷"

# Initialize the wine concierge agent
try:
    from wine_agent import WineConciergeAgent
except ImportError:
    WineConciergeAgent = SimpleWineConcierge

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
async def chat_endpoint(payload: dict = Body(...)):
    """Chat endpoint for the wine concierge"""
    try:
        if not wine_agent:
            return JSONResponse(
                content={"error": "Wine concierge agent not available"},
                status_code=503
            )

        message = payload.get("message", "").strip()
        if not message:
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

if __name__ == "__main__":
    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", 8000))
    logger.info(f"Starting Wine Concierge server on {host}:{port}")
    uvicorn.run("main:app", host=host, port=port, reload=True)
