"""
Ollama Configuration for Amazon Strand Agents
"""
import os
from typing import Dict, Any

class OllamaConfig:
    """Configuration class for Ollama integration with Strand Agents"""
    
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.default_model = os.getenv("OLLAMA_DEFAULT_MODEL", "llama3.2")
        self.timeout = int(os.getenv("OLLAMA_TIMEOUT", "30"))
        
    def get_model_config(self, model_name: str = None) -> Dict[str, Any]:
        """Get configuration for a specific model"""
        model = model_name or self.default_model
        return {
            "base_url": self.base_url,
            "model": model,
            "timeout": self.timeout,
            "stream": False,
            "temperature": 0.7,
            "max_tokens": 2048
        }
    
    def get_available_models(self) -> list:
        """Return list of commonly used models"""
        return [
            "llama3.2",
            "llama3.2:3b",
            "llama3.1",
            "codellama",
            "mistral",
            "phi3",
            "gemma2"
        ]

# Global configuration instance
ollama_config = OllamaConfig()