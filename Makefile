# Makefile for Amazon Strand Agents with Ollama
# Usage: make <target>
# Run 'make help' to see all available commands

.PHONY: help setup test clean start stop status jupyter interactive agents ollama models

# Default target
.DEFAULT_GOAL := help

# Variables
VENV_DIR = venv
PYTHON = $(VENV_DIR)/bin/python
PIP = $(VENV_DIR)/bin/pip
JUPYTER = $(VENV_DIR)/bin/jupyter
OLLAMA_URL = http://localhost:11434
DEFAULT_MODEL = llama3.2:3b

# Colors for output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[1;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Amazon Strand Agents - Development Commands$(NC)"
	@echo "=============================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Quick Start:$(NC)"
	@echo "  make setup    # Initial setup"
	@echo "  make start    # Start everything"
	@echo "  make test     # Run tests"
	@echo "  make jupyter  # Start Jupyter Lab"

setup: ## Complete project setup (install dependencies, create venv, setup kernel)
	@echo "$(BLUE)Setting up Amazon Strand Agents environment...$(NC)"
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "$(YELLOW)Creating virtual environment...$(NC)"; \
		python3.11 -m venv $(VENV_DIR) || python3 -m venv $(VENV_DIR); \
	fi
	@echo "$(YELLOW)Installing dependencies...$(NC)"
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@echo "$(YELLOW)Installing Jupyter kernel...$(NC)"
	@$(PYTHON) -m ipykernel install --user --name strand-agents --display-name "Python (Strand Agents)"
	@echo "$(GREEN)✅ Setup complete!$(NC)"
	@echo "$(YELLOW)Next: make start$(NC)"

