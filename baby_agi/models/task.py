"""Task models for Baby AGI system."""
from enum import Enum
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import uuid


class TaskStatus(Enum):
    """Task execution status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class TaskType(Enum):
    """Types of tasks the Baby AGI can execute."""
    FILE_CREATE = "file_create"
    FILE_EDIT = "file_edit"
    FILE_DELETE = "file_delete"
    FOLDER_CREATE = "folder_create"
    CODE_WRITE = "code_write"
    CODE_EXECUTE = "code_execute"
    RESEARCH = "research"
    PLAN = "plan"
    REVIEW = "review"
    TEST = "test"
    GENERIC = "generic"


@dataclass
class Task:
    """Represents a single task in the Baby AGI system."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    task_type: TaskType = TaskType.GENERIC
    priority: int = 5  # 1-10, 10 being highest
    status: TaskStatus = TaskStatus.PENDING

    # Task dependencies
    depends_on: List[str] = field(default_factory=list)

    # Task execution details
    context: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    # Metadata
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    attempts: int = 0
    max_attempts: int = 3

    # Learning data
    success_patterns: List[str] = field(default_factory=list)
    failure_patterns: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "id": self.id,
            "description": self.description,
            "task_type": self.task_type.value,
            "priority": self.priority,
            "status": self.status.value,
            "depends_on": self.depends_on,
            "context": self.context,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "attempts": self.attempts,
            "max_attempts": self.max_attempts,
        }

    def can_execute(self, completed_task_ids: set) -> bool:
        """Check if task can be executed based on dependencies."""
        if self.status != TaskStatus.PENDING:
            return False
        if self.attempts >= self.max_attempts:
            return False
        return all(dep_id in completed_task_ids for dep_id in self.depends_on)

    def mark_started(self):
        """Mark task as started."""
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = datetime.now()
        self.attempts += 1

    def mark_completed(self, result: Dict[str, Any]):
        """Mark task as completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.result = result

    def mark_failed(self, error: str):
        """Mark task as failed."""
        if self.attempts >= self.max_attempts:
            self.status = TaskStatus.FAILED
        else:
            self.status = TaskStatus.PENDING
        self.error = error


@dataclass
class Objective:
    """Represents a high-level goal for Baby AGI."""

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    description: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    is_completed: bool = False

    # Context for the objective
    context: Dict[str, Any] = field(default_factory=dict)

    # Success criteria
    success_criteria: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert objective to dictionary."""
        return {
            "id": self.id,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "is_completed": self.is_completed,
            "context": self.context,
            "success_criteria": self.success_criteria,
        }
