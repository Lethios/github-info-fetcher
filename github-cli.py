"""
GitHub Info Fetcher

This CLI tool allows users to fetch and display GitHub user information and activity events.

Features:
1. Fetch GitHub User Info:
  - Retrieve user details such as name, bio, location, followers, and account creation date.
  - Display information in a structured and visually appealing format using Rich.
  
2. Fetch GitHub Events:
  - Retrieve recent activity events of a specified user.
  - Supports filtering by event types (Push, PullRequest, Issues, Fork, Watch, etc.).
  - Allows combining multiple filters for customized event fetching.

Usage:
    python github-cli.py <command> <github_username> <flag(s)>

Available Commands:
    search       : Fetch and display GitHub user profile information.
    event        : Fetch and display GitHub activity events for the user.

Available Flags (For "event" command):
    --help             : Show the help message.
    --default-events   : Fetch only the main events (Push, PullRequest, Issues, Fork, Watch).
    --all-events       : Fetch every type of event.
    --push             : Fetch Push events.
    --pullrequest      : Fetch Pull Request events.
    --issues           : Fetch Issues events.
    --fork             : Fetch Fork events.
    --watch            : Fetch Watch events.
    --create           : Fetch Create events.
    --release          : Fetch Release events.
    --delete           : Fetch Delete events.

Examples:
1. Fetch GitHub user information:
   python github-cli.py search <github_username>

2. Fetch standard events of a user:
   python github-cli.py event <github_username> --default-events

3. Fetch all available events:
   python github-cli.py event <github_username> --all-events

4. Fetch specific events (e.g., Pull Requests and Issues):
   python github-cli.py event <github_username> --pullrequest --issues

Notes:
- A valid internet connection is required.
- The output is styled using the `rich` library for improved readability.

Author: Lethios
"""

import argparse
import sys
import requests
from rich.console import Console

console = Console()
HELP_MESSAGE = """
[bold cyan] GitHub CLI Tool[/bold cyan]

 This program allows you to fetch GitHub user information and activity events directly in your terminal.

[bold green] Usage:[/bold green]
[bold yellow] python github-cli.py <command> <github_username> <flag(s)>[/bold yellow]

[bold green] Available Commands:[/bold green]

[bold magenta] search[/bold magenta]      Fetch and display GitHub user profile information.
[bold magenta] event[/bold magenta]       Fetch and display GitHub user activity events.

[bold green] Flags (For "event" command):[/bold green]

[bold magenta] --help[/bold magenta]             Show this help message.
[bold magenta] --default-events[/bold magenta]   Fetch only the main events (Push, PullRequest, Issues, Fork, Watch).
[bold magenta] --all-events[/bold magenta]       Fetch every type of event.
[bold magenta] --push[/bold magenta]             Fetch Push events.
[bold magenta] --pullrequest[/bold magenta]      Fetch Pull Request events.
[bold magenta] --issues[/bold magenta]           Fetch Issues events.
[bold magenta] --fork[/bold magenta]             Fetch Fork events.
[bold magenta] --watch[/bold magenta]            Fetch Watch events.
[bold magenta] --create[/bold magenta]           Fetch Create events.
[bold magenta] --release[/bold magenta]          Fetch Release events.
[bold magenta] --delete[/bold magenta]           Fetch Delete events.

[bold green] Examples:[/bold green]

 1. Fetch GitHub user information:
    [bold yellow] python github-cli.py search Lethios[/bold yellow]

 2. Fetch the standard events:
    [bold yellow] python github-cli.py event Lethios[/bold yellow] or
    [bold yellow] python github-cli.py event Lethios --default-events[/bold yellow]

 3. Fetch all available events:
    [bold yellow] python github-cli.py event Lethios --all-events[/bold yellow]

 4. Fetch only push events:
    [bold yellow] python github-cli.py event Lethios --push[/bold yellow]

 5. Fetch pull request and issues events:
    [bold yellow] python github-cli.py event Lethios --pullrequest --issues[/bold yellow]

[bold magenta] Additional Information:[/bold magenta] 
 - Events display relevant details such as repository, message, and timestamp.
 - Combine flags to filter events, such as [bold yellow]--fork --watch[/bold yellow].

[bold red] Note:[/bold red] This program fetches data from GitHub, so a valid internet connection is required.
"""

