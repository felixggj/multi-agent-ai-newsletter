from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

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

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			agent=self.researcher()
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['reporting_task'],
			agent=self.reporting_analyst(),
			output_file='report.md'
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