from ai_football_newsletter.crew import FootballNewsletterCrew
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st
load_dotenv()

def run():
    inputs = {
        'current_time':  datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    FootballNewsletterCrew().crew().kickoff(inputs=inputs)
    
    
if __name__ == "__main__":
    st.title("AI Football Newsletter Generator")
    
    # Use a button to trigger the run function and capture output
    if st.button("Generate Football Newsletter"):
        with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
            with st.container(height=500, border=False):
                run()
            status.update(label="✅ Trip Plan Ready!",
                        state="complete", expanded=False)

        st.subheader(f"Here is your newsletter for {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", anchor=False, divider="rainbow")
        st.markdown('./football_newsletter.md')
                
    