if "--help" == sys.argv[1] or "help" == sys.argv[1]:
    console.print(HELP_MESSAGE)
    sys.exit(0)

parser = argparse.ArgumentParser(description="Github Activity Tracker")
subparser = parser.add_subparsers(dest="command")

search_parser = subparser.add_parser("search")
search_parser.add_argument("search")

event_parser = subparser.add_parser("event")
event_parser.add_argument("event")
event_parser.add_argument("--default-events", action="store_true")
event_parser.add_argument("--all-events", action="store_true")
event_parser.add_argument("--push", action="store_true")
event_parser.add_argument("--pullrequest", action="store_true")
event_parser.add_argument("--issues", action="store_true")
event_parser.add_argument("--fork", action="store_true")
event_parser.add_argument("--watch", action="store_true")
event_parser.add_argument("--create", action="store_true")
event_parser.add_argument("--release", action="store_true")
event_parser.add_argument("--delete", action="store_true")

args = parser.parse_args()

def check_conflicts(parsed_args):
    arg_list = [
        parsed_args.push,
        parsed_args.pullrequest,
        parsed_args.issues,
        parsed_args.fork,
        parsed_args.watch,
        parsed_args.create,
        parsed_args.release,
        parsed_args.delete
    ]

    if parsed_args.default_events and parsed_args.all_events:
        print("Error: The --default-events and --all-events flags cannot be used together.")
        sys.exit(1)

    if parsed_args.default_events and any(arg_list):
        print("The --default-events flag can only be used on its own.")
        sys.exit(1)

    elif args.all_events and any(arg_list):
        print("The --all-events flag can only be used on its own.")
        sys.exit(1)

def fetch_github_user(username):
    try:
        response = requests.get(f"https://api.github.com/users/{username}", timeout=10)
        return response.json()
    except requests.exceptions.Timeout:
        print("Error: Request timed out. Please try again later.")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("Error: Connection error. Please check your internet connection.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to fetch data from GitHub API. {e}")
        sys.exit(1)

def fetch_github_activity(username):
    try:
        response = requests.get(f"https://api.github.com/users/{username}/events", timeout=10)
        return response.json()
    except requests.exceptions.Timeout:
        print("Error: Request timed out. Please try again later.")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("Error: Connection error. Please check your internet connection.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: Unable to fetch data from GitHub API. {e}")
        sys.exit(1)

if args.command == "search":
    data = fetch_github_user(args.search)
    user_info = {
        "username": data['login'],
        "name": data['name'],
        "bio": data['bio'],
        "location": data['location'],
        "blog": data['blog'],
        "email": data['email'],
        "twitter_username": data['twitter_username'],
        "public_repos": data['public_repos'],
        "followers": data['followers'],
        "following": data['following'],
        "created": data['created_at'][0:10],
        "updated": data['updated_at'][0:10]
    }

elif args.command == "event":
    data = fetch_github_activity(args.event)
    repo_event_info = [
        {
            "type": "PushEvent",
            "info": None
        },
        {
            "type": "PullRequestEvent",
            "info": None
        },
        {
            "type": "IssuesEvent",
            "info": None
        },
        {
            "type": "ForkEvent",
            "info": None
        },
        {
            "type": "WatchEvent",
            "info": None
        },
        {
            "type": "CreateEvent",
            "info": None
        },
        {
            "type": "ReleaseEvent",
            "info": None
        },
        {
            "type": "DeleteEvent",
            "info": None
        }
    ]

else:
    print("Invalid arguments.")
    sys.exit(1)

