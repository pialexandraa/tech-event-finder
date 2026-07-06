# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types
from pydantic import BaseModel, Field
from typing import List

import os
import google.auth

# Import custom tools and schemas
from app.tools import get_watchlist, fetch_and_parse_events, send_notification
from app.schemas import Event

# Setup environment
if "GOOGLE_GENAI_USE_VERTEXAI" not in os.environ:
    if "GOOGLE_API_KEY" in os.environ and os.environ["GOOGLE_API_KEY"] not in (
        "your_api_key_here",
        "",
    ):
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
    else:
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "True"

if os.environ.get("GOOGLE_GENAI_USE_VERTEXAI") == "True":
    if "GOOGLE_CLOUD_LOCATION" not in os.environ:
        os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
    if "GOOGLE_CLOUD_PROJECT" not in os.environ:
        try:
            _, project_id = google.auth.default()
            os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
        except Exception:
            os.environ["GOOGLE_CLOUD_PROJECT"] = "mock-project"


# Define the structured output container for filtration
class EventCurationOutput(BaseModel):
    events: List[Event] = Field(
        description="A list of curation results containing events, their relevance scores, and justifications."
    )


# 1. Filtration Agent Layer
# Specialized agent responsible for scoring event candidates against the target developer profile
filtration_agent = Agent(
    name="filtration_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="""
    You are an expert developer advocate and tech event curator.
    Your task is to evaluate and score event candidates against the target developer profile:
    - Cloud infrastructure (Kubernetes, Terraform, AWS/GCP/Azure)
    - Go (Golang) programming language and system tooling
    - Python programming language and data/AI tooling
    - Systems monitoring, observability, metrics, and alerting (Prometheus, OpenTelemetry)
    - AI engineering (Generative AI, LLMs, model integration, agent development)

    For each event candidate:
    - Determine a relevance score between 0 and 100.
    - Provide a short and precise justification for your score.
    - Populate the output list matching the schema exactly.
    """,
    output_schema=EventCurationOutput,
    output_key="curation_result",
    description="Filters, scores, and justifies tech events based on a developer profile focusing on Cloud, Go, Python, Observability, and AI.",
)

# 2. Main Coordinator Agent
# Coordinates finding events from watchlists and delegates candidate screening to the filtration layer
root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="""
    You are the TechEvent Finder coordinator.
    Follow this exact workflow to serve the user:
    1. Retrieve the watchlist of event sources using the `get_watchlist` tool.
    2. For each source found in the watchlist, fetch and parse raw events using the `fetch_and_parse_events` tool.
    3. Aggregate all parsed candidate events.
    4. Call the `filtration_agent` sub-agent to filter, score, and justify the relevance of the candidates.
    5. ONLY AFTER filtering, use the `send_notification` tool to send the highly-scored curated events to the configured destination.
    6. Present the final curated event list to the user and report the status of the notification.
    """,
    tools=[get_watchlist, fetch_and_parse_events, send_notification],
    sub_agents=[filtration_agent],
)

app = App(
    root_agent=root_agent,
    name="app",
)
