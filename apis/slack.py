import asyncio
import os
import logging
import json
import traceback

from slack_bolt.async_app import AsyncApp
from apis.agent_handler import call_agent_async, get_session_service, get_runner, get_restricted_runner

SLACK_BOT_TOKEN = os.environ.get('SLACK_OAUTH_TOKEN')
SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET')

# Initializes your app with your bot token and signing secret
app = AsyncApp(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

# Agent session and runner initialization
session_service = get_session_service()
full_runner = get_runner(session_service)
restricted_runner = get_restricted_runner(session_service)

# Other settings
max_text_length = 3000
logger = logging.getLogger("jm.slack.handler")


def build_blocks_from_markdown(text: str, max_length: int = 3000) -> list:
    """
    Intelligently splits markdown text into a list of Slack Block Kit sections.
    Splits by paragraph first, then by character limit if a paragraph is too long.
    """
    blocks = []
    # Split the text into paragraphs
    chunks = text.split('\n\n')
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        # If a chunk is longer than the max length, split it into sub-chunks
        if len(chunk) > max_length:
            # Find a good split point (like a newline or space) near the max_length
            # to avoid breaking mid-word.
            for i in range(0, len(chunk), max_length):
                sub_chunk = chunk[i:i + max_length]
                blocks.append({
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": sub_chunk
                    }
                })
        else:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": chunk
                }
            })
    return blocks


async def run_agent_and_respond(query, user_id, session_id, channel_id, ts, client, runner_to_use):
    """
    Runs the agent and posts a nicely formatted response to Slack.
    
    This function implements an "Intelligent Adaptive Rendering" strategy:
    1. It first tries to parse the agent's response as Block Kit JSON.
       - If successful, it validates and sends the rich blocks.
    2. If JSON parsing fails, it treats the response as Markdown.
       - It uses `build_blocks_from_markdown` to intelligently split the text
         by paragraph, creating a much more readable multi-section message.
    3. As a final safety net, any error during posting results in a simple
       plain-text error message.
    """
    await client.reactions_add(name="thinking_face", channel=channel_id, timestamp=ts)
    try:
        response = await call_agent_async(
            query=query,
            session_service=session_service,
            runner=runner_to_use, # Use the passed runner
            user_id=user_id,
            session_id=session_id,
        )
    except Exception as e:
        logger.error(traceback.format_exc())
        response = f"An error occurred during agent execution: {str(e)}"
    await client.reactions_remove(name="thinking_face", channel=channel_id, timestamp=ts)

    blocks = []
    response_text = response if isinstance(response, str) else str(response)

    try:
        # 1. Attempt to parse the response as Block Kit JSON
        json_str = response_text
        if response_text.strip().startswith("```json"):
            json_str = response_text.strip()[7:-3].strip()
        
        parsed_json = json.loads(json_str)

        if isinstance(parsed_json, dict):
            blocks = [parsed_json]  # Wrap single block object in a list
        elif isinstance(parsed_json, list):
            blocks = parsed_json  # Already a valid list of blocks
        else:
            # The parsed JSON is not a valid block structure, fall back to markdown
            raise TypeError("Parsed JSON is not a dict or list.")

    except (json.JSONDecodeError, TypeError) as e:
        # 2. If JSON parsing fails, render as intelligent Markdown blocks
        logger.warning(
            f"Failed to parse agent response as JSON (Error: {e}). "
            "Falling back to Markdown rendering."
        )
        blocks = build_blocks_from_markdown(response_text, max_text_length)

    # Fallback text for notifications is the first line of the original response
    fallback_text = response_text.split('\n')[0]

    try:
        # 3. Post the message to Slack
        await client.chat_postMessage(
            channel=channel_id,
            thread_ts=ts,
            text=fallback_text,
            blocks=blocks
        )
    except Exception as e:
        # Final safety net: if posting the blocks fails, send raw text
        logger.error(f"Failed to post formatted blocks to Slack: {traceback.format_exc()}")
        error_message = (
            f"An error occurred while posting the message to Slack: {str(e)}\n\n"
            f"*Original Agent Response:*\n"
            f"```{response_text}```"
        )
        await client.chat_postMessage(
            channel=channel_id,
            thread_ts=ts,
            text=error_message
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
            client=client,
            runner_to_use=full_runner # Use the full runner for DMs
        ))

@app.event("app_mention")
async def handle_app_mentions(body, logger, client):
    logger.debug(f"Received message event {body=}")
    event = body["event"]

    # Ignore app mentions in DMs to avoid duplicate processing,
    # as the `message` event handler already covers all DM interactions.
    channel_type = event.get("channel_type", "")
    if channel_type == "im":
        logger.debug("Ignoring app_mention in a DM channel.")
        return

    user_id = event.get("user", "anonymous")
    channel_id = event.get("channel", "UnknownChannel")
    thread_ts = event.get("thread_ts", event["ts"])
    ts = event.get("ts", "null")
    query = event.get("text", "")

    session_id = f"{channel_id}-{thread_ts}"

    # For public/private channels, always use the restricted runner
    runner_to_use = restricted_runner 

    asyncio.create_task(run_agent_and_respond(
        query=query,
        user_id=user_id,
        session_id=session_id,
        channel_id=channel_id,
        ts=ts,
        client=client,
        runner_to_use=runner_to_use
    ))