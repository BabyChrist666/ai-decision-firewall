"""
Baby AGI - Autonomous Agent System

A self-learning autonomous agent that can:
- Accept high-level objectives
- Break them down into actionable tasks
- Execute tasks (file operations, code creation, etc.)
- Learn from results and adapt
- Iterate until objectives are achieved
"""

from baby_agi.agent import BabyAGI
from baby_agi.models import Task, TaskType, TaskStatus, Objective
from baby_agi.core import TaskQueue, ObjectiveManager, TaskExecutor
from baby_agi.llm import LLMAgent
from baby_agi.memory import MemoryManager

__version__ = "0.1.0"

__all__ = [
    "BabyAGI",
    "Task",
    "TaskType",
    "TaskStatus",
    "Objective",
    "TaskQueue",
    "ObjectiveManager",
    "TaskExecutor",
    "LLMAgent",
    "MemoryManager",
]
