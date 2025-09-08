# 🍷 Napa Valley Wine Concierge - Conversational Agent

A sophisticated conversational AI agent built with LangGraph that serves as an intelligent concierge for a Napa Valley wine business. The agent combines document retrieval, real-time data access (weather, web search), and natural conversation to provide comprehensive customer support.

## ✨ Features

- **📚 Knowledge Base**: Answers questions about wines, tastings, events, and business information
- **🌤️ Real-time Weather**: Provides current weather conditions for Napa Valley
- **🔍 Web Search**: Performs real-time web searches for current information
- **💬 Natural Conversation**: Maintains context and provides human-like responses
- **🌐 Modern Web UI**: Beautiful, responsive chat interface
- **🚀 Multiple Interfaces**: REST API, WebSocket, and web UI
- **🏗️ Production Ready**: Docker support, health checks, and monitoring

## 🏗️ Architecture

The system is built using **LangGraph** (preferred over LangChain) with a state-based agent architecture:

```
User Input → Intent Detection → Context Retrieval → Tool Execution → Response Generation
```

### Core Components

1. **LangGraph Agent**: State-based conversation flow with tool integration
2. **FastAPI Backend**: REST API and WebSocket support
3. **Tool System**: Modular tools for knowledge base, weather, and web search
4. **Web Interface**: Modern React-like UI with real-time chat
5. **Vector Store**: FAISS-based document retrieval (expandable)

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- OpenAI API key
- (Optional) OpenWeatherMap API key for real weather data

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/wine-concierge-agent.git
cd wine-concierge-agent
```

2. **Set up Python environment**:
```bash
python -m venv myenv
venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment**:
```bash
cp .env.template .env
# Edit .env with your API keys
```

4. **Run the application**:
```bash
python main.py
```

5. **Access the interface**:
   - Web UI: http://localhost:8000
   - API docs: http://localhost:8000/docs
   - WebSocket: ws://localhost:8000/ws

### Docker Setup

```bash
# Build and run with Docker
docker build -t wine-concierge .
docker run -p 8000:8000 --env-file .env wine-concierge
```

### Docker Compose (with Redis)

```yaml
version: '3.8'
services:
  wine-concierge:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - redis
  
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

## 🛠️ Usage Examples

### Web Interface
Visit http://localhost:8000 for the interactive chat interface.

### REST API
```bash
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "What wines do you have available?"}'
```

### WebSocket (JavaScript)
```javascript
const ws = new WebSocket('ws://localhost:8000/ws');
ws.send(JSON.stringify({
    message: "What's the weather like today?",
    timestamp: new Date().toISOString()
}));
```

### Python Client
```python
import requests

response = requests.post(
    "http://localhost:8000/api/chat",
    json={"message": "Tell me about your Cabernet Sauvignon"}
)
print(response.json())
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key (required) | - |
| `WEATHER_API_KEY` | OpenWeatherMap API key | Mock data |
| `MODEL_NAME` | OpenAI model to use | gpt-4o-mini |
| `TEMPERATURE` | Model temperature | 0.7 |
