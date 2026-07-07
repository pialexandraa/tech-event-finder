import asyncio

from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from google.adk.runners import InMemoryRunner
from google.genai import types

from app.agent import root_agent


async def main():
    """Run the TechEvent Finder agent autonomously in the background."""
    print("Starting autonomous curation job...")

    # Initialize the runner
    runner = InMemoryRunner(agent=root_agent, app_name="app")

    # Initialize the session using the runner's built-in session service
    session = await runner.session_service.create_session(
        user_id="demo-user",
        app_name="app",
        session_id="demo-session"
    )

    # The initial prompt that kicks off the workflow without user interaction
    prompt = "Fetch and curate the events from the watchlist"
    print(f"\n[USER] {prompt}\n")

    msg = types.Content(role="user", parts=[types.Part.from_text(text=prompt)])

    # Run the agent and stream the events
    async for event in runner.run_async(user_id="demo-user", session_id="demo-session", new_message=msg):
        if event.content:
            print(f"[{event.author}] {event.content}")

    print("\nJob complete. Check 'latest_notifications.json' for the curated output if no webhook was set.")

if __name__ == "__main__":
    # Ensure uv/python runs this with asyncio
    asyncio.run(main())
