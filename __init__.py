"""
Amazon Strand Agents with Ollama Integration

This package provides a comprehensive framework for creating and managing
multiple AI agents using Amazon Strand Agents with local Ollama models.
"""

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Import main classes for easy access
from agents.ollama_agent import OllamaStrandAgent
from agents.specialized_agents import (
    MathAgent,
    ResearchAgent, 
    CodeAgent,
    AnalysisAgent,
    CreativeAgent,
    create_agent,
    math_agent,
    research_agent,
    code_agent,
    analysis_agent,
    creative_agent
)
from config.ollama_config import ollama_config
from tools.custom_tools import CUSTOM_TOOLS

__all__ = [
    "OllamaStrandAgent",
    "MathAgent",
    "ResearchAgent",
    "CodeAgent", 
    "AnalysisAgent",
    "CreativeAgent",
    "create_agent",
    "math_agent",
    "research_agent",
    "code_agent",
    "analysis_agent", 
    "creative_agent",
    "ollama_config",
    "CUSTOM_TOOLS"
]