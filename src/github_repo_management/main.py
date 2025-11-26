#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from github_repo_management.crew import GithubRepoManagement

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew with a simple project idea.
    The AI will generate a full PRD from your idea automatically!
    """
    # Simple project idea - just describe what you want to build!
    project_idea = """
    I want to build an e-commerce platform where users can browse products, 
    add items to their shopping cart, and checkout securely using Stripe. 
    It should have user authentication, product search, order tracking, 
    and an admin dashboard for managing inventory.
    """
    
    inputs = {
        'project_idea': project_idea,
        'prd_content': '',  # Will be generated automatically
        'prd_data': '',     # Will be extracted from generated PRD
        'repo_name': ''     # Will be determined from PRD
    }

    try:
        result = GithubRepoManagement().crew().kickoff(inputs=inputs)
        print("\n" + "="*50)
        print("✓ Project Setup Complete!")
        print("="*50)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs",
        'current_year': str(datetime.now().year)
    }
    try:
        GithubRepoManagement().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        GithubRepoManagement().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs",
        "current_year": str(datetime.now().year)
    }

    try:
        GithubRepoManagement().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

def run_with_trigger():
    """
    Run the crew with trigger payload.
    """
    import json

    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    inputs = {
        "crewai_trigger_payload": trigger_payload,
        "topic": "",
        "current_year": ""
    }

    try:
        result = GithubRepoManagement().crew().kickoff(inputs=inputs)
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the crew with trigger: {e}")