def push_event():
    repo_names = set()
    repo_data = []
    event_exists = False

    for event in data:
        if event['type'] == "PushEvent":
            if event['payload']['commits']:
                commit_msg = []
                for commit in event['payload']['commits']:
                    commit_msg.append({
                        "message": commit['message'],
                        "timestamp": event['created_at'][0:10]
                    })
            else:
                continue

            if event['repo']['name'] not in repo_names:
                repo_names.add(event['repo']['name'])
                repo_data.append({
                    "repo_name": event['repo']['name'],
                    "repo_msgs": commit_msg
                })
            else:
                for repo in repo_data:
                    if repo['repo_name'] == event['repo']['name']:
                        repo['repo_msgs'].extend(commit_msg)

            event_exists = True

    if event_exists:
        repo_event_info[0]['info'] = repo_data
    else:
        repo_event_info[0]['info'] = "Event does not exist"

def pull_request_event():    
    repo_names = set()
    repo_data = []
    event_exists = False

    for event in data:
        if event['type'] == "PullRequestEvent":
            if event['repo']['name'] not in repo_names:
                repo_names.add(event['repo']['name'])
                repo_data.append({
                    "repo_name": event['repo']['name'],
                    "pr_info": [{
                        "action": event['payload']['action'],
                        "title": event['payload']['pull_request']['title'],
                        "timestamp": event['created_at'][0:10]
                    }]
                })
            else:
                for repo in repo_data:
                    if repo['repo_name'] == event['repo']['name']:
                        repo['pr_info'].append({
                            "action": event['payload']['action'],
                            "title": event['payload']['pull_request']['title'],
                            "timestamp": event['created_at'][0:10]
                        })

            event_exists = True

    if event_exists:
        repo_event_info[1]['info'] = repo_data
    else:
        repo_event_info[1]['info'] = "Event does not exist"

def issues_event():    
    repo_names = set()
    repo_data = []
    event_exists = False

    for event in data:
        if event['type'] == "IssuesEvent":
            if event['repo']['name'] not in repo_names:
                repo_names.add(event['repo']['name'])
                repo_data.append({
                    "repo_name": event['repo']['name'],
                    "issue_info": [{
                        "action": event['payload']['action'],
                        "title": event['payload']['issue']['title'],
                        "timestamp": event['created_at'][0:10]
                    }]
                })
            else:
                for repo in repo_data:
                    if repo['repo_name'] == event['repo']['name']:
                        repo['issue_info'].append({
                            "action": event['payload']['action'],
                            "title": event['payload']['issue']['title'],
                            "timestamp": event['created_at'][0:10]
                        })

            event_exists = True

    if event_exists:
        repo_event_info[2]['info'] = repo_data
    else:
        repo_event_info[2]['info'] = "Event does not exist"

def fork_event():    
    repo_data = []
    event_exists = False

    for event in data:
        if event['type'] == "ForkEvent":
            repo_data.append({
                "repo_name": event['repo']['name'],
                "forked_repo_name": event['payload']['forkee']['full_name'],
                "timestamp": event['created_at'][0:10]
            })

            event_exists = True

    if event_exists:
        repo_event_info[3]['info'] = repo_data
    else:
        repo_event_info[3]['info'] = "Event does not exist"

def watch_event():    
    repo_data = []
    event_exists = False

    for event in data:
        if event['type'] == "WatchEvent":
            repo_data.append({
                "repo_name": event['repo']['name'],
                "action": event['payload']['action'],
                "timestamp": event['created_at'][0:10]
            })

            event_exists = True

    if event_exists:
        repo_event_info[4]['info'] = repo_data
    else:
        repo_event_info[4]['info'] = "Event does not exist"

def create_event():    
    repo_data = []
    event_exists = False

    for event in data:
        if event['type'] == "CreateEvent":
            repo_data.append({
                "repo_name": event['repo']['name'],
                "timestamp": event['created_at'][0:10]
            })

            event_exists = True

    if event_exists:
        repo_event_info[5]['info'] = repo_data
    else:
        repo_event_info[5]['info'] = "Event does not exist"

