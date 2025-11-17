from datetime import datetime

def get_current_time_string():
    """
    Returns the current time as a string in the format "YYYY-MM-DD HH:MM:SS".
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


