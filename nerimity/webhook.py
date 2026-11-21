from nerimity.attachment import Attachment
from nerimity.embed import Embed, Embed

class Webhook:
    """
    Represents a webhook in the Nerimity API.
    """
    def __init__(self, *, id: str, name: str, hexcolor: str, avatar: str = None, channel_id: int, server_id: int, created_by: int, created_at: float) -> None:
        self.id = id
        self.name = name
        self.hexcolor = hexcolor
        self.avatar = avatar
        self.channel_id = channel_id
        self.server_id = server_id
        self.created_by = created_by
        self.created_at = created_at
        self.url 

    @classmethod
    def deserialize(cls, json: dict) -> 'Webhook':
        """
        Deserializes a JSON object into a Webhook instance.
        """
        return cls(
            id=json["id"],
            name=json["name"],
            hexcolor=json["hexcolor"],
            avatar=json["avatar"],
            channel_id=json["channelId"],
            server_id=json["serverId"],
            created_by=json["createdBy"],
            created_at=float(json["createdAt"])
        )

    async def send_message(self, content: str, attachment: 'Attachment' = None, embed: 'Embed' = None) -> None:
        """
        Sends a message through the webhook.

        Args:
            content (str): The content of the message.
            attachment (Attachment, optional): An attachment to include in the message.
            embed (Embed, optional): An embed to include in the message.
        """
        payload = {
            "content": content,
            "attachment": attachment.upload() if attachment else None,
            "embed": embed.to_payload() if embed else None
        }


        