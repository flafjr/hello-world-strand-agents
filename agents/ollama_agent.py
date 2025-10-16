"""
Base Agent class with Ollama integration for Amazon Strand Agents
"""
import asyncio
import logging
from typing import Optional, Dict, Any, List
import ollama
from strands import Agent
from config.ollama_config import ollama_config

logger = logging.getLogger(__name__)

class OllamaStrandAgent:
    """
    Base class for Strand Agents with Ollama integration
    """
    
    def __init__(
        self, 
        name: str,
        model: str = None,
        tools: List = None,
        system_prompt: str = None,
        **kwargs
    ):
        self.name = name
        self.model = model or ollama_config.default_model
        self.tools = tools or []
        self.system_prompt = system_prompt
        self.config = ollama_config.get_model_config(self.model)
        
        # Initialize the Strand Agent
        self.strand_agent = Agent(
            name=self.name,
            tools=self.tools,
            **kwargs
        )
        
        logger.info(f"Initialized OllamaStrandAgent '{self.name}' with model '{self.model}'")
    
    def chat(self, message: str, **kwargs) -> str:
        """
        Send a message to the agent and get a response
        """
        try:
            # Prepare the conversation
            messages = []
            
            if self.system_prompt:
                messages.append({
                    "role": "system",
                    "content": self.system_prompt
                })
            
            messages.append({
                "role": "user", 
                "content": message
            })
            
            # Use Ollama for the response
            response = ollama.chat(
                model=self.model,
                messages=messages,
                **kwargs
            )
            
            return response['message']['content']
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return f"Error: {str(e)}"
    
    async def async_chat(self, message: str, **kwargs) -> str:
        """
        Async version of chat method
        """
        try:
            messages = []
            
            if self.system_prompt:
                messages.append({
                    "role": "system",
                    "content": self.system_prompt
                })
            
            messages.append({
                "role": "user", 
                "content": message
            })
            
            # Use async Ollama client
            response = await ollama.AsyncClient().chat(
                model=self.model,
                messages=messages,
                **kwargs
            )
            
            return response['message']['content']
            
        except Exception as e:
            logger.error(f"Error in async_chat: {e}")
            return f"Error: {str(e)}"
    
    def stream_chat(self, message: str, **kwargs):
        """
        Stream response from the agent
        """
        try:
            messages = []
            
            if self.system_prompt:
                messages.append({
                    "role": "system",
                    "content": self.system_prompt
                })
            
            messages.append({
                "role": "user", 
                "content": message
            })
            
            # Stream response
            for chunk in ollama.chat(
                model=self.model,
                messages=messages,
                stream=True,
                **kwargs
            ):
                yield chunk['message']['content']
                
        except Exception as e:
            logger.error(f"Error in stream_chat: {e}")
            yield f"Error: {str(e)}"
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model
        """
        try:
            return ollama.show(self.model)
        except Exception as e:
            logger.error(f"Error getting model info: {e}")
            return {"error": str(e)}
    
    def list_available_models(self) -> List[str]:
        """
        List all available models in Ollama
        """
        try:
            models = ollama.list()
            return [model['name'] for model in models['models']]
        except Exception as e:
            logger.error(f"Error listing models: {e}")
            return []
    
    def add_tool(self, tool):
        """
        Add a tool to the agent
        """
        self.tools.append(tool)
        # Reinitialize strand agent with new tools
        self.strand_agent = Agent(
            name=self.name,
            tools=self.tools
        )
        logger.info(f"Added tool to agent '{self.name}'")
    
    def __str__(self):
        return f"OllamaStrandAgent(name={self.name}, model={self.model})"
    
    def __repr__(self):
        return self.__str__()