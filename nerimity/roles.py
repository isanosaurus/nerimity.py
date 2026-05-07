from nerimity._enums import GlobalClientInformation
from nerimity.logger import logger
import aiohttp
import requests
import json

class Role():
    """
    Represents a role in Nerimity.

    id: Snowflake ID of the role.
    name: The name of the role.
    hex_color: The hex color of the role.
    creator_id: Snowflake ID of the creator of the role.
    server_id: Snowflake ID of the server the role is in.
    order: The order of the role.
    hide_role: Whether the role is hidden or not.
    bot_role: Whether the role is a bot role or not.
    created_at: The timestamp of when the role was created.
    default_role: Whether the role is the default role or not.

    update_role(): Updates itself with the specified information.

    deserialize(json): static | Deserialize a json string to a Role object.
    """

    def __init__(self) -> None:
        self.id             : int          = None
        self.name           : str          = None
        self.hex_color      : str          = None
        self.creator_id     : int          = None
        self.server_id      : int          = None
        self.order          : int          = None
        self.hide_role      : bool         = None
        self.bot_role       : bool         = None
        self.created_at     : float        = None
        self.default_role   : bool         = None

    # Public: Updates itself with the specified information.
    def update_role(self, name: str=None, hex_color: str=None, hide_role: bool=None) -> 'Role':
        """Updates itself with the specified information."""
        
        api_endpoint = f"{GlobalClientInformation.API_URL}/servers/{self.server_id}/roles/{self.id}"

        headers = {
            "Authorization": GlobalClientInformation.TOKEN,
            "Content-Type": "application/json",
        }
        data = {
            "name": name,
            "hexColor": hex_color,
            "hideRole": hide_role,
        }

        response = requests.post(api_endpoint, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            logger.error(f"Failed to update a role for {self}. Status code: {response.status_code}. Response Text: {response.text}")
            raise requests.RequestException
        response_json = response.json()
        response_json["id"] = self.id
        response_json["serverId"] = self.server_id
        response_json["createdById"] = self.creator_id
        response_json["order"] = self.order
        response_json["botRole"] = self.bot_role
        response_json["createdAt"] = self.created_at

        if not hex_color: response_json["hexColor"] = self.hex_color
        if not name: response_json["name"] = self.name
        if not hide_role: response_json["hideRole"] = self.hide_role


        return Role.deserialize(response_json)
    
    async def set_permissions(self, permission_integer: int) -> 'Role':
        api_endpoint = f"{GlobalClientInformation.API_URL}/servers/{self.server_id}/roles/{self.id}"

        headers = {
            "Authorization": GlobalClientInformation.TOKEN,
            "Content-Type": "application/json",
        }
        data = {
            "permissions": permission_integer,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(api_endpoint, headers=headers, data=json.dumps(data)) as response:
                if response.status != 200:
                    logger.error(f"Failed to set permissions for {self}. Status code: {response.status}. Response Text: {await response.text()}")
                    raise requests.RequestException
                
                response_json = await response.json()
                response_json["id"] = self.id
                response_json["serverId"] = self.server_id
                response_json["createdById"] = self.creator_id
                response_json["order"] = self.order
                response_json["botRole"] = self.bot_role
                response_json["createdAt"] = self.created_at
                response_json["hexColor"] = self.hex_color
                response_json["name"] = self.name
                response_json["hideRole"] = self.hide_role

                return Role.deserialize(response_json)

    # Public Static: Deserialize a json string to a Role object.
    @staticmethod
    def deserialize(json: dict) -> 'Role':
        """static | Deserialize a json string to a Role object."""

        new_role = Role()
        new_role.id          = int(json["id"])
        new_role.name        = str(json["name"])
        new_role.hex_color   = str(json["hexColor"])
        new_role.creator_id  = int(json["createdById"])
        new_role.server_id   = int(json["serverId"])
        new_role.order       = int(json["order"])
        new_role.hide_role   = bool(json["hideRole"])
        new_role.bot_role    = bool(json["botRole"])        if json["botRole"]     is not None else False
        new_role.created_at  = float(json["createdAt"])

        return new_role