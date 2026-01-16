"""
Simple tests for Baby AGI functionality.

Run with: python test_baby_agi.py
"""

import os
import shutil
from baby_agi import BabyAGI
from baby_agi.models import Task, TaskType, Objective
from baby_agi.core import TaskQueue, TaskExecutor


def test_task_queue():
    """Test task queue functionality."""
    print("\n=== Testing Task Queue ===")

    queue = TaskQueue()

    # Create tasks
    task1 = Task(description="Task 1", priority=5)
    task2 = Task(description="Task 2", priority=10)
    task3 = Task(description="Task 3", priority=8, depends_on=[task1.id])

    # Add tasks
    queue.add_task(task1)
    queue.add_task(task2)
    queue.add_task(task3)

    # Get next task (should be highest priority without dependencies)
    next_task = queue.get_next_task()
    assert next_task.id == task2.id, "Should get highest priority task"

    # Mark as completed
    queue.mark_task_completed(task2.id, {"success": True})

    # Get status
    status = queue.get_status_summary()
    assert status["completed"] == 1
    assert status["pending"] == 2

    print("✓ Task queue tests passed")


def test_task_executor():
    """Test task executor functionality."""
    print("\n=== Testing Task Executor ===")

    # Clean up test workspace
    test_workspace = "./test_workspace"
    if os.path.exists(test_workspace):
        shutil.rmtree(test_workspace)

    executor = TaskExecutor(workspace_dir=test_workspace)

    # Test folder creation
    task_folder = Task(
        description="Create test folder",
        task_type=TaskType.FOLDER_CREATE,
        context={"folder_path": "test_folder"}
    )

    result = executor.execute(task_folder)
    assert result["success"], "Folder creation should succeed"
    assert os.path.exists(os.path.join(test_workspace, "test_folder"))

    # Test file creation
    task_file = Task(
        description="Create test file",
        task_type=TaskType.FILE_CREATE,
        context={
            "file_path": "test_file.txt",
            "content": "Hello, Baby AGI!"
        }
    )

    result = executor.execute(task_file)
    assert result["success"], "File creation should succeed"

    file_path = os.path.join(test_workspace, "test_file.txt")
    assert os.path.exists(file_path)

    with open(file_path, "r") as f:
        content = f.read()
        assert content == "Hello, Baby AGI!"

    # Test code writing
    task_code = Task(
        description="Write Python code",
        task_type=TaskType.CODE_WRITE,
        context={
            "file_path": "hello.py",
            "code": 'print("Hello from Baby AGI")',
            "language": "python"
        }
    )

    result = executor.execute(task_code)
    assert result["success"], "Code writing should succeed"

    # Clean up
    shutil.rmtree(test_workspace)

    print("✓ Task executor tests passed")


def test_baby_agi_simple_objective():
    """Test Baby AGI with a simple objective."""
    print("\n=== Testing Baby AGI with Simple Objective ===")

    # Clean up test directories
    test_workspace = "./test_baby_agi_workspace"
    test_memory = "./test_baby_agi_memory"

    for directory in [test_workspace, test_memory]:
        if os.path.exists(directory):
            shutil.rmtree(directory)

    # Create Baby AGI instance
    agent = BabyAGI(
        workspace_dir=test_workspace,
        memory_dir=test_memory,
        llm_model="local",
        verbose=False
    )

    # Set a simple objective
    agent.set_objective("Create a folder called my_test_project")

    # Run
    summary = agent.run()

    # Check results
    assert summary["tasks"]["completed"] > 0, "Should complete at least one task"
    assert os.path.exists(os.path.join(test_workspace, "my_test_project")), "Folder should be created"

    # Clean up
    shutil.rmtree(test_workspace)
    shutil.rmtree(test_memory)

    print("✓ Baby AGI simple objective test passed")


def test_baby_agi_file_creation():
    """Test Baby AGI creating a Python file."""
    print("\n=== Testing Baby AGI File Creation ===")

    # Clean up test directories
    test_workspace = "./test_baby_agi_workspace"
    test_memory = "./test_baby_agi_memory"

    for directory in [test_workspace, test_memory]:
        if os.path.exists(directory):
            shutil.rmtree(directory)

    # Create Baby AGI instance
    agent = BabyAGI(
        workspace_dir=test_workspace,
        memory_dir=test_memory,
        llm_model="local",
        verbose=False
    )

    # Set objective
    agent.set_objective("Create a Python file that prints hello world")

    # Run
    summary = agent.run()

    # Check results
    assert summary["tasks"]["completed"] > 0, "Should complete at least one task"

    # Check if Python file was created
    files = agent.get_workspace_files()
    python_files = [f for f in files if f.endswith('.py')]
    assert len(python_files) > 0, "Should create at least one Python file"

    # Clean up
    shutil.rmtree(test_workspace)
    shutil.rmtree(test_memory)

    print("✓ Baby AGI file creation test passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("🧪 Baby AGI Test Suite")
    print("=" * 70)

    tests = [
        test_task_queue,
        test_task_executor,
        test_baby_agi_simple_objective,
        test_baby_agi_file_creation,
    ]

    passed = 0
    failed = 0

    for test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test_func.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test_func.__name__} error: {e}")
            import traceback
            traceback.print_exc()
            failed += 1

    print("\n" + "=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 70)

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
