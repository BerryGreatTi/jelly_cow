import os
import logging

from google.adk.sessions import InMemorySessionService, DatabaseSessionService
from google.genai import types # For creating message Content/Parts
from google.adk.runners import Runner

from agents.root_agent import agent as root_agent


logger = logging.getLogger("jm.agent.handler")
APP_NAME = "JellyMonster"


def get_session_service():
    is_agent_session_db = int(os.environ.get("IS_AGENT_SESSION_DB", 0))
    db_path = os.environ.get("AGENT_SESSION_DB_PATH", "db/agent_session.db")
    logger.debug(f"$IS_AGENT_SESSION_DB={is_agent_session_db}, $AGENT_SESSION_DB_PATH='{db_path}'")
    
    if is_agent_session_db == 1:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        logger.info(f"Initializing database session service with '{db_path}'")
        return DatabaseSessionService(db_url=f"sqlite:///./{db_path}")
    
    else:
        logger.info("Initializing in-memory session service")
        return InMemorySessionService()
    

def get_runner(session_service):
    return Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)


async def call_agent_async(query: str, session_service, runner, user_id, session_id):
    """Sends a query to the agent and prints the final response."""
    logger.debug(f"User Query: {query}")

    # 에이전트 세션 생성
    try: 
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id
        )
        logger.debug(f"{session_id=} created")
    except:
        logger.debug(f"{session_id=} loaded")

    # Prepare the user's message in ADK format
    content = types.Content(role='user', parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response." # Default

    async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            break

    logger.debug(f"Agent Response: {final_response_text}")
    return final_response_text
