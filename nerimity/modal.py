from __future__ import annotations
from nerimity._enums import ModalComponentTypes
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from nerimity.button import Button

class ModalData():
    def __init__(self, customId: str, value: str) -> None:
        self.customId = customId
        self.value = value

class ModalSubmission():
    def __init__(self, messageId: str, channelId: str, userId: str, data: dict, type: str) -> None:
        self.messageId = messageId
        self.channelId = channelId
        self.userId = userId
        self.data = data
        self.type = type

    def get_data(self) -> list[ModalData]:
        return [ModalData(k, v) for k, v in self.data.items()]

    @staticmethod
    def deserialize(json: dict) -> 'ModalSubmission':
        return ModalSubmission(**json)

class ModalDropdownOption():
    def __init__(self, label: str, value: str, id: str = None) -> None:
        self.label = label
        self.value = value
        self.id = id if id is not None else value

class ModalComponent():
    def __init__(self, type: ModalComponentTypes, customId: str, label: str = None, content: str = None, placeholder: str = None, options: list[ModalDropdownOption] | None = None) -> None:
        self.type = type
        self.customId = customId
        self.content = content
        self.label = label
        self.placeholder = placeholder
        self.options = options

    def to_payload(self) -> dict:
        payload = {
            "type": self.type,
            "id": self.customId,
            "label": self.label,
            "content": self.content,
            "placeholder": self.placeholder,
        }
        if self.options is not None:
            payload["items"] = [{"id": o.id, "label": o.label, "value": o.value} for o in self.options]
        return payload

class Modal():
    def __init__(self, title: str, content: str, button: 'Button', closebuttonlabel: str = "Close", body: list[ModalComponent] = None) -> None:
        """Represents a modal attached to a button."""
        if body is None:
            raise ValueError("Body cannot be None.")
        self.title = title
        self.content = content
        self.closebuttonlabel = closebuttonlabel
        self.button = button
        self.body = body
        self._callback = None

    async def callback(self, buttoninteraction):
        """Invokes the registered submit callback."""
        if self._callback:
            await self._callback(buttoninteraction)

    def set_callback(self, callback_func):
        """Registers the function called when the user submits this modal."""
        self._callback = callback_func

    @staticmethod
    def deserialize(json: dict) -> 'Modal':
        """Deserialize a json dict to a Modal object."""
        from nerimity.button import Button
        return Modal(
            title=json["title"],
            content=json["content"],
            button=Button.deserialize(json["button"]),
            buttonlabel=json.get("closebuttonlabel", "Close"),

            body=[ModalComponent(**component) for component in json["body"]],
        )