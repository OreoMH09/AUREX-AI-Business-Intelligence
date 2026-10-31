"""
AUREX Gemini LLM Client
Handles communication with Google Gemini API
"""
from typing import Dict, List, Any, Optional
import google.generativeai as genai

from app.core import settings, get_logger

logger = get_logger(__name__)


class GeminiClient:
    """Client for Google Gemini API"""
    
    def __init__(
        self,
        api_key: str = None,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None
    ):
        """
        Initialize Gemini client
        
        Args:
            api_key: Gemini API key
            model: Model name
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
        """
        self.api_key = api_key or settings.gemini_api_key
        self.model_name = model or settings.gemini_model
        self.temperature = temperature or settings.llm_temperature
        self.max_tokens = max_tokens or settings.llm_max_tokens
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        
        # Initialize model
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            generation_config={
                "temperature": self.temperature,
                "max_output_tokens": self.max_tokens,
            }
        )
        
        logger.info(f"GeminiClient initialized with model: {self.model_name}")
    
    def check_health(self) -> bool:
        """
        Check if Gemini API is accessible
        
        Returns:
            True if API is healthy
        """
        try:
            # Try a simple generation
            response = self.model.generate_content("Hello")
            return bool(response.text)
        except Exception as e:
            logger.error(f"Gemini health check failed: {e}")
            return False
    
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
            stream: Whether to stream response (not used for Gemini)
            
        Returns:
            Generated text
        """
        try:
            # Build full prompt
            full_prompt = ""
            
            if system_prompt:
                full_prompt += f"System Instructions: {system_prompt}\n\n"
            
            if context:
                full_prompt += f"Context:\n{context}\n\n"
            
            full_prompt += f"Question: {prompt}"
            
            logger.info(f"Generating completion with Gemini (model: {self.model_name})")
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            
            generated_text = response.text
            logger.info(f"Generated {len(generated_text)} characters")
            
            return generated_text
                
        except Exception as e:
            logger.error(f"Error generating text with Gemini: {e}", exc_info=True)
            raise Exception(f"Gemini API error: {str(e)}")
    
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
            # Convert messages to Gemini format
            chat = self.model.start_chat(history=[])
            
            # Build conversation context
            conversation = ""
            for msg in messages[:-1]:  # All but last
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                conversation += f"{role}: {content}\n\n"
            
            # Last message is the current query
            last_message = messages[-1].get('content', '')
            full_prompt = conversation + f"user: {last_message}"
            
            logger.info(f"Chat completion with {len(messages)} messages")
            
            response = chat.send_message(full_prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"Error in Gemini chat completion: {e}")
            raise


# Global Gemini client instance
gemini_client = None


def get_gemini_client() -> GeminiClient:
    """Get or create global Gemini client instance"""
    global gemini_client
    if gemini_client is None:
        gemini_client = GeminiClient()
    return gemini_client
