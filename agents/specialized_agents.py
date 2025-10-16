"""
Specialized Agent Examples for Amazon Strand Agents with Ollama
"""
import logging
from agents.ollama_agent import OllamaStrandAgent
from strands_tools import calculator

logger = logging.getLogger(__name__)

class MathAgent(OllamaStrandAgent):
    """
    Specialized agent for mathematical calculations and problem solving
    """
    
    def __init__(self, model: str = "llama3.2"):
        system_prompt = """
        You are a mathematical expert assistant. You excel at:
        - Solving complex mathematical problems
        - Explaining mathematical concepts clearly
        - Performing calculations accurately
        - Working with statistics, algebra, calculus, and more
        
        Always show your work step-by-step and use the calculator tool when needed.
        """
        
        super().__init__(
            name="MathAgent",
            model=model,
            tools=[calculator],
            system_prompt=system_prompt
        )

class ResearchAgent(OllamaStrandAgent):
    """
    Specialized agent for research and information gathering
    """
    
    def __init__(self, model: str = "llama3.2"):
        system_prompt = """
        You are a research specialist assistant. You excel at:
        - Finding and analyzing information from various sources
        - Summarizing complex topics
        - Fact-checking and verification
        - Providing comprehensive research reports
        
        Always cite your sources and provide accurate, up-to-date information.
        """
        
        super().__init__(
            name="ResearchAgent",
            model=model,
            tools=[],  # Web search tool not available yet
            system_prompt=system_prompt
        )

class CodeAgent(OllamaStrandAgent):
    """
    Specialized agent for programming and code-related tasks
    """
    
    def __init__(self, model: str = "codellama"):
        system_prompt = """
        You are a programming expert assistant. You excel at:
        - Writing clean, efficient code in multiple languages
        - Debugging and troubleshooting code issues
        - Explaining programming concepts
        - Code review and optimization
        - Best practices and design patterns
        
        Always provide working code examples with clear explanations.
        """
        
        super().__init__(
            name="CodeAgent",
            model=model,
            tools=[],
            system_prompt=system_prompt
        )

class AnalysisAgent(OllamaStrandAgent):
    """
    Specialized agent for data analysis and insights
    """
    
    def __init__(self, model: str = "llama3.2"):
        system_prompt = """
        You are a data analysis expert assistant. You excel at:
        - Analyzing datasets and finding patterns
        - Creating data visualizations
        - Statistical analysis and interpretation
        - Business intelligence and reporting
        - Machine learning concepts
        
        Always provide clear insights with supporting evidence.
        """
        
        super().__init__(
            name="AnalysisAgent",
            model=model,
            tools=[calculator],
            system_prompt=system_prompt
        )

class CreativeAgent(OllamaStrandAgent):
    """
    Specialized agent for creative writing and content generation
    """
    
    def __init__(self, model: str = "llama3.2"):
        system_prompt = """
        You are a creative writing expert assistant. You excel at:
        - Creative writing and storytelling
        - Content creation for various formats
        - Brainstorming and ideation
        - Editing and improving existing content
        - Adapting tone and style for different audiences
        
        Always be creative, engaging, and original in your responses.
        """
        
        super().__init__(
            name="CreativeAgent",
            model=model,
            tools=[],
            system_prompt=system_prompt
        )

# Agent factory function
def create_agent(agent_type: str, model: str = None) -> OllamaStrandAgent:
    """
    Factory function to create different types of agents
    
    Args:
        agent_type: Type of agent to create ('math', 'research', 'code', 'analysis', 'creative')
        model: Ollama model to use (optional)
    
    Returns:
        Initialized agent instance
    """
    agents = {
        'math': MathAgent,
        'research': ResearchAgent,
        'code': CodeAgent,
        'analysis': AnalysisAgent,
        'creative': CreativeAgent
    }
    
    if agent_type.lower() not in agents:
        raise ValueError(f"Unknown agent type: {agent_type}. Available types: {list(agents.keys())}")
    
    agent_class = agents[agent_type.lower()]
    
    if model:
        return agent_class(model=model)
    else:
        return agent_class()

# Quick access functions
def math_agent(model: str = "llama3.2") -> MathAgent:
    """Create a math agent"""
    return MathAgent(model)

def research_agent(model: str = "llama3.2") -> ResearchAgent:
    """Create a research agent"""
    return ResearchAgent(model)

def code_agent(model: str = "codellama") -> CodeAgent:
    """Create a code agent"""
    return CodeAgent(model)

def analysis_agent(model: str = "llama3.2") -> AnalysisAgent:
    """Create an analysis agent"""
    return AnalysisAgent(model)

def creative_agent(model: str = "llama3.2") -> CreativeAgent:
    """Create a creative agent"""
    return CreativeAgent(model)