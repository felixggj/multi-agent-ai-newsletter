import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
import json


# Adjust the import path according to your project structure
from ai_football_newsletter.tools.search_tools import SearchTools

# Initialize the OpenAI GPT language models
OpenAIGPT3 = ChatOpenAI(model="gpt-3.5-turbo")
OpenAIGPT4 = ChatOpenAI(model="gpt-4-0125-preview")

import streamlit as st

def streamlit_callback(step_output):
    # This function will be called after each step of the agent's execution
    st.markdown("---")
    for step in step_output:
        if isinstance(step, tuple) and len(step) == 2:
            action, observation = step
            if isinstance(action, dict) and "tool" in action and "tool_input" in action and "log" in action and "thought" in action:
                st.markdown("# Action")
                st.markdown(f"**Tool:** {action['tool']}")
                st.markdown(f"**Tool Input:** `{action['tool_input']}`")
                st.markdown(f"**Log:** {action['log']}")
                st.markdown(f"**Action:** {action.get('Action', 'N/A')}")
                st.markdown(
                    f"**Action Input:** ```json\n{action['tool_input']}\n```")
                
                # Using HTML and CSS to style the thoughts with a purple background
                st.markdown(
                    f"<div style='background-color:#D8BFD8;padding:10px;border-radius:10px;'>"
                    f"<b>Agent's Thoughts:</b> {action['thought']}"
                    f"</div>", unsafe_allow_html=True)
            elif isinstance(action, str):
                st.markdown(f"**Action:** {action}")
            else:
                st.markdown(f"**Action:** {str(action)}")

            # Observations section
            st.markdown("**Observation**")
            if isinstance(observation, str):
                observation_lines = observation.split('\n')
                for line in observation_lines:
                    if line.startswith('Title: '):
                        st.markdown(f"**Title:** {line[7:]}")
                    elif line.startswith('Link: '):
                        st.markdown(f"**Link:** {line[6:]}")
                    elif line.startswith('Snippet: '):
                        st.markdown(f"**Snippet:** {line[9:]}")
                    elif line.startswith('-'):
                        st.markdown(line)
                    else:
                        st.markdown(line)
            else:
                st.markdown(str(observation))
        else:
            st.markdown(str(step))




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
            max_iter=5,
            step_callback=streamlit_callback  # Use the streamlit_callback
        )

    @agent
    def news_fetcher_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['news_fetcher_agent'],
            tools=[SearchTools.search_internet],
            verbose=True,
            allow_delegation=True,
            step_callback=streamlit_callback  # Use the streamlit_callback
        )

    @agent
    def news_analyzer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['news_analyzer_agent'],
            tools=[SearchTools.search_internet],
            verbose=True,
            allow_delegation=True,
            step_callback=streamlit_callback  # Use the streamlit_callback
        )
    
    @agent
    def newsletter_compiler_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['newsletter_compiler_agent'],
            verbose=True,
            step_callback=streamlit_callback  # Use the streamlit_callback
        )
    
    # Tasks for the above agents

    @task
    def fetch_news_task(self) -> Task:
        return Task(
            config=self.tasks_config['fetch_news_task'],
            agent=self.news_fetcher_agent(),
        )

    @task
    def analyze_news_task(self) -> Task:
        return Task(
            config=self.tasks_config['analyze_news_task'],
            agent=self.news_analyzer_agent(),
        )
    
    @task
    def compile_newsletter_task(self) -> Task:
        return Task(
            config=self.tasks_config['compile_newsletter_task'],
            agent=self.newsletter_compiler_agent(),
            output_file="football_newsletter.md"
        )

    @crew
    def crew(self) -> Crew:
        """Creates the FootballNewsletter crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks,
            process=Process.hierarchical,
            #manager_llm=OpenAIGPT4,
        	manager_llm=OpenAIGPT3,
            verbose=2
        )


#m