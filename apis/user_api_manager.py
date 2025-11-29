import os
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

# Global instance of the UserApiHandler
user_api_handler = UserApiHandler()
