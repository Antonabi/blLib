import websocket
import json

from . import activeUsers

class ProjectConnection:
    """
    A connection to blocklive project. With this you can send messages, change things in the project etc.
    """
    def __init__(self, projectId, username, pk) -> None: # idk what pk is
        self.projectId = projectId
        self.username = username
        self.pk = pk

        self._connect()

    def _connect(self):
        """
        Connects to the websocket. Nothing else.
        """
        self._websocket = websocket.WebSocket()
        self._websocket.connect("wss://spore.us.to:4000/socket.io/?EIO=4&transport=websocket")

    def _joinSession(self):
        self._sendMessage( # joins the session
            {
                "id": self.projectId,
                "username": self.username,
                "pk": self.pk
            }, 
            number=42,
            type="joinSession"
        )

    def _sendMessage(self, type, message, number: int): # idk what the number means
        """
        Sends a message to the websocket server in the standart bl format.
        """
        data = message
        data["type"] = type
        self._websocket.send(str(number)+json.dumps(["message", type]))

    def setCursor(self, scrollX, scrollY, scale, targetName, editorTab):
        """
        Sets the cursor of you.
        """

        data = {
            "cursor": {
                "scrollX": scrollX,
                "scrollY": scrollY,
                "scale": scale,
                "targetName": targetName,
                "editorTab": editorTab
            },
            "blId": self.projectId
        }
        self._sendMessage(type="setCursor", number=42, message=data)

    def sendChatMessage(self, message):
        data = {
            "blId": self.projectId,
            "msg": {
                "meta": "chat",
                "msg": {
                    "sender": self.username,
                    "text": message
                }
            }
        }
        self._sendMessage(type="chat", number=42, message=data)