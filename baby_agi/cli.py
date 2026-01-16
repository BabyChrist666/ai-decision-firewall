"""CLI interface for Baby AGI."""
import argparse
import sys
import os
from baby_agi.agent import BabyAGI


def print_banner():
    """Print Baby AGI banner."""
    banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║                      🤖 Baby AGI 🤖                       ║
║                                                           ║
║          Autonomous Agent for Any Task                   ║
║          - Create folders and files                      ║
║          - Write and execute code                        ║
║          - Build complete software                       ║
║          - Learn and adapt                               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(banner)


def run_interactive_mode():
    """Run Baby AGI in interactive mode."""
    print_banner()
    print("\n🌟 Welcome to Baby AGI Interactive Mode!\n")
    print("I can help you achieve any objective by breaking it down into tasks.")
    print("Just tell me what you want to accomplish!\n")

    # Get configuration
    print("Configuration:")
    workspace = input("  Workspace directory [./workspace]: ").strip() or "./workspace"
    memory = input("  Memory directory [./memory]: ").strip() or "./memory"

    llm_choice = input("  LLM model (local/openai/anthropic) [local]: ").strip().lower() or "local"
    api_key = None

    if llm_choice in ["openai", "anthropic"]:
        api_key = input(f"  {llm_choice.upper()} API key: ").strip()
        if not api_key:
            print("  ⚠️  No API key provided, falling back to local mode")
            llm_choice = "local"

    # Create Baby AGI instance
    print(f"\n🚀 Initializing Baby AGI...")
    agent = BabyAGI(
        workspace_dir=workspace,
        memory_dir=memory,
        llm_model=llm_choice,
        api_key=api_key,
        verbose=True,
    )

    # Interactive loop
    while True:
        print("\n" + "=" * 60)
        objective = input("\n💡 What would you like me to do? (or 'quit' to exit)\n> ").strip()

        if objective.lower() in ["quit", "exit", "q"]:
            print("\n👋 Goodbye!")
            break

        if not objective:
            print("  ⚠️  Please provide an objective")
            continue

        # Set objective and run
        print(f"\n🎯 Objective: {objective}\n")
        agent.set_objective(objective)

        try:
            summary = agent.run()

            # Show results
            print("\n" + "=" * 60)
            print("📊 Results:")
            print(f"  ✓ Completed tasks: {summary['tasks']['completed']}")
            print(f"  ✗ Failed tasks: {summary['tasks']['failed']}")
            print(f"  ⏱️  Time: {summary['elapsed_time']:.2f}s")

            # Show created files
            files = agent.get_workspace_files()
            if files:
                print(f"\n📁 Created {len(files)} file(s) in workspace:")
                for file in files:
                    print(f"    - {file}")

            # Ask if user wants to continue
            continue_choice = input("\n🔄 Start a new objective? (y/n) [y]: ").strip().lower()
            if continue_choice == 'n':
                print("\n👋 Goodbye!")
                break

        except KeyboardInterrupt:
            print("\n\n⏸️  Interrupted by user")
            agent.stop()
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()


def run_single_objective(objective: str, workspace: str, memory: str, llm_model: str, api_key: str = None):
    """Run Baby AGI with a single objective."""
    print_banner()
    print(f"\n🎯 Objective: {objective}\n")

    agent = BabyAGI(
        workspace_dir=workspace,
        memory_dir=memory,
        llm_model=llm_model,
        api_key=api_key,
        verbose=True,
    )

    agent.set_objective(objective)
    summary = agent.run()

    # Show summary
    print("\n" + "=" * 60)
    print("📊 Final Summary:")
    print(f"  Success: {'✓' if summary['success'] else '✗'}")
    print(f"  Completed: {summary['tasks']['completed']}")
    print(f"  Failed: {summary['tasks']['failed']}")
    print(f"  Time: {summary['elapsed_time']:.2f}s")

    # Show created files
    files = agent.get_workspace_files()
    if files:
        print(f"\n📁 Created files:")
        for file in files:
            print(f"    - {file}")

    return summary


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Baby AGI - Autonomous agent for any task",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python -m baby_agi.cli

  # Run with specific objective
  python -m baby_agi.cli -o "Create a Python calculator"

  # Use with OpenAI
  python -m baby_agi.cli -o "Build a web scraper" --llm openai --api-key YOUR_KEY

  # Customize workspace
  python -m baby_agi.cli -o "Create a TODO app" -w ./my_workspace
        """,
    )

    parser.add_argument(
        "-o", "--objective",
        type=str,
        help="Objective to achieve (if not provided, runs in interactive mode)",
    )

    parser.add_argument(
        "-w", "--workspace",
        type=str,
        default="./workspace",
        help="Workspace directory (default: ./workspace)",
    )

    parser.add_argument(
        "-m", "--memory",
        type=str,
        default="./memory",
        help="Memory directory (default: ./memory)",
    )

    parser.add_argument(
        "--llm",
        type=str,
        choices=["local", "openai", "anthropic"],
        default="local",
        help="LLM model to use (default: local)",
    )

    parser.add_argument(
        "--api-key",
        type=str,
        help="API key for cloud LLM providers",
    )

    parser.add_argument(
        "--max-iterations",
        type=int,
        default=50,
        help="Maximum iterations (default: 50)",
    )

    args = parser.parse_args()

    # Get API key from environment if not provided
    api_key = args.api_key
    if not api_key:
        if args.llm == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
        elif args.llm == "anthropic":
            api_key = os.getenv("ANTHROPIC_API_KEY")

    if args.objective:
        # Single objective mode
        run_single_objective(
            objective=args.objective,
            workspace=args.workspace,
            memory=args.memory,
            llm_model=args.llm,
            api_key=api_key,
        )
    else:
        # Interactive mode
        run_interactive_mode()


if __name__ == "__main__":
    main()
