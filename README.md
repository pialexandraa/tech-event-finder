# TechEvent Finder (TEFinder)

This application is the final submission project for the Google - Kaggle course: ["5-Day AI Agents: AI Agents and intensive vibe-coding"](https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google)

## Architecture

This project implements a modular, agent-based curation system for tech events built on the Gemini Enterprise Agent Platform ADK.

- **Ingestion & Parsing Tool Layer**: A modular pipeline that accepts watchlists of sources, fetches URLs, and leverages specialized parsers to extract raw event announcements.
- **Data Schemas**: Standardized Pydantic models for type safety, validation, and structured representation of filtered events.
- **LLM Filtration & Scoring Agent**: A Gemini-powered agent that scores incoming events against a target developer profile (Cloud Infrastructure, Go, Python, Systems Monitoring, and AI Engineering), justifying the relevance of each selected event.