def release_event():   
    repo_data = []
    event_exists = False

    for event in data:
        if event['type'] == "ReleaseEvent":
            repo_data.append({
                "repo_name": event['repo']['name'],
                "release_name": event['payload']['name'],
                "tag_name": event['payload']['tag_name'],
                "timestamp": event['payload']['published_at'][0:10]
            })

            event_exists = True

    if event_exists:
        repo_event_info[6]['info'] = repo_data
    else:
        repo_event_info[6]['info'] = "Event does not exist"

def delete_event():    
    repo_data = []
    event_exists = False

    for event in data:
        if event['type'] == "DeleteEvent":
            repo_data.append({
                "repo_name": event['repo']['name'],
                "ref": event['payload']['ref'],
                "ref_type": event['payload']['ref_type'],
                "timestamp": event['created_at'][0:10]
            })

            event_exists = True

    if event_exists:
        repo_event_info[7]['info'] = repo_data
    else:
        repo_event_info[7]['info'] = "Event does not exist"

def display_events():    
    if args.command == "search":
        print()
        console.print(f" [bold cyan]Displaying Github User Info of {data['login']}[/bold cyan]")
        print()

        console.print(f" [bold green]Username:[/bold green] {user_info['username']}")
        console.print(f" [bold green]Name:[/bold green] {user_info['name']}")
        print()

        console.print(f" [bold magenta]Bio:[/bold magenta] {user_info['bio']}")
        console.print(f" [bold magenta]Location:[/bold magenta] {user_info['location']}")
        print()

        console.print(f" [bold purple]Email:[/bold purple] {user_info['email']}")
        print()

        console.print(f" [bold blue]Twitter:[/bold blue] {user_info['twitter_username']}")
        print()

        console.print(f" [bold orange3]Followers:[/bold orange3] [white]{user_info['followers']}")
        console.print(f" [bold orange3]Following:[/bold orange3] [white]{user_info['following']}")
        print()

        console.print(f" [bold blue3]Account created on[/bold blue3] [white]{user_info['created']}")
        console.print(f" [bold blue3]Last updated on[/bold blue3] [white]{user_info['updated']}")
        print()

    elif args.command == "event":    
        print()
        console.print("{:^100s}".format(f" [bold cyan]Displaying Github Event Activities of {data[0]['actor']['login']}[/bold cyan]"))

        if repo_event_info[0]['info'] is None:
            pass
        elif repo_event_info[0]['info'] == "Event does not exist":
            print()
            console.print(" [bold red]Push event not found.[/bold red]\n")
        else:
            print()
            console.print(" [bold green]Push Events[/bold green] " + "[bold green]=[/bold green]"* 80)
            print()
            for repo in repo_event_info[0]['info']:
                console.print(f" [bold cyan]Pushed {len(repo['repo_msgs'])} commit(s) to {repo['repo_name']}[/bold cyan]")
                for message in repo['repo_msgs']:
                    console.print(f" - [magenta][{message['timestamp']}][/magenta] {message['message']}.")
                print()

        if repo_event_info[1]['info'] is None:
            pass
        elif repo_event_info[1]['info'] == "Event does not exist":
            print()
            console.print(" [bold red]PullRequest event not found.[/bold red]\n")
        else:
            print()
            console.print(" [bold green]PullRequest Events[/bold green] " + "[bold green]=[/bold green]"* 73)        
            print()
            for repo in repo_event_info[1]['info']:
                console.print(f" [bold cyan]{repo['repo_name']}[/bold cyan]")
                for pr in repo['pr_info']:
                    console.print(f" - [magenta][{pr['timestamp']}][/magenta] {pr['action'].capitalize()} PR: {pr['title']}")
                print()

        if repo_event_info[2]['info'] is None:
            pass
        elif repo_event_info[2]['info'] == "Event does not exist":
            print()
            console.print(" [bold red]Issues event not found.[/bold red]\n")
        else:
            print()
            console.print(" [bold green]Issues Events[/bold green] " + "[bold green]=[/bold green]"* 78)
            print()
            for repo in repo_event_info[2]['info']:
                console.print(f" [bold cyan]{repo['repo_name']}[/bold cyan]")
                for issue in repo['issue_info']:
                    console.print(f" - [magenta][{issue['timestamp']}][/magenta] {issue['action'].capitalize()} Issue: {issue['title']}")
                print()

        if repo_event_info[3]['info'] is None:
            pass
        elif repo_event_info[3]['info'] == "Event does not exist":
            print()
            console.print(" [bold red]Fork event not found.[/bold red]\n")
        else:
            print()
            console.print(" [bold green]Fork Events[/bold green] " + "[bold green]=[/bold green]"* 80)
            print()
            for repo in repo_event_info[3]['info']:
                console.print(f" - [magenta][{repo['timestamp']}][/magenta] Forked [bold cyan]{repo['repo_name']} [/bold cyan]to [bold cyan]{repo['forked_repo_name']}[/bold cyan]")
                print()

        if repo_event_info[4]['info'] is None:
            pass
        elif repo_event_info[4]['info'] == "Event does not exist":
            print()
            console.print(" [bold red]Watch event not found.[/bold red]\n")
        else:
            print()
            console.print(" [bold green]Watch Events[/bold green] " + "[bold green]=[/bold green]"* 79)
            print()
            for repo in repo_event_info[4]['info']:
                console.print(f" - [magenta][{repo['timestamp']}][/magenta] Starred [bold cyan]{repo['repo_name']}[/bold cyan]")
                print()

        if repo_event_info[5]['info'] is None:
            pass
        elif repo_event_info[5]['info'] == "Event does not exist":
            print()
            console.print(" [bold red]Create event not found.[/bold red]\n")
        else:
            print()
            console.print(" [bold green]Create Events[/bold green] " + "[bold green]=[/bold green]"* 78)
            print()
            for repo in repo_event_info[5]['info']:
                console.print(f" - [magenta][{repo['timestamp']}][/magenta] Created new repository [bold cyan]{repo['repo_name']}[/bold cyan]")
                print()

        if repo_event_info[6]['info'] is None:
            pass
        elif repo_event_info[6]['info'] == "Event does not exist":
            print()
            console.print(" [bold red]Release event not found.[/bold red]\n")
        else:
            print()
            console.print(" [bold green]Release Events[/bold green] " + "[bold green]=[/bold green]"* 77)
            print()
            for repo in repo_event_info[6]['info']:
                console.print(f" [bold cyan]{repo['repo_name']}[/bold cyan]")
                console.print(f" - [magenta][{repo['timestamp']}][/magenta] Release: {repo['release_name']} (Tag: {repo['tag_name']})")
                print()

        if repo_event_info[7]['info'] is None:
            pass
        elif repo_event_info[7]['info'] == "Event does not exist":
            print()
            console.print(" [bold red]Delete event not found.[/bold red]\n")
        else:
            print()
            console.print(" [bold green]Delete Events[/bold green] " + "[bold green]=[/bold green]"* 78)
            print()
            for repo in repo_event_info[7]['info']:
                console.print(f" [bold cyan]{repo['repo_name']}[/bold cyan]")
                console.print(f" - [magenta][{repo['timestamp']}][/magenta] Deleted {repo['ref_type']}: {repo['ref']}")
                print()

def main():    
    if args.command == "search":
        display_events()

    elif args.command == "event":
        check_conflicts(args)

        if not any([args.default_events, args.all_events, args.push, args.pullrequest, args.issues, args.fork, args.watch, args.create, args.release, args.delete]):
            args.default_events = True

        if args.default_events:
            push_event()
            pull_request_event()
            issues_event()
            fork_event()
            watch_event()

        elif args.all_events:
            push_event()
            pull_request_event()
            issues_event()
            fork_event()
            watch_event()
            create_event()
            release_event()
            delete_event()

        else:
            if args.push:
                push_event()
            if args.pullrequest:
                pull_request_event()
            if args.issues:
                issues_event()
            if args.fork:
                fork_event()
            if args.watch:
                watch_event()
            if args.create:
                create_event()
            if args.release:
                release_event()
            if args.delete:
                delete_event()

        display_events()

if __name__ == "__main__":
    main()
    sys.exit(0)
