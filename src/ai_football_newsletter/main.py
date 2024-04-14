from ai_football_newsletter.crew import FootballNewsletterCrew
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

def run():
    inputs = {
        'current_time':  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    FootballNewsletterCrew().crew().kickoff(inputs=inputs)