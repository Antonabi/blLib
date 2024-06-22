class ActiveUser:
    """
    A blocklive active user.
    """
    def __init__(self, userInfo=None, username=None, userProject=None, cursor=None) -> None:
        self._userInfo = userInfo
        
        self.username = self._userInfo["username"]
        self.userProject = self._userInfo["pk"] # the scratch project which the user is working on (every user is working on a different one)
        self.cursor = Cursor(self._userInfo["cursor"])

class Cursor:
    """
    The state of the user. Contains the name of the sprite the user edits, the scroll wheel pos etc.
    """
    def __init__(self, cursorInfo) -> None:
        self._cursorInfo = cursorInfo

        self.targetName = self._cursorInfo["targetName"] # the name of the thing that the cursor is on
        self.scale = self._cursorInfo["scale"]
        self.scrollX = self._cursorInfo["scrollX"]
        self.scrollY = self._cursorInfo["scrollY"]
        self.cursorX = self._cursorInfo["cursorX"]
        self.cursorY = self._cursorInfo["cursorY"]
        self.editorTab = self._cursorInfo["editorTab"]