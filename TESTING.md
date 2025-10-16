# Local Testing Guide for Amazon Strand Agents with Ollama

This guide helps you test and verify your local Amazon Strand Agents setup with Ollama integration.

## 🚀 Quick Test

Run the automated test suite:

```bash
# Make sure you're in the project directory
cd hello-world-strand-agents

# Activate virtual environment
source venv/bin/activate

# Run the test suite
python main.py
```

## 📋 Prerequisites Checklist

Before testing, ensure you have:

- [ ] **Ollama installed** - Download from [ollama.ai](https://ollama.ai)
- [ ] **Ollama running** - Command: `ollama serve`
- [ ] **At least one model** - We'll pull one automatically if needed
- [ ] **Virtual environment activated** - Command: `source venv/bin/activate`
- [ ] **Dependencies installed** - Command: `pip install -r requirements.txt`

## 🔧 Step-by-Step Local Testing

### Step 1: Start Ollama

```bash
# Start Ollama service (run in background or separate terminal)
ollama serve
```

You should see output like:
```
Listening on 127.0.0.1:11434 (version 0.x.x)
```

### Step 2: Check Available Models

```bash
# List your models
ollama list
```

If no models are available, pull a basic one:
```bash
# Pull a lightweight model (good for testing)
ollama pull llama3.2:3b

# Or use a more capable model
ollama pull llama3.2
```

### Step 3: Test Direct Ollama Connection

```bash
# Test if Ollama API is responding
curl -s http://localhost:11434/api/tags | python -m json.tool
```

### Step 4: Run Our Test Suite

```bash
# Activate environment and run tests
source venv/bin/activate
python main.py
```

## 🧪 Manual Testing Examples

### Test 1: Basic Agent Chat

```python
from agents.ollama_agent import OllamaStrandAgent

# Create a basic agent
agent = OllamaStrandAgent(
    name="TestAgent",
    model="deepseek-r1:7b",  # or your available model
    system_prompt="You are a helpful assistant."
)

# Test basic chat
response = agent.chat("Hello! Can you help me with math?")
print(response)
```

### Test 2: Specialized Agents

```python
from agents.specialized_agents import math_agent, creative_agent

# Create specialized agents
math_ai = math_agent(model="deepseek-r1:7b")
creative_ai = creative_agent(model="deepseek-r1:7b")

# Test math agent
math_result = math_ai.chat("What is 25 * 25?")
print("Math:", math_result)

# Test creative agent
story = creative_ai.chat("Write a haiku about programming")
print("Creative:", story)
```

### Test 3: Custom Tools

```python
from tools.custom_tools import text_analyzer_tool, timestamp_tool

# Test text analyzer
text = "This is a sample text for analysis."
analysis = text_analyzer_tool(text)
print("Analysis:", analysis)

# Test timestamp tool
timestamp = timestamp_tool()
print("Timestamp:", timestamp)
```

### Test 4: Agent with Tools

```python
from agents.ollama_agent import OllamaStrandAgent
from strands_tools import calculator

# Create agent with calculator tool
agent = OllamaStrandAgent(
    name="MathBot",
    model="deepseek-r1:7b",
    tools=[calculator],
    system_prompt="You are a math expert. Use the calculator tool when needed."
)

# Test calculation
result = agent.chat("Calculate the factorial of 5")
print("With tool:", result)
```

## 🔍 Troubleshooting Common Issues

### Issue 1: "Connection refused" or "Ollama not responding"

**Solution:**
```bash
# Check if Ollama is running
ps aux | grep ollama

# If not running, start it
ollama serve

# Test connection
curl http://localhost:11434/api/version
```

### Issue 2: "Model not found"

**Solution:**
```bash
# List available models
ollama list

# If empty, pull a model
ollama pull llama3.2:3b

# Verify it's downloaded
ollama list
```

### Issue 3: Import errors

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Check if packages are installed
pip list | grep -E "(strands|ollama)"

# If missing, reinstall requirements
pip install -r requirements.txt
```

### Issue 4: "No module named 'agents'"

**Solution:**
```bash
# Make sure you're in the project directory
pwd  # Should show .../hello-world-strand-agents

# Check directory structure
ls -la agents/

# Run Python from project root
python main.py
```

### Issue 5: Slow responses

**Possible causes:**
- Model is large for your hardware
- First request (model loading)
- Insufficient RAM

**Solutions:**
```bash
# Use a smaller model
ollama pull llama3.2:3b

# Check system resources
top | grep ollama

# Monitor Ollama logs
ollama serve  # watch the output
```

## 📊 Performance Testing

### Test Response Times

```python
import time
from agents.specialized_agents import math_agent

agent = math_agent(model="deepseek-r1:7b")

# Time a simple request
start = time.time()
response = agent.chat("What is 2+2?")
duration = time.time() - start

print(f"Response time: {duration:.2f} seconds")
print(f"Response: {response}")
```

### Test Multiple Agents

```python
from agents.specialized_agents import *

# Create multiple agents
agents = {
    'math': math_agent(model="deepseek-r1:7b"),
    'creative': creative_agent(model="deepseek-r1:7b"),
    'code': code_agent(model="deepseek-r1:7b")
}

# Test each agent
for name, agent in agents.items():
    start = time.time()
    response = agent.chat(f"Hello from {name} agent!")
    duration = time.time() - start
    print(f"{name}: {duration:.2f}s - {response[:50]}...")
```

## 🎯 Jupyter Notebook Testing

### Start Jupyter Lab

```bash
# Activate environment
source venv/bin/activate

# Start Jupyter Lab
jupyter lab
```

### Test in Notebook

1. Create a new notebook
2. Select the "Python (Strand Agents)" kernel
3. Test basic functionality:

```python
# Cell 1: Test imports
from agents.specialized_agents import math_agent
import ollama

print("✅ Imports successful")

# Cell 2: Test agent
agent = math_agent(model="deepseek-r1:7b")
response = agent.chat("Hello, are you working?")
print(response)

# Cell 3: Test Ollama directly
response = ollama.chat(
    model="deepseek-r1:7b",
    messages=[{"role": "user", "content": "Say hello!"}]
)
print(response['message']['content'])
```

## 🚀 Advanced Testing

### Test Agent Orchestration

```python
from agents.specialized_agents import math_agent, creative_agent

# Create agents
math_ai = math_agent(model="deepseek-r1:7b")
creative_ai = creative_agent(model="deepseek-r1:7b")

# Sequential workflow
math_result = math_ai.chat("Calculate 12 * 8")
story_prompt = f"Write a short story involving the number {math_result}"
story = creative_ai.chat(story_prompt)

print("Math result:", math_result)
print("Story:", story)
```

### Test Error Handling

```python
from agents.ollama_agent import OllamaStrandAgent

# Test with non-existent model
try:
    agent = OllamaStrandAgent(name="Test", model="nonexistent-model")
    response = agent.chat("Hello")
except Exception as e:
    print(f"Expected error: {e}")

# Test with invalid prompt
try:
    agent = OllamaStrandAgent(name="Test", model="deepseek-r1:7b")
    response = agent.chat("")  # Empty prompt
    print(f"Empty prompt response: {response}")
except Exception as e:
    print(f"Error with empty prompt: {e}")
```

## 🎉 Success Indicators

Your setup is working correctly if:

- ✅ `python main.py` shows all tests passing
- ✅ Ollama responds to direct API calls
- ✅ Agents can chat and provide responses
- ✅ Jupyter notebooks can import and use agents
- ✅ No import errors or connection failures

## 📞 Getting Help

If tests fail:

1. **Check Ollama**: Ensure it's running with `ps aux | grep ollama`
2. **Check Models**: Verify models with `ollama list`
3. **Check Environment**: Ensure virtual environment is activated
4. **Check Logs**: Look at Ollama output for errors
5. **Restart**: Try `pkill -f ollama && ollama serve`

For specific errors, check the [main README](README.md) troubleshooting section.

---

## 🎯 What's Next?

Once all tests pass:

1. **Explore Notebooks**: Open `notebooks/01_getting_started.ipynb`
2. **Build Custom Agents**: Create your own specialized agents
3. **Add Tools**: Extend agents with custom tools
4. **Create Workflows**: Build multi-agent pipelines

**Happy testing! 🚀**