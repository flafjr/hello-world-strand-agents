# Amazon Strand Agents with Ollama Integration

A comprehensive development environment for creating multiple AI agents using Amazon Strand Agents with local Ollama models.

## 🚀 Features

- **Multiple Specialized Agents**: Math, Research, Code, Analysis, and Creative agents
- **Local Ollama Integration**: Run powerful AI models locally without external API dependencies
- **Jupyter Notebook Examples**: Interactive examples and tutorials
- **Custom Tools**: Extensible toolkit for agent capabilities
- **Makefile Automation**: 30+ commands for easy development workflow
- **Virtual Environment**: Isolated Python environment with all dependencies

## 📋 Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.ai/) installed and running
- Git (for version control)
- At least 8GB RAM (for running AI models)

## 🛠️ Quick Setup

### 1. Install Ollama

```bash
# macOS (using Homebrew)
brew install ollama

# Or download from https://ollama.ai/
```

### 2. Clone and Setup Project

```bash
# Clone the repository
git clone <your-repo-url>
cd hello-world-strand-agents

# One-command setup
make setup
```

This will:

- Create Python 3.11 virtual environment
- Install all dependencies
- Setup Jupyter kernel
- Prepare development environment

### 3. Start Development

```bash
# Start everything (Ollama + environment)
make start

# Or start components individually
make ollama-start    # Start Ollama service
make jupyter         # Start Jupyter Lab
```

## 🧪 Testing Your Setup

### Quick Test

```bash
# Full automated test suite
make test

# Quick validation
make test-quick

# Interactive agent chat
make interactive
```

### Manual Verification

```bash
# Check system status
make status

# List available models
make models

# Test specific components
make test-vscode     # VS Code integration
```

## 🏗️ Project Structure

```text
hello-world-strand-agents/
├── README.md                       # This file
├── requirements.txt                # Python dependencies
├── Makefile                        # Development commands (30+ targets)
├── main.py                         # Getting started example
├── test_interactive.py             # Interactive testing script
├── test_vscode.py                  # VS Code integration test
├── venv/                           # Python virtual environment
├── agents/                         # Agent implementations
│   ├── ollama_agent.py             # Base Ollama agent class
│   └── specialized_agents.py       # Specialized agent types
├── config/                         # Configuration files
│   ├── settings.py                 # Global settings
│   └── ollama_config.py            # Ollama-specific configuration
├── tools/                          # Custom tools for agents
│   └── custom_tools.py             # Tool implementations
└── notebooks/                      # Jupyter notebooks
    ├── 01_getting_started.ipynb    # Basic examples
    └── 02_advanced_patterns.ipynb  # Advanced patterns
```

## 🛠️ Makefile Commands

This project includes comprehensive automation with 30+ commands:

### Essential Commands

```bash
make setup              # Complete project setup
make start              # Start development environment  
make test               # Full test suite
make jupyter            # Start Jupyter Lab
make help               # Show all available commands
```

### Testing & Validation

```bash
make test-quick         # Quick validation
make test-interactive   # Interactive testing
make test-vscode        # VS Code integration test
make status             # Check system status
```

### Ollama Management

```bash
make ollama-start       # Start Ollama service
make ollama-stop        # Stop Ollama service
make models             # List available models
make model-pull         # Pull default model (llama3.2:3b)
make model-pull-large   # Pull larger model (llama3.2)
make model-pull-code    # Pull code-specialized model (codellama)
```

### Development Tools

```bash
make agents             # List and test agents
make interactive        # Start interactive agent chat
make clean              # Clean up environment
```

## 🚀 Quick Start Examples

### 1. Jupyter Notebook (Recommended)

```bash
make jupyter
```

Open `notebooks/01_getting_started.ipynb` and run the cells.

### 2. Python Script

```python
from agents.specialized_agents import math_agent, creative_agent

# Create agents
math_ai = math_agent()
creative_ai = creative_agent()

# Use agents
math_result = math_ai.chat("What is the square root of 1764?")
story = creative_ai.chat("Write a short story about AI agents")

print(f"Math: {math_result}")
print(f"Story: {story}")
```

### 3. Interactive Terminal

