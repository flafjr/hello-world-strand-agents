"""
Environment Configuration for Amazon Strand Agents
"""
import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
AGENTS_DIR = PROJECT_ROOT / "agents"
TOOLS_DIR = PROJECT_ROOT / "tools"
CONFIG_DIR = PROJECT_ROOT / "config"

# Ollama Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
OLLAMA_DEFAULT_MODEL = "llama3.2"

# AWS Configuration (if needed)
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "default")

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Agent Configuration
DEFAULT_AGENT_TIMEOUT = 30
MAX_RETRIES = 3

# Memory and Context Settings
MAX_CONTEXT_LENGTH = 4096
DEFAULT_TEMPERATURE = 0.7