from ai_football_newsletter.crew import FootballNewsletterCrew
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'current_time': datetime.now()
    }
    FootballNewsletterCrew().crew().kickoff(inputs=inputs)