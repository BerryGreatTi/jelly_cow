import asyncio
import os
import logging
import json
import traceback

from slack_bolt.async_app import AsyncApp
from apis.agent_handler import call_agent_async, get_session_service, get_runner

SLACK_BOT_TOKEN = os.environ.get('SLACK_OAUTH_TOKEN')
SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET')

# Initializes your app with your bot token and signing secret
app = AsyncApp(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

# Agent session and runner initialization
session_service = get_session_service()
runner = get_runner(session_service)

# Other settings
max_text_length = 3000
logger = logging.getLogger("jm.slack.handler")

async def run_agent_and_respond(query, user_id, session_id, channel_id, ts, client):
    await client.reactions_add(name="thinking_face", channel=channel_id, timestamp=ts)
    try:
        response = await call_agent_async(
            query=query,
            session_service=session_service,
            runner=runner,
            user_id=user_id,
            session_id=session_id,
        )
    except Exception as e:
        logger.error(traceback.format_exc())
        response = f"An error occurred: {str(e)}"
    await client.reactions_remove(name="thinking_face", channel=channel_id, timestamp=ts)

    blocks = []
    try:
        # Check if the response is a JSON block
        if response.strip().startswith("```json"):
            # Extract JSON content from the markdown block
            json_str = response.strip()[7:-3].strip()
            blocks = json.loads(json_str)
        else:
            # Try to load the response as a plain JSON
            blocks = json.loads(response)
    except (json.JSONDecodeError, TypeError):
        # If it's not a valid JSON, treat it as plain text and chunk it.
        response_text = response if isinstance(response, str) else str(response)
        for i in range(0, len(response_text), max_text_length):
            chunk = response_text[i:i + max_text_length]
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": chunk
                }
            })

    # Fallback text for notifications
    fallback_text = response.split('\n')[0] if isinstance(response, str) else "Agent response"

    await client.chat_postMessage(
        channel=channel_id,
        thread_ts=ts,
        text=fallback_text,
        blocks=blocks
    )

@app.event("message")
async def handle_message_events(body, logger, client):
    logger.debug(f"Received message event {body=}")
    # Handle direct messages
    event = body["event"]
    if event.get("channel_type", "") == "im":
        user_id = event.get("user", "anonymous")
        channel_id = event.get("channel", "im")
        thread_ts = event.get("thread_ts", event["ts"])
        ts = event.get("ts", "null")
        query = event.get("text", "")

        session_id = f"{user_id}-{channel_id}-{thread_ts}"

        asyncio.create_task(run_agent_and_respond(
            query=query,
            user_id=user_id,
            session_id=session_id,
            channel_id=channel_id,
            ts=ts,
            client=client
        ))

@app.event("app_mention")
async def handle_app_mentions(body, logger, client):
    logger.debug(f"Received message event {body=}")
    event = body["event"]
    user_id = event.get("user", "anonymous")
    channel_id = event.get("channel", "UnknownChannel")
    thread_ts = event.get("thread_ts", event["ts"])
    ts = event.get("ts", "null")
    query = event.get("text", "")

    session_id = f"{user_id}-{channel_id}-{thread_ts}"

    asyncio.create_task(run_agent_and_respond(
        query=query,
        user_id=user_id,
        session_id=session_id,
        channel_id=channel_id,
        ts=ts,
        client=client
    ))