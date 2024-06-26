import requests
import scratchattach as scratch3

from . import exceptions
from . import activeUsers
from . import userStuff
from . import chat
from . import projectConnection
from . import commons

class Session:
    """
    A blocklive session. You can just put a username in or also a password. (For advanced features) Password isnt needed.
    """

    def __init__(self, username, password=None) -> None:
        self.username = username
        self.password = password

        self._authenticated = False
        self._saSession = None

        if password != None:
            self._saSession = scratch3.login(self.username, self.password)
            self._authenticated = True

    def getActiveUsers(self, projectId):
        """
        Gets the active users from blocklive projects. The id has to be a blocklive id. \n
        Returns a list of ActiveUsers.
        """

        response = requests.get(f"{commons.serverUrl}/active/{projectId}")
        users = []
        for user in response.json():
            users.append(activeUsers.ActiveUser(user))
        return users
    
    def getUserProjects(self, user=None):
        """
        Gets the projects that a user has used with blocklive. \n
        Returns a list of UserProject objects.
        """
        if user == None:
            user = self.username
        response = requests.get(f"{commons.serverUrl}/userProjectsScratch/{user}")
        projects = []
        for project in response.json():
            projects.append(userStuff.UserProject(project))
        return projects
    
    def getProjectJson(self, projectId):
        """
        Gets the project json of a blocklive project.\n
        Just returns a json object.
        """

        response = requests.get(f"{commons.serverUrl}/projectJSON/{projectId}")
        return response.json()
    
    def getProjectOwner(self, projectId):
        """
        Just gets the owner of a blocklive project. Uses the scratch id. \n
        Return the owners username.
        """
        response = requests.get(f"{commons.serverUrl}/scratchIdInfo/{projectId}")
        return response.json()["owner"]
    
    def getProjectChat(self, projectId):
        """
        Gets the chat of blocklive project.\n
        Returns a list ChatMessage objects.
        """

        response = requests.get(f"{commons.serverUrl}/chat/{projectId}")
        messages = []
        for message in response.json():
            messages.append(chat.ChatMessage(message))
        return messages
    
    def getBlockliveIdFromScratchId(self, projectId, creator=""):
        """
        Gets the blocklive id from the scratch id.
        """
        response = requests.get(f"{commons.serverUrl}/blId/{projectId}/{creator}")
        return response.text
    
    def getScratchIdFromBlockliveId(self, blProjectId, creator):
        """
        Get the scratchId from the blocklive id.
        """
        projects = self.getUserProjects(creator)
        for project in projects:
            if project.blId == blProjectId:
                return project.scratchId
        raise exceptions.ProjectNotAvailable
    
    def getSharedProjectCount(days):
        """
        Gets the count of shared projects in the last days.
        """
        response = requests.get(f"{commons.serverUrl}/dau/{days}")
        return response.text
    
    def getUserFriends(self, user=None):
        """
        Gets the friends of a user. \n
        Returns a list of usernames.
        """

        if user == None:
            user = self.username
        
        response = requests.get(f"{commons.serverUrl}/friends/{user}")
        return response.json()

    def addFriend(self, friend):
        """
        Adds a friend to the users friends list.
        """

        requests.post(f"{commons.serverUrl}/friends/{self.username}/{friend}")
        return "awwww :) (I didnt think you had any)"

    def shareProject(self, friend, blProjectId, scratchProjectId):
        """
        Shares a blocklive project with a friend. The blProjectId is the id of blocklive.
        """

        requests.put(f"{commons.serverUrl}/share/{blProjectId}/{friend}/{self.username}?pk={scratchProjectId}")
        return "Why are you printing me?"

    def addProject(self, scratchProjectId, title=None, projectJson=None):
        """
        Adds a project to the blocklive servers. If you dont supply the project json it will try to get it from the servers (If your project isnt published you need an authenticated session). The title is the title of the project. \n
        Returns the id of the project.
        """
        if projectJson == None:
            if self._authenticated:
                project = self._saSession.connect_project(scratchProjectId) # only get the 
            else:
                project = scratch3.get_project(scratchProjectId)

            if hasattr(project, "get_raw_json"): # if the project is partial or not
                projectJson = project.get_raw_json()
                if title == None:
                    title = project.title
            else:
                raise exceptions.ProjectNotAvailable
        
        response = requests.post(f"{commons.serverUrl}/newProject/{scratchProjectId}/{self.username}?title={title}", json=projectJson)
        return int(response.json()["id"])
    
    def connectToProject(self, projectId, pk=None):
        """
        Connects to a blocklive project via websocket. The projectId is that of blocklive.
        """

        return projectConnection.ProjectConnection(projectId, self.username, pk)