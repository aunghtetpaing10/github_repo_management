#!/usr/bin/env python
"""
Quick test script to run individual agents.
Modify the function call at the bottom to test different agents.
"""

import warnings
from crewai import Crew, Process
from src.github_repo_management.crew import GithubRepoManagement

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def test_prd_generator():
    """Test ONLY the PRD generator"""
    print("="*60)
    print("Testing PRD Generator Agent")
    print("="*60 + "\n")
    
    crew_instance = GithubRepoManagement()
    
    crew = Crew(
        agents=[crew_instance.prd_generator()],
        tasks=[crew_instance.generate_prd_task()],
        process=Process.sequential,
        verbose=True,
    )
    
    project_idea = """
    Build a task management app where teams can create projects,
    assign tasks, track progress, and collaborate in real-time.
    Include user authentication, notifications, and file attachments.
    """
    
    result = crew.kickoff(inputs={'project_idea': project_idea})
    
    print("\n" + "="*60)
    print("✓ PRD Generated Successfully!")
    print("="*60)
    print(result)
    return result


def test_repository_creator():
    """Test ONLY the repository creator (requires PRD data)"""
    print("="*60)
    print("Testing Repository Creator Agent")
    print("="*60 + "\n")
    
    crew_instance = GithubRepoManagement()
    
    crew = Crew(
        agents=[crew_instance.repository_creator()],
        tasks=[crew_instance.create_repository_task()],
        process=Process.sequential,
        verbose=True,
    )
    
    # Sample PRD data (you'd get this from the PRD analyzer)
    prd_data = """{
        "project_name": "TaskMaster",
        "description": "A collaborative task management platform",
        "tech_stack": {
            "backend": "FastAPI (Python)",
            "frontend": "React with TypeScript",
            "database": "PostgreSQL"
        },
        "features": [
            {
                "name": "User Authentication",
                "description": "Secure login and registration",
                "priority": "High"
            },
            {
                "name": "Task Management",
                "description": "Create, assign, and track tasks",
                "priority": "High"
            }
        ]
    }"""
    
    result = crew.kickoff(inputs={'prd_data': prd_data})
    
    print("\n" + "="*60)
    print("✓ Repository Created Successfully!")
    print("="*60)
    print(result)
    return result


def test_issue_manager():
    """Test ONLY the issue manager (requires PRD data and repo name)"""
    print("="*60)
    print("Testing Issue Manager Agent")
    print("="*60 + "\n")
    
    crew_instance = GithubRepoManagement()
    
    crew = Crew(
        agents=[crew_instance.issue_manager()],
        tasks=[crew_instance.create_issues_task()],
        process=Process.sequential,
        verbose=True,
    )
    
    # Sample PRD data
    prd_data = """{
        "project_name": "TaskMaster",
        "description": "A collaborative task management platform",
        "tech_stack": {
            "backend": "FastAPI (Python)",
            "frontend": "React with TypeScript",
            "database": "PostgreSQL"
        },
        "features": [
            {
                "name": "User Authentication",
                "description": "Secure user login and registration system",
                "user_stories": [
                    "As a user, I want to register with email/password",
                    "As a user, I want to login securely"
                ],
                "acceptance_criteria": [
                    "User can register with email and password",
                    "Password must be hashed and secure",
                    "JWT tokens issued on login",
                    "Token expires after 24 hours"
                ],
                "technical_requirements": {
                    "api_endpoints": [
                        {"method": "POST", "path": "/api/auth/register"},
                        {"method": "POST", "path": "/api/auth/login"}
                    ],
                    "database_models": ["User"],
                    "security": ["Password hashing", "JWT tokens"]
                },
                "priority": "High"
            }
        ]
    }"""
    
    # Replace with your actual repository name
    repo_name = "your-username/TaskMaster"
    
    result = crew.kickoff(inputs={
        'prd_data': prd_data,
        'repo_name': repo_name
    })
    
    print("\n" + "="*60)
    print("✓ Issues Created Successfully!")
    print("="*60)
    print(result)
    return result


if __name__ == "__main__":
    # Uncomment the function you want to test:
    
    # test_prd_generator()
    
    test_repository_creator()
    
    # test_issue_manager()
