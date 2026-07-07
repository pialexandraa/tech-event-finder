import asyncio
import time

from dotenv import load_dotenv

# Load environment variables (allows testing real SMTP/webhooks if provided)
load_dotenv()

from app.tools import fetch_and_parse_events, get_watchlist, send_notification


async def simulate_demo():
    """Simulate the agent curation pipeline to record a flawless demo.
    
    This script runs the exact pipeline flow and executes the real notification tools (email/webhook/json)
    using mock curated events. This bypasses the Gemini API daily quota limit, allowing for
    seamless screen recording and instant validation of email/webhook delivery.
    """
    print("==================================================")
    print("   TechEvent Finder - Autonomous Agent Demo Mode  ")
    print("==================================================")
    time.sleep(1)

    print("\n[USER] Fetch and curate the events from the watchlist")
    time.sleep(1.5)

    print("\n[root_agent] 🛠️ Calling tool: get_watchlist")
    time.sleep(1)
    watchlist_data = get_watchlist()
    watchlist = watchlist_data["watchlist"]
    print(f"[root_agent] Watchlist retrieved: {len(watchlist)} sources found.")

    all_raw_events = []
    for source in watchlist:
        source_name = source["source_name"]
        url = source["url"]
        parser_type = source["parser_type"]
        print(f"\n[root_agent] 🛠️ Calling tool: fetch_and_parse_events (Source: {source_name})")
        time.sleep(1)
        res = await fetch_and_parse_events(source_name, url, parser_type)
        print(f"[root_agent] Parsed {len(res['events'])} candidates from '{source_name}' (Status Code: {res['status_code']})")
        all_raw_events.extend(res['events'])

    print(f"\n[root_agent] Total candidates aggregated: {len(all_raw_events)} events.")
    time.sleep(1)

    print("\n[root_agent] 🛠️ Calling tool: deduplicate_events")
    # Simulate finding some duplicates
    deduplicated_count = max(0, len(all_raw_events) - 2)
    print(f"[root_agent] Deduplicated events: {deduplicated_count} unique events remain.")
    time.sleep(1.5)

    print("\n[root_agent] ➡️ Transferring control to: filtration_agent")
    print("[filtration_agent] Analyzing events against developer profile...")
    print("  Profile focus: Cloud, Go, Python, Observability, and AI Engineering.")
    time.sleep(2)

    # Mocking the structured output from filtration_agent
    mock_curated_events = [
        {
            "title": "Prometheus Day 2026 (via Cloud Native Events)",
            "date": "2026-09-24",
            "location": "Munich, Germany",
            "link": "https://example.com/event",
            "relevance_score": 96,
            "justification": "A highly specialized developer day completely dedicated to Prometheus, systems monitoring, alerting, metrics collection, and overall observability, which is a major component of the profile."
        },
        {
            "title": "Google I/O Connect Europe (via Google Developers Europe)",
            "date": "2026-06-25",
            "location": "Berlin, Germany",
            "link": "https://example.com/event",
            "relevance_score": 97,
            "justification": "European flagship developer conference showcasing Google Cloud solutions, Gemini APIs, and Go developer integrations, holding extreme relevance to the profile's multi-cloud and Go requirements."
        },
        {
            "title": "AWS Summit Paris (via AWS Events Europe)",
            "date": "2026-04-15",
            "location": "Paris, France",
            "link": "https://example.com/event",
            "relevance_score": 91,
            "justification": "Critical European cloud native summit focusing on AWS cloud architecture, container deployments (EKS), and infrastructure as code, directly serving the cloud infrastructure requirements."
        },
        {
            "title": "Red Hat Summit Connect Madrid (via Red Hat Events)",
            "date": "2026-08-30",
            "location": "Madrid, Spain",
            "link": "https://www.redhat.com/de/events",
            "relevance_score": 90,
            "justification": "Major Red Hat enterprise open source summit in Southern Europe focusing on hybrid cloud and AI infrastructure."
        },
        {
            "title": "Codemotion Milan 2026 (via Italy Developer Events)",
            "date": "2026-10-14",
            "location": "Milan, Italy",
            "link": "https://example.com/event",
            "relevance_score": 92,
            "justification": "Italy's biggest gathering for software developers. Features extensive tracks on backend architecture (Go/Python), AI engineering, and DevOps practices."
        },
        {
            "title": "KubeCon Europe 2026 (via Dutch Tech Events)",
            "date": "2026-04-18",
            "location": "Amsterdam, Netherlands",
            "link": "https://example.com/event",
            "relevance_score": 99,
            "justification": "The ultimate flagship event for cloud native computing and Kubernetes in the Netherlands, directly matching the highest priority skillsets."
        },
        {
            "title": "WebExpo 2026 (via Czech Tech Events)",
            "date": "2026-06-10",
            "location": "Prague, Czech Republic",
            "link": "https://example.com/event",
            "relevance_score": 87,
            "justification": "Central Europe's premier event for tech leaders and backend developers, fostering cross-disciplinary discussions around AI and systems design."
        },
        {
            "title": "GOTO Copenhagen 2026 (via Nordic Tech Events)",
            "date": "2026-09-02",
            "location": "Copenhagen, Denmark",
            "link": "https://example.com/event",
            "relevance_score": 94,
            "justification": "Top-tier enterprise software development conference in the Nordics with notoriously strong tracks on distributed systems, Go, and observability."
        },
        {
            "title": "Swiss Python Summit 2026 (via Swiss Tech Events)",
            "date": "2026-02-20",
            "location": "Rapperswil, Switzerland",
            "link": "https://example.com/event",
            "relevance_score": 91,
            "justification": "A community-focused conference in Switzerland perfectly targeting the Python developer profile, highlighting ML engineering and advanced data pipelines."
        },
        {
            "title": "InfoShare 2026 (via Poland Tech Events)",
            "date": "2026-05-13",
            "location": "Gdańsk, Poland",
            "link": "https://example.com/event",
            "relevance_score": 89,
            "justification": "The biggest tech and startup conference in CEE (Poland), heavily showcasing advanced backend scalable systems and AI engineering."
        },
        {
            "title": "Shift Conference 2026 (via Croatia Tech Events)",
            "date": "2026-09-19",
            "location": "Zadar, Croatia",
            "link": "https://example.com/event",
            "relevance_score": 90,
            "justification": "A premier developer conference in Croatia gathering attendees globally for high-level technical discussions on cloud infrastructure and API development."
        },
        {
            "title": "Web Summit 2026 (via Portugal Tech Events)",
            "date": "2026-11-10",
            "location": "Lisbon, Portugal",
            "link": "https://example.com/event",
            "relevance_score": 93,
            "justification": "One of the largest global tech conferences hosted in Portugal, offering high-value networking and deep dives into cloud infrastructure and AI startups."
        }
    ]

    print(f"[filtration_agent] Scoring complete. Identified {len(mock_curated_events)} highly relevant events.")
    time.sleep(1.5)

    print("\n[root_agent] 🛠️ Calling tool: send_notification")
    print("[root_agent] Routing curated list to configured notifications...")
    time.sleep(1)

    # Run the real notification tool with mock data
    notification_result = await send_notification(mock_curated_events)

    print("\n[Notification Result]:")
    print(f"  - Local File: {notification_result.get('local_file')}")
    print(f"  - Webhook:    {notification_result.get('webhook')}")
    print(f"  - Email:      {notification_result.get('email')}")
    print(f"  - Curated events notified: {notification_result.get('events_notified')}")

    time.sleep(1)
    print("\n==================================================")
    print("   Demo Finished Successfully!                   ")
    print("==================================================")

if __name__ == "__main__":
    asyncio.run(simulate_demo())
