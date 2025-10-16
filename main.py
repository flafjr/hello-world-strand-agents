#!/usr/bin/env python3
"""
Test script for Amazon Strand Agents with Ollama integration
"""
import sys
import os
import requests
import time

def test_ollama_connection():
    """Test if Ollama is running and accessible"""
    print("🔍 Testing Ollama connection...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama is running with {len(models)} model(s)")
            for model in models:
                print(f"   - {model['name']}")
            return True, models
        else:
            print(f"❌ Ollama responded with status code: {response.status_code}")
            return False, []
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama. Make sure it's running with: ollama serve")
        return False, []
    except Exception as e:
        print(f"❌ Error connecting to Ollama: {e}")
        return False, []

def test_simple_ollama_chat(model_name="deepseek-r1:7b"):
    """Test direct Ollama chat API"""
    print(f"\n🤖 Testing direct Ollama chat with {model_name}...")
    
    try:
        payload = {
            "model": model_name,
            "messages": [
                {"role": "user", "content": "What is 2 + 2? Please answer briefly."}
            ],
            "stream": False
        }
        
        print("   Sending request to Ollama...")
        response = requests.post(
            "http://localhost:11434/api/chat", 
            json=payload, 
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            answer = result.get('message', {}).get('content', 'No content')
            print(f"✅ Ollama responded: {answer.strip()}")
            return True
        else:
            print(f"❌ Chat failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error in chat: {e}")
        return False

def test_ollama_agent():
    """Test our custom Ollama agent"""
    print(f"\n🎯 Testing custom Ollama agent...")
    
    try:
        # Import our custom agent
        from agents.ollama_agent import OllamaStrandAgent
        
        # Create agent with available model
        agent = OllamaStrandAgent(
            name="TestAgent",
            model="deepseek-r1:7b",
            system_prompt="You are a helpful assistant. Keep responses brief and clear."
        )
        
        print("   Created agent, testing chat...")
        response = agent.chat("What is the square root of 1764?")
        print(f"✅ Agent responded: {response}")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're running from the project directory")
        return False
    except Exception as e:
        print(f"❌ Agent error: {e}")
        return False

def test_specialized_agents():
    """Test specialized agents"""
    print(f"\n🔧 Testing specialized agents...")
    
    try:
        from agents.specialized_agents import math_agent
        
        # Create math agent with available model
        math_ai = math_agent(model="deepseek-r1:7b")
        
        print("   Testing math agent...")
        response = math_ai.chat("Calculate 15 * 24")
        print(f"✅ Math agent: {response[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Specialized agent error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Amazon Strand Agents + Ollama Test Suite")
    print("=" * 50)
    
    # Test 1: Ollama connection
    ollama_ok, models = test_ollama_connection()
    if not ollama_ok:
        print("\n❌ Cannot proceed without Ollama. Please run: ollama serve")
        sys.exit(1)
    
    if not models:
        print("\n⚠️  No models found. Installing a basic model...")
        os.system("ollama pull llama3.2:3b")
        models = [{"name": "llama3.2:3b"}]
    
    model_name = models[0]["name"]
    
    # Test 2: Direct Ollama chat
    chat_ok = test_simple_ollama_chat(model_name)
    
    # Test 3: Custom agent
    agent_ok = test_ollama_agent()
    
    # Test 4: Specialized agents
    specialized_ok = test_specialized_agents()
    
    # Summary
    print(f"\n📋 Test Results:")
    print(f"   Ollama Connection: {'✅' if ollama_ok else '❌'}")
    print(f"   Direct Chat: {'✅' if chat_ok else '❌'}")
    print(f"   Custom Agent: {'✅' if agent_ok else '❌'}")
    print(f"   Specialized Agents: {'✅' if specialized_ok else '❌'}")
    
    if all([ollama_ok, chat_ok, agent_ok, specialized_ok]):
        print(f"\n🎉 All tests passed! Your setup is working perfectly.")
        print(f"\nNext steps:")
        print(f"   1. Open Jupyter: jupyter lab")
        print(f"   2. Try the notebooks in /notebooks/")
        print(f"   3. Build your own agents!")
    else:
        print(f"\n⚠️  Some tests failed. Check the errors above.")
        if not agent_ok:
            print(f"   💡 Try: source venv/bin/activate")

if __name__ == "__main__":
    main()