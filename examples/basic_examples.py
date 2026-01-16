"""
Basic examples demonstrating Baby AGI capabilities.

Run this file to see Baby AGI in action with various objectives.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from baby_agi import BabyAGI


def example_1_create_folder():
    """Example 1: Create a simple folder."""
    print("\n" + "=" * 70)
    print("Example 1: Create a Folder")
    print("=" * 70)

    agent = BabyAGI(
        workspace_dir="./workspace_examples",
        verbose=True
    )

    agent.set_objective("Create a folder called my_project")
    summary = agent.run()

    print(f"\n✓ Result: {summary['success']}")
    print(f"  Files/folders created: {agent.get_workspace_files()}")


def example_2_create_file():
    """Example 2: Create a text file."""
    print("\n" + "=" * 70)
    print("Example 2: Create a Text File")
    print("=" * 70)

    agent = BabyAGI(
        workspace_dir="./workspace_examples",
        verbose=True
    )

    agent.set_objective("Create a file called notes.txt with some content")
    summary = agent.run()

    print(f"\n✓ Result: {summary['success']}")


def example_3_python_script():
    """Example 3: Create a Python script."""
    print("\n" + "=" * 70)
    print("Example 3: Create Python Script")
    print("=" * 70)

    agent = BabyAGI(
        workspace_dir="./workspace_examples",
        verbose=True
    )

    agent.set_objective("Create a Python file that prints hello world")
    summary = agent.run()

    print(f"\n✓ Result: {summary['success']}")
    print(f"  Files created: {agent.get_workspace_files()}")


def example_4_calculator():
    """Example 4: Build a calculator."""
    print("\n" + "=" * 70)
    print("Example 4: Build a Calculator")
    print("=" * 70)

    agent = BabyAGI(
        workspace_dir="./workspace_examples",
        verbose=True
    )

    agent.set_objective("Create a Python calculator")
    summary = agent.run()

    print(f"\n✓ Result: {summary['success']}")
    print(f"  Tasks completed: {summary['tasks']['completed']}")


def example_5_complete_project():
    """Example 5: Create a complete software project."""
    print("\n" + "=" * 70)
    print("Example 5: Build Complete Software Project")
    print("=" * 70)

    agent = BabyAGI(
        workspace_dir="./workspace_examples",
        verbose=True
    )

    agent.set_objective("Create software that calculates the Fibonacci sequence")
    summary = agent.run()

    print(f"\n✓ Result: {summary['success']}")
    print(f"  Files created: {agent.get_workspace_files()}")


def example_6_multiple_tasks():
    """Example 6: Multiple sequential objectives."""
    print("\n" + "=" * 70)
    print("Example 6: Multiple Sequential Objectives")
    print("=" * 70)

    agent = BabyAGI(
        workspace_dir="./workspace_examples",
        verbose=True
    )

    objectives = [
        "Create a folder called utils",
        "Create a Python file that has helper functions",
        "Create a README file",
    ]

    for i, objective in enumerate(objectives, 1):
        print(f"\n--- Objective {i}/{len(objectives)} ---")
        agent.set_objective(objective)
        summary = agent.run()
        print(f"✓ Status: {summary['success']}")


def run_all_examples():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("🤖 Baby AGI - Basic Examples")
    print("=" * 70)
    print("\nThis will demonstrate Baby AGI's capabilities with various objectives.")
    print("Each example shows how Baby AGI autonomously breaks down and achieves goals.\n")

    input("Press Enter to start...")

    examples = [
        example_1_create_folder,
        example_2_create_file,
        example_3_python_script,
        example_4_calculator,
        example_5_complete_project,
        example_6_multiple_tasks,
    ]

    for example_func in examples:
        try:
            example_func()
            input("\nPress Enter for next example...")
        except KeyboardInterrupt:
            print("\n\n⏸️  Interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Error in example: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 70)
    print("✓ All examples completed!")
    print("=" * 70)
    print("\nCheck the workspace_examples/ directory to see what was created.")


if __name__ == "__main__":
    run_all_examples()
