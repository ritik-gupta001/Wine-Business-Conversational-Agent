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
myenv\Scripts\activate
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

### Extending the Knowledge Base

Add your wine business information to the `WINE_BUSINESS_DATA` constant in `main.py`, or implement a proper vector database:

```python
# For production, use a vector database
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# Load documents
documents = load_documents("path/to/your/wine_docs")
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents, embeddings)

# Use in retrieval tool
@tool
def search_wine_knowledge(query: str) -> str:
    docs = vectorstore.similarity_search(query, k=3)
    return "\n".join([doc.page_content for doc in docs])
```

## 🧪 Testing

Run the test suite:

```bash
# Unit tests
pytest tests/ -v

# Integration tests
pytest tests/integration/ -v

# Test specific functionality
pytest tests/test_agent.py::test_wine_knowledge_retrieval -v
```

### Test Examples

```python
def test_wine_knowledge():
    response = client.post("/api/chat", json={
        "message": "What's your most expensive wine?"
    })
    assert "Reserve Cabernet Sauvignon" in response.json()["response"]

def test_weather_functionality():
    response = client.post("/api/chat", json={
        "message": "What's the weather like?"
    })
    assert "temperature" in response.json()["response"].lower()
```

## 📊 Monitoring and Analytics

### Health Check Endpoint
```bash
curl http://localhost:8000/health
```

### Metrics Collection
The system logs conversation metrics:
- Response times
- Tool usage frequency
- Popular queries
- Error rates

### Production Monitoring

```python
# Add to main.py for production monitoring
import logging
from prometheus_client import Counter, Histogram

# Metrics
CONVERSATION_COUNTER = Counter('conversations_total', 'Total conversations')
RESPONSE_TIME = Histogram('response_time_seconds', 'Response time')

# Usage in endpoints
@app.post("/api/chat")
async def chat_endpoint(message: ChatMessage):
    CONVERSATION_COUNTER.inc()
    with RESPONSE_TIME.time():
        # ... existing code
```

## 🚀 Deployment

### Production Checklist

- [ ] Set strong API keys in environment variables
- [ ] Enable HTTPS with reverse proxy (nginx/Caddy)
- [ ] Set up proper logging and monitoring
- [ ] Configure rate limiting
- [ ] Set up database for conversation history
- [ ] Enable CORS for web clients
- [ ] Set up backup for knowledge base

### AWS Deployment

```bash
# Using AWS ECS with Fargate
aws ecs create-cluster --cluster-name wine-concierge

# Deploy with Terraform or CDK
terraform apply -var="openai_api_key=${OPENAI_API_KEY}"
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: wine-concierge
spec:
  replicas: 3
  selector:
    matchLabels:
      app: wine-concierge
  template:
    metadata:
      labels:
        app: wine-concierge
    spec:
      containers:
      - name: wine-concierge
        image: wine-concierge:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-keys
              key: openai-api-key
```

## 🎯 Agent Capabilities

### Current Tools

1. **Wine Knowledge Base**
   - Wine catalog and pricing
   - Tasting room information
   - Events and experiences
   - Vineyard practices

2. **Weather Service**
   - Current conditions
   - Temperature and humidity
   - Weather recommendations

3. **Web Search**
   - Current wine industry news
   - General information lookup
   - Real-time data retrieval

### Conversation Examples

**Wine Information:**
```
User: "What's your most expensive wine?"
Agent: "Our most expensive wine is the Reserve Cabernet Sauvignon 2019 at $150/bottle. 
        It's a limited production wine aged 24 months in French oak with exceptional 
        depth and complexity. Would you like to schedule a tasting?"
```

**Weather Integration:**
```
User: "Is it good weather for a vineyard visit today?"
Agent: "The current weather in Napa Valley is 72°F and partly cloudy - perfect 
        conditions for a vineyard visit! Our tasting room is open daily from 
        10 AM to 5 PM. Would you like to make a reservation?"
```

**Complex Queries:**
```
User: "I'm planning a corporate event for 50 people next month"
Agent: "Perfect! We specialize in corporate events and can accommodate 50 people. 
        Our packages include private tastings, wine pairings, and vineyard tours. 
        Let me search for current availability and pricing options for you..."
```

## 🔄 Future Enhancements

### Planned Features

1. **Advanced RAG System**
   - Multi-modal document processing
   - Citation tracking
   - Context-aware chunking

2. **Personalization**
   - User preferences memory
   - Purchase history integration
   - Personalized recommendations

3. **Integration Capabilities**
   - CRM system integration
   - Inventory management
   - Booking system API

4. **Advanced Analytics**
   - Conversation insights
   - Customer sentiment analysis
   - Sales conversion tracking

### Roadmap

- **Phase 1**: Core functionality (✅ Complete)
- **Phase 2**: Production deployment and monitoring
- **Phase 3**: Advanced personalization and CRM integration
- **Phase 4**: Multi-language support and voice interface

## 🤝 Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and test thoroughly
4. Submit a pull request with detailed description

### Code Style

```bash
# Format code
black main.py tests/
isort main.py tests/

# Type checking
mypy main.py

# Linting
flake8 main.py tests/
```

### Testing Guidelines

- Write tests for all new features
- Maintain >80% code coverage
- Test both success and error cases
- Include integration tests for API endpoints

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/wine-concierge-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/wine-concierge-agent/discussions)
- **Email**: support@napavalleypremiumwines.com

## 🙏 Acknowledgments

- **LangChain/LangGraph**: Core agent framework
- **FastAPI**: High-performance web framework
- **OpenAI**: Language model capabilities
- **Anthropic**: Claude for development assistance

---

**Built with ❤️ for Napa Valley Premium Wines**

*Turning conversations into connections, one bottle at a time.*
