"""
Repository scaffolding tools that combine templates with Git operations.
"""
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from github import Github, GithubException
import os

from .project_templates import get_template, list_templates


class ScaffoldProjectInput(BaseModel):
    """Input schema for ScaffoldProjectTool."""
    repo_name: str = Field(..., description="Repository name (format: owner/repo or just repo)")
    project_name: str = Field(..., description="Display name for the project")
    template: str = Field(..., description="Template to use (e.g., 'python-fastapi', 'react', 'node-express')")
    branch: str = Field(default="main", description="Branch to create files in")


class ScaffoldProjectTool(BaseTool):
    name: str = "scaffold_project"
    description: str = (
        f"Scaffolds a complete project structure in a GitHub repository based on a template. "
        f"Creates folders and base files for quick project setup. "
        f"Available templates: {', '.join(list_templates())}"
    )
    args_schema: Type[BaseModel] = ScaffoldProjectInput

    def _run(
        self, 
        repo_name: str, 
        project_name: str,
        template: str,
        branch: str = "main"
    ) -> str:
        try:
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                return "Error: GITHUB_TOKEN not found in environment variables"
            
            g = Github(token)
            
            # Normalize repo name
            if '/' not in repo_name:
                user = g.get_user()
                repo_name = f"{user.login}/{repo_name}"
            
            repo = g.get_repo(repo_name)
            
            # Get template
            try:
                template_obj = get_template(template, project_name)
            except ValueError as e:
                return f"Error: {str(e)}"
            
            # Create folder structure
            folders = template_obj.get_folders()
            created_folders = []
            
            for folder in folders:
                try:
                    folder = folder.rstrip('/')
                    gitkeep_path = f"{folder}/.gitkeep"
                    
                    repo.create_file(
                        path=gitkeep_path,
                        message=f"Create {folder} directory",
                        content="",
                        branch=branch
                    )
                    created_folders.append(folder)
                except GithubException as e:
                    if e.status != 422:  # Ignore "already exists"
                        pass
            
            # Create files
            files = template_obj.get_files()
            created_files = []
            failed_files = []
            
            for file_data in files:
                try:
                    file_path = file_data.get('path')
                    content = file_data.get('content', '')
                    
                    repo.create_file(
                        path=file_path,
                        message=f"Add {file_path}",
                        content=content,
                        branch=branch
                    )
                    created_files.append(file_path)
                except GithubException as e:
                    if e.status == 422:
                        failed_files.append(f"{file_path} (already exists)")
                    else:
                        failed_files.append(f"{file_path} (error)")
            
            result = f"Project scaffolded successfully in {repo_name}:\n"
            result += f"- Created {len(created_folders)} folders\n"
            result += f"- Created {len(created_files)} files\n"
            result += f"- Template: {template}\n"
            result += f"- Branch: {branch}"
            
            if failed_files:
                result += f"\n- Skipped {len(failed_files)} existing files"
            
            return result
            
        except GithubException as e:
            return f"GitHub API Error: {e.data.get('message', str(e))}"
        except Exception as e:
            return f"Error scaffolding project: {str(e)}"


class ListTemplatesInput(BaseModel):
    """Input schema for ListTemplatesTool."""
    pass


class ListTemplatesTool(BaseTool):
    name: str = "list_project_templates"
    description: str = (
        "Lists all available project templates that can be used for scaffolding."
    )
    args_schema: Type[BaseModel] = ListTemplatesInput

    def _run(self) -> str:
        templates = list_templates()
        result = "Available project templates:\n"
        for template in templates:
            result += f"- {template}\n"
        return result
