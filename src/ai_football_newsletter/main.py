#!/usr/bin/env python
from ai_football_newsletter.crew import AiFootballNewsletterCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': 'AI LLMs'
    }
    AiFootballNewsletterCrew().crew().kickoff(inputs=inputs)