import argparse
import sys
import requests
from rich.console import Console

console = Console()
HELP_MESSAGE = """
[bold cyan] GitHub CLI Tool[/bold cyan]

 This program allows you to fetch GitHub user information and activity events directly in your terminal.

[bold green] Usage:[/bold green]
[bold yellow] python github-cli.py <command>[/bold yellow]

[bold green] Available Commands:[/bold green]

[bold magenta] help[/bold magenta]        Display this help message.
[bold magenta] search[/bold magenta]      Fetch and display GitHub user profile information.
[bold magenta] events[/bold magenta]      Fetch and display GitHub user activity events.
[bold magenta] popular[/bold magenta]     Discover popular repositories using optional filters.

[bold green] Flags for "events" command:[/bold green]
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

[bold green] Flags for "popular" command:[/bold green]
[bold magenta] --language[/bold magenta]         Filter by programming language.
[bold magenta] --topic[/bold magenta]            Filter by repository topic.
[bold magenta] --after[/bold magenta]            Filter repositories created after this date (YYYY-MM-DD).
[bold magenta] --min_stars[/bold magenta]        Filter repositories with at least this many stars.
[bold magenta] --limit[/bold magenta]            Limit the number of results shown (max 100).

[bold green] Examples:[/bold green]

 1. To fetch GitHub user profile information:
    [bold yellow] python github-cli.py search Lethios[/bold yellow]

 2. To fetch the standard events:
    [bold yellow] python github-cli.py events Lethios[/bold yellow] or
    [bold yellow] python github-cli.py events Lethios --default-events[/bold yellow]

 3. To fetch pull request and issues events:
    [bold yellow] python github-cli.py events Lethios --pullrequest --issues[/bold yellow]

 4. To discover popular Python CLI repos with 200+ stars since 2023:
    [bold yellow] python github-cli.py popular --language python --topic cli --min-stars 200 --since 2023-01-01[/bold yellow]

[bold red] Note:[/bold red] This program fetches data from GitHub, so a valid internet connection is required.
"""

if "help" == sys.argv[1] or "--help" == sys.argv[1]:
    console.print(HELP_MESSAGE)
    sys.exit(0)

parser = argparse.ArgumentParser(description="Github Activity Tracker")
subparser = parser.add_subparsers(dest="command")

search_parser = subparser.add_parser("search")
search_parser.add_argument("search")

events_parser = subparser.add_parser("events")
events_parser.add_argument("events")
events_parser.add_argument("--default-events", action="store_true")
events_parser.add_argument("--all-events", action="store_true")
events_parser.add_argument("--push", action="store_true")
events_parser.add_argument("--pullrequest", action="store_true")
events_parser.add_argument("--issues", action="store_true")
events_parser.add_argument("--fork", action="store_true")
events_parser.add_argument("--watch", action="store_true")
events_parser.add_argument("--create", action="store_true")
events_parser.add_argument("--release", action="store_true")
events_parser.add_argument("--delete", action="store_true")

popular_parser = subparser.add_parser("popular")
popular_parser.add_argument("--language", action="store")
popular_parser.add_argument("--topic", action="store")
popular_parser.add_argument("--after", action="store")
popular_parser.add_argument("--min-stars", action="store")
popular_parser.add_argument("--limit", action="store")

args = parser.parse_args()

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

def fetch_github_repo(queries):
    try:
        response = requests.get(f"https://api.github.com/search/repositories{queries}", timeout=10)
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

def handle_search_command():
    data = fetch_github_user(args.search)    

    try:
        print()
        console.print(f" [bold cyan]Displaying Github User Info of {data['login']}[/bold cyan]")
    except:
        print("Error: User not found.")
        sys.exit(1)
    print()

    console.print(f" [bold green]Username:[/bold green] {data['login']}")
    console.print(f" [bold green]Name:[/bold green] {data['name'] or "Not provided"}")
    console.print(f" [bold green]Profile link:[/bold green] {data['html_url']}")
    print()

    console.print(f" [bold magenta]Bio:[/bold magenta] {data['bio'] or "Not provided"}")
    console.print(f" [bold magenta]Location:[/bold magenta] {data['location'] or "Not provided"}")
    print()

    console.print(f" [bold purple]Email:[/bold purple] {data['email'] or "Not provided"}")
    print()

    console.print(f" [bold blue]Twitter:[/bold blue] {data['twitter_username'] or "Not provided"}")
    print()

    console.print(f" [bold orange3]Followers:[/bold orange3] [white not bold]{data['followers']}")
    console.print(f" [bold orange3]Following:[/bold orange3] [white not bold]{data['following']}")
    print()

    console.print(f" [bold blue3]Account created on[/bold blue3] [white not bold]{data['created_at'][0:10]}")
    console.print(f" [bold blue3]Last updated on[/bold blue3] [white not bold]{data['updated_at'][0:10]}")
    print()

