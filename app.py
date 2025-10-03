import os

import dotenv
dotenv.load_dotenv()

from apis.agent_handler import get_session_service


if __name__ == '__main__':
    session_service = get_session_service()