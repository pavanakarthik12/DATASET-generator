"""
Chatbot routes using OpenRouter API
Handles AI-powered suggestions and interactions
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
import requests
import json
from config.config import config
from app.utils.helpers import handle_api_error

router = APIRouter()

class ChatbotService:
    """Service for OpenRouter chatbot integration"""
    
    def __init__(self):
        self.api_key = config.OPENROUTER_API_KEY
        self.base_url = config.OPENROUTER_BASE_URL
    
    def get_suggestion(self, query: str, context: Optional[str] = None) -> Dict[str, Any]:
        """Get AI-powered suggestion based on user query"""
        try:
            if not self.api_key:
                return {"error": "OpenRouter API key not configured"}
            
            if not query.strip():
                return {"error": "Query cannot be empty"}
            
            # Prepare the prompt
            system_prompt = """You are a helpful assistant for a Smart Dataset Generator. 
            Your role is to provide suggestions for dataset generation based on user queries.
            You can suggest:
            - Weather data collection strategies
            - Stock market analysis approaches
            - News data filtering and categorization
            - Image search optimization
            - COVID-19 data analysis methods
            - Data visualization recommendations
            - Export format suggestions (CSV, JSON, Parquet)
            
            Always provide practical, actionable advice."""
            
            user_prompt = f"User query: {query}"
            if context:
                user_prompt += f"\nContext: {context}"
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://smart-dataset-generator.com",
                "X-Title": "Smart Dataset Generator"
            }
            
            payload = {
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            
            return {
                "suggestion": result["choices"][0]["message"]["content"],
                "model": result["model"],
                "usage": result.get("usage", {}),
                "timestamp": result.get("created", "")
            }
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "OpenRouter")
        except Exception as e:
            return handle_api_error(e, "OpenRouter")
    
    def get_dataset_recommendations(self, data_type: str, purpose: str) -> Dict[str, Any]:
        """Get dataset generation recommendations"""
        try:
            if not self.api_key:
                return {"error": "OpenRouter API key not configured"}
            
            system_prompt = f"""You are a data science expert. Provide specific recommendations for generating a {data_type} dataset for {purpose}.
            Include:
            - Data collection strategies
            - API endpoints to use
            - Data filtering criteria
            - Export format recommendations
            - Data quality considerations
            - Analysis suggestions"""
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://smart-dataset-generator.com",
                "X-Title": "Smart Dataset Generator"
            }
            
            payload = {
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Data type: {data_type}, Purpose: {purpose}"}
                ],
                "max_tokens": 600,
                "temperature": 0.5
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            
            return {
                "recommendations": result["choices"][0]["message"]["content"],
                "data_type": data_type,
                "purpose": purpose,
                "model": result["model"]
            }
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "OpenRouter")
        except Exception as e:
            return handle_api_error(e, "OpenRouter")
    
    def analyze_data_quality(self, data_sample: str) -> Dict[str, Any]:
        """Analyze data quality and provide suggestions"""
        try:
            if not self.api_key:
                return {"error": "OpenRouter API key not configured"}
            
            system_prompt = """You are a data quality expert. Analyze the provided data sample and provide:
            - Data quality assessment
            - Missing value identification
            - Data consistency issues
            - Improvement suggestions
            - Data cleaning recommendations"""
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://smart-dataset-generator.com",
                "X-Title": "Smart Dataset Generator"
            }
            
            payload = {
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Data sample: {data_sample}"}
                ],
                "max_tokens": 500,
                "temperature": 0.3
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            
            return {
                "analysis": result["choices"][0]["message"]["content"],
                "model": result["model"]
            }
            
        except requests.exceptions.RequestException as e:
            return handle_api_error(e, "OpenRouter")
        except Exception as e:
            return handle_api_error(e, "OpenRouter")

# Initialize chatbot service
chatbot_service = ChatbotService()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = None

@router.post("/chat")
async def chat_completion(payload: ChatRequest):
    """Generic chat endpoint that accepts a messages array and returns one assistant reply."""
    try:
        if not chatbot_service.api_key:
            raise HTTPException(status_code=400, detail="OpenRouter API key not configured")

        if not payload.messages or len(payload.messages) == 0:
            raise HTTPException(status_code=400, detail="Messages array is required")

        headers = {
            "Authorization": f"Bearer {chatbot_service.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://smart-dataset-generator.com",
            "X-Title": "Smart Dataset Generator"
        }

        body = {
            "model": payload.model or "openai/gpt-4o-mini",
            "messages": [m.dict() for m in payload.messages],
            "max_tokens": 800,
            "temperature": 0.7
        }

        response = requests.post(
            f"{chatbot_service.base_url}/chat/completions",
            headers=headers,
            json=body,
            timeout=30
        )
        response.raise_for_status()

        data = response.json()
        assistant = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        model_used = data.get("model", body["model"])

        return {
            "success": True,
            "data": {
                "message": assistant,
                "model": model_used,
                "usage": data.get("usage", {}),
                "created": data.get("created", None)
            }
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"OpenRouter error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/suggest")
async def get_suggestion(
    query: str = Query(..., description="User query for AI suggestion"),
    context: Optional[str] = Query(None, description="Additional context")
):
    """Get AI-powered suggestion for dataset generation"""
    try:
        data = chatbot_service.get_suggestion(query, context)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        return {"success": True, "data": data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommendations")
async def get_dataset_recommendations(
    data_type: str = Query(..., description="Type of data (weather, stocks, news, images, covid)"),
    purpose: str = Query(..., description="Purpose of the dataset")
):
    """Get dataset generation recommendations"""
    try:
        data = chatbot_service.get_dataset_recommendations(data_type, purpose)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        return {"success": True, "data": data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
async def analyze_data_quality(
    data_sample: str = Query(..., description="Sample of data to analyze")
):
    """Analyze data quality and provide suggestions"""
    try:
        data = chatbot_service.analyze_data_quality(data_sample)
        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"])
        
        return {"success": True, "data": data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def get_available_models():
    """Get available AI models (placeholder)"""
    return {
        "success": True,
        "data": {
            "models": [
                "openai/gpt-3.5-turbo",
                "openai/gpt-4",
                "anthropic/claude-3-sonnet",
                "meta-llama/llama-2-70b-chat"
            ],
            "current_model": "openai/gpt-3.5-turbo",
            "note": "Model selection can be configured in the service"
        }
    }
