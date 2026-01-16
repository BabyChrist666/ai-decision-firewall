# 🤖 Baby AGI - Autonomous Agent System

**An intelligent, self-learning agent that can autonomously achieve any objective**

Baby AGI is an autonomous agent system that can take high-level objectives and break them down into actionable tasks, execute those tasks, learn from the results, and adapt until the objective is achieved.

---

## 🌟 Features

### Core Capabilities

✅ **Autonomous Task Planning** - Breaks down complex objectives into manageable tasks
✅ **Multi-Task Execution** - Handles file operations, code writing, execution, and more
✅ **Self-Learning** - Learns from successes and failures to improve over time
✅ **Adaptive Behavior** - Generates new tasks based on progress and results
✅ **Memory System** - Maintains short-term and long-term memory for context
✅ **Local Execution** - Runs completely locally, no cloud required (optional LLM integration)

### Supported Task Types

- 📁 **File Operations** - Create, edit, delete files
- 📂 **Folder Management** - Create directory structures
- 💻 **Code Writing** - Generate code in Python, JavaScript, and more
- ⚡ **Code Execution** - Run scripts and programs
- 🔍 **Research** - Gather information (with LLM integration)
- 📝 **Planning** - Create detailed plans
- ✅ **Testing** - Run tests and validate code
- 🔄 **Generic Tasks** - Execute any command-line task

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd ai-decision-firewall

# Install dependencies (optional, for LLM integration)
pip install openai anthropic  # Only if using cloud LLMs
```

### Basic Usage

#### Interactive Mode

Run Baby AGI in interactive mode to give it objectives interactively:

```bash
python -m baby_agi
```

#### Single Objective Mode

Run with a specific objective:

```bash
# Simple task
python -m baby_agi -o "Create a folder called projects"

# Complex task
python -m baby_agi -o "Create a Python calculator that can add, subtract, multiply, and divide"

# Build software
python -m baby_agi -o "Build a web scraper that extracts article titles from a webpage"
```

#### With Custom Workspace

```bash
python -m baby_agi -o "Create a TODO app" -w ./my_workspace
```

---

## 📖 Examples

### Example 1: Create a Folder

```bash
python -m baby_agi -o "Create a folder called projects"
```

**What Baby AGI does:**
1. Parses the objective
2. Creates a FOLDER_CREATE task
3. Executes the task
4. Confirms completion

**Result:** A new folder `projects/` in the workspace

---

### Example 2: Write a Python Script

```bash
python -m baby_agi -o "Create a Python file that prints hello world"
```

**What Baby AGI does:**
1. Identifies this as a code creation task
2. Generates appropriate Python code
3. Creates the file with the code
4. Saves it to workspace

**Result:** A `script.py` file containing:
```python
print("Hello, World!")
```

---

### Example 3: Build a Calculator

```bash
python -m baby_agi -o "Create a Python calculator"
```

**What Baby AGI does:**
1. Plans the calculator structure
2. Generates calculator code with functions
3. Creates the file
4. Validates the implementation

**Result:** A complete calculator program with add, subtract, multiply, divide functions

---

### Example 4: Build Complete Software

```bash
python -m baby_agi -o "Build a web scraper that extracts titles from websites"
```

**What Baby AGI does:**
1. Creates a plan for the software
2. Sets up project structure
3. Writes the main code
4. Creates a README file
5. Organizes everything properly

**Result:** A complete project with:
- Project folder structure
- Working web scraper code
- README documentation

---

## 🧠 How It Works

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      User Input                         │
│                   (Objective)                           │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   LLM Agent                             │
│            (Task Generation & Reasoning)                │
│  - Breaks down objective into tasks                     │
│  - Evaluates completion                                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Task Queue                             │
│            (Priority & Dependencies)                    │
│  - Manages task execution order                         │
│  - Handles dependencies                                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                Task Executor                            │
│         (File, Code, Command Execution)                 │
│  - Executes different task types                        │
│  - Returns results                                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│               Memory Manager                            │
│          (Learning & Adaptation)                        │
│  - Stores successful patterns                           │
│  - Learns from failures                                 │
│  - Provides context for new tasks                       │
└─────────────────────────────────────────────────────────┘
```

### The Main Loop

1. **Accept Objective** - User provides a high-level goal
2. **Generate Tasks** - LLM breaks it down into specific tasks
3. **Prioritize** - Tasks are ordered by priority and dependencies
4. **Execute** - Tasks are executed one by one
5. **Learn** - Results are analyzed and patterns are stored
6. **Adapt** - New tasks are generated if needed
7. **Repeat** - Continue until objective is achieved

---

## 🎯 Advanced Usage

### Using with OpenAI

```bash
export OPENAI_API_KEY="your-api-key"
python -m baby_agi -o "Your objective" --llm openai
```

