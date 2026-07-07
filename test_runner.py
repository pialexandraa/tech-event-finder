import asyncio

from google.adk.runners import InMemoryRunner
from google.genai import types

from app.agent import root_agent


async def main():
    runner = InMemoryRunner(agent=root_agent, app_name="app")
    await runner.session_service.create_session(user_id="u", app_name="app", session_id="test")
    msg = types.Content(role="user", parts=[types.Part.from_text(text="Fetch events")])
    async for event in runner.run_async(user_id="u", session_id="test", new_message=msg):
        if event.content:
            print(event.content)
asyncio.run(main())
