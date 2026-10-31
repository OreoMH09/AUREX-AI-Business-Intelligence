"""
AUREX Groq LLM Client
Handles communication with Groq API (ULTRA FAST!)
"""
from typing import Dict, List, Any, Optional
import requests

from app.core import settings, get_logger

logger = get_logger(__name__)


class GroqClient:
    """Client for Groq API - Ultra fast LLM inference"""
    
    def __init__(
        self,
        api_key: str = None,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None
    ):
        """
        Initialize Groq client
        
        Args:
            api_key: Groq API key
            model: Model name
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
        """
        self.api_key = api_key or settings.groq_api_key
        self.model = model or settings.groq_model
        self.temperature = temperature or settings.llm_temperature
        self.max_tokens = max_tokens or settings.llm_max_tokens
        self.base_url = "https://api.groq.com/openai/v1"
        
        logger.info(f"GroqClient initialized with model: {self.model}")
    
    def check_health(self) -> bool:
        """
        Check if Groq API is accessible
        
        Returns:
            True if API is healthy
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # List models to check connectivity
            response = requests.get(
                f"{self.base_url}/models",
                headers=headers,
                timeout=5
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Groq health check failed: {e}")
            return False
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        context: Optional[str] = None,
        stream: bool = False
    ) -> str:
        """
        Generate text completion using Groq
        
        Args:
            prompt: User prompt
            system_prompt: System prompt for instruction
            context: Additional context
            stream: Whether to stream response (not implemented)
            
        Returns:
            Generated text
        """
        try:
            # Build messages
            messages = []
            
            if system_prompt:
                messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            # Add context if provided
            user_content = prompt
            if context:
                user_content = f"Context:\n{context}\n\nQuestion: {prompt}"
            
            messages.append({
                "role": "user",
                "content": user_content
            })
            
            logger.info(f"Generating completion with Groq (model: {self.model})")
            
            # Make API request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30  # Groq is FAST - 30s is plenty
            )
            
            # Log response for debugging
            logger.info(f"Response status: {response.status_code}")
            if response.status_code != 200:
                logger.error(f"Response body: {response.text}")
            
            response.raise_for_status()
            result = response.json()
            
            generated_text = result["choices"][0]["message"]["content"]
            logger.info(f"Generated {len(generated_text)} characters in {result.get('usage', {}).get('total_time', 'N/A')}s")
            
            return generated_text
                
        except requests.exceptions.HTTPError as e:
            logger.error(f"Groq API HTTP error: {e}")
            logger.error(f"Response content: {e.response.text if e.response else 'No response'}")
            if e.response.status_code == 401:
                raise Exception("Invalid Groq API key. Get one from https://console.groq.com/keys")
            elif e.response.status_code == 429:
                raise Exception("Groq rate limit exceeded. Wait a moment and try again.")
            else:
                raise Exception(f"Groq API error: {str(e)} - {e.response.text if e.response else 'No details'}")
        except requests.exceptions.Timeout:
            logger.error("Groq request timed out")
            raise Exception("Groq API request timed out")
        except Exception as e:
            logger.error(f"Error generating text with Groq: {e}", exc_info=True)
            raise Exception(f"Groq API error: {str(e)}")
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False
    ) -> str:
        """
        Chat completion with message history
        
        Args:
            messages: List of messages with 'role' and 'content'
            stream: Whether to stream response
            
        Returns:
            Generated response
        """
        try:
            logger.info(f"Chat completion with {len(messages)} messages")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens
            }
            
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            return result["choices"][0]["message"]["content"]
            
        except Exception as e:
            logger.error(f"Error in Groq chat completion: {e}")
            raise


# Global Groq client instance
groq_client = None


def get_groq_client() -> GroqClient:
    """Get or create global Groq client instance"""
    global groq_client
    if groq_client is None:
        groq_client = GroqClient()
    return groq_client
