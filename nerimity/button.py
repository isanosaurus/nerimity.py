class Button():
    """Represents a button.
    ## Attributes

    label: string | The label of the button.
    id: string | The ID of the button.
    alert: bool | Whether the button is an alert button. (Button will be red if true)
    """
    def __init__(self, label: str , id: str, alert: bool = False) -> None:
        self.label      : str           = label
        self.id         : str           = id
        self.alert      : bool          = alert
        self._callback                  = None
    
    
    async def callback(self, buttoninteraction):
        """Callback function for the button."""
        if self._callback:
            await self._callback(buttoninteraction)
    
    def set_callback(self, callback_func):
        """Sets the callback function for the button."""
        self._callback = callback_func
    
    # Public: Serializes the button to a json string.
    @staticmethod
    def deserialize(json: dict) -> 'Button':
        """Deserialize a json string to a Button object."""
        button = Button(
            label=str(json["label"]),
            id=str(json["id"]),
            alert=bool(json["alert"])
        )
        return button