### Using with Anthropic Claude

```bash
export ANTHROPIC_API_KEY="your-api-key"
python -m baby_agi -o "Your objective" --llm anthropic
```

### Custom Configuration

```bash
python -m baby_agi \
  -o "Build a REST API" \
  -w ./my_workspace \
  -m ./my_memory \
  --llm openai \
  --max-iterations 100
```

### Python API

```python
from baby_agi import BabyAGI

# Create agent
agent = BabyAGI(
    workspace_dir="./workspace",
    memory_dir="./memory",
    llm_model="local",
    verbose=True
)

# Set objective
agent.set_objective("Create a Python calculator")

# Run
summary = agent.run()

# Check results
print(f"Completed: {summary['tasks']['completed']}")
print(f"Files created: {agent.get_workspace_files()}")
```

---

## 🔧 Configuration

### Command Line Options

```
-o, --objective      Objective to achieve
-w, --workspace      Workspace directory (default: ./workspace)
-m, --memory         Memory directory (default: ./memory)
--llm               LLM model: local, openai, anthropic (default: local)
--api-key           API key for cloud LLMs
--max-iterations    Maximum iterations (default: 50)
```

### Environment Variables

```bash
export OPENAI_API_KEY="your-key"      # For OpenAI
export ANTHROPIC_API_KEY="your-key"   # For Anthropic Claude
```

---

## 🧪 Testing

Create a test script to try various objectives:

```python
from baby_agi import BabyAGI

objectives = [
    "Create a folder called test_project",
    "Create a Python file that prints hello world",
    "Build a simple calculator",
]

agent = BabyAGI(verbose=True)

for obj in objectives:
    print(f"\n{'='*60}")
    print(f"Testing: {obj}")
    print('='*60)

    agent.set_objective(obj)
    summary = agent.run()

    print(f"✓ Success: {summary['success']}")
    print(f"  Completed: {summary['tasks']['completed']}")
```

---

## 📚 Task Types Reference

### File Operations

```python
# Create file
Task(
    task_type=TaskType.FILE_CREATE,
    context={
        "file_path": "example.txt",
        "content": "Hello, World!"
    }
)

# Edit file
Task(
    task_type=TaskType.FILE_EDIT,
    context={
        "file_path": "example.txt",
        "content": "New content",
        "append": False
    }
)
```

### Code Operations

```python
# Write code
Task(
    task_type=TaskType.CODE_WRITE,
    context={
        "file_path": "script.py",
        "code": "print('Hello')",
        "language": "python"
    }
)

# Execute code
Task(
    task_type=TaskType.CODE_EXECUTE,
    context={
        "file_path": "script.py",
        "language": "python",
        "args": []
    }
)
```

---

## 🎓 Learning System

Baby AGI learns and improves over time by:

1. **Recording Task Success Rates** - Tracks which task types succeed/fail
2. **Storing Successful Patterns** - Remembers sequences that work
3. **Avoiding Common Failures** - Learns from mistakes
4. **Context Building** - Uses past experience for new objectives
5. **Strategy Adaptation** - Adjusts approach based on feedback

Memory is stored in JSON files and persists across sessions.

---

## 🔒 Safety & Limitations

### What Baby AGI Can Do

✅ Create and manage files in the workspace
✅ Write and execute code
✅ Run command-line tools
✅ Build complete software projects
✅ Learn and adapt from experience

### What Baby AGI Cannot Do (Currently)

❌ Access the internet (without LLM integration)
❌ Modify files outside the workspace
❌ Install system packages
❌ Execute privileged commands
❌ Make network requests (unless code it writes does)

### Safety Features

- **Sandboxed Workspace** - All file operations are limited to workspace directory
- **Timeout Protection** - Commands have timeouts to prevent hanging
- **Error Handling** - Graceful failure recovery
- **Task Limits** - Maximum iteration count prevents infinite loops

---

## 🛣️ Roadmap

### Planned Features

- [ ] Web browsing capability
- [ ] Integration with external APIs
- [ ] Multi-agent collaboration
- [ ] Visual feedback and monitoring
- [ ] Web UI dashboard
- [ ] Docker containerization
- [ ] Package installation capability
- [ ] Git integration
- [ ] Enhanced LLM reasoning
- [ ] Reinforcement learning

---

## 🤝 Contributing

Baby AGI is open for contributions! Areas of interest:

- New task executors
- Better LLM prompts
- Enhanced learning algorithms
- UI improvements
- Documentation
- Examples and tutorials

---

## 📝 License

[Specify your license here]

---

## 🙏 Acknowledgments

Inspired by the original Baby AGI concept and autonomous agent research.

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the documentation
- Review examples

---

**Baby AGI - Making AI truly autonomous, one task at a time.** 🚀
