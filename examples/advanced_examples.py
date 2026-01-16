"""
Advanced examples demonstrating Baby AGI's learning and adaptation.

These examples show how Baby AGI can handle complex objectives,
learn from experience, and adapt its strategies.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from baby_agi import BabyAGI


def example_web_scraper():
    """Create a web scraper project."""
    print("\n" + "=" * 70)
    print("Advanced Example: Web Scraper Project")
    print("=" * 70)

    agent = BabyAGI(
        workspace_dir="./workspace_advanced",
        memory_dir="./memory_advanced",
        verbose=True
    )

    objective = """
    Create software that scrapes a website and extracts article titles.
    The program should use requests and BeautifulSoup libraries.
    """

    agent.set_objective(objective.strip())
    summary = agent.run()

    print(f"\n✓ Project completed: {summary['success']}")
    print(f"  Files created: {len(agent.get_workspace_files())}")

    return summary


def example_learning_from_experience():
    """Demonstrate learning from repeated similar tasks."""
    print("\n" + "=" * 70)
    print("Advanced Example: Learning from Experience")
    print("=" * 70)

    # Use the same agent for multiple similar tasks
    agent = BabyAGI(
        workspace_dir="./workspace_advanced",
        memory_dir="./memory_advanced",
        verbose=True
    )

    # First task
    print("\n--- Task 1: First calculator ---")
    agent.set_objective("Create a Python calculator")
    summary1 = agent.run()

    # Second similar task (should be faster due to learning)
    print("\n--- Task 2: Another calculator ---")
    agent.set_objective("Create a Python calculator with different name")
    summary2 = agent.run()

    print("\n📊 Learning Analysis:")
    print(f"  First attempt: {summary1['elapsed_time']:.2f}s")
    print(f"  Second attempt: {summary2['elapsed_time']:.2f}s")
    print(f"  Memory summary: {agent.memory.get_memory_summary()}")


def example_complex_project():
    """Build a more complex multi-file project."""
    print("\n" + "=" * 70)
    print("Advanced Example: Complex Multi-File Project")
    print("=" * 70)

    agent = BabyAGI(
        workspace_dir="./workspace_advanced",
        memory_dir="./memory_advanced",
        verbose=True,
        max_iterations=100
    )

    objective = """
    Build a TODO application with the following:
    - A main.py file with the application logic
    - A utils.py file with helper functions
    - A README.md with instructions
    - The app should support adding, removing, and listing TODOs
    """

    agent.set_objective(objective.strip())
    summary = agent.run()

    print(f"\n✓ Project Status: {summary['success']}")
    print(f"  Total iterations: {summary['iterations']}")
    print(f"  Files created:")
    for file in agent.get_workspace_files():
        print(f"    - {file}")


def example_api_with_llm():
    """
    Example using OpenAI or Anthropic for better task generation.
    Requires API key.
    """
    print("\n" + "=" * 70)
    print("Advanced Example: Using Cloud LLM")
    print("=" * 70)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY not found. Skipping this example.")
        print("   Set OPENAI_API_KEY environment variable to run this example.")
        return

    agent = BabyAGI(
        workspace_dir="./workspace_advanced",
        memory_dir="./memory_advanced",
        llm_model="openai",
        api_key=api_key,
        verbose=True
    )

    objective = """
    Create a data analysis script that:
    - Reads a CSV file
    - Calculates basic statistics (mean, median, mode)
    - Generates a simple text report
    """

    agent.set_objective(objective.strip())
    summary = agent.run()

    print(f"\n✓ Analysis: {summary['success']}")


def example_memory_inspection():
    """Inspect what Baby AGI has learned."""
    print("\n" + "=" * 70)
    print("Advanced Example: Memory and Learning Inspection")
    print("=" * 70)

    from baby_agi.memory import MemoryManager

    memory = MemoryManager(memory_dir="./memory_advanced")

    print("\n📊 Memory Summary:")
    summary = memory.get_memory_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")

    print("\n📈 Task Success Rates:")
    if memory.long_term_memory.get("task_success_rate"):
        for task_type, stats in memory.long_term_memory["task_success_rate"].items():
            success_rate = stats["successful"] / stats["total"] if stats["total"] > 0 else 0
            print(f"  {task_type}: {success_rate:.1%} ({stats['successful']}/{stats['total']})")

    print("\n✅ Successful Objectives:")
    for obj in memory.long_term_memory.get("successful_objectives", [])[-5:]:
        print(f"  - {obj['objective']}")


def run_advanced_examples():
    """Run all advanced examples."""
    print("\n" + "=" * 70)
    print("🤖 Baby AGI - Advanced Examples")
    print("=" * 70)
    print("\nThese examples demonstrate Baby AGI's advanced capabilities:")
    print("- Complex project creation")
    print("- Learning from experience")
    print("- Memory and adaptation")
    print()

    input("Press Enter to start...")

    examples = [
        ("Web Scraper", example_web_scraper),
        ("Learning from Experience", example_learning_from_experience),
        ("Complex Project", example_complex_project),
        ("Memory Inspection", example_memory_inspection),
        # ("Cloud LLM", example_api_with_llm),  # Uncomment if you have API key
    ]

    for name, example_func in examples:
        try:
            print(f"\n{'='*70}")
            print(f"Running: {name}")
            print('='*70)
            example_func()
            input("\nPress Enter for next example...")
        except KeyboardInterrupt:
            print("\n\n⏸️  Interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Error in {name}: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 70)
    print("✓ Advanced examples completed!")
    print("=" * 70)


if __name__ == "__main__":
    run_advanced_examples()
