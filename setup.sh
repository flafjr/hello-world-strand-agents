#!/bin/bash

# Amazon Strand Agents with Ollama - Startup Script
# This script helps you start the development environment

set -e

echo "🚀 Amazon Strand Agents with Ollama - Startup Script"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Ollama is installed
check_ollama() {
    print_status "Checking Ollama installation..."
    if command -v ollama &> /dev/null; then
        print_success "Ollama is installed"
        return 0
    else
        print_error "Ollama is not installed"
        echo "Please install Ollama from https://ollama.ai/"
        return 1
    fi
}

# Check if Ollama is running
check_ollama_service() {
    print_status "Checking if Ollama service is running..."
    if curl -s http://localhost:11434/api/tags &> /dev/null; then
        print_success "Ollama service is running"
        return 0
    else
        print_warning "Ollama service is not running"
        print_status "Starting Ollama service in background..."
        ollama serve &
        sleep 3
        if curl -s http://localhost:11434/api/tags &> /dev/null; then
            print_success "Ollama service started successfully"
            return 0
        else
            print_error "Failed to start Ollama service"
            return 1
        fi
    fi
}

# Check for required models
check_models() {
    print_status "Checking available models..."
    local models=$(ollama list 2>/dev/null | grep -v "NAME" | wc -l)
    
    if [ "$models" -eq 0 ]; then
        print_warning "No models found. Pulling default model..."
        print_status "Pulling llama3.2 model (this may take a while)..."
        ollama pull llama3.2
        print_success "llama3.2 model pulled successfully"
    else
        print_success "Found $models model(s)"
        ollama list
    fi
}

# Check Python version
check_python() {
    print_status "Checking Python version..."
    
    if command -v python3.11 &> /dev/null; then
        local python_cmd="python3.11"
    elif command -v python3.10 &> /dev/null; then
        local python_cmd="python3.10"
    elif command -v python3 &> /dev/null; then
        local python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        if [[ $(echo "$python_version >= 3.10" | bc -l) -eq 1 ]]; then
            local python_cmd="python3"
        else
            print_error "Python 3.10+ required, found Python $python_version"
            return 1
        fi
    else
        print_error "Python 3.10+ not found"
        return 1
    fi
    
    print_success "Using $python_cmd"
    echo $python_cmd > .python_cmd
}

# Setup virtual environment
setup_venv() {
    local python_cmd=$(cat .python_cmd 2>/dev/null || echo "python3")
    
    print_status "Setting up virtual environment..."
    
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        $python_cmd -m venv venv
        print_success "Virtual environment created"
    else
        print_success "Virtual environment already exists"
    fi
    
    print_status "Activating virtual environment..."
    source venv/bin/activate
    
    print_status "Upgrading pip..."
    pip install --upgrade pip > /dev/null 2>&1
    
    print_status "Installing requirements..."
    pip install -r requirements.txt > /dev/null 2>&1
    print_success "Requirements installed"
    
    print_status "Installing Jupyter kernel..."
    python -m ipykernel install --user --name strand-agents --display-name "Python (Strand Agents)" > /dev/null 2>&1
    print_success "Jupyter kernel installed"
}

# Start Jupyter Lab
start_jupyter() {
    print_status "Starting Jupyter Lab..."
    print_success "Jupyter Lab will open in your browser"
    print_status "Use Ctrl+C to stop Jupyter Lab when you're done"
    echo ""
    echo "📚 Open these notebooks to get started:"
    echo "   - notebooks/01_getting_started.ipynb"
    echo "   - notebooks/02_advanced_patterns.ipynb"
    echo ""
    
    source venv/bin/activate
    jupyter lab --ip=127.0.0.1 --port=8888 --no-browser
}

# Main execution
main() {
    echo ""
    
    # Run checks
    if ! check_ollama; then
        exit 1
    fi
    
    if ! check_ollama_service; then
        exit 1
    fi
    
    check_models
    
    if ! check_python; then
        exit 1
    fi
    
    setup_venv
    
    print_success "Setup complete! 🎉"
    echo ""
    echo "Next steps:"
    echo "  1. Activate virtual environment: source venv/bin/activate"
    echo "  2. Start Jupyter Lab: jupyter lab"
    echo "  3. Open notebooks/01_getting_started.ipynb"
    echo ""
    
    read -p "Would you like to start Jupyter Lab now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        start_jupyter
    fi
    
    # Cleanup
    rm -f .python_cmd
}

# Run main function
main "$@"