"""
All of the complaining stuff.
"""

class ProjectNotAvailable:
    """
    If a project is not available.
    """
    def __init__(self, message=""):
        self.message = "The project you wanted to access is not available. Create an anthenticated session if the project is yours or share the project."
        super().__init__(self.message)

class ResourceNotModified:
    """
    If the server thinks that the client has cashed something and wont give it to the client again. (Currently not in use)
    """
    def __init__(self, message=""):
        self.message = "The resource you wanted to access was not modified. You have to wait until it is."
        super().__init__(self.message)