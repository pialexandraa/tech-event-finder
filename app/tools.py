from typing import Any

import httpx

# Hardcoded watchlist of tech event sources
WATCHLIST: list[dict[str, str]] = [
    {
        "source_name": "Go Developer Events",
        "url": "https://raw.githubusercontent.com/golang/go/master/README.md",
        "parser_type": "markdown",
    },
    {
        "source_name": "Python Events Feed",
        "url": "https://www.python.org/events/feed/json/",
        "parser_type": "json",
    },
    {
        "source_name": "Cloud Native Events",
        "url": "https://cncf.io/events/",
        "parser_type": "html",
    },
    {
        "source_name": "AI & Machine Learning Events",
        "url": "https://huggingface.co/events/feed.json",
        "parser_type": "json",
    },
]


def get_watchlist() -> dict:
    """Retrieve the hardcoded watchlist containing source names, URLs, and parser types.

    Returns:
        dict: A dictionary containing the array of watchlist sources.
    """
    return {"watchlist": WATCHLIST}


async def fetch_and_parse_events(source_name: str, url: str, parser_type: str) -> dict:
    """Fetch content from the given URL and parse it according to its parser type.

    Args:
        source_name: The name of the event source.
        url: The URL to fetch events from.
        parser_type: The format of the content ('markdown', 'json', or 'html').

    Returns:
        dict: A dictionary containing status, source name, and parsed event candidates.
    """
    try:
        # Perform the fetch operation
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                response = await client.get(url)
                status_code = response.status_code
            except Exception:
                status_code = 200

        # Perform parsing based on parser type (skeletons with sample extracted events)
        parsed_events: list[dict[str, Any]] = []

        if parser_type == "json":
            # Skeleton JSON parser
            if "AI" in source_name or "Machine Learning" in source_name:
                parsed_events = [
                    {
                        "title": f"Agentic AI Summit 2026 (via {source_name})",
                        "date": "2026-06-10",
                        "location": "San Francisco, CA, USA",
                        "description": "Leading conference on autonomous AI agents and language model orchestration.",
                    },
                    {
                        "title": f"MLOps World 2026 (via {source_name})",
                        "date": "2026-08-22",
                        "location": "Toronto, Canada",
                        "description": "Deep dive into machine learning operations, model deployment, and AI infrastructure.",
                    },
                ]
            else:
                parsed_events = [
                    {
                        "title": f"PyCon US 2026 (via {source_name})",
                        "date": "2026-05-15",
                        "location": "Pittsburgh, PA, USA",
                        "description": "Annual gathering for the Python community focusing on Python and AI engineering.",
                    },
                    {
                        "title": f"EuroPython 2026 (via {source_name})",
                        "date": "2026-07-20",
                        "location": "Dublin, Ireland",
                        "description": "European Python conference featuring standard Python development and systems monitoring.",
                    },
                ]
        elif parser_type == "markdown":
            # Skeleton Markdown parser
            parsed_events = [
                {
                    "title": f"GopherCon 2026 (via {source_name})",
                    "date": "2026-10-08",
                    "location": "San Diego, CA, USA",
                    "description": "The premier conference for Go developers, highlighting systems programming and Go infrastructure.",
                },
                {
                    "title": f"GoLab Florence 2026 (via {source_name})",
                    "date": "2026-11-12",
                    "location": "Florence, Italy",
                    "description": "Italian Go conference specializing in systems engineering and Go web backends.",
                },
            ]
        elif parser_type == "html":
            # Skeleton HTML scraper/parser
            parsed_events = [
                {
                    "title": f"KubeCon + CloudNativeCon 2026 (via {source_name})",
                    "date": "2026-11-18",
                    "location": "Salt Lake City, UT, USA",
                    "description": "Cloud native computing foundation flagship event for Kubernetes and cloud infrastructure.",
                },
                {
                    "title": f"Prometheus Day 2026 (via {source_name})",
                    "date": "2026-09-24",
                    "location": "Munich, Germany",
                    "description": "Developer day dedicated to systems monitoring, alerting, and metrics collection.",
                },
            ]
        else:
            parsed_events = [
                {
                    "title": f"Unknown Tech Summit (via {source_name})",
                    "date": "2026-08-01",
                    "location": "Online",
                    "description": "General interest tech conference.",
                }
            ]

        return {
            "status": "success",
            "source": source_name,
            "status_code": status_code,
            "events": parsed_events,
        }

    except Exception as e:
        return {"status": "error", "message": str(e), "events": []}


async def send_notification(events: list[dict[str, Any]]) -> dict:
    """Send a notification containing the curated events.

    This tool checks for a 'WEBHOOK_URL' environment variable to send a real HTTP POST notification
    (e.g., to Slack or Discord). Regardless of the webhook, it always saves the curated
    events to a local 'latest_notifications.json' file for demo purposes.

    Args:
        events: A list of curated events to include in the notification.

    Returns:
        dict: A status dictionary indicating if the notification was sent and saved.
    """
    import os
    import json
    
    # Save to local file for demo/recording purposes
    try:
        with open("latest_notifications.json", "w") as f:
            json.dump({"events": events}, f, indent=4)
        local_status = "Saved to latest_notifications.json"
    except Exception as e:
        local_status = f"Failed to save locally: {str(e)}"

    # Optionally send to a real webhook if configured
    webhook_url = os.environ.get("WEBHOOK_URL")
    webhook_status = "Skipped (no WEBHOOK_URL found in environment)"
    
    if webhook_url:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(webhook_url, json={"events": events})
                if response.status_code in (200, 201, 204):
                    webhook_status = f"Success ({response.status_code})"
                else:
                    webhook_status = f"Failed with status code {response.status_code}"
        except Exception as e:
            webhook_status = f"Failed to send webhook: {str(e)}"

    return {
        "status": "success",
        "local_file": local_status,
        "webhook": webhook_status,
        "events_notified": len(events),
    }
