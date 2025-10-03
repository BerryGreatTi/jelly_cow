import os
import logging

from google.adk.sessions import InMemorySessionService, DatabaseSessionService
from google.genai import types # For creating message Content/Parts


logger = logging.getLogger("jm.app.agent_handler")

def get_session_service():
    is_agent_session_db = os.environ.get("IS_AGENT_SESSION_DB", 0)
    db_path = os.environ.get("AGENT_SESSION_DB_PATH", "db/agent_session.db")
    logger.debug(f"$IS_AGENT_SESSION_DB={is_agent_session_db}, $AGENT_SESSION_DB_PATH='{db_path}'")
    
    if is_agent_session_db == 1:
        os.mkdir(os.path.dirname(db_path), exist_ok=True)
        logger.info(f"Initializing database session service with '{db_path}'")
        return DatabaseSessionService(db_url=f"sqlite:///./{db_path}")
    
    else:
        logger.info("Initializing in-memory session service")
        return InMemorySessionService()
    

async def call_agent_async(query: str, runner, user_id, session_id):
    """Sends a query to the agent and prints the final response."""
    logger.debug(f"User Query: {query}")

    # Prepare the user's message in ADK format
    content = types.Content(role='user', parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response." # Default

    # Key Concept: run_async executes the agent logic and yields Events.
    # We iterate through events to find the final answer.
    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        # You can uncomment the line below to see *all* events during execution
        # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

        # Key Concept: is_final_response() marks the concluding message for the turn.
        if event.is_final_response():
            if event.content and event.content.parts:
                # Assuming text response in the first part
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate: # Handle potential errors/escalations
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            # Add more checks here if needed (e.g., specific error codes)
            break # Stop processing events once the final response is found

    logger.debug(f"Agent Response: {final_response_text}")