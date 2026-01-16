"""Task execution engine for Baby AGI."""
import os
import subprocess
import shutil
from typing import Dict, Any, Optional
from pathlib import Path
from baby_agi.models import Task, TaskType, TaskStatus


class TaskExecutor:
    """Executes different types of tasks."""

    def __init__(self, workspace_dir: str = "./workspace"):
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(exist_ok=True, parents=True)

    def execute(self, task: Task) -> Dict[str, Any]:
        """Execute a task based on its type."""
        try:
            task.mark_started()

            if task.task_type == TaskType.FILE_CREATE:
                return self._execute_file_create(task)
            elif task.task_type == TaskType.FILE_EDIT:
                return self._execute_file_edit(task)
            elif task.task_type == TaskType.FILE_DELETE:
                return self._execute_file_delete(task)
            elif task.task_type == TaskType.FOLDER_CREATE:
                return self._execute_folder_create(task)
            elif task.task_type == TaskType.CODE_WRITE:
                return self._execute_code_write(task)
            elif task.task_type == TaskType.CODE_EXECUTE:
                return self._execute_code_execute(task)
            elif task.task_type == TaskType.RESEARCH:
                return self._execute_research(task)
            elif task.task_type == TaskType.PLAN:
                return self._execute_plan(task)
            elif task.task_type == TaskType.REVIEW:
                return self._execute_review(task)
            elif task.task_type == TaskType.TEST:
                return self._execute_test(task)
            else:
                return self._execute_generic(task)

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "output": None,
            }

    def _execute_file_create(self, task: Task) -> Dict[str, Any]:
        """Create a new file."""
        file_path = task.context.get("file_path")
        content = task.context.get("content", "")

        if not file_path:
            raise ValueError("file_path is required for FILE_CREATE task")

        full_path = self.workspace_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, "w") as f:
            f.write(content)

        return {
            "success": True,
            "output": f"File created: {full_path}",
            "file_path": str(full_path),
        }

    def _execute_file_edit(self, task: Task) -> Dict[str, Any]:
        """Edit an existing file."""
        file_path = task.context.get("file_path")
        content = task.context.get("content")
        append = task.context.get("append", False)

        if not file_path:
            raise ValueError("file_path is required for FILE_EDIT task")

        full_path = self.workspace_dir / file_path

        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {full_path}")

        mode = "a" if append else "w"
        with open(full_path, mode) as f:
            f.write(content)

        return {
            "success": True,
            "output": f"File edited: {full_path}",
            "file_path": str(full_path),
        }

    def _execute_file_delete(self, task: Task) -> Dict[str, Any]:
        """Delete a file."""
        file_path = task.context.get("file_path")

        if not file_path:
            raise ValueError("file_path is required for FILE_DELETE task")

        full_path = self.workspace_dir / file_path

        if full_path.exists():
            full_path.unlink()
            return {
                "success": True,
                "output": f"File deleted: {full_path}",
            }
        else:
            return {
                "success": False,
                "output": f"File not found: {full_path}",
            }

    def _execute_folder_create(self, task: Task) -> Dict[str, Any]:
        """Create a new folder."""
        folder_path = task.context.get("folder_path")

        if not folder_path:
            raise ValueError("folder_path is required for FOLDER_CREATE task")

        full_path = self.workspace_dir / folder_path
        full_path.mkdir(parents=True, exist_ok=True)

        return {
            "success": True,
            "output": f"Folder created: {full_path}",
            "folder_path": str(full_path),
        }

    def _execute_code_write(self, task: Task) -> Dict[str, Any]:
        """Write code to a file."""
        file_path = task.context.get("file_path")
        code = task.context.get("code", "")
        language = task.context.get("language", "python")

        if not file_path:
            raise ValueError("file_path is required for CODE_WRITE task")

        full_path = self.workspace_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, "w") as f:
            f.write(code)

        return {
            "success": True,
            "output": f"Code written: {full_path}",
            "file_path": str(full_path),
            "language": language,
        }

    def _execute_code_execute(self, task: Task) -> Dict[str, Any]:
        """Execute code from a file."""
        file_path = task.context.get("file_path")
        language = task.context.get("language", "python")
        args = task.context.get("args", [])

        if not file_path:
            raise ValueError("file_path is required for CODE_EXECUTE task")

        full_path = self.workspace_dir / file_path

        if not full_path.exists():
            raise FileNotFoundError(f"File not found: {full_path}")

        # Determine the command based on language
        if language == "python":
            command = ["python3", str(full_path)] + args
        elif language == "bash":
            command = ["bash", str(full_path)] + args
        elif language == "javascript" or language == "node":
            command = ["node", str(full_path)] + args
        else:
            raise ValueError(f"Unsupported language: {language}")

        # Execute the command
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=self.workspace_dir,
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
            "exit_code": result.returncode,
        }

    def _execute_research(self, task: Task) -> Dict[str, Any]:
        """Perform research task (placeholder for LLM integration)."""
        query = task.context.get("query", task.description)

        # This would integrate with an LLM or search API
        # For now, just return a placeholder
        return {
            "success": True,
            "output": f"Research completed for: {query}",
            "findings": "Placeholder for research results",
        }

    def _execute_plan(self, task: Task) -> Dict[str, Any]:
        """Create a plan (placeholder for LLM integration)."""
        objective = task.context.get("objective", task.description)

        # This would integrate with an LLM for planning
        return {
            "success": True,
            "output": f"Plan created for: {objective}",
            "plan": "Placeholder for plan",
        }

    def _execute_review(self, task: Task) -> Dict[str, Any]:
        """Review content (placeholder for LLM integration)."""
        content = task.context.get("content", "")

        return {
            "success": True,
            "output": "Review completed",
            "review": "Placeholder for review",
        }

    def _execute_test(self, task: Task) -> Dict[str, Any]:
        """Run tests."""
        test_command = task.context.get("command", "pytest")
        test_path = task.context.get("test_path", ".")

        result = subprocess.run(
            test_command.split(),
            capture_output=True,
            text=True,
            timeout=60,
            cwd=self.workspace_dir / test_path,
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None,
            "exit_code": result.returncode,
        }

    def _execute_generic(self, task: Task) -> Dict[str, Any]:
        """Execute a generic task."""
        command = task.context.get("command")

        if command:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.workspace_dir,
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
            }
        else:
            return {
                "success": True,
                "output": f"Generic task completed: {task.description}",
            }
