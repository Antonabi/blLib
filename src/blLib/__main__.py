import argparse
import termcolor
import art

from . import createSession
from . import exceptions


"""This whole code is extremely bad. This is the worst CLI i've ever made and seen."""

def printLogo():
    logo = art.text2art("blCLI")
    termcolor.cprint(logo, "red")
    termcolor.cprint("- The worst cli you've ever seen -\n\n\n\n", "cyan")

username = "user"
password = "pass"


def getActiveProjects(args):
    print(args)
    termcolor.cprint(f"Started getActiveProjects.\n\n", "blue")
    session = createSession(username, password)
    if args.agressive:
        args.startId = session.addProject(1038158928)
        termcolor.cprint(f"Agressively got the id {args.startId}", "yellow")
    termcolor.cprint(f"Starting the fuzzing...", "blue")

    foundProjects = []

    projectIds = list(range(args.startId, args.startId - args.tries, -1)) # all ids
    termcolor.cprint(f"Fuzzing these: {projectIds}", "dark_grey")
    for projectId in projectIds:
        try:
            projectInfo = session.getProjectInfo(projectId)
            termcolor.cprint(f"Found project with {len(projectInfo.users)} users (admin: {projectInfo.users[0]})", "green")
            foundProjects.append(projectInfo)
        except Exception:
            termcolor.cprint(f"Failed at {projectId}", "dark_grey")
    
    termcolor.cprint(f"Done with the fuzzing found projects:")
    for project in foundProjects:
        termcolor.cprint({"id": project.id, "users": project.users})

def getBlIdFromScratchId(args):
    print(args)
    termcolor.cprint(f"Started getBlIdFromScratchId.\n\n", "blue")

    session = createSession(username, password)

    projects = session.getUserProjects(args.username)
    for project in projects:
        if int(project.scratchId) == args.projectId:
            termcolor.cprint(f"Found id: {project.scratchId}", "green")
            return
        
    termcolor.cprint("Couldnt find the project. Maybe the username is wrong?", "red")

def getScratchIdFromBlId(args):
    print(args)
    termcolor.cprint(f"Started getScratchIdFromBlId.\n\n", "blue")
    print("Doing nothing rn")

def main():
    printLogo()


    parser = argparse.ArgumentParser(description="A few CLI functions for blLib.")
    
    commandSubparser = parser.add_subparsers(title="commands", dest="command")

    parserGetActiveProjects = commandSubparser.add_parser("getActiveProjects", help="Fuzzes the active projects.")
    parserGetBlIdFromScratchId = commandSubparser.add_parser("getBlIdFromScratchId", help="Gets the blocklive id from a scratch id. (Need the username of the creator)")

    parserGetActiveProjects.set_defaults(func=getActiveProjects)
    parserGetBlIdFromScratchId.set_defaults(func=getBlIdFromScratchId)
    parserGetActiveProjects.add_argument(
        "-a", "--agressive",
        action="store_true",
        help="If the programm should create a new project to get the newest ids.",
        default=False
    )

    parserGetActiveProjects.add_argument(
        "-s", "--startId",
        type=int,
        help="The id wich the programm starts fuzzing with."
    )

    parserGetActiveProjects.add_argument(
        "-t", "--tries",
        type=int,
        help="How deep it will go down.",
        default=20
    )

    parserGetBlIdFromScratchId.add_argument(
        "-i", "--projectId",
        type=int,
        help="The scratchId."
    )

    parserGetBlIdFromScratchId.add_argument(
        "-u", "--username",
        type=str,
        help="The username of the creator of the project."
    )


    args = parser.parse_args()

    if args.command == None:
        parser.print_help()
        
    elif hasattr(args, "func"):
        args.func(args)