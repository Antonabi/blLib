"""
A library for interacting with the blocklive scratch extension and its servers.
"""

from . import session

#---------------------------------------
# functions
#---------------------------------------

def createSession(username, password=None):
    """
    'Log in' with this. \n
    Returns a Session object. 
    """
    return session.Session(username, password)