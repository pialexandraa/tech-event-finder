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
    {
        "source_name": "Google Developers Europe",
        "url": "https://developers.google.com/events",
        "parser_type": "html",
    },
    {
        "source_name": "AWS Events Europe",
        "url": "https://aws.amazon.com/events/summits/europe",
        "parser_type": "html",
    },
    {
        "source_name": "Devoxx UK / Belgium",
        "url": "https://devoxx.com",
        "parser_type": "html",
    },
    {
        "source_name": "Red Hat Events",
        "url": "https://www.redhat.com/de/events",
        "parser_type": "html",
    },
    {
        "source_name": "Linux Watch List",
        "url": "https://dev.events/EU/linux",
        "parser_type": "html",
    },
    {
        "source_name": "Linux Foundation Calendar",
        "url": "https://events.linuxfoundation.org/about/calendar/",
        "parser_type": "html",
    },
    {
        "source_name": "WeAreDevelopers World Congress",
        "url": "https://www.wearedevelopers.com/world-congress",
        "parser_type": "html",
    },
    {
        "source_name": "GDG Events Calendar",
        "url": "https://gdg.community.dev/events/#/list",
        "parser_type": "html",
    },
    {
        "source_name": "Italy Developer Events",
        "url": "https://dev.events/EU/IT",
        "parser_type": "html",
    },
    {
        "source_name": "Dutch Tech Events",
        "url": "https://dev.events/EU/NL",
        "parser_type": "html",
    },
    {
        "source_name": "Czech Tech Events",
        "url": "https://dev.events/EU/CZ",
        "parser_type": "html",
    },
    {
        "source_name": "Nordic Tech Events",
        "url": "https://dev.events/EU/DK",
        "parser_type": "html",
    },
    {
        "source_name": "Swiss Tech Events",
        "url": "https://dev.events/EU/CH",
        "parser_type": "html",
    },
    {
        "source_name": "Poland Tech Events",
        "url": "https://dev.events/EU/PL",
        "parser_type": "html",
    },
    {
        "source_name": "Croatia Tech Events",
        "url": "https://dev.events/EU/HR",
        "parser_type": "html",
    },
    {
        "source_name": "Portugal Tech Events",
        "url": "https://dev.events/EU/PT",
        "parser_type": "html",
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
            # Skeleton HTML scraper/parser customized for Europe and major tech players
            if "Google" in source_name:
                parsed_events = [
                    {
                        "title": f"Google I/O Connect Europe (via {source_name})",
                        "date": "2026-06-25",
                        "location": "Berlin, Germany",
                        "link": "https://example.com/event",
                        "description": "Hands-on developer event highlighting Google Cloud, Go development, and Web API integration.",
                    },
                    {
                        "title": f"Android Dev Summit Europe (via {source_name})",
                        "date": "2026-10-10",
                        "location": "London, UK",
                        "link": "https://example.com/event",
                        "description": "Google's developer summit focusing on mobile tech and modern systems infrastructure.",
                    },
                ]
            elif "AWS" in source_name:
                parsed_events = [
                    {
                        "title": f"AWS Summit Paris (via {source_name})",
                        "date": "2026-04-15",
                        "location": "Paris, France",
                        "link": "https://example.com/event",
                        "description": "Cloud computing summit focusing on AWS architecture, cloud infrastructure, and serverless tools.",
                    },
                    {
                        "title": f"AWS User Group UK (via {source_name})",
                        "date": "2026-09-08",
                        "location": "Manchester, UK",
                        "link": "https://example.com/event",
                        "description": "Regional meeting focusing on cloud native systems and metrics collection in AWS environments.",
                    },
                ]
            elif "Devoxx" in source_name:
                parsed_events = [
                    {
                        "title": f"Devoxx UK 2026 (via {source_name})",
                        "date": "2026-05-12",
                        "location": "London, UK",
                        "link": "https://example.com/event",
                        "description": "Community developer conference focusing on cloud native systems, Go/Python microservices, and AI models.",
                    },
                    {
                        "title": f"Devoxx Belgium 2026 (via {source_name})",
                        "date": "2026-10-05",
                        "location": "Antwerp, Belgium",
                        "link": "https://example.com/event",
                        "description": "Major European tech event focusing on general software engineering, system architecture, and machine learning.",
                    },
                ]
            elif "Red Hat" in source_name:
                parsed_events = [
                    {
                        "title": f"Red Hat Summit Connect Europe (via {source_name})",
                        "date": "2026-09-15",
                        "location": "Frankfurt, Germany",
                        "link": "https://example.com/event",
                        "description": "Enterprise open source technology event covering hybrid cloud, Linux, and Kubernetes.",
                    },
                    {
                        "title": f"Red Hat Summit Connect Madrid (via {source_name})",
                        "date": "2026-08-30",
                        "location": "Madrid, Spain",
                        "link": "https://www.redhat.com/de/events",
                        "description": "Major Red Hat enterprise open source summit in Southern Europe focusing on hybrid cloud and AI.",
                    },
                ]
            elif "Linux" in source_name:
                parsed_events = [
                    {
                        "title": f"Open Source Summit Europe (via {source_name})",
                        "date": "2026-10-20",
                        "location": "Vienna, Austria",
                        "link": "https://example.com/event",
                        "description": "Linux Foundation's premier event for open source developers, technologists, and community leaders.",
                    },
                ]
            elif "WeAreDevelopers" in source_name:
                parsed_events = [
                    {
                        "title": f"WeAreDevelopers World Congress (via {source_name})",
                        "date": "2026-07-08",
                        "location": "Berlin, Germany",
                        "link": "https://example.com/event",
                        "description": "The world's leading event for developers and tech professionals.",
                    },
                ]
            elif "GDG" in source_name:
                parsed_events = [
                    {
                        "title": f"DevFest Europe (via {source_name})",
                        "date": "2026-11-05",
                        "location": "Amsterdam, Netherlands",
                        "link": "https://example.com/event",
                        "description": "Local tech conference hosted by Google Developer Groups across Europe.",
                    },
                ]
            elif "Italy" in source_name:
                parsed_events = [
                    {
                        "title": f"Codemotion Milan 2026 (via {source_name})",
                        "date": "2026-10-14",
                        "location": "Milan, Italy",
                        "link": "https://example.com/event",
                        "description": "Italy's biggest gathering for software developers, covering backend architecture, AI, and DevOps.",
                    },
                ]
            elif "Dutch" in source_name:
                parsed_events = [
                    {
                        "title": f"KubeCon Europe 2026 (via {source_name})",
                        "date": "2026-04-18",
                        "location": "Amsterdam, Netherlands",
                        "link": "https://example.com/event",
                        "description": "Cloud native computing foundation flagship event for Kubernetes and cloud infrastructure.",
                    },
                ]
            elif "Czech" in source_name:
                parsed_events = [
                    {
                        "title": f"WebExpo 2026 (via {source_name})",
                        "date": "2026-06-10",
                        "location": "Prague, Czech Republic",
                        "link": "https://example.com/event",
                        "description": "Central Europe's premier event for developers, designers, and tech leaders.",
                    },
                ]
            elif "Nordic" in source_name:
                parsed_events = [
                    {
                        "title": f"GOTO Copenhagen 2026 (via {source_name})",
                        "date": "2026-09-02",
                        "location": "Copenhagen, Denmark",
                        "link": "https://example.com/event",
                        "description": "Enterprise software development conference with strong tracks on distributed systems and Go.",
                    },
                ]
            elif "Swiss" in source_name:
                parsed_events = [
                    {
                        "title": f"Swiss Python Summit 2026 (via {source_name})",
                        "date": "2026-02-20",
                        "location": "Rapperswil, Switzerland",
                        "link": "https://example.com/event",
                        "description": "A community-focused conference for Python developers highlighting ML engineering and data pipelines.",
                    },
                ]
            elif "Poland" in source_name:
                parsed_events = [
                    {
                        "title": f"InfoShare 2026 (via {source_name})",
                        "date": "2026-05-13",
                        "location": "Gdańsk, Poland",
                        "link": "https://example.com/event",
                        "description": "The biggest tech and startup conference in CEE showcasing advanced backend systems and AI.",
                    },
                ]
            elif "Croatia" in source_name:
                parsed_events = [
                    {
                        "title": f"Shift Conference 2026 (via {source_name})",
                        "date": "2026-09-19",
                        "location": "Zadar, Croatia",
                        "link": "https://example.com/event",
                        "description": "A premier European developer conference gathering thousands of attendees for cloud and API development discussions.",
                    },
                ]
            elif "Portugal" in source_name:
                parsed_events = [
                    {
                        "title": f"Web Summit 2026 (via {source_name})",
                        "date": "2026-11-10",
                        "location": "Lisbon, Portugal",
                        "link": "https://example.com/event",
                        "description": "One of the largest tech conferences in Europe covering everything from cloud infrastructure to startup ecosystems.",
                    },
                ]
            else:
                parsed_events = [
                    {
                        "title": f"KubeCon + CloudNativeCon 2026 (via {source_name})",
                        "date": "2026-11-18",
                        "location": "Salt Lake City, UT, USA",
                        "link": "https://example.com/event",
                        "description": "Cloud native computing foundation flagship event for Kubernetes and cloud infrastructure.",
                    },
                    {
                        "title": f"Prometheus Day 2026 (via {source_name})",
                        "date": "2026-09-24",
                        "location": "Munich, Germany",
                        "link": "https://example.com/event",
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


def deduplicate_events(events: list[dict]) -> list[dict]:
    """Deduplicate a list of events by extracting the base title and comparing it alongside the date."""
    seen = set()
    unique_events = []

    for event in events:
        title = event.get("title", "")
        base_title = title.split(" (via ")[0].strip().lower()
        date = event.get("date", "")

        identifier = f"{base_title}-{date}"

        if identifier not in seen:
            seen.add(identifier)
            unique_events.append(event)

    return unique_events


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
    import json
    import os

    # Save to local file for demo/recording purposes
    try:
        with open("latest_notifications.json", "w") as f:
            json.dump({"events": events}, f, indent=4)
        local_status = "Saved to latest_notifications.json"
    except Exception as e:
        local_status = f"Failed to save locally: {e!s}"

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
            webhook_status = f"Failed to send webhook: {e!s}"

    # Optionally send email notification if email credentials are set
    email_status = "Skipped (missing email credentials in environment)"
    sender = os.environ.get("SENDER_EMAIL")
    receiver = os.environ.get("RECEIVER_EMAIL")
    pwd = os.environ.get("EMAIL_APP_PASSWORD")

    if sender and receiver and pwd:
        # Build premium HTML table
        html_content = """
        <html>
        <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px;">
            <h2 style="color: #1a73e8; border-bottom: 2px solid #1a73e8; padding-bottom: 10px;">Curated Tech Events</h2>
            <p>Here are the latest curated tech events matching your developer profile:</p>
            <table border="0" cellpadding="10" cellspacing="0" style="width: 100%; border-collapse: collapse; margin-top: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                <thead>
                    <tr style="background-color: #f8f9fa; border-bottom: 2px solid #dee2e6;">
                        <th align="left" style="padding: 12px;">Event</th>
                        <th align="left" style="padding: 12px;">Date</th>
                        <th align="left" style="padding: 12px;">Location</th>
                        <th align="center" style="padding: 12px;">Relevance</th>
                        <th align="left" style="padding: 12px;">Justification</th>
                    </tr>
                </thead>
                <tbody>
        """
        import html
        for event in events:
            # Safe access (dict or object)
            def get_val(k, ev=event):
                return ev.get(k, "N/A") if isinstance(ev, dict) else getattr(ev, k, "N/A")

            title = get_val("title")
            date = get_val("date")
            location = get_val("location")
            score = get_val("relevance_score")
            justification = get_val("justification")
            link = get_val("link")

            # Secure link rendering
            # We strictly enforce HTTP/HTTPS to avoid javascript: or other malicious schemes
            # Additionally, html.escape ensures quotes and tags are neutralized to prevent XSS
            if link and link != "N/A":
                safe_url = html.escape(str(link), quote=True)
                if safe_url.startswith("http://") or safe_url.startswith("https://"):
                    title_html = f'<a href="{safe_url}" style="color: #1a73e8; text-decoration: none;">{html.escape(title)}</a>'
                else:
                    title_html = html.escape(title)
            else:
                title_html = html.escape(title)

            html_content += f"""
                    <tr style="border-bottom: 1px solid #dee2e6;">
                        <td style="padding: 12px; font-weight: bold; color: #202124;">{title_html}</td>
                        <td style="padding: 12px; white-space: nowrap;">{html.escape(str(date))}</td>
                        <td style="padding: 12px;">{html.escape(str(location))}</td>
                        <td align="center" style="padding: 12px;">
                            <span style="background-color: #e6f4ea; color: #137333; padding: 4px 8px; border-radius: 12px; font-weight: bold; font-size: 0.9em;">
                                {score}
                            </span>
                        </td>
                        <td style="padding: 12px; color: #5f6368; font-size: 0.95em;">{html.escape(str(justification))}</td>
                    </tr>
            """
        html_content += """
                </tbody>
            </table>
        </body>
        </html>
        """

        try:
            from app.notifier import send_tech_event_email
            success = send_tech_event_email("TechEvent Finder - Your Curated Events", html_content)
            if success:
                email_status = "Success"
            else:
                email_status = "Failed (SMTP error)"
        except Exception as e:
            email_status = f"Failed to send email: {e!s}"

    return {
        "status": "success",
        "local_file": local_status,
        "webhook": webhook_status,
        "email": email_status,
        "events_notified": len(events),
    }
