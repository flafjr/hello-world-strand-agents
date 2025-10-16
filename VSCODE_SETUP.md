# VS Code Setup for Amazon Strand Agents

This guide will help you configure VS Code properly to work with Jupyter notebooks and Python environments for the Amazon Strand Agents project.

## 🔧 Required VS Code Extensions

### Essential Extensions

Install these extensions for full functionality:

1. **Jupyter** (`ms-toolsai.jupyter`) - Core Jupyter notebook support
2. **Python** (`ms-python.python`) - Python language support
3. **Pylance** (`ms-python.vscode-pylance`) - Python IntelliSense 
4. **Python Debugger** (`ms-python.debugpy`) - Python debugging support

### Optional but Recommended Extensions

5. **Jupyter Notebook Renderers** (`ms-toolsai.jupyter-renderers`) - Enhanced output rendering
6. **Jupyter PowerToys** (`ms-toolsai.vscode-jupyter-powertoys`) - Additional Jupyter features
7. **GitHub Copilot** (`github.copilot`) - AI code assistance
8. **GitHub Copilot Chat** (`github.copilot-chat`) - AI chat features

## 📦 Installation Methods

### Method 1: Command Palette (Recommended)

1. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
2. Type: "Extensions: Install Extensions"
3. Search for and install each extension by ID:
   - `ms-toolsai.jupyter`
   - `ms-python.python`
   - `ms-python.vscode-pylance`
   - `ms-python.debugpy`

### Method 2: Extensions Marketplace

1. Click the Extensions icon in the sidebar (or press `Ctrl+Shift+X`)
2. Search for "Jupyter" and install the official Microsoft Jupyter extension
3. Search for "Python" and install the official Microsoft Python extension

### Method 3: Command Line

```bash
# Install via VS Code CLI (if available)
code --install-extension ms-toolsai.jupyter
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-python.debugpy
```

## 🐍 Python Environment Setup

### 1. Select Python Interpreter

1. Open VS Code in your project directory
2. Press `Ctrl+Shift+P` and type "Python: Select Interpreter"
3. Choose the interpreter from your virtual environment:
   ```
   ./venv/bin/python
   ```

### 2. Verify Virtual Environment

Ensure your virtual environment is activated:

```bash
# Navigate to project directory
cd hello-world-strand-agents

# Activate virtual environment
source venv/bin/activate

# Verify Python version
python --version  # Should show Python 3.10+

# Verify packages
pip list | grep -E "(jupyter|strand|ollama)"
```

### 3. Install/Reinstall Jupyter Kernel

If the kernel is not showing up:

```bash
# Activate virtual environment
source venv/bin/activate

# Install ipykernel
pip install ipykernel

# Install kernel for VS Code
python -m ipykernel install --user --name strand-agents --display-name "Python (Strand Agents)"

# List available kernels
jupyter kernelspec list
```

## 📓 Jupyter Notebook Configuration

### 1. Open Notebook in VS Code

1. Open VS Code in the project directory
2. Navigate to `notebooks/01_getting_started.ipynb`
3. VS Code should automatically detect it as a Jupyter notebook

### 2. Select Kernel

1. Click on the kernel selector in the top-right of the notebook
2. Choose "Python (Strand Agents)" or the venv Python interpreter
3. If you don't see the kernel, try refreshing with `Ctrl+Shift+P` → "Developer: Reload Window"

### 3. Test Kernel Connection

Run this cell to test the setup:

```python
import sys
print(f"Python version: {sys.version}")
print(f"Python path: {sys.executable}")

# Test Ollama connection
try:
    import ollama
    models = ollama.list()
    print(f"Ollama connected! Available models: {len(models['models'])}")
except Exception as e:
    print(f"Ollama connection error: {e}")
```

## 🛠️ Troubleshooting Common Issues

### Issue 1: "Jupyter is not installed"

**Solution:**
```bash
source venv/bin/activate
pip install jupyter jupyterlab ipykernel
python -m ipykernel install --user --name strand-agents
```

