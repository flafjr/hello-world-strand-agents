#!/usr/bin/env python3
"""
Interactive test script for Amazon Strand Agents with Ollama
"""
import sys
import os
import requests

def interactive_test():
    """Interactive testing session"""
    print("🤖 Amazon Strand Agents - Interactive Test")
    print("=" * 40)
    
    # Check Ollama
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        models = response.json().get('models', [])
        if not models:
            print("⚠️  No models found. Let's pull one...")
            os.system("ollama pull llama3.2:3b")
            models = [{"name": "llama3.2:3b"}]
        
        model_name = models[0]["name"]
        print(f"✅ Using model: {model_name}")
        
    except:
        print("❌ Ollama not running. Please start it: ollama serve")
        return
    
    # Import agents
    try:
        from agents.specialized_agents import math_agent, creative_agent, code_agent
        print("✅ Agents imported successfully")
    except Exception as e:
        print(f"❌ Import error: {e}")
        return
    
    # Create agents
    agents = {
        "1": ("Math Agent", math_agent(model=model_name)),
        "2": ("Creative Agent", creative_agent(model=model_name)),
        "3": ("Code Agent", code_agent(model=model_name))
    }
    
    print(f"\n🎯 Available Agents:")
    for key, (name, _) in agents.items():
        print(f"   {key}. {name}")
    
    while True:
        print(f"\n" + "─" * 40)
        choice = input("Choose agent (1-3) or 'q' to quit: ").strip()
        
        if choice.lower() == 'q':
            print("👋 Goodbye!")
            break
        
        if choice not in agents:
            print("❌ Invalid choice")
            continue
        
        agent_name, agent = agents[choice]
        print(f"\n🤖 {agent_name} selected")
        
        message = input("Your message: ").strip()
        if not message:
            continue
        
        print(f"\n💭 {agent_name} is thinking...")
        try:
            response = agent.chat(message)
            print(f"\n🗣️  {agent_name}:")
            print(f"   {response}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    interactive_test()