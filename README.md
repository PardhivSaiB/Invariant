# AI DSA Mentor Platform

An AI-powered mentor that teaches algorithmic thinking through interactive feedback and visualization.

## Tech Stack

- **Backend:** FastAPI, Python, Google ADK, MCP
- **Frontend:** React, TailwindCSS, Monaco Editor
- **Infrastructure:** Docker, Google Cloud Run
- **AI:** Gemini 2.5 Flash

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (with `uv`)
- Node.js 18+

### Setup

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your Gemini API key
3. Run the platform using Docker Compose:

```bash
docker-compose up --build
```

4. Access the frontend at `http://localhost:5173` and the backend API at `http://localhost:8000`.

## Architecture

- `backend/`: FastAPI application with agentic workflows.
- `frontend/`: React application with interactive editor and visualization.
- `mcp/`: Model Context Protocol tools for AI capabilities.
