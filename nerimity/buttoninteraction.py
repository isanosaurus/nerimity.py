from nerimity.button import Button
import requests
from nerimity._enums import GlobalClientInformation
from nerimity.logger import logger
from nerimity.modal import Modal
from nerimity.embed import Embed
from nerimity.attachment import Attachment
from nerimity.context import Context
from nerimity.message import Message
from nerimity.channel import Channel
from nerimity.member import ServerMember


class ButtonInteraction():
    def __init__(self) -> None:
        self.message    : 'Message' = None
        self.channel    : 'Channel' = None
        self.button     : 'Button' = None
        self.user       : 'ServerMember' = None
        self.data       : dict = None

    async def send_message(self, content: str, attachment: 'Attachment' = None, buttons: list['Button'] = None, embed: 'Embed' = None) -> None:
        """Sends a message to the channel where the button was clicked."""
        await self.channel.send_message(content, attachment, buttons, embed)

    async def send_modal(self, modal: 'Modal') -> None:
        """Sends a modal to the user who clicked the button and registers it for submit routing."""
        await self.channel.send_modal(modal=modal, user_id=self.user.id, message_id=self.message.id, closebuttonlabel=modal.closebuttonlabel)

    @staticmethod
    def deserialize(json: dict) -> 'ButtonInteraction':
        """Deserialize a json string to a ButtonInteraction object."""
        from nerimity.message import Message
        from nerimity.channel import Channel
        from nerimity.member import ServerMember

        bi = ButtonInteraction()

        msg = Message()
        msg.id = int(json["messageId"])
        bi.message = msg

        bi.channel = Channel.get_channel(int(json["channelId"]))
        bi.button  = json["button"]
        bi.user    = ServerMember.get_member(int(json["userId"]))
        bi.data    = json.get("data", None)

        return bi
