"""LLM integration for Baby AGI task generation and reasoning."""
import os
import json
from typing import List, Dict, Any, Optional
from baby_agi.models import Task, TaskType, Objective


class LLMAgent:
    """Agent that uses LLM to generate and reason about tasks."""

    def __init__(self, model: str = "local", api_key: Optional[str] = None):
        """
        Initialize the LLM agent.

        Args:
            model: Model to use (local, openai, anthropic, etc.)
            api_key: API key for cloud models
        """
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self._setup_client()

    def _setup_client(self):
        """Setup the LLM client based on model type."""
        if self.model == "openai":
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
                self.model_name = "gpt-4"
            except ImportError:
                print("OpenAI not installed. Install with: pip install openai")
                self.model = "local"
        elif self.model == "anthropic":
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
                self.model_name = "claude-3-sonnet-20240229"
            except ImportError:
                print("Anthropic not installed. Install with: pip install anthropic")
                self.model = "local"

        # For local mode, we'll use simple rule-based generation
        if self.model == "local":
            self.client = None

    def generate_tasks_for_objective(
        self, objective: Objective, context: Dict[str, Any] = None
    ) -> List[Task]:
        """
        Generate initial tasks to achieve an objective.

        Args:
            objective: The objective to achieve
            context: Additional context

        Returns:
            List of tasks to achieve the objective
        """
        if self.model == "local":
            return self._generate_tasks_local(objective, context)
        else:
            return self._generate_tasks_llm(objective, context)

    def _generate_tasks_local(
        self, objective: Objective, context: Dict[str, Any] = None
    ) -> List[Task]:
        """Generate tasks using local rule-based approach."""
        tasks = []

        # Parse the objective to determine task type
        obj_lower = objective.description.lower()

        # Example: "create a folder called projects"
        if "create" in obj_lower and "folder" in obj_lower:
            # Extract folder name (simple parsing)
            words = objective.description.split()
            folder_name = "new_folder"
            if "called" in words:
                idx = words.index("called")
                if idx + 1 < len(words):
                    folder_name = words[idx + 1].strip('"\',.')

            tasks.append(
                Task(
                    description=f"Create folder: {folder_name}",
                    task_type=TaskType.FOLDER_CREATE,
                    priority=8,
                    context={"folder_path": folder_name},
                )
            )

        # Example: "create a python file that prints hello world"
        elif "create" in obj_lower and ("file" in obj_lower or "python" in obj_lower or "code" in obj_lower):
            file_name = "script.py"
            language = "python"

            if "python" in obj_lower:
                language = "python"
                file_name = "script.py"
            elif "javascript" in obj_lower or "js" in obj_lower:
                language = "javascript"
                file_name = "script.js"

            # Generate simple code based on objective
            code = self._generate_simple_code(objective.description, language)

            tasks.append(
                Task(
                    description=f"Create {language} file",
                    task_type=TaskType.CODE_WRITE,
                    priority=9,
                    context={
                        "file_path": file_name,
                        "code": code,
                        "language": language,
                    },
                )
            )

        # Example: "create software that does X"
        elif "create software" in obj_lower or "build a program" in obj_lower:
            # Break down into planning, implementation, testing
            tasks.extend([
                Task(
                    description="Plan software architecture",
                    task_type=TaskType.PLAN,
                    priority=10,
                    context={"objective": objective.description},
                ),
                Task(
                    description="Create project structure",
                    task_type=TaskType.FOLDER_CREATE,
                    priority=9,
                    depends_on=[],  # Will be set to plan task ID
                    context={"folder_path": "project"},
                ),
                Task(
                    description="Write main code file",
                    task_type=TaskType.CODE_WRITE,
                    priority=8,
                    depends_on=[],  # Will be set to structure task ID
                    context={
                        "file_path": "project/main.py",
                        "code": self._generate_simple_code(objective.description, "python"),
                        "language": "python",
                    },
                ),
                Task(
                    description="Write README",
                    task_type=TaskType.FILE_CREATE,
                    priority=5,
                    context={
                        "file_path": "project/README.md",
                        "content": f"# Project\n\n{objective.description}\n",
                    },
                ),
            ])

            # Set up dependencies
            if len(tasks) >= 3:
                tasks[1].depends_on = [tasks[0].id]
                tasks[2].depends_on = [tasks[1].id]

        # Default: create a plan task
        else:
            tasks.append(
                Task(
                    description=f"Plan how to: {objective.description}",
                    task_type=TaskType.PLAN,
                    priority=10,
                    context={"objective": objective.description},
                )
            )

        return tasks

    def _generate_simple_code(self, objective: str, language: str) -> str:
        """Generate simple code based on objective."""
        obj_lower = objective.lower()

        if language == "python":
            if "hello world" in obj_lower or "print hello" in obj_lower:
                return 'print("Hello, World!")\n'
            elif "calculator" in obj_lower:
                return '''def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b != 0:
        return a / b
    return "Cannot divide by zero"

if __name__ == "__main__":
    print("Simple Calculator")
    print("5 + 3 =", add(5, 3))
    print("5 - 3 =", subtract(5, 3))
    print("5 * 3 =", multiply(5, 3))
    print("5 / 3 =", divide(5, 3))
'''
            elif "web scraper" in obj_lower or "scraper" in obj_lower:
                return '''import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    """Scrape a website and return the title."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title')

        return title.text if title else "No title found"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    url = "https://example.com"
    print(f"Scraping: {url}")
    print(f"Title: {scrape_website(url)}")
'''
            else:
                return f'''"""
{objective}
"""

def main():
    print("Program started")
    # TODO: Implement functionality
    print("Program completed")

if __name__ == "__main__":
    main()
'''
        elif language == "javascript":
            if "hello world" in obj_lower:
                return 'console.log("Hello, World!");\n'
            else:
                return f'''// {objective}

function main() {{
    console.log("Program started");
    // TODO: Implement functionality
    console.log("Program completed");
}}

main();
'''
        else:
            return f"# {objective}\n# TODO: Implement\n"

    def _generate_tasks_llm(
        self, objective: Objective, context: Dict[str, Any] = None
    ) -> List[Task]:
        """Generate tasks using LLM."""
        prompt = self._create_task_generation_prompt(objective, context)

        try:
            if self.model == "openai":
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a task planning AI. Generate a list of specific, actionable tasks to achieve the given objective. Return tasks as JSON.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                )
                content = response.choices[0].message.content
            elif self.model == "anthropic":
                response = self.client.messages.create(
                    model=self.model_name,
                    max_tokens=2000,
                    messages=[{"role": "user", "content": prompt}],
                )
                content = response.content[0].text

            # Parse the response and create tasks
            return self._parse_llm_tasks(content)

        except Exception as e:
            print(f"LLM generation failed: {e}. Falling back to local generation.")
            return self._generate_tasks_local(objective, context)

    def _create_task_generation_prompt(
        self, objective: Objective, context: Dict[str, Any] = None
    ) -> str:
        """Create prompt for LLM task generation."""
        prompt = f"""Generate a list of specific, actionable tasks to achieve this objective:

Objective: {objective.description}

Context: {json.dumps(context or {}, indent=2)}

For each task, provide:
1. description: Clear description of what needs to be done
2. task_type: One of [file_create, file_edit, folder_create, code_write, code_execute, research, plan, review, test, generic]
3. priority: Integer 1-10 (10 is highest)
4. context: Any additional context needed (file_path, code, command, etc.)
5. depends_on: List of task indices this depends on (0-indexed)

Return ONLY a JSON array of tasks."""

        return prompt

    def _parse_llm_tasks(self, content: str) -> List[Task]:
        """Parse LLM response into Task objects."""
        try:
            # Try to extract JSON from the response
            start = content.find("[")
            end = content.rfind("]") + 1
            if start != -1 and end > start:
                json_str = content[start:end]
                task_dicts = json.loads(json_str)

                tasks = []
                task_id_map = {}

                for i, task_dict in enumerate(task_dicts):
                    task = Task(
                        description=task_dict.get("description", ""),
                        task_type=TaskType(task_dict.get("task_type", "generic")),
                        priority=task_dict.get("priority", 5),
                        context=task_dict.get("context", {}),
                    )
                    tasks.append(task)
                    task_id_map[i] = task.id

                # Set up dependencies
                for i, task_dict in enumerate(task_dicts):
                    depends_on_indices = task_dict.get("depends_on", [])
                    tasks[i].depends_on = [
                        task_id_map[idx]
                        for idx in depends_on_indices
                        if idx in task_id_map
                    ]

                return tasks

        except Exception as e:
            print(f"Failed to parse LLM tasks: {e}")

        return []

    def evaluate_objective_completion(
        self,
        objective: Objective,
        completed_tasks: List[Task],
        context: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """
        Evaluate if the objective has been completed.

        Returns:
            Dict with 'is_complete', 'confidence', and 'reasoning'
        """
        if self.model == "local":
            # Simple heuristic: if we have completed tasks, consider it done
            return {
                "is_complete": len(completed_tasks) > 0,
                "confidence": 0.7 if len(completed_tasks) > 0 else 0.3,
                "reasoning": f"Completed {len(completed_tasks)} tasks",
            }

        # TODO: Implement LLM-based evaluation
        return {
            "is_complete": False,
            "confidence": 0.5,
            "reasoning": "Evaluation not yet implemented",
        }
