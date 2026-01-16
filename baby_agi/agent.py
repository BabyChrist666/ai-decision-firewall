"""Main Baby AGI agent orchestrator."""
import time
from typing import Optional, Dict, Any, List
from datetime import datetime

from baby_agi.models import Objective, Task, TaskStatus
from baby_agi.core import TaskQueue, ObjectiveManager, TaskExecutor
from baby_agi.llm import LLMAgent
from baby_agi.memory import MemoryManager


class BabyAGI:
    """
    Baby AGI - An autonomous agent that can achieve objectives by:
    1. Breaking down objectives into tasks
    2. Executing tasks
    3. Learning from results
    4. Adapting and generating new tasks
    5. Iterating until objective is achieved
    """

    def __init__(
        self,
        workspace_dir: str = "./workspace",
        memory_dir: str = "./memory",
        llm_model: str = "local",
        api_key: Optional[str] = None,
        max_iterations: int = 50,
        verbose: bool = True,
    ):
        """
        Initialize Baby AGI.

        Args:
            workspace_dir: Directory for task execution workspace
            memory_dir: Directory for memory storage
            llm_model: LLM model to use (local, openai, anthropic)
            api_key: API key for cloud LLMs
            max_iterations: Maximum iterations before stopping
            verbose: Print detailed logs
        """
        self.workspace_dir = workspace_dir
        self.memory_dir = memory_dir
        self.max_iterations = max_iterations
        self.verbose = verbose

        # Initialize components
        self.task_queue = TaskQueue()
        self.objective_manager = ObjectiveManager()
        self.executor = TaskExecutor(workspace_dir=workspace_dir)
        self.llm_agent = LLMAgent(model=llm_model, api_key=api_key)
        self.memory = MemoryManager(memory_dir=memory_dir)

        # State
        self.iteration_count = 0
        self.is_running = False

    def log(self, message: str, level: str = "INFO"):
        """Log a message if verbose is enabled."""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [{level}] {message}")

    def set_objective(self, objective_description: str, context: Dict[str, Any] = None):
        """
        Set a new objective for the Baby AGI.

        Args:
            objective_description: The goal to achieve
            context: Additional context
        """
        objective = Objective(
            description=objective_description,
            context=context or {},
        )

        self.objective_manager.set_objective(objective)
        self.log(f"Objective set: {objective_description}", "OBJECTIVE")

        # Get context from memory
        memory_context = self.memory.get_context_for_objective(objective)
        if memory_context["similar_successful_objectives"]:
            self.log(f"Found {len(memory_context['similar_successful_objectives'])} similar past objectives")

        # Generate initial tasks
        initial_tasks = self.llm_agent.generate_tasks_for_objective(objective, memory_context)

        if initial_tasks:
            self.task_queue.add_tasks(initial_tasks)
            self.log(f"Generated {len(initial_tasks)} initial tasks")
            for i, task in enumerate(initial_tasks, 1):
                self.log(f"  {i}. [{task.task_type.value}] {task.description}", "TASK")
        else:
            self.log("No tasks generated. Objective may be unclear.", "WARNING")

    def run(self) -> Dict[str, Any]:
        """
        Run the Baby AGI main loop.

        Returns:
            Summary of execution
        """
        if not self.objective_manager.has_active_objective():
            self.log("No active objective. Set an objective first.", "ERROR")
            return {"success": False, "error": "No active objective"}

        self.is_running = True
        self.iteration_count = 0
        start_time = time.time()

        self.log("Starting Baby AGI execution loop...", "START")
        self.log("=" * 60)

        while self.is_running and self.iteration_count < self.max_iterations:
            self.iteration_count += 1
            self.log(f"\n--- Iteration {self.iteration_count} ---", "ITERATION")

            # Check if objective is complete
            if self._check_objective_completion():
                self.log("Objective completed!", "SUCCESS")
                break

            # Get next task
            next_task = self.task_queue.get_next_task()

            if next_task is None:
                self.log("No executable tasks available", "INFO")

                # Check if we should generate new tasks or stop
                if not self.task_queue.has_pending_tasks():
                    self.log("No pending tasks. Objective may be complete or blocked.", "WARNING")
                    break
                else:
                    self.log("Tasks are blocked by dependencies", "WARNING")
                    time.sleep(1)
                    continue

            # Execute task
            self._execute_task(next_task)

            # Learn from execution
            self._learn_from_task(next_task)

            # Check if we should generate new tasks
            if self.iteration_count % 5 == 0:
                self._generate_adaptive_tasks()

            # Print status
            status = self.task_queue.get_status_summary()
            self.log(f"Status: {status['completed']} completed, {status['pending']} pending, {status['failed']} failed")

            # Small delay to avoid spinning
            time.sleep(0.1)

        # Execution complete
        elapsed_time = time.time() - start_time
        self.is_running = False

        return self._generate_summary(elapsed_time)

    def _execute_task(self, task: Task):
        """Execute a single task."""
        self.log(f"\nExecuting: [{task.task_type.value}] {task.description}", "EXECUTE")

        try:
            # Execute the task
            result = self.executor.execute(task)

            if result.get("success"):
                self.log(f"✓ Success: {result.get('output', '')}", "SUCCESS")
                self.task_queue.mark_task_completed(task.id, result)
                self.memory.record_task_execution(task, success=True)
            else:
                error = result.get("error", "Unknown error")
                self.log(f"✗ Failed: {error}", "ERROR")
                self.task_queue.mark_task_failed(task.id, error)
                self.memory.record_task_execution(task, success=False)

        except Exception as e:
            self.log(f"✗ Exception: {str(e)}", "ERROR")
            self.task_queue.mark_task_failed(task.id, str(e))
            self.memory.record_task_execution(task, success=False)

    def _learn_from_task(self, task: Task):
        """Learn from task execution."""
        # Record patterns from successful tasks
        if task.status == TaskStatus.COMPLETED:
            completed_tasks = self.task_queue.get_completed_tasks()
            if len(completed_tasks) >= 3:
                self.memory.learn_from_task_sequence(completed_tasks[-3:])

    def _generate_adaptive_tasks(self):
        """Generate new tasks based on progress."""
        # This is where Baby AGI adapts
        # For now, just log that we're checking
        self.log("Checking if new tasks are needed...", "ADAPT")

        # Could generate new tasks here based on:
        # - Failed tasks that need retry with different approach
        # - New insights from completed tasks
        # - Gaps in the plan

    def _check_objective_completion(self) -> bool:
        """Check if the current objective is complete."""
        objective = self.objective_manager.get_current_objective()
        if not objective:
            return False

        completed_tasks = self.task_queue.get_completed_tasks()

        # Use LLM to evaluate completion
        evaluation = self.llm_agent.evaluate_objective_completion(
            objective, completed_tasks
        )

        if evaluation.get("is_complete", False):
            self.memory.record_objective_completion(objective, success=True)
            self.objective_manager.complete_objective()
            return True

        return False

    def _generate_summary(self, elapsed_time: float) -> Dict[str, Any]:
        """Generate execution summary."""
        status = self.task_queue.get_status_summary()

        summary = {
            "objective": self.objective_manager.get_current_objective().description,
            "iterations": self.iteration_count,
            "elapsed_time": elapsed_time,
            "tasks": status,
            "success": status["completed"] > 0 and status["failed"] == 0,
            "completed_tasks": [
                task.to_dict() for task in self.task_queue.get_completed_tasks()
            ],
            "failed_tasks": [
                task.to_dict() for task in self.task_queue.get_failed_tasks()
            ],
        }

        self.log("\n" + "=" * 60, "SUMMARY")
        self.log(f"Execution Summary:")
        self.log(f"  Objective: {summary['objective']}")
        self.log(f"  Iterations: {summary['iterations']}")
        self.log(f"  Time: {elapsed_time:.2f}s")
        self.log(f"  Completed: {status['completed']}")
        self.log(f"  Failed: {status['failed']}")
        self.log(f"  Pending: {status['pending']}")
        self.log("=" * 60)

        return summary

    def stop(self):
        """Stop the Baby AGI execution."""
        self.is_running = False
        self.log("Stopping Baby AGI...", "STOP")

    def get_status(self) -> Dict[str, Any]:
        """Get current status."""
        return {
            "is_running": self.is_running,
            "iteration": self.iteration_count,
            "objective": self.objective_manager.get_current_objective().to_dict()
            if self.objective_manager.get_current_objective()
            else None,
            "tasks": self.task_queue.get_status_summary(),
            "memory": self.memory.get_memory_summary(),
        }

    def get_workspace_files(self) -> List[str]:
        """Get list of files created in workspace."""
        import os

        files = []
        for root, dirs, filenames in os.walk(self.workspace_dir):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, self.workspace_dir)
                files.append(rel_path)

        return files
