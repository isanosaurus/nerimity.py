import aiohttp
import asyncio
import json
from nerimity.message import Message
from nerimity.attachment import Attachment
from nerimity.embed import Embed
from nerimity._enums import GlobalClientInformation, ConsoleShortcuts
from nerimity.button import Button
from nerimity.roles import Role

class Channel():
    """
    Represents a channel in Nerimity.

    id: Snowflake ID of the channel
    name: Name of the channel.
    type: Type of the channel
    creator_id: ID of the creator of the channel.
    server_id: ID of the server the channel is in.
    category_id: ID of the category the channel is in.
    last_messaged_at: Timestamp from when the last message was send.
    created_at: Timestamp from when the channel was created.
    order: Priority of the channel in its category.
    
    update_channel(): Updates itself with specified information.
    send_message(): Sends a message to the channel.
    get_messages(): Gets a list of up to 50 message from the channel.

    deserialize(json): static | Deserialize a json string to a Channel object.
    """

    def __init__(self) -> None:
        self.id               : int             = None
        self.name             : str             = None
        self.type             : int             = None
        self.creator_id       : int             = None
        self.server_id        : int             = None
        self.category_id      : int             = None
        self.last_messaged_at : float | None    = None
        self.created_at       : float           = None
        self.order            : int | None      = None
    
    # Public: Updates itself with specified information.
    async def update_channel(self, server_id: int, name: str=None, icon: str=None, content: str=None) -> 'Channel':
        """Updates itself with specified information."""

        api_endpoint = f"{GlobalClientInformation.API_URL}/servers/{server_id}/channels/{self.id}"

        headers = {
            "Authorization": GlobalClientInformation.TOKEN,
            "Content-Type": "application/json",
        }
        data = {
            "name": name,
            "icon": icon,
        }

        if icon is None:
            del data["icon"]

        async with aiohttp.ClientSession() as session:
            async with session.post(api_endpoint, headers=headers, json=data) as response:
                if response.status != 200:
                    print(f"{ConsoleShortcuts.error()} Failed to update a channel for {self}. Status code: {response.status}. Response Text: {await response.text()}")
                    raise aiohttp.ClientResponseError(response.request_info, response.history)

            if content is not None:
                api_endpoint = f"{GlobalClientInformation.API_URL}/servers/{server_id}/channels/{self.id}/notice"

                if content == "":
                    async with session.delete(api_endpoint, headers=headers) as response:
                        if response.status != 200:
                            print(f"{ConsoleShortcuts.error()} Failed to update a channel for {self}. Status code: {response.status}. Response Text: {await response.text()}")
                            raise aiohttp.ClientResponseError(response.request_info, response.history)
                        return Channel.deserialize(await response.json())
                else:
                    async with session.put(api_endpoint, headers=headers, json={"content": content}) as response:
                        if response.status != 200:
                            print(f"{ConsoleShortcuts.error()} Failed to update a channel for {self}. Status code: {response.status}. Response Text: {await response.text()}")
                            raise aiohttp.ClientResponseError(response.request_info, response.history)
                        return Channel.deserialize(await response.json())

    # Public: Sends a message to the channel.
    async def send_message(self, message_content: str, attachment: Attachment | None = None, buttons: list[Button] | None = None, embed: Embed | None = None) -> Message:
        """Sends a message to the channel."""
        
        api_endpoint = f"{GlobalClientInformation.API_URL}/channels/{self.id}/messages"
        headers = {
            "Authorization": GlobalClientInformation.TOKEN,
            "Content-Type": "application/json",
        }
        data = {
            "content": message_content,
            "buttons": []
        }

        if embed is not None:
            data.update(embed.to_payload())

        if buttons is not None:
            for button in buttons:
                data["buttons"].append({
                    "label": str(button.label),
                    "id": str(button.id),
                    "alert": button.alert
                })
                GlobalClientInformation.BUTTONS.append(button)
                

        async with aiohttp.ClientSession() as session:
            if attachment is not None:
                async with session.post(f"{GlobalClientInformation.CDN_URL}/attachments/{str(self.id)}/{attachment.file_id}") as response:
                    if response.status != 200:
                        print(f"{ConsoleShortcuts.error()} Failed to send attachment to {self}. Status code: {response.status}. Response Text: {await response.text()}")
                        raise aiohttp.ClientResponseError(response.request_info, response.history)
                    data["nerimityCdnFileId"] = (await response.json()).get("fileId")

            async with session.post(api_endpoint, headers=headers, json=data) as response:
                if response.status != 200:
                    print(f"{ConsoleShortcuts.error()} Failed to send message to {self}. Status code: {response.status}. Response Text: {await response.text()}")
                    raise aiohttp.ClientResponseError(response.request_info, response.history)
                message_data = await response.json()
                return Message.deserialize(message_data)

    # Private: Gets a raw string of messages.
    async def _get_messages_raw(self, amount: int) -> str:
        if amount > 50:
            amount = 50
        elif amount < 1:
            raise ValueError("Amount of requested messages must be positive.")

        api_endpoint = f"{GlobalClientInformation.API_URL}/channels/{self.id}/messages?limit={amount}"

        headers = {
            "Authorization": GlobalClientInformation.TOKEN,
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(api_endpoint, headers=headers) as response:
                if response.status != 200:
                    print(f"Failed to get messages from {self}. Status code: {response.status}. Response Text: {await response.text()}")
                    raise aiohttp.ClientResponseError(response.request_info, response.history)
                
                return await response.text()

    # Public: Gets a list of up to 50 message from the channel.
    async def get_messages(self, amount: int) -> list[Message]:
        """Gets a list of up to 50 message from the channel."""

        messages_raw = json.loads(await self._get_messages_raw(amount))
        messages = []
        for message_raw in messages_raw:
            message = Message.deserialize(message_raw)
            messages.append(message)
        
        return messages
    
    # Public: Purge the channel of the specified amount of messages.
    async def purge(self, amount: int) -> None:
        """Purges the channel of the specified amount of messages."""

        if amount > 50: 
            print(f"{ConsoleShortcuts.warn()} Attempted to purge an illegal amount '{amount}' of messages in {self}.")
            amount = 50
        if amount <= 0: 
            print(f"{ConsoleShortcuts.warn()} Attempted to purge an illegal amount '{amount}' of messages in {self}.")
            return

        messages = await self.get_messages(amount)
        messages.reverse()
        messages = messages[:amount]
        for message in messages:
            await message.delete()
    
    # Public: Set the permissions of the channel.
    async def set_permissions(self, permission_integer: int, role: Role) -> 'Channel':
        """
        Sets the permissions of the channel.
        # Attributes
        integer: int - The permission integer. Can be constructed using Permissions.ChannelPermissions.construct()
        # Returns
        Channel: The channel object.
        """
        api_url = f"{GlobalClientInformation.API_URL}/servers/{self.server_id}/channels/{self.id}/permissions/{role.id}"
        headers = {
            "Authorization": GlobalClientInformation.TOKEN,
            "Content-Type": "application/json",
        }
        data = {
            "permissions": permission_integer,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, headers=headers, json=data) as response:
                if response.status != 200:
                    print(f"{ConsoleShortcuts.error()} Failed to set permissions for {self}. Status code: {response.status}. Response Text: {await response.text()}")
                    raise aiohttp.ClientResponseError(response.request_info, response.history)
                return Channel.deserialize(await response.json())
        




    # Public Static: Deserialize a json string to a Channel object.
    @staticmethod
    def deserialize(json: dict) -> 'Channel':
        """static | Deserialize a json string to a Channel object."""

        new_channel = Channel()
        new_channel.id                  = int(json["id"])
        new_channel.name                = str(json["name"])
        new_channel.type                = int(json["type"])
        new_channel.creator_id          = int(json["createdById"])      if json["createdById"]    is not None else 0
        new_channel.server_id           = int(json["serverId"])         if json["serverId"]       is not None else 0
        new_channel.category_id         = int(json["categoryId"])       if json["categoryId"]     is not None else 0
        new_channel.last_messaged_at    = float(json["lastMessagedAt"]) if json["lastMessagedAt"] is not None else None
        new_channel.created_at          = float(json["createdAt"])
        new_channel.order               = json["order"]
    
        return new_channel