from crewai.tools import BaseTool
from typing import Type, Optional, List, Dict
from pydantic import BaseModel, Field
from github import Github, GithubException
import os


class CreateRepositoryInput(BaseModel):
    """Input schema for CreateRepositoryTool."""
    name: str = Field(..., description="Name of the repository to create")
    description: str = Field(..., description="Description of the repository")
    private: bool = Field(default=False, description="Whether the repository should be private")
    auto_init: bool = Field(default=True, description="Whether to initialize with README")


class CreateRepositoryTool(BaseTool):
    name: str = "create_github_repository"
    description: str = (
        "Creates a new GitHub repository with the specified name and description. "
        "Returns the repository URL if successful."
    )
    args_schema: Type[BaseModel] = CreateRepositoryInput

    def _run(self, name: str, description: str, private: bool = False, auto_init: bool = True) -> str:
        try:
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                return "Error: GITHUB_TOKEN not found in environment variables"
            
            g = Github(token)
            user = g.get_user()
            
            repo = user.create_repo(
                name=name,
                description=description,
                private=private,
                auto_init=auto_init
            )
            
            return f"Repository created successfully: {repo.html_url}"
        except GithubException as e:
            return f"GitHub API Error: {e.data.get('message', str(e))}"
        except Exception as e:
            return f"Error creating repository: {str(e)}"


class CreateIssueInput(BaseModel):
    """Input schema for CreateIssueTool."""
    repo_name: str = Field(..., description="Repository name (format: owner/repo or just repo)")
    title: str = Field(..., description="Title of the issue")
    body: str = Field(..., description="Body/description of the issue")
    labels: Optional[List[str]] = Field(default=None, description="List of label names to apply")


class CreateIssueTool(BaseTool):
    name: str = "create_github_issue"
    description: str = (
        "Creates a new issue in the specified GitHub repository. "
        "You can optionally add labels to categorize the issue."
    )
    args_schema: Type[BaseModel] = CreateIssueInput

    def _run(self, repo_name: str, title: str, body: str, labels: Optional[List[str]] = None) -> str:
        try:
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                return "Error: GITHUB_TOKEN not found in environment variables"
            
            g = Github(token)
            
            # If repo_name doesn't contain '/', prepend the authenticated user's login
            if '/' not in repo_name:
                user = g.get_user()
                repo_name = f"{user.login}/{repo_name}"
            
            repo = g.get_repo(repo_name)
            
            # Create the issue
            issue = repo.create_issue(
                title=title,
                body=body,
                labels=labels or []
            )
            
            return f"Issue created successfully: {issue.html_url}"
        except GithubException as e:
            return f"GitHub API Error: {e.data.get('message', str(e))}"
        except Exception as e:
            return f"Error creating issue: {str(e)}"


class CreateLabelsInput(BaseModel):
    """Input schema for CreateLabelsTool."""
    repo_name: str = Field(..., description="Repository name (format: owner/repo or just repo)")
    labels: List[Dict[str, str]] = Field(
        ..., 
        description="List of labels with 'name', 'color' (hex without #), and optional 'description'"
    )


class CreateLabelsTool(BaseTool):
    name: str = "create_github_labels"
    description: str = (
        "Creates multiple labels in a GitHub repository. "
        "Labels help categorize issues and pull requests."
    )
    args_schema: Type[BaseModel] = CreateLabelsInput

    def _run(self, repo_name: str, labels: List[Dict[str, str]]) -> str:
        try:
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                return "Error: GITHUB_TOKEN not found in environment variables"
            
            g = Github(token)
            
            # If repo_name doesn't contain '/', prepend the authenticated user's login
            if '/' not in repo_name:
                user = g.get_user()
                repo_name = f"{user.login}/{repo_name}"
            
            repo = g.get_repo(repo_name)
            
            created_labels = []
            for label_data in labels:
                try:
                    label = repo.create_label(
                        name=label_data['name'],
                        color=label_data.get('color', 'ededed'),
                        description=label_data.get('description', '')
                    )
                    created_labels.append(label.name)
                except GithubException as e:
                    if e.status == 422:  # Label already exists
                        created_labels.append(f"{label_data['name']} (already exists)")
                    else:
                        return f"Error creating label '{label_data['name']}': {e.data.get('message', str(e))}"
            
            return f"Labels created: {', '.join(created_labels)}"
        except GithubException as e:
            return f"GitHub API Error: {e.data.get('message', str(e))}"
        except Exception as e:
            return f"Error creating labels: {str(e)}"


class UpdateReadmeInput(BaseModel):
    """Input schema for UpdateReadmeTool."""
    repo_name: str = Field(..., description="Repository name (format: owner/repo or just repo)")
    content: str = Field(..., description="Content for the README.md file")
    commit_message: str = Field(default="Update README.md", description="Commit message")


class UpdateReadmeTool(BaseTool):
    name: str = "update_github_readme"
    description: str = (
        "Updates or creates the README.md file in a GitHub repository with the provided content."
    )
    args_schema: Type[BaseModel] = UpdateReadmeInput

    def _run(self, repo_name: str, content: str, commit_message: str = "Update README.md") -> str:
        try:
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                return "Error: GITHUB_TOKEN not found in environment variables"
            
            g = Github(token)
            
            # If repo_name doesn't contain '/', prepend the authenticated user's login
            if '/' not in repo_name:
                user = g.get_user()
                repo_name = f"{user.login}/{repo_name}"
            
            repo = g.get_repo(repo_name)
            
            # Try to get existing README
            try:
                readme = repo.get_contents("README.md")
                repo.update_file(
                    path="README.md",
                    message=commit_message,
                    content=content,
                    sha=readme.sha
                )
                return f"README.md updated successfully in {repo_name}"
            except GithubException:
                # README doesn't exist, create it
                repo.create_file(
                    path="README.md",
                    message=commit_message,
                    content=content
                )
                return f"README.md created successfully in {repo_name}"
        except GithubException as e:
            return f"GitHub API Error: {e.data.get('message', str(e))}"
        except Exception as e:
            return f"Error updating README: {str(e)}"
