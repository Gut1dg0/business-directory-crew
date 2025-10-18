from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import (
    SerperDevTool,
    SeleniumScrapingTool,
)
from typing import List
from .tools.publish_to_wordpress import publish_to_wordpress
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators
gemini_llm = LLM(
    model="gemini/gemini-2.0-flash",
    temperature=0.7,
)

openai_llm = LLM(
    model="openai/gpt-5-2025-08-07",
    temperature=0.7,
)

anthropic_llm = LLM(
    model="anthropic/claude-opus-4-1-20250805",
    temperature=0.7,
)

scrape_tool = SeleniumScrapingTool()

@CrewBase
class AppMaster():
    """AppMaster crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
       return Agent(
           config=self.agents_config['researcher'], # type: ignore[index]
           verbose=True,
           llm=gemini_llm,
           tools=[SerperDevTool()]
       )
    
    @agent
    def writer(self) -> Agent:
       return Agent(
           config=self.agents_config['writer'], # type: ignore[index]
           verbose=True,
           llm=gemini_llm
       )
    
    @agent
    def web_scraper(self) -> Agent:
       return Agent(
           config=self.agents_config['web_scraper'], # type: ignore[index]
           verbose=True,
           llm=gemini_llm,
           tools=[scrape_tool]
       )
    
    @agent
    def developer(self) -> Agent:
       return Agent(
           config=self.agents_config['developer'], # type: ignore[index]
           verbose=True,
           llm=gemini_llm,
       )
    
    @agent
    def publisher(self) -> Agent:
        return Agent(
            config=self.agents_config['publisher'], # type: ignore[index]
            verbose=True,
            llm=gemini_llm,
            tools=[publish_to_wordpress]
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def research_task(self) -> Task:
       return Task(
           config=self.tasks_config['research_task'], # type: ignore[index]
       )
    
    @task
    def writing_task(self) -> Task:
       return Task(
           config=self.tasks_config['writing_task'], # type: ignore[index]
           async_execution=True,  # This task will run asynchronously
       )
    
    @task
    def web_scraping_task(self) -> Task:
       return Task(
           config=self.tasks_config['web_scraping_task'], # type: ignore[index]
           async_execution=True,  # This task will run asynchronously
       )
    
    @task
    def development_task(self) -> Task:
       return Task(
           config=self.tasks_config['development_task'], # type: ignore[index]
       )
    
    @task
    def publishing_task(self) -> Task:
        return Task(
            config=self.tasks_config['publishing_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AppMaster crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
