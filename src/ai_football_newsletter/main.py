#!/usr/bin/env python
from ai_football_newsletter.crew import FootballNewsletterCrew


def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': 'AI LLMs'
    }
    FootballNewsletterCrew().crew().kickoff(inputs=inputs)