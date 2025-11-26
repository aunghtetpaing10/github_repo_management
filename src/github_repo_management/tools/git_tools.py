"""
Git operations tools for repository scaffolding and file management.
"""
from crewai.tools import BaseTool
from typing import Type, List, Dict
from pydantic import BaseModel, Field
from github import Github, GithubException
import os


class CreateFileInput(BaseModel):
    """Input schema for CreateFileTool."""
    repo_name: str = Field(..., description="Repository name (format: owner/repo or just repo)")
    file_path: str = Field(..., description="Path where the file should be created (e.g., 'src/main.py')")
    content: str = Field(..., description="Content of the file")
    commit_message: str = Field(default="Add new file", description="Commit message")
    branch: str = Field(default="main", description="Branch name to create the file in")


class CreateFileTool(BaseTool):
    name: str = "create_file_in_repo"
    description: str = (
        "Creates a new file in a GitHub repository with specified content. "
        "Can create files in any directory path and on any branch."
    )
    args_schema: Type[BaseModel] = CreateFileInput

    def _run(
        self, 
        repo_name: str, 
        file_path: str, 
        content: str, 
        commit_message: str = "Add new file",
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
            
            # Create the file
            repo.create_file(
                path=file_path,
                message=commit_message,
                content=content,
                branch=branch
            )
            
            return f"File '{file_path}' created successfully in {repo_name} on branch '{branch}'"
        except GithubException as e:
            if e.status == 422:
                return f"File already exists: {file_path}"
            return f"GitHub API Error: {e.data.get('message', str(e))}"
        except Exception as e:
            return f"Error creating file: {str(e)}"


class CreateMultipleFilesInput(BaseModel):
    """Input schema for CreateMultipleFilesTool."""
    repo_name: str = Field(..., description="Repository name (format: owner/repo or just repo)")
    files: List[Dict[str, str]] = Field(
        ..., 
        description="List of files with 'path' and 'content' keys"
    )
    commit_message: str = Field(default="Add project files", description="Commit message")
    branch: str = Field(default="main", description="Branch name")


class CreateMultipleFilesTool(BaseTool):
    name: str = "create_multiple_files"
    description: str = (
        "Creates multiple files in a GitHub repository in a batch. "
        "Useful for scaffolding entire project structures."
    )
    args_schema: Type[BaseModel] = CreateMultipleFilesInput

    def _run(
        self, 
        repo_name: str, 
        files: List[Dict[str, str]], 
        commit_message: str = "Add project files",
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
            
            # Create all files
            created_files = []
            failed_files = []
            
            for file_data in files:
                try:
                    file_path = file_data.get('path')
                    content = file_data.get('content', '')
                    
                    if not file_path:
                        failed_files.append("Missing file path")
                        continue
                    
                    repo.create_file(
                        path=file_path,
                        message=commit_message,
                        content=content,
                        branch=branch
                    )
                    created_files.append(file_path)
                except GithubException as e:
                    if e.status == 422:
                        failed_files.append(f"{file_path} (already exists)")
                    else:
                        failed_files.append(f"{file_path} ({str(e)})")
            
            result = f"Created {len(created_files)} files in {repo_name}"
            if failed_files:
                result += f"\nFailed: {', '.join(failed_files)}"
            
            return result
        except GithubException as e:
            return f"GitHub API Error: {e.data.get('message', str(e))}"
        except Exception as e:
            return f"Error creating files: {str(e)}"


class CreateBranchInput(BaseModel):
    """Input schema for CreateBranchTool."""
    repo_name: str = Field(..., description="Repository name (format: owner/repo or just repo)")
    branch_name: str = Field(..., description="Name of the new branch to create")
    source_branch: str = Field(default="main", description="Source branch to create from")


class CreateBranchTool(BaseTool):
    name: str = "create_branch"
    description: str = (
        "Creates a new branch in a GitHub repository from an existing branch."
    )
    args_schema: Type[BaseModel] = CreateBranchInput

    def _run(
        self, 
        repo_name: str, 
        branch_name: str, 
        source_branch: str = "main"
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
            
            # Get the source branch
            source_ref = repo.get_branch(source_branch)
            
            # Create new branch
            repo.create_git_ref(
                ref=f"refs/heads/{branch_name}",
                sha=source_ref.commit.sha
            )
            
            return f"Branch '{branch_name}' created successfully from '{source_branch}' in {repo_name}"
        except GithubException as e:
            if e.status == 422:
                return f"Branch '{branch_name}' already exists in {repo_name}"
            return f"GitHub API Error: {e.data.get('message', str(e))}"
        except Exception as e:
            return f"Error creating branch: {str(e)}"


class CreateFolderStructureInput(BaseModel):
    """Input schema for CreateFolderStructureTool."""
    repo_name: str = Field(..., description="Repository name (format: owner/repo or just repo)")
    folders: List[str] = Field(..., description="List of folder paths to create (e.g., ['src', 'tests', 'docs'])")
    branch: str = Field(default="main", description="Branch name")


class CreateFolderStructureTool(BaseTool):
    name: str = "create_folder_structure"
    description: str = (
        "Creates a folder structure in a GitHub repository by adding .gitkeep files. "
        "GitHub doesn't support empty folders, so this creates placeholder files."
    )
    args_schema: Type[BaseModel] = CreateFolderStructureInput

    def _run(
        self, 
        repo_name: str, 
        folders: List[str], 
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
            
            created_folders = []
            
            for folder in folders:
                try:
                    # Ensure folder path ends properly
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
                    if e.status != 422:  # Ignore "already exists" errors
                        return f"Error creating folder '{folder}': {e.data.get('message', str(e))}"
            
            return f"Created {len(created_folders)} folders in {repo_name}: {', '.join(created_folders)}"
        except GithubException as e:
            return f"GitHub API Error: {e.data.get('message', str(e))}"
        except Exception as e:
            return f"Error creating folder structure: {str(e)}"


class UpdateFileInput(BaseModel):
    """Input schema for UpdateFileTool."""
    repo_name: str = Field(..., description="Repository name (format: owner/repo or just repo)")
    file_path: str = Field(..., description="Path to the file to update")
    content: str = Field(..., description="New content for the file")
    commit_message: str = Field(default="Update file", description="Commit message")
    branch: str = Field(default="main", description="Branch name")


class UpdateFileTool(BaseTool):
    name: str = "update_file_in_repo"
    description: str = (
        "Updates an existing file in a GitHub repository with new content."
    )
    args_schema: Type[BaseModel] = UpdateFileInput

    def _run(
        self, 
        repo_name: str, 
        file_path: str, 
        content: str, 
        commit_message: str = "Update file",
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
            
            # Get existing file
            file = repo.get_contents(file_path, ref=branch)
            
            # Update the file
            repo.update_file(
                path=file_path,
                message=commit_message,
                content=content,
                sha=file.sha,
                branch=branch
            )
            
            return f"File '{file_path}' updated successfully in {repo_name}"
        except GithubException as e:
            if e.status == 404:
                return f"File not found: {file_path}"
            return f"GitHub API Error: {e.data.get('message', str(e))}"
        except Exception as e:
            return f"Error updating file: {str(e)}"
