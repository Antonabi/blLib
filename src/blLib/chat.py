class ChatMessage:
    def __init__(self, messageInfo) -> None:
        self._messageInfo = messageInfo

        self.sender = self._messageInfo["sender"]
        self.text = self._messageInfo["text"]