clean: ## Clean up environment and temporary files
	@echo "$(YELLOW)Cleaning up...$(NC)"
	@rm -rf $(VENV_DIR)
	@rm -rf __pycache__ */__pycache__ */*/__pycache__
	@rm -rf .pytest_cache
	@rm -rf *.egg-info
	@jupyter kernelspec uninstall strand-agents -f 2>/dev/null || true
	@echo "$(GREEN)✅ Cleanup complete!$(NC)"

# Ollama Management
ollama-check: ## Check if Ollama is running
	@echo "$(BLUE)Checking Ollama status...$(NC)"
	@if curl -s $(OLLAMA_URL)/api/version > /dev/null 2>&1; then \
		echo "$(GREEN)✅ Ollama is running$(NC)"; \
		curl -s $(OLLAMA_URL)/api/version | python3 -m json.tool 2>/dev/null || echo "Running"; \
	else \
		echo "$(RED)❌ Ollama is not running$(NC)"; \
		echo "$(YELLOW)Start with: make ollama-start$(NC)"; \
		exit 1; \
	fi

ollama-start: ## Start Ollama service in background
	@echo "$(BLUE)Starting Ollama service...$(NC)"
	@if ! pgrep -f "ollama serve" > /dev/null; then \
		echo "$(YELLOW)Starting Ollama in background...$(NC)"; \
		nohup ollama serve > ollama.log 2>&1 & \
		sleep 3; \
		if curl -s $(OLLAMA_URL)/api/version > /dev/null 2>&1; then \
			echo "$(GREEN)✅ Ollama started successfully$(NC)"; \
		else \
			echo "$(RED)❌ Failed to start Ollama$(NC)"; \
			exit 1; \
		fi \
	else \
		echo "$(GREEN)✅ Ollama is already running$(NC)"; \
	fi

ollama-stop: ## Stop Ollama service
	@echo "$(BLUE)Stopping Ollama service...$(NC)"
	@pkill -f "ollama serve" 2>/dev/null || true
	@echo "$(GREEN)✅ Ollama stopped$(NC)"

ollama-logs: ## Show Ollama logs
	@echo "$(BLUE)Ollama logs:$(NC)"
	@tail -f ollama.log 2>/dev/null || echo "No logs found. Start Ollama with: make ollama-start"

models: ## List available Ollama models
	@echo "$(BLUE)Available Ollama models:$(NC)"
	@curl -s $(OLLAMA_URL)/api/tags | python3 -c "import sys, json; data=json.load(sys.stdin); [print(f'  - {m[\"name\"]}') for m in data.get('models', [])]" 2>/dev/null || echo "$(RED)❌ Cannot connect to Ollama$(NC)"

model-pull: ## Pull default model (llama3.2:3b)
	@echo "$(BLUE)Pulling model: $(DEFAULT_MODEL)$(NC)"
	@ollama pull $(DEFAULT_MODEL)
	@echo "$(GREEN)✅ Model $(DEFAULT_MODEL) ready$(NC)"

model-pull-large: ## Pull larger model (llama3.2)
	@echo "$(BLUE)Pulling larger model: llama3.2$(NC)"
	@ollama pull llama3.2
	@echo "$(GREEN)✅ Model llama3.2 ready$(NC)"

model-pull-code: ## Pull code-specialized model (codellama)
	@echo "$(BLUE)Pulling code model: codellama$(NC)"
	@ollama pull codellama
	@echo "$(GREEN)✅ Model codellama ready$(NC)"

# Environment and Dependencies
venv: ## Create virtual environment
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "$(YELLOW)Creating virtual environment...$(NC)"; \
		python3.11 -m venv $(VENV_DIR) || python3 -m venv $(VENV_DIR); \
		echo "$(GREEN)✅ Virtual environment created$(NC)"; \
	else \
		echo "$(GREEN)✅ Virtual environment already exists$(NC)"; \
	fi

install: venv ## Install Python dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

kernel: ## Install Jupyter kernel
	@echo "$(BLUE)Installing Jupyter kernel...$(NC)"
	@$(PYTHON) -m ipykernel install --user --name strand-agents --display-name "Python (Strand Agents)"
	@echo "$(GREEN)✅ Kernel installed$(NC)"

# Testing
test: ollama-check ## Run complete test suite
	@echo "$(BLUE)Running test suite...$(NC)"
	@$(PYTHON) main.py

test-quick: ## Quick test without Ollama check
	@echo "$(BLUE)Running quick test...$(NC)"
	@$(PYTHON) test_vscode.py

test-interactive: ollama-check ## Run interactive agent testing
	@echo "$(BLUE)Starting interactive test...$(NC)"
	@$(PYTHON) test_interactive.py

test-all: ollama-check ## Run all tests including notebooks
	@echo "$(BLUE)Running comprehensive tests...$(NC)"
	@$(PYTHON) main.py
	@echo "$(YELLOW)Testing notebook imports...$(NC)"
	@$(PYTHON) -c "import sys; sys.path.append('.'); from agents.specialized_agents import *; print('✅ All imports successful')"

# Development
start: ollama-start ## Start complete development environment
	@echo "$(BLUE)Starting development environment...$(NC)"
	@make models
	@echo "$(GREEN)🚀 Development environment ready!$(NC)"
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "  make jupyter      # Start Jupyter Lab"
	@echo "  make test         # Run tests"
	@echo "  make interactive  # Interactive testing"

stop: ollama-stop ## Stop all services
	@echo "$(GREEN)✅ All services stopped$(NC)"

status: ## Show status of all services
	@echo "$(BLUE)Service Status:$(NC)"
	@echo "==============="
	@if [ -d "$(VENV_DIR)" ]; then \
		echo "$(GREEN)✅ Virtual Environment$(NC)"; \
	else \
		echo "$(RED)❌ Virtual Environment$(NC)"; \
	fi
	@if curl -s $(OLLAMA_URL)/api/version > /dev/null 2>&1; then \
		echo "$(GREEN)✅ Ollama Service$(NC)"; \
		MODEL_COUNT=$$(curl -s $(OLLAMA_URL)/api/tags | python3 -c "import sys, json; print(len(json.load(sys.stdin).get('models', [])))" 2>/dev/null || echo "0"); \
		echo "$(GREEN)✅ Models Available: $$MODEL_COUNT$(NC)"; \
	else \
		echo "$(RED)❌ Ollama Service$(NC)"; \
	fi
	@if $(PYTHON) -c "import jupyter" 2>/dev/null; then \
		echo "$(GREEN)✅ Jupyter Available$(NC)"; \
	else \
		echo "$(RED)❌ Jupyter Not Available$(NC)"; \
	fi

# Jupyter and Development
jupyter: ollama-check ## Start Jupyter Lab
	@echo "$(BLUE)Starting Jupyter Lab...$(NC)"
	@echo "$(YELLOW)Opening in browser...$(NC)"
	@$(JUPYTER) lab --ip=127.0.0.1 --port=8888

jupyter-bg: ollama-check ## Start Jupyter Lab in background
	@echo "$(BLUE)Starting Jupyter Lab in background...$(NC)"
	@nohup $(JUPYTER) lab --ip=127.0.0.1 --port=8888 --no-browser > jupyter.log 2>&1 &
	@sleep 2
	@echo "$(GREEN)✅ Jupyter Lab started in background$(NC)"
	@echo "$(YELLOW)Access at: http://localhost:8888$(NC)"

notebook: jupyter ## Alias for jupyter

agents: ollama-check ## Test all specialized agents
	@echo "$(BLUE)Testing specialized agents...$(NC)"
	@$(PYTHON) -c "\
import sys; sys.path.append('.'); \
from agents.specialized_agents import *; \
print('🧮 Testing Math Agent...'); \
math_ai = math_agent(model='deepseek-r1:7b'); \
print('  Result:', math_ai.chat('What is 12 * 8?')[:50] + '...'); \
print('🎨 Testing Creative Agent...'); \
creative_ai = creative_agent(model='deepseek-r1:7b'); \
print('  Result:', creative_ai.chat('Write a haiku about AI')[:50] + '...'); \
print('💻 Testing Code Agent...'); \
code_ai = code_agent(model='deepseek-r1:7b'); \
print('  Result:', code_ai.chat('Write a Python hello world')[:50] + '...'); \
print('✅ All agents working!'); \
"

interactive: test-interactive ## Alias for test-interactive

# Utilities
logs: ## Show all logs
	@echo "$(BLUE)Recent logs:$(NC)"
	@echo "============"
	@echo "$(YELLOW)Ollama logs:$(NC)"
	@tail -10 ollama.log 2>/dev/null || echo "No Ollama logs"
	@echo "$(YELLOW)Jupyter logs:$(NC)"
	@tail -10 jupyter.log 2>/dev/null || echo "No Jupyter logs"

ports: ## Show used ports
	@echo "$(BLUE)Port usage:$(NC)"
	@echo "==========="
	@lsof -i :11434 2>/dev/null | grep LISTEN && echo "$(GREEN)✅ Ollama (11434)$(NC)" || echo "$(RED)❌ Ollama (11434)$(NC)"
	@lsof -i :8888 2>/dev/null | grep LISTEN && echo "$(GREEN)✅ Jupyter (8888)$(NC)" || echo "$(RED)❌ Jupyter (8888)$(NC)"

info: ## Show environment information
	@echo "$(BLUE)Environment Information:$(NC)"
	@echo "======================="
	@echo "Python: $$($(PYTHON) --version 2>/dev/null || echo 'Not available')"
	@echo "Virtual Env: $$([ -d '$(VENV_DIR)' ] && echo 'Available' || echo 'Not found')"
	@echo "Working Dir: $$(pwd)"
	@echo "Ollama URL: $(OLLAMA_URL)"
	@echo "Default Model: $(DEFAULT_MODEL)"

# Quick development workflows
dev: start test ## Full development setup and test
	@echo "$(GREEN)🎉 Development environment ready and tested!$(NC)"

demo: ollama-check agents ## Run a quick demo of all agents
	@echo "$(GREEN)🎭 Demo complete!$(NC)"

# Install system dependencies (macOS)
install-ollama: ## Install Ollama using Homebrew (macOS)
	@echo "$(BLUE)Installing Ollama...$(NC)"
	@if command -v brew >/dev/null 2>&1; then \
		brew install ollama; \
		echo "$(GREEN)✅ Ollama installed$(NC)"; \
	else \
		echo "$(RED)❌ Homebrew not found$(NC)"; \
		echo "$(YELLOW)Please install from: https://ollama.ai$(NC)"; \
	fi

install-python: ## Install Python 3.11 using Homebrew (macOS)
	@echo "$(BLUE)Installing Python 3.11...$(NC)"
	@if command -v brew >/dev/null 2>&1; then \
		brew install python@3.11; \
		echo "$(GREEN)✅ Python 3.11 installed$(NC)"; \
	else \
		echo "$(RED)❌ Homebrew not found$(NC)"; \
		echo "$(YELLOW)Please install Python 3.11 manually$(NC)"; \
	fi

# Emergency fixes
fix-permissions: ## Fix file permissions
	@echo "$(BLUE)Fixing permissions...$(NC)"
	@chmod +x setup.sh test_interactive.py
	@echo "$(GREEN)✅ Permissions fixed$(NC)"

fix-kernel: ## Reinstall Jupyter kernel
	@echo "$(BLUE)Fixing Jupyter kernel...$(NC)"
	@jupyter kernelspec uninstall strand-agents -f 2>/dev/null || true
	@$(PYTHON) -m ipykernel install --user --name strand-agents --display-name "Python (Strand Agents)"
	@echo "$(GREEN)✅ Kernel reinstalled$(NC)"

# Documentation
docs: ## Open documentation
	@echo "$(BLUE)Available documentation:$(NC)"
	@echo "======================="
	@echo "$(YELLOW)README.md$(NC) - Main documentation"
	@echo "$(YELLOW)TESTING.md$(NC) - Testing guide"
	@echo "$(YELLOW)VSCODE_SETUP.md$(NC) - VS Code setup"
	@echo ""
	@echo "Open with: code README.md"