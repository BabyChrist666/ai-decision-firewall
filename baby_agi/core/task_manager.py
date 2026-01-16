"""Task queue and management for Baby AGI."""
from typing import List, Optional, Dict, Any, Set
from collections import deque
from datetime import datetime
import heapq
from baby_agi.models import Task, TaskStatus, Objective


class TaskQueue:
    """Priority queue for managing Baby AGI tasks."""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.completed_task_ids: Set[str] = set()
        self.failed_task_ids: Set[str] = set()

    def add_task(self, task: Task) -> str:
        """Add a task to the queue."""
        self.tasks[task.id] = task
        return task.id

    def add_tasks(self, tasks: List[Task]) -> List[str]:
        """Add multiple tasks to the queue."""
        return [self.add_task(task) for task in tasks]

    def get_next_task(self) -> Optional[Task]:
        """Get the highest priority task that is ready to execute."""
        executable_tasks = [
            task
            for task in self.tasks.values()
            if task.can_execute(self.completed_task_ids)
        ]

        if not executable_tasks:
            return None

        # Sort by priority (higher first), then by creation time (older first)
        executable_tasks.sort(
            key=lambda t: (-t.priority, t.created_at)
        )

        return executable_tasks[0]

    def mark_task_completed(self, task_id: str, result: Dict[str, Any]):
        """Mark a task as completed."""
        if task_id in self.tasks:
            self.tasks[task_id].mark_completed(result)
            self.completed_task_ids.add(task_id)

    def mark_task_failed(self, task_id: str, error: str):
        """Mark a task as failed."""
        if task_id in self.tasks:
            self.tasks[task_id].mark_failed(error)
            if self.tasks[task_id].status == TaskStatus.FAILED:
                self.failed_task_ids.add(task_id)

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID."""
        return self.tasks.get(task_id)

    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks."""
        return [
            task
            for task in self.tasks.values()
            if task.status == TaskStatus.PENDING
        ]

    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks."""
        return [
            task
            for task in self.tasks.values()
            if task.status == TaskStatus.COMPLETED
        ]

    def get_failed_tasks(self) -> List[Task]:
        """Get all failed tasks."""
        return [
            task
            for task in self.tasks.values()
            if task.status == TaskStatus.FAILED
        ]

    def has_pending_tasks(self) -> bool:
        """Check if there are any pending or in-progress tasks."""
        return any(
            task.status in [TaskStatus.PENDING, TaskStatus.IN_PROGRESS]
            for task in self.tasks.values()
        )

    def get_status_summary(self) -> Dict[str, int]:
        """Get a summary of task statuses."""
        summary = {
            "total": len(self.tasks),
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
            "failed": 0,
            "blocked": 0,
        }

        for task in self.tasks.values():
            if task.status == TaskStatus.PENDING:
                summary["pending"] += 1
            elif task.status == TaskStatus.IN_PROGRESS:
                summary["in_progress"] += 1
            elif task.status == TaskStatus.COMPLETED:
                summary["completed"] += 1
            elif task.status == TaskStatus.FAILED:
                summary["failed"] += 1
            elif task.status == TaskStatus.BLOCKED:
                summary["blocked"] += 1

        return summary

    def clear(self):
        """Clear all tasks from the queue."""
        self.tasks.clear()
        self.completed_task_ids.clear()
        self.failed_task_ids.clear()


class ObjectiveManager:
    """Manages objectives for Baby AGI."""

    def __init__(self):
        self.current_objective: Optional[Objective] = None
        self.objective_history: List[Objective] = []

    def set_objective(self, objective: Objective):
        """Set the current objective."""
        if self.current_objective:
            self.objective_history.append(self.current_objective)
        self.current_objective = objective

    def complete_objective(self):
        """Mark the current objective as completed."""
        if self.current_objective:
            self.current_objective.is_completed = True
            self.current_objective.completed_at = datetime.now()

    def get_current_objective(self) -> Optional[Objective]:
        """Get the current objective."""
        return self.current_objective

    def has_active_objective(self) -> bool:
        """Check if there's an active objective."""
        return self.current_objective is not None and not self.current_objective.is_completed
