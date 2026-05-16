from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import analyze, hint, visualize, similar, health
from app.config import settings
import logging

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("main")

app = FastAPI(
    title="AI DSA Mentor API",
    description="Backend API for the AI DSA Mentor platform",
    version="0.1.0",
)

# Configure CORS to allow all origins for development/testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # settings.CORS_ORIGINS or ["*"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health.router, prefix="/api/health", tags=["Health"])
app.include_router(analyze.router, prefix="/api/analyze", tags=["Analysis"])
# The following routes might be legacy or for individual tool testing
app.include_router(hint.router, prefix="/api/hint", tags=["Hints"])
app.include_router(visualize.router, prefix="/api/visualize", tags=["Visualization"])
app.include_router(similar.router, prefix="/api/similar", tags=["Recommendations"])

@app.on_event("startup")
async def startup_event():
    logger.info("Starting AI DSA Mentor API...")
    logger.info(f"Environment: {settings.ENV}")
    # We could trigger agent initialization here to catch errors early
    try:
        from app.agents.agent import get_agent
        get_agent()
        logger.info("DSAMentorAgent ready.")
    except Exception as e:
        logger.error(f"Agent failed to initialize at startup: {e}")

@app.get("/")
async def root():
    return {"message": "Welcome to AI DSA Mentor API"}
