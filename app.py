import warnings
warnings.filterwarnings("ignore")
import dotenv
dotenv.load_dotenv()
import asyncio
import os
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

from apis.log_handler import initialize_loggers
initialize_loggers()
from apis.slack import app as slack_app

async def main():
    # Initializes a handler for the Slack app
    handler = AsyncSocketModeHandler(slack_app, os.environ.get("SLACK_APP_TOKEN"))
    await handler.start_async()

# Main execution block to run the app with socket mode
if __name__ == "__main__":
    asyncio.run(main())