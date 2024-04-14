# AiFootballNewsletter Crew

Welcome to the AiFootballNewsletter Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install Poetry:

```bash
pip install poetry
```

Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and then install them:
```bash
poetry lock
```
```bash
poetry install
```
### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/ai_football_newsletter/config/agents.yaml` to define your agents
- Modify `src/ai_football_newsletter/config/tasks.yaml` to define your tasks
- Modify `src/ai_football_newsletter/crew.py` to add your own logic, tools and specific args
- Modify `src/ai_football_newsletter/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
poetry run ai_football_newsletter
```

## Understanding Your Crew

The ai-football-newsletter Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.