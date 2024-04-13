from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from langchain_openai import ChatOpenAI

from ai_football_newsletter.tools.search_tools import SearchTools 

from file_io import save_markdown

# Initialize the OpenAI GPT-3.5 language model
OpenAIGPT3 = ChatOpenAI(
    model="gpt-3.5-turbo",
)

# Initialize the OpenAI GPT-4 language model
OpenAIGPT4 = ChatOpenAI(
    model="gpt-4-0125-preview",
)

@CrewBase
class FootballNewsletterCrew():
	"""FootballNewsletter crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def editor_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['editor_agent'],
			verbose=True,
			allow_delegation=True,
			max_iter=15
		)

	@agent
	def news_fetcher_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['news_fetcher_agent'],
			tools=[SearchTools.search_internet],
			verbose=True,
			allow_delegation=True,
		)

	@agent
	def news_analyzer_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['news_analyzer_agent'],
			tools=[SearchTools.search_internet],
			verbose=True,
			allow_delegation=True,
		)
	
	@agent
	def newsletter_compiler_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['newsletter_compiler_agent'],
			verbose=True,
		)
	
	# Tasks for the above agents

	@task
	def fetch_news_task(self) -> Task:
		return Task(
			config=self.tasks_config['fetch_news_task'],
            agent=self.news_fetcher_agent,
            async_execution=True, # allows us to fetch 5-10 different articles at the same time
		)

	@task
	def analyze_news_task(self, context) -> Task:
		return Task(
			config=self.tasks_config['analyze_news_task'],
            agent=self.news_analyzer_agent,
            async_execution=True,
			context=context, # feeds the previous task's output to this task
		)
	
	@task
	def compile_newsletter_task(self, context) -> Task:
		return Task(
			config=self.tasks_config['compile_newsletter_task'],
            agent=self.newsletter_compiler_agent,
            context=context,
			callback_function=save_markdown, # saves the newsletter to a markdown file
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the FootballNewsletter crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.hierarchical,
			manager_llm=OpenAIGPT3,
			# manager_llm=OpenAIGPT4,
			verbose=2
		)