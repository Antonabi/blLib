from datetime import datetime # for the last time timestamp

class UserProject:
    def __init__(self, projectInfo) -> None:
        self._projectInfo = projectInfo

        self.scratchId = projectInfo["scratchId"]
        self.blId = projectInfo["blId"]
        self.title = projectInfo["title"]
        self.lastTimeOnline = datetime.fromtimestamp(projectInfo["lastTime"]/1000) # dividing because blocklive provides the timestamp in miliseconds 
        self.lastUserOnline = projectInfo["lastUser"]
        self.usersOnline = projectInfo["online"]