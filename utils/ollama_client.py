import asyncio
import json
import httpx
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = base_url
        self.model = model
        self.client = httpx.AsyncClient(timeout=60.0)
    
    async def generate(self, prompt: str, max_tokens: int = 500) -> str:
        """Generate text using Ollama API"""
        try:
            url = f"{self.base_url}/api/generate"
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            }
            
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result.get("response", "").strip()
            
        except Exception as e:
            logger.error(f"Error calling Ollama API: {str(e)}")
            raise Exception(f"Model generation failed: {str(e)}")
    
    async def health_check(self) -> bool:
        """Check if Ollama service is available"""
        try:
            url = f"{self.base_url}/api/tags"
            response = await self.client.get(url)
            return response.status_code == 200
        except:
            return False
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
