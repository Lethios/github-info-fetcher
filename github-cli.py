import argparse
import sys
import requests

parser = argparse.ArgumentParser()

parser.add_argument("username", type=str)
args = parser.parse_args()

try:
    response = requests.get(f"https://api.github.com/users/{args.username}/events")
    data = response.json()
except:
    print("Error: Unable to fetch data from GitHub API.")
    sys.exit(1)

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

def push_event():
    repo_names = set()
    repo_data = []

    for event in data:
        if event['type'] == "PushEvent":
            if event['payload']['commits']:
                commit_msg = []
                for commit in event['payload']['commits']:
                    commit_msg.append(commit['message'])
            else:
                continue

            if event['repo']['name'] not in repo_names:
                repo_names.add(event['repo']['name'])
                repo_data.append({"repo_name": event['repo']['name'], "repo_msgs": commit_msg})
            else:
                for repo in repo_data:
                    if repo['repo_name'] == event['repo']['name']:
                        repo['repo_msgs'].extend(commit_msg)

    repo_event_info[0]['info'] = repo_data

def pull_request_event():
    repo_names = set()
    repo_data = []

    for event in data:
        if event['type'] == "PullRequestEvent":
            if event['repo']['name'] not in repo_names:
                repo_names.add(event['repo']['name'])
                repo_data.append({"repo_name": event['repo']['name'], "pr_info": [{"action": event['payload']['action'], "title": event['payload']['pull_request']['title']}]})
            else:
                for repo in repo_data:
                    if repo['repo_name'] == event['repo']['name']:
                        repo['pr_info'].append({"action": event['payload']['action'], "title": event['payload']['pull_request']['title']})

    repo_event_info[1]['info'] = repo_data

push_event()
pull_request_event()
print(repo_event_info)
