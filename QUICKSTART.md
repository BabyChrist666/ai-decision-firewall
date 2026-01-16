# 🚀 Baby AGI - Quick Start Guide

Get started with Baby AGI in 5 minutes!

## Installation

No installation needed! Baby AGI runs with just Python 3.8+.

```bash
# Clone the repository
git clone <repository-url>
cd ai-decision-firewall

# Optional: Install LLM dependencies (only if using cloud LLMs)
pip install openai anthropic
```

## Your First Baby AGI Command

### 1. Create a Folder

```bash
python -m baby_agi -o "Create a folder called my_project"
```

**What happens:**
- Baby AGI analyzes the objective
- Generates a task to create the folder
- Executes the task
- Confirms completion

**Result:** A new folder `workspace/my_project/` is created.

---

### 2. Create a Python File

```bash
python -m baby_agi -o "Create a Python file that prints hello world"
```

**What happens:**
- Baby AGI recognizes this as a code creation task
- Generates appropriate Python code
- Creates the file in the workspace

**Result:** A `workspace/script.py` file containing:
```python
print("Hello, World!")
```

---

### 3. Build a Calculator

```bash
python -m baby_agi -o "Create a Python calculator"
```

**What happens:**
- Baby AGI breaks this into subtasks
- Generates calculator code with functions
- Creates the complete program

**Result:** A working calculator with add, subtract, multiply, divide functions.

---

## Interactive Mode

Want to give multiple objectives? Use interactive mode:

```bash
python -m baby_agi
```

Then type your objectives:
```
💡 What would you like me to do?
> Create a folder called utils

💡 What would you like me to do?
> Create a Python file in utils that has helper functions

💡 What would you like me to do?
> quit
```

---

## Check What Was Created

All created files are in the `workspace/` directory:

```bash
ls -la workspace/
```

---

## Python API

Use Baby AGI in your Python code:

```python
from baby_agi import BabyAGI

# Create agent
agent = BabyAGI(verbose=True)

# Give it an objective
agent.set_objective("Create a Python calculator")

# Run it
summary = agent.run()

# Check results
print(f"Success: {summary['success']}")
print(f"Files created: {agent.get_workspace_files()}")
```

---

## More Examples

### Build a Complete Project

```bash
python -m baby_agi -o "Build a TODO app with add, remove, and list functions"
```

### Custom Workspace

```bash
python -m baby_agi -o "Create a web scraper" -w ./my_workspace
```

### Run Example Scripts

```bash
python examples/basic_examples.py
```

---

## How It Works

```
Your Objective
     ↓
Baby AGI analyzes it
     ↓
Generates tasks
     ↓
Executes tasks
     ↓
Learns from results
     ↓
Completes objective!
```

---

## What Can Baby AGI Do?

✅ Create folders and files
✅ Write code (Python, JavaScript, etc.)
✅ Build complete software projects
✅ Learn from experience
✅ Adapt to new situations
✅ Run completely locally

---

## Tips for Success

1. **Be Specific** - "Create a Python calculator" is better than "make a calculator"
2. **Start Simple** - Begin with basic tasks to understand how it works
3. **Check Output** - Look in `workspace/` to see what was created
4. **Use Verbose** - Add `-v` to see detailed progress
5. **Iterate** - Baby AGI learns over time!

---

## Common Use Cases

### File Operations
```bash
python -m baby_agi -o "Create a folder structure for a web project"
```

### Code Generation
```bash
python -m baby_agi -o "Create a Python script that sorts numbers"
```

### Complete Projects
```bash
python -m baby_agi -o "Build a contact manager with name, email, and phone"
```

---

## Next Steps

1. ✅ Try the quick start examples above
2. 📚 Read the full [BABY_AGI_README.md](BABY_AGI_README.md)
3. 🧪 Run the test suite: `python test_baby_agi.py`
4. 💡 Try the examples: `python examples/basic_examples.py`
5. 🚀 Build something amazing!

---

## Troubleshooting

**Q: Nothing happens when I run a command**
- Make sure you're in the project directory
- Check that Python 3.8+ is installed

**Q: Where are the created files?**
- Check the `workspace/` directory

**Q: Can I use it without internet?**
- Yes! Baby AGI runs completely locally by default

**Q: How do I use GPT-4 or Claude?**
- Set your API key and use `--llm openai` or `--llm anthropic`

---

## Ready to Start?

Try it now:

```bash
python -m baby_agi -o "Create a folder called my_first_baby_agi_project"
```

**Welcome to autonomous AI!** 🤖✨