def handle_event_command():    
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

        elif parsed_args.all_events and any(arg_list):
            print("The --all-events flag can only be used on its own.")
            sys.exit(1)
    
    check_conflicts(args)
    
    repo_event_info = [
        {"type": "PushEvent", "info": None},
        {"type": "PullRequestEvent", "info": None},
        {"type": "IssuesEvent", "info": None},
        {"type": "ForkEvent", "info": None},
        {"type": "WatchEvent", "info": None},
        {"type": "CreateEvent", "info": None},
        {"type": "ReleaseEvent", "info": None},
        {"type": "DeleteEvent", "info": None}
    ]    
    
    data = fetch_github_activity(args.events)
    
    if not any([args.default_events, args.all_events, args.push, args.pullrequest, args.issues, args.fork, args.watch, args.create, args.release, args.delete]):
        args.default_events = True
    
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
    
    print()
    console.print("{:^100s}".format(f" [bold cyan]Displaying Github Event Activities of {data[0]['actor']['login']}[/bold cyan]"))

    if repo_event_info[0]['info'] is None:
        pass
    elif repo_event_info[0]['info'] == "Event does not exist":
        print()
        console.print(" [bold red]Push event not found.[/bold red]\n")
    else:
        print()
        console.print(" [bold green]Push Events[/bold green] " + "[bold green]=[/bold green]" * 80)
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
        console.print(" [bold green]PullRequest Events[/bold green] " + "[bold green]=[/bold green]" * 73)        
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
        console.print(" [bold green]Issues Events[/bold green] " + "[bold green]=[/bold green]" * 78)
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
        console.print(" [bold green]Fork Events[/bold green] " + "[bold green]=[/bold green]" * 80)
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
        console.print(" [bold green]Watch Events[/bold green] " + "[bold green]=[/bold green]" * 79)
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
        console.print(" [bold green]Create Events[/bold green] " + "[bold green]=[/bold green]" * 78)
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

def handle_popular_command():
    def check_conflicts(parsed_args):
        conflicted_flags = [parsed_args.language, parsed_args.topic, parsed_args.after, parsed_args.min_stars]
        if args.limit is not None and all(flag is None for flag in conflicted_flags):
            print("Error: The --limit flag cannot be used as the only flag.")
            sys.exit(1)

    check_conflicts(args)

    flags = [args.language, args.topic, args.after, args.min_stars, args.limit]

    if all(flag is None for flag in flags):
        queries = "?q=stars:>1000&per_page=5&sort=stars&order=desc"
        data = fetch_github_repo(queries)
    else:
        dict = {
            args.language: "language:",
            args.topic: "topic:",
            args.after: "created:>=",
            args.min_stars: "stars:>=",
            args.limit: "&per_page="
        }
        queries = "?q="
        for flag in flags:
            if flag is not None:
                query = ""
                if flag is not None:
                    if flag is not args.limit:
                        query = dict[flag] + flag + "+"
                    else:
                        query = dict[flag] + flag
                    queries += query

        queries += "&sort=stars&order=desc"
        data = fetch_github_repo(queries)
    
    print()
    console.print(" [bold cyan]Displaying Popular GitHub Repositories[/bold cyan]")
    print()

    for repo in data['items']:
        console.print(" " + "[bold cyan]=[/bold cyan]" * 80)      
        console.print(f" [bold green]Repository name:[/bold green] {repo['name']}")
        console.print(f" [bold green]Owner:[/bold green] {repo['owner']['login']}")
        console.print(f" [bold green]Link:[/bold green] {repo['html_url']}")
        print()

        console.print(f" [bold magenta]Description:[/bold magenta] {repo['description']}")
        console.print(f" [bold magenta]Language:[/bold magenta] {repo['language']}")
        print()
        
        console.print(f" [bold orange3]Watchers:[/bold orange3] [white not bold]{repo['watchers_count']}")
        console.print(f" [bold red]Forks:[/bold red] [white not bold]{repo['forks_count']}")
        console.print(f" [bold yellow]Stars:[/bold yellow] [white not bold]{repo['stargazers_count']}")
        print()

        console.print(f" [bold blue3]Created on[/bold blue3] [white not bold]{repo['created_at'][0:10]}")
        console.print(f" [bold blue3]Last updated on[/bold blue3] [white not bold]{repo['updated_at'][0:10]}")
        console.print(" " + "[bold cyan]=[/bold cyan]" * 80)
        print()

def main():
    if args.command == "search":
        handle_search_command()
    elif args.command == "events":
        handle_event_command()
    elif args.command == "popular":
        handle_popular_command()
    else:
        print("Invalid arguments.")
        sys.exit(1)

if __name__ == "__main__":
    main()
    sys.exit(0)
