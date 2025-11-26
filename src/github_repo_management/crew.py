from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from github_repo_management.tools import (
    PRDParserTool,
    CreateRepositoryTool,
    CreateIssueTool,
    CreateLabelsTool,
    UpdateReadmeTool,
    ScaffoldProjectTool,
    CreateBranchTool,
    CreateFileTool,
    CreateFolderStructureTool
)

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class GithubRepoManagement():
    """GithubRepoManagement crew for automated GitHub project setup from PRDs"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def prd_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['prd_analyst'], # type: ignore[index]
            tools=[PRDParserTool()],
            verbose=True
        )

    @agent
    def repository_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['repository_creator'], # type: ignore[index]
            tools=[
                CreateRepositoryTool(),
                CreateLabelsTool(),
                UpdateReadmeTool()
            ],
            verbose=True
        )

    @agent
    def issue_manager(self) -> Agent:
        return Agent(
            config=self.agents_config['issue_manager'], # type: ignore[index]
            tools=[CreateIssueTool()],
            verbose=True
        )

    @agent
    def project_scaffolder(self) -> Agent:
        return Agent(
            config=self.agents_config['project_scaffolder'], # type: ignore[index]
            tools=[
                ScaffoldProjectTool(),
                CreateBranchTool(),
                CreateFileTool(),
                CreateFolderStructureTool()
            ],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def analyze_prd_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_prd_task'], # type: ignore[index]
        )

    @task
    def create_repository_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_repository_task'], # type: ignore[index]
        )

    @task
    def create_issues_task(self) -> Task:
        return Task(
            config=self.tasks_config['create_issues_task'], # type: ignore[index]
        )

    @task
    def scaffold_project_task(self) -> Task:
        return Task(
            config=self.tasks_config['scaffold_project_task'], # type: ignore[index]
            output_file='project_setup_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GithubRepoManagement crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
