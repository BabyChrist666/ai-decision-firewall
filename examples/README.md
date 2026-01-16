# Baby AGI Examples

This directory contains example scripts demonstrating Baby AGI's capabilities.

## Basic Examples

Run basic examples to see fundamental capabilities:

```bash
python examples/basic_examples.py
```

**Includes:**
- Creating folders
- Creating files
- Writing Python scripts
- Building a calculator
- Creating complete projects
- Multiple sequential objectives

## Advanced Examples

Run advanced examples to see learning and adaptation:

```bash
python examples/advanced_examples.py
```

**Includes:**
- Building a web scraper
- Learning from repeated tasks
- Creating complex multi-file projects
- Memory and learning inspection
- Using cloud LLMs (optional)

## Quick Examples

### Example 1: Simple Folder

```bash
python -m baby_agi -o "Create a folder called test_project"
```

### Example 2: Python Script

```bash
python -m baby_agi -o "Create a Python file that prints hello world"
```

### Example 3: Calculator

```bash
python -m baby_agi -o "Create a Python calculator"
```

### Example 4: Web Scraper

```bash
python -m baby_agi -o "Build a web scraper that extracts titles"
```

### Example 5: Complete Project

```bash
python -m baby_agi -o "Build a TODO application with add, remove, and list functions"
```

## Tips

1. **Start Simple** - Begin with basic objectives to understand how Baby AGI works
2. **Be Specific** - Clear objectives lead to better results
3. **Iterate** - Baby AGI learns over time, so repeat similar tasks
4. **Check Output** - Look in the workspace directory to see what was created
5. **Use Verbose** - The `-v` flag or `verbose=True` shows detailed progress

## Workspace

All examples create files in workspace directories:
- `basic_examples.py` → `./workspace_examples/`
- `advanced_examples.py` → `./workspace_advanced/`

## Memory

Baby AGI stores learning in memory directories:
- `basic_examples.py` → `./memory/`
- `advanced_examples.py` → `./memory_advanced/`

Memory persists across runs, allowing Baby AGI to learn and improve!
