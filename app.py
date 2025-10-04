import warnings
warnings.filterwarnings("ignore")
import dotenv
dotenv.load_dotenv()
import uvicorn
from fastapi import FastAPI, Request
from slack_bolt.adapter.fastapi.async_handler import AsyncSlackRequestHandler

from apis.slack import app as slack_app
from apis.log_handler import initialize_loggers
initialize_loggers()

# Initializes a FastAPI app
api = FastAPI()

# Initializes a handler for the Slack app
handler = AsyncSlackRequestHandler(slack_app)

# Endpoint for Slack events
@api.post("/slack/events")
async def endpoint(req: Request):
    return await handler.handle(req)

# Main execution block to run the app with uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "app:api",
        host="0.0.0.0",
        port=3000,
        reload=True,
    )