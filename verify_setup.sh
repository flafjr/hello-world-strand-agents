#!/bin/bash

# VS Code Jupyter Setup Verification Script
echo "🔍 Verifying VS Code Jupyter setup for Amazon Strand Agents..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠️${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ️${NC} $1"
}

# Check if in project directory
if [ ! -f "requirements.txt" ]; then
    print_error "Please run this from the hello-world-strand-agents directory"
    exit 1
fi

print_info "Checking project structure..."

# Check virtual environment
if [ ! -d "venv" ]; then
    print_error "Virtual environment not found. Run ./setup.sh first"
    exit 1
fi
print_success "Virtual environment found"

# Activate environment
source venv/bin/activate

# Check Python version
python_version=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
if [[ $(echo "$python_version >= 3.10" | bc -l) -eq 1 ]]; then
    print_success "Python version: $python_version"
else
    print_error "Python version $python_version is too old. Need 3.10+"
    exit 1
fi

# Check required packages
print_info "Checking required packages..."
packages=("jupyter" "jupyterlab" "ipykernel" "ollama" "strands-agents")
for package in "${packages[@]}"; do
    if pip show $package >/dev/null 2>&1; then
        print_success "$package installed"
    else
        print_error "$package missing - run: pip install $package"
    fi
done

# Check Jupyter kernels
print_info "Checking Jupyter kernels..."
if jupyter kernelspec list | grep -q "strand-agents"; then
    print_success "Strand Agents kernel found"
else
    print_warning "Strand Agents kernel missing"
    print_info "Installing kernel..."
    python -m ipykernel install --user --name strand-agents --display-name "Python (Strand Agents)"
    if [ $? -eq 0 ]; then
        print_success "Kernel installed successfully"
    else
        print_error "Failed to install kernel"
    fi
fi

# List all available kernels
print_info "Available Jupyter kernels:"
jupyter kernelspec list

# Check Ollama
print_info "Testing Ollama connection..."
if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    print_success "Ollama is running"
    
    # Check available models
    models_count=$(curl -s http://localhost:11434/api/tags | python -c "import sys, json; data=json.load(sys.stdin); print(len(data['models']))" 2>/dev/null || echo "0")
    if [ "$models_count" -gt 0 ]; then
        print_success "Found $models_count Ollama model(s)"
    else
        print_warning "No Ollama models found. Pull models with: ollama pull llama3.2"
    fi
else
    print_error "Ollama is not running. Start with: ollama serve"
fi

# Check VS Code settings
if [ -f ".vscode/settings.json" ]; then
    print_success "VS Code settings configured"
else
    print_warning "VS Code settings not found"
fi

# Check project structure
print_info "Checking project structure..."
directories=("agents" "tools" "config" "notebooks")
for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        print_success "$dir/ directory exists"
    else
        print_error "$dir/ directory missing"
    fi
done

# Check important files
files=("agents/ollama_agent.py" "agents/specialized_agents.py" "tools/custom_tools.py" "notebooks/01_getting_started.ipynb")
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        print_success "$file exists"
    else
        print_error "$file missing"
    fi
done

echo ""
print_info "=== VERIFICATION SUMMARY ==="

# Final recommendations
echo ""
print_info "Next steps to use VS Code with Jupyter:"
echo "1. Open VS Code in this directory: code ."
echo "2. Install required extensions (see VSCODE_SETUP.md)"
echo "3. Open notebooks/01_getting_started.ipynb"
echo "4. Select 'Python (Strand Agents)' kernel"
echo "5. Run the first cell to test setup"

echo ""
print_success "Verification complete! Check VSCODE_SETUP.md for detailed instructions."