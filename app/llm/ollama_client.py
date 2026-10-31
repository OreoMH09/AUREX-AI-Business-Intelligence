"""
AUREX Ollama LLM Client
Handles communication with local Ollama server
"""
from typing import Dict, List, Any, Optional, Generator
import requests
import json

from app.core import settings, get_logger

logger = get_logger(__name__)


class OllamaClient:
    """Client for Ollama LLM API"""
    
    def __init__(
        self,
        base_url: str = None,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None
    ):
        """
        Initialize Ollama client
        
        Args:
            base_url: Ollama server URL
            model: Model name
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
        """
        self.base_url = base_url or settings.ollama_base_url
        self.model = model or settings.ollama_model
        self.temperature = temperature or settings.llm_temperature
        self.max_tokens = max_tokens or settings.llm_max_tokens
        
        logger.info(f"OllamaClient initialized: {self.base_url}, model: {self.model}")
    
    def check_health(self) -> bool:
        """
        Check if Ollama server is running
        
        Returns:
            True if server is healthy
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return False
    
    def list_models(self) -> List[str]:
        """
        List available models
        
        Returns:
            List of model names
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=10)
            response.raise_for_status()
            
            data = response.json()
            models = [model['name'] for model in data.get('models', [])]
            
            logger.info(f"Available models: {models}")
            return models
            
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        context: Optional[str] = None,
        stream: bool = False
    ) -> str:
        """
        Generate text completion
        
        Args:
            prompt: User prompt
            system_prompt: System prompt for instruction
            context: Additional context
            stream: Whether to stream response
            
        Returns:
            Generated text
        """
        try:
            # Build full prompt
            full_prompt = prompt
            if context:
                full_prompt = f"Context:\n{context}\n\nQuestion: {prompt}"
            
            # Prepare request
            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": stream,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            }
            
            if system_prompt:
                payload["system"] = system_prompt
            
            logger.info(f"Generating completion with Ollama (model: {self.model})")
            
            if stream:
                return self._generate_stream(payload)
            else:
                return self._generate_sync(payload)
                
        except Exception as e:
            logger.error(f"Error generating text: {e}", exc_info=True)
            raise
    
    def _generate_sync(self, payload: Dict[str, Any]) -> str:
        """Generate synchronous response"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=90  # 90 seconds - let it complete
            )
            response.raise_for_status()
            
            data = response.json()
            generated_text = data.get('response', '')
            
            logger.info(f"Generated {len(generated_text)} characters")
            return generated_text
            
        except requests.exceptions.Timeout:
            logger.error("Ollama request timed out")
            raise Exception("Request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            logger.error("Cannot connect to Ollama server")
            raise Exception("Cannot connect to Ollama server. Please ensure Ollama is running.")
        except Exception as e:
            logger.error(f"Error in sync generation: {e}")
            raise
    
    def _generate_stream(self, payload: Dict[str, Any]) -> Generator[str, None, None]:
        """Generate streaming response"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                stream=True,
                timeout=90  # 90 seconds - let it complete
            )
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if 'response' in data:
                        yield data['response']
                        
        except Exception as e:
            logger.error(f"Error in stream generation: {e}")
            raise
    
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
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": stream,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens
                }
            }
            
            logger.info(f"Chat completion with {len(messages)} messages")
            
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=90  # 90 seconds - let it complete
            )
            response.raise_for_status()
            
            data = response.json()
            message = data.get('message', {})
            generated_text = message.get('content', '')
            
            return generated_text
            
        except Exception as e:
            logger.error(f"Error in chat completion: {e}")
            raise


# Global Ollama client instance
ollama_client = None


def get_ollama_client() -> OllamaClient:
    """Get or create global Ollama client instance"""
    global ollama_client
    if ollama_client is None:
        ollama_client = OllamaClient()
    return ollama_client
