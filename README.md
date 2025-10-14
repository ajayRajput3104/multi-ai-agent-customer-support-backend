# AI Customer Support API

Multi-agent AI-powered customer support system using LangGraph and Groq.

## Features

- 🤖 Multi-agent workflow with LangGraph
- 📊 Automatic query categorization (Technical/Billing/General)
- 😊 Sentiment analysis
- 🚀 FastAPI backend
- 🐳 Docker support
- ☁️ Ready for Render deployment

## Local Development

### Prerequisites

- Python 3.11+
- Groq API key

### Setup

1. Clone the repository
2. Create virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file:

   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

5. Run the application:

   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

6. Access the API:
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## Docker

### Build and run locally:

```bash
docker build -t ai-support-api .
docker run -p 8000:8000 -e GROQ_API_KEY=your_key ai-support-api
```

## Deployment on Render

### Method 1: Using Dockerfile (Recommended)

1. Push code to GitHub
2. Go to Render Dashboard → New → Web Service
3. Connect your repository
4. Configure:

   - **Name**: ai-customer-support-api
   - **Environment**: Docker
   - **Region**: Choose closest to your users
   - **Branch**: main
   - **Plan**: Starter (or Free)

5. Add Environment Variables:

   - `GROQ_API_KEY`: Your Groq API key
   - `ENVIRONMENT`: production
   - `LOG_LEVEL`: INFO

6. Click "Create Web Service"

### Method 2: Using render.yaml (Blueprint)

1. Include `render.yaml` in your repository
2. Go to Render Dashboard → New → Blueprint
3. Connect repository
4. Add `GROQ_API_KEY` in environment variables
5. Deploy

## API Endpoints

### POST /api/v1/query

Process a customer query

**Request:**

```json
{
  "query": "How do I reset my password?"
}
```

**Response:**

```json
{
  "success": true,
  "data": {
    "category": "Technical",
    "sentiment": "Neutral",
    "response": "To reset your password, follow these steps..."
  },
  "message": "Query processed successfully"
}
```

### GET /health

Health check endpoint

### GET /

Root endpoint with API information

## Project Structure

```
project-root/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration management
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py        # API endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   └── multi_ai_support.py  # AI agent logic
│   └── models/
│       ├── __init__.py
│       └── schemas.py       # Pydantic models
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
├── render.yaml
└── README.md
```

## License

MIT
