from nerimity.attachment import Attachment
from nerimity.channel import Channel
from nerimity.member import ServerMember
from nerimity.message import Message
from nerimity.server import Server
from nerimity._enums import GlobalClientInformation
from nerimity.button import Button
from nerimity.embed import Embed

class Context():
    """
    Represents the context for the command.

    message: The message that triggered the command.
    author: The author of the message that triggered the command.
    channel: The channel where the command was triggered in.
    server: The server where the command was triggered in.

    send(): Sends a message to the channel the command was sent to.
    remove(): Removes the original message.
    react(): Adds an emoji to the original message.
    """

    def __init__(self, message: Message):
        self.message: Message       = message
        self.author : ServerMember  = None
        self.channel: Channel       = message.channel
        self.server : Server        = None
        self.embed  : None          = None # TODO: Add 

        for server in GlobalClientInformation.SERVERS.values():
            if str(message.channel_id) in server.channels.keys():
                self.server  = GlobalClientInformation.SERVERS[f"{server.id}"]
                self.channel = GlobalClientInformation.SERVERS[f"{server.id}"].channels[f"{message.channel_id}"]
                self.author  = GlobalClientInformation.SERVERS[f"{server.id}"].members[f"{message.author_id}"]

    # Public: Sends a message to the channel the command was sent to.
    async def send(self, response: str, attachment: Attachment | None = None, buttons: list[Button] = None, embed: Embed | None = None) -> Message:
        """Sends a message to the channel the command was sent to."""
        return await self.channel.send_message(response, attachment, buttons, embed)

    # Public: Removes the original message.
    async def remove(self) -> None:
        """Removes the original message."""
        await self.message.delete()
    
    # Public: Adds an emoji to the original message.
    async def react(self, emoji: str) -> None:
        """Adds an emoji to the original message."""
        await self.message.react(emoji)