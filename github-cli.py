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

    repo_event_info[0]['info'] = repo_data

def pull_request_event():
    repo_names = set()
    repo_data = []

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

    repo_event_info[1]['info'] = repo_data

def issues_event():
    repo_names = set()
    repo_data = []

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

    repo_event_info[2]['info'] = repo_data

def fork_event():
    repo_data = []

    for event in data:
        if event['type'] == "ForkEvent":
            repo_data.append({
                "repo_name": event['repo']['name'],
                "forked_repo_name": event['payload']['forkee']['full_name'],
                "timestamp": event['created_at'][0:10]
            })

    repo_event_info[3]['info'] = repo_data

def watch_event():
    repo_data = []

    for event in data:
        if event['type'] == "WatchEvent":
            repo_data.append({
                "repo_name": event['repo']['name'],
                "action": event['payload']['action'],
                "timestamp": event['created_at'][0:10]
            })
    
    repo_event_info[4]['info'] = repo_data

def create_event():
    repo_data = []

    for event in data:
        if event['type'] == "CreateEvent":
            repo_data.append({
                "repo_name": event['repo']['name'],
                "timestamp": event['created_at'][0:10]
            })

    repo_event_info[5]['info'] = repo_data

def release_event():
    repo_data = []

    for event in data:
        if event['type'] == "ReleaseEvent":
            repo_data.append({
                "repo_name": event['repo']['name'],
                "release_name": event['payload']['name'],
                "tag_name": event['payload']['tag_name'],
                "timestamp": event['payload']['published_at'][0:10]
            })

    repo_event_info[6]['info'] = repo_data

def delete_event():
    repo_data = []

    for event in data:
        if event['type'] == "DeleteEvent":
            repo_data.append({
                "repo_name": event['repo']['name'],
                "ref": event['payload']['ref'],
                "ref_type": event['payload']['ref_type'],
                "timestamp": event['created_at'][0:10]
            })

    repo_event_info[7]['info'] = repo_data
