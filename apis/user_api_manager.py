import os
import json
import logging
from apis.koreainvestment import KoreaInvestmentAPI

logger = logging.getLogger("jm.user_api_manager")

class UserApiHandler:
    """
    Manages KoreaInvestmentAPI instances on a per-user basis to optimize
    access token usage.
    """
    def __init__(self):
        self._instances = {}
        logger.info("UserApiHandler initialized.")

    def get_api_for_user(self, user_id: str):
        """
        Retrieves a valid KoreaInvestmentAPI instance for a given user.
        It caches instances and reuses them until their access token expires.

        Args:
            user_id: The Slack user ID.

        Returns:
            An instance of KoreaInvestmentAPI if the profile exists, otherwise None.
        """
        profile_path = f"profiles/{user_id}.json"
        if not os.path.exists(profile_path):
            logger.error(f"Profile not found for user '{user_id}' at '{profile_path}'")
            return None

        # Check for a cached and valid instance
        if user_id in self._instances and self._instances[user_id].is_access_token_valid():
            logger.info(f"Returning cached API instance for user '{user_id}'.")
            return self._instances[user_id]

        # Create a new instance if none exists or the token is invalid
        logger.info(f"Creating new API instance for user '{user_id}'.")
        api_instance = KoreaInvestmentAPI(profile_path)
        self._instances[user_id] = api_instance
        return api_instance

class UserNotionHandler:
    """
    Manages Notion API configurations on a per-user basis.
    """
    def __init__(self):
        logger.info("UserNotionHandler initialized.")
    
    def get_notion_config_for_user(self, user_id: str):
        """
        Retrieves Notion configuration for a given user from their profile.

        Args:
            user_id: The Slack user ID.

        Returns:
            A tuple (api_key, database_id) if the profile and config exist, otherwise None.
        """
        profile_path = f"profiles/{user_id}.json"
        if not os.path.exists(profile_path):
            logger.error(f"Profile not found for user '{user_id}' at '{profile_path}'")
            return None, None
            
        with open(profile_path, 'r') as f:
            profile = json.load(f)
        
        api_key = profile.get("notion_api_key")
        database_id = profile.get("notion_database_id")

        if not api_key or not database_id:
            logger.error(f"Notion configuration not found or incomplete for user '{user_id}'.")
            return None, None
        
        logger.info(f"Loaded Notion config for user '{user_id}'.")
        return api_key, database_id

    def get_public_notion_config(self):
        """
        Retrieves the public Notion configuration from environment variables.

        Returns:
            A tuple (api_key, database_id).
        """
        api_key = os.getenv("NOTION_API_KEY")
        database_id = os.getenv("NOTION_DATABASE_ID")
        
        if not api_key or not database_id:
            logger.error("Public Notion configuration (NOTION_API_KEY, NOTION_DATABASE_ID) not found in environment variables.")
            return None, None
            
        logger.info("Loaded public Notion config from environment variables.")
        return api_key, database_id

# Global instances
user_api_handler = UserApiHandler()
user_notion_handler = UserNotionHandler()
