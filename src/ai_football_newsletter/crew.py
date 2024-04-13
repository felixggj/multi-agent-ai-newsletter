from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from datetime import datetime

# Uncomment the following line to use an example of a custom tool
# from ai_football_newsletter.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class FootballNewsletterCrew():
	"""FootballNewsletter crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def editor_agent(self) -> Agent:
		return Agent(
			verbose=True,
			allow_delegation=True,
			max_iter=15
		)

	@agent
	def news_fetcher_agent(self) -> Agent:
		return Agent(
			verbose=True,
			allow_delegation=True,
		)

	@agent
	def news_analyzer_agent(self) -> Agent:
		return Agent(
			verbose=True,
			allow_delegation=True,
		)
	
	@agent
	def newsletter_compiler_agent(self) -> Agent:
		return Agent(
			verbose=True,
		)
	
	# Tasks for the above agents

	@task
	def fetch_news_task(self, agent) -> Task:
		return Task(
			# including description here instead of yaml as we want to use the datetime module
            description=f'Fetch top AI news stories from the past 24 hours. The current time is {datetime.now()}.',
            agent=agent,
            async_execution=True, # allows us to fetch 5-10 different articles at the same time
		)

	@task
	def analyze_news_task(self, agent, context) -> Task:
		return Task(
            agent=agent,
            async_execution=True,
			context=context, # feeds the previous task's output to this task
		)
	
	@task
	def compile_newsletter_task(self, agent, context, callback_function) -> Task:
		return Task(
            agent=agent,
            context=context,
			callback=callback_function,
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the FootballNewsletter crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)