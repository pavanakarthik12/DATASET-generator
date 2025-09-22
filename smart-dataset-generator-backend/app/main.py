"""
Smart Dataset Generator Backend
FastAPI application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api_routes, chatbot_routes, download_routes

# Initialize FastAPI app
app = FastAPI(
    title="Smart Dataset Generator API",
    description="A comprehensive API for generating datasets from multiple sources",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_routes.router, prefix="/api", tags=["Data APIs"])
app.include_router(chatbot_routes.router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(download_routes.router, prefix="/download", tags=["Downloads"])

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Smart Dataset Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "weather": "/api/weather",
            "stocks": "/api/stocks",
            "news": "/api/news",
            "images": "/api/images",
            "covid": "/api/covid",
            "chatbot": "/chatbot/suggest",
            "downloads": "/download"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Smart Dataset Generator API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
