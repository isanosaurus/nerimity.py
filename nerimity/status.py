import nerimity
from nerimity._enums import GlobalClientInformation
from nerimity.logger import logger
import requests
import json

class Status():
    """
    Represents the status of the user.

    status: The current status of the user.
    activity: The current activity of the user.
    """

    def __init__(self, status: str, activity: str):
        self.status: str = status
        self.activity: str = activity
    
    class StatusType():
        """
        Represents the status type of the user.

        online: The user is online.
        looking: The user is idle.
        idle : The user is idle.
        dnd: The user is in Do Not Disturb mode.
        offline: The user is invisible.
        """
        type = int
        online = 1
        looking_to_play = 2
        idle = 3
        dnd = 4
        offline = 5
    
    # Public: Changes the status of the user.
    @staticmethod
    def change_presence(status: StatusType = None, text: str = None) -> None:
        """Changes the status of the user."""
        api_endpoint = f"{GlobalClientInformation.API_URL}/users/presence"
        headers = {
            "Authorization": GlobalClientInformation.TOKEN,
            "Content-Type": "application/json",
        }
        data = {
        }
        if status:
            data["status"] = status
        if text:
            data["custom"] = text
        
        response = requests.post(api_endpoint, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            logger.error(f"Failed to change presence. Status code: {response.status_code}. Response Text: {response.text}")
            raise requests.RequestException


        