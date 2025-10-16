"""
VS Code Integration Test for Amazon Strand Agents
Run this in a Jupyter notebook to verify everything works
"""

def test_vscode_integration():
    """Test VS Code + Jupyter integration with our agents"""
    print("🧪 VS Code Integration Test")
    print("=" * 30)
    
    # Test 1: Environment check
    import sys
    print(f"✅ Python: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    print(f"✅ Virtual Environment: {'venv' in sys.executable}")
    
    # Test 2: Package imports
    try:
        import ollama
        import jupyter
        from agents.specialized_agents import math_agent
        print("✅ All packages imported successfully")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test 3: Agent creation
    try:
        agent = math_agent(model="deepseek-r1:7b")
        print("✅ Agent created successfully")
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False
    
    # Test 4: Simple chat
    try:
        response = agent.chat("What is 3 + 4?")
        print(f"✅ Agent response: {response[:50]}...")
    except Exception as e:
        print(f"❌ Chat failed: {e}")
        return False
    
    print("\n🎉 All tests passed! VS Code integration is working.")
    return True

# Auto-run when imported
if __name__ == "__main__":
    test_vscode_integration()
else:
    # Run automatically in notebook
    test_vscode_integration()