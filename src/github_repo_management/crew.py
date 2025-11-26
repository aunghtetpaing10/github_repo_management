from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from github_repo_management.tools import (
    PRDParserTool,
    CreateRepositoryTool,
    CreateIssueTool,
    CreateLabelsTool,
    UpdateReadmeTool
)

@CrewBase
class GithubRepoManagement():
    """GithubRepoManagement crew for automated GitHub project setup from PRDs"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def prd_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['prd_generator'], # type: ignore[index]
            verbose=True
        )

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

    @task
    def generate_prd_task(self) -> Task:
        return Task(
            config=self.tasks_config['generate_prd_task'], # type: ignore[index]
        )

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

    @crew
    def crew(self) -> Crew:
        """Creates the GithubRepoManagement crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
