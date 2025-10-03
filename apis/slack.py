import asyncio
import os
import logging

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
max_text_length = 1000
logger = logging.getLogger("jm.slack.handler")

async def run_agent_and_respond(query, user_id, session_id, channel_id, thread_ts, client):
    await client.reactions_add(name="thinking_face", channel=channel_id, timestamp=thread_ts)
    try:
        response = await call_agent_async(
            query=query,
            session_service=session_service,
            runner=runner,
            user_id=user_id,
            session_id=session_id,
        )
    except Exception as e:
        response = f"An error occurred: {str(e)}"
    await client.reactions_remove(name="thinking_face", channel=channel_id, timestamp=thread_ts)

    blocks = []
    for i in range(0, len(response), max_text_length):
        chunk = response[i:i + max_text_length]
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": chunk
            }
        })

    await client.chat_postMessage(
        channel=channel_id,
        thread_ts=thread_ts,
        text=response.split('\n')[0],  # Use first line as fallback
        blocks=blocks
    )

@app.event("message")
async def handle_message_events(body, logger, client):
    logger.debug(f"Received message event {body=}")
    # Handle direct messages
    if body["event"]["channel_type"] == "im":
        user_id = body["event"]["user"]
        channel_id = body["event"]["channel"]
        thread_ts = body["event"]["ts"]
        query = body["event"]["text"]

        session_id = f"{user_id}-{channel_id}-{thread_ts}"

        asyncio.create_task(run_agent_and_respond(
            query=query,
            user_id=user_id,
            session_id=session_id,
            channel_id=channel_id,
            thread_ts=thread_ts,
            client=client
        ))

@app.event("app_mention")
async def handle_app_mentions(body, logger, client):
    logger.debug(f"Received message event {body=}")
    user_id = body["event"]["user"]
    channel_id = body["event"]["channel"]
    thread_ts = body["event"]["ts"]
    query = body["event"]["text"]

    session_id = f"{user_id}-{channel_id}-{thread_ts}"

    asyncio.create_task(run_agent_and_respond(
        query=query,
        user_id=user_id,
        session_id=session_id,
        channel_id=channel_id,
        thread_ts=thread_ts,
        client=client
    ))