### Issue 2: Kernel not appearing in VS Code

**Solution:**
1. Restart VS Code completely
2. Ensure virtual environment is activated
3. Try reinstalling the kernel:
   ```bash
   jupyter kernelspec uninstall strand-agents
   python -m ipykernel install --user --name strand-agents --display-name "Python (Strand Agents)"
   ```

### Issue 3: "Module not found" errors in notebooks

**Solution:**
1. Verify the correct kernel is selected
2. Check that all packages are installed in the virtual environment:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### Issue 4: Ollama connection fails

**Solution:**
1. Ensure Ollama is running:
   ```bash
   ollama serve
   ```
2. Test connection:
   ```bash
   curl http://localhost:11434/api/tags
   ```
3. Pull required models:
   ```bash
   ollama pull llama3.2
   ollama pull codellama
   ```

### Issue 5: VS Code doesn't recognize Python files

**Solution:**
1. Install Python extension if not installed
2. Select correct Python interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter"
3. Choose the venv Python: `./venv/bin/python`

## ⚙️ VS Code Settings Configuration

Create or update `.vscode/settings.json` in your project:

```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "jupyter.kernels.excludePythonEnvironments": [],
    "jupyter.interactiveWindow.cellMarker.codeRegex": "^(#\\s*%%|#\\s*\\<codecell\\>|#\\s*In\\[\\d*?\\]|#\\s*In\\[ \\])",
    "python.analysis.extraPaths": [
        "./agents",
        "./tools", 
        "./config"
    ],
    "python.analysis.include": [
        "./agents/**",
        "./tools/**",
        "./config/**",
        "./notebooks/**"
    ],
    "files.associations": {
        "*.ipynb": "jupyter-notebook"
    }
}
```

## 🚀 Quick Verification Script

Run this script to verify everything is working:

```bash
#!/bin/bash
echo "🔍 Verifying VS Code Jupyter setup..."

# Check if in project directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Please run this from the hello-world-strand-agents directory"
    exit 1
fi

# Check virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run ./setup.sh first"
    exit 1
fi

# Activate environment
source venv/bin/activate

# Check Python version
python_version=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python version: $python_version"

# Check required packages
echo "🔍 Checking required packages..."
packages=("jupyter" "ollama" "strands-agents")
for package in "${packages[@]}"; do
    if pip show $package >/dev/null 2>&1; then
        echo "✅ $package installed"
    else
        echo "❌ $package missing"
    fi
done

# Check Jupyter kernels
echo "🔍 Available Jupyter kernels:"
jupyter kernelspec list | grep strand-agents && echo "✅ Strand Agents kernel found" || echo "❌ Strand Agents kernel missing"

# Check Ollama
echo "🔍 Testing Ollama connection..."
if curl -s http://localhost:11434/api/tags >/dev/null; then
    echo "✅ Ollama is running"
else
    echo "❌ Ollama is not running. Start with: ollama serve"
fi

echo "✅ Verification complete!"
```

## 📝 Next Steps

After completing the setup:

1. **Open VS Code** in the project directory
2. **Open a notebook**: `notebooks/01_getting_started.ipynb`
3. **Select the kernel**: Choose "Python (Strand Agents)"
4. **Run the first cell** to test the setup
5. **Follow the notebook examples** to learn the framework

## 🆘 Still Having Issues?

If you're still experiencing problems:

1. **Check VS Code Output Panel**: View → Output → Select "Jupyter" or "Python"
2. **Restart VS Code completely**
3. **Reinstall extensions** if necessary
4. **Use the automated setup script**: `./setup.sh`
5. **Check the main README** for additional troubleshooting steps

## 📚 Additional Resources

- [VS Code Jupyter Documentation](https://code.visualstudio.com/docs/datascience/jupyter-notebooks)
- [VS Code Python Documentation](https://code.visualstudio.com/docs/python/python-tutorial)
- [Ollama Documentation](https://ollama.ai/docs)
- [Jupyter Kernels Guide](https://jupyter.readthedocs.io/en/latest/install-kernel.html)