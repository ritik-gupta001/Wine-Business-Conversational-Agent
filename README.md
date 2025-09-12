# Wine Concierge Conversational Agent 🍷

A sophisticated AI-powered chatbot designed to serve as a virtual wine concierge for Napa Valley Premium Winery. This agent provides information about wines, tasting experiences, current weather, and more.

## Video Overview



https://github.com/user-attachments/assets/a4f8163b-9e56-4495-95e4-26a60c7a13c2


## Features

- 🍇 **Wine Information**: Details about available wines, pricing, and tasting notes
- 🕒 **Tasting Room Hours**: Information about operating hours and reservations
- 🌤️ **Real-time Weather**: Current weather conditions in Napa Valley
- 📅 **Events**: Updates about winery events and experiences
- 🔍 **Web Search**: Current wine trends and news
- 💬 **Natural Conversation**: Engaging, sommelier-like interactions

## Technology Stack

- **Backend**: FastAPI
- **AI/ML**: LangChain with OpenAI GPT
- **Frontend**: HTML/Jinja2 Templates
- **APIs**: OpenWeather API, DuckDuckGo Search
- **Containerization**: Docker

## Prerequisites

- Python 3.8+
- OpenAI API Key
- OpenWeather API Key
- Docker (optional, for containerized deployment)

## Environment Variables

Create a `.env` file with the following:

```env
OPENAI_API_KEY=your_openai_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd wine-concierge-conversational-agent
```

2. Create and activate a virtual environment:
```bash
python -m venv wine_env
# On Windows
wine_env\Scripts\activate
# On Unix/MacOS
source wine_env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Local Development
```bash
python main.py
```
Visit http://localhost:8000 in your browser.

### Docker Deployment
```bash
docker-compose up -d
```

## Project Structure

- `main.py`: FastAPI application entry point
- `wine_agent.py`: Core conversational agent implementation
- `tools.py`: Utility tools (Weather, Web Search, Knowledge Base)
- `test_agent.py`: Test suite for the agent
- `templates/`: HTML templates for the web interface
- `wine_business_info.txt`: Knowledge base for wine business information

## Testing

Run the test suite to verify functionality:
```bash
python test_agent.py
```

## API Endpoints

- `GET /`: Main chat interface
- `GET /health`: Health check endpoint
- `POST /chat`: Chat endpoint for agent interaction

## Features in Detail

### Wine Knowledge Base
- Comprehensive information about wines
- Pricing details
- Tasting notes
- Business information

### Weather Integration
- Real-time weather data for Napa Valley
- Temperature, conditions, and humidity
- Powered by OpenWeather API

### Web Search Capability
- Current wine trends
- Industry news
- Event information

## Docker Support

The application includes Docker support for containerized deployment:
- Multi-stage build for optimized image size
- Volume mounts for persistent data
- Health checks for container monitoring
- Environment variable configuration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenAI for GPT integration
- OpenWeather for weather data
- DuckDuckGo for web search capabilities