```bash
make interactive
```

## 🤖 Available Agents

### Specialized Agents

1. **MathAgent** - Mathematical calculations and problem solving
2. **CodeAgent** - Programming and software development
3. **CreativeAgent** - Creative writing and content generation
4. **AnalysisAgent** - Data analysis and insights
5. **ResearchAgent** - Information gathering and research

### Creating Custom Agents

```python
from agents.ollama_agent import OllamaStrandAgent

custom_agent = OllamaStrandAgent(
    name="MyAgent",
    model="llama3.2",
    system_prompt="You are a helpful assistant specialized in...",
    tools=[custom_tool]
)
```

## 🛠️ Custom Tools

The project includes several custom tools:

- **Text Analyzer** - Analyze text statistics
- **Unit Converter** - Convert between different units
- **File Reader** - Read and process files
- **JSON Validator** - Validate and parse JSON
- **Timestamp Tool** - Get timestamps in various formats

### Adding New Tools

```python
def my_custom_tool(input_data: str) -> Dict[str, Any]:
    """Your custom tool implementation"""
    return {"result": "processed data"}

# Add to agents
agent.add_tool(my_custom_tool)
```

## 🔧 Configuration

### Ollama Settings

Edit `config/ollama_config.py`:

```python
class OllamaConfig:
    def __init__(self):
        self.base_url = "http://localhost:11434"
        self.default_model = "llama3.2"
        self.timeout = 30
```

### Environment Variables (Optional)

Create `.env` file:

```bash
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_DEFAULT_MODEL=llama3.2
OLLAMA_TIMEOUT=30
LOG_LEVEL=INFO
```

## 🚦 Troubleshooting

### Common Issues

1. **Ollama not running**

   ```bash
   make ollama-start
   # OR
   ollama serve
   ```

2. **Model not found**

   ```bash
   make model-pull        # Pull default model
   # OR
   ollama pull llama3.2
   ```

3. **Python version issues**
   - Ensure Python 3.10+ is installed
   - Run `make clean && make setup` to recreate environment

4. **Import errors**

   ```bash
   source venv/bin/activate  # Ensure virtual environment is activated
   make test-quick           # Validate setup
   ```

5. **Jupyter kernel not found**

   ```bash
   make setup  # This installs the kernel automatically
   ```

### Getting Help

- Run `make help` for all available commands
- Check Ollama documentation: <https://ollama.ai/>
- Review notebook examples for common patterns
- Run `make status` to check system health

## ✅ Verification

Your setup is working correctly when:

- `make status` shows all green checkmarks ✅
- `make test-quick` passes without errors
- `make models` shows at least one available model
- Jupyter notebooks run successfully

## 🎯 Use Cases

This setup is perfect for:

- **Prototyping AI applications** with multiple specialized agents
- **Learning multi-agent systems** concepts and patterns
- **Building content generation pipelines** with different agent roles
- **Experimenting with local AI models** without external API costs
- **Developing agent orchestration patterns** for complex workflows

## 🔄 Development Workflow

### Daily Development

```bash
# Start your day
make start              # Start everything

# During development
make test-quick         # Quick validation
make jupyter            # Interactive development
make interactive        # Test agents

# End of day
make clean              # Optional cleanup
```

### Advanced Patterns

The `02_advanced_patterns.ipynb` notebook demonstrates:

- **Agent Orchestration**: Sequential and parallel workflows
- **Context Management**: Conversation history and memory
- **Error Handling**: Retry logic and graceful degradation
- **Performance Monitoring**: Metrics and optimization
- **Complex Workflows**: Multi-stage pipelines

## 📝 Documentation

- **README.md** - This file (project overview)
- **TESTING.md** - Comprehensive testing guide
- **VSCODE_SETUP.md** - VS Code configuration help
- **notebooks/** - Interactive examples and tutorials
- **Makefile** - All available commands (`make help`)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test with `make test`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Amazon Web Services for Strand Agents
- Ollama team for local AI model serving
- Python and Jupyter communities
- All contributors and users

---

## 🚀 Happy coding with AI agents

**Quick Start**: `make setup && make start && make test`