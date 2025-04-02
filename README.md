# Github Info Fetcher

Github Info Fetcher is a command-line tool that allows users to fetch and retrieve user profile information and display various GitHub events for a specified user.

## Features
- Fetch GitHub user profile information.
- Fetch main GitHub events such as Push, PullRequest, Issues, Fork, and Watch.
- Option to fetch all events including Create, Release, and Delete events.
- Filter events by type using specific flags.
- Combine multiple flags to customize the events fetched.
- Display events in a user-friendly format using rich text formatting.

## Installation
1. **Ensure Python is installed (Python 3.x recommended).**
2. **Clone the repository and install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Fetch Github User Profile Info:
```bash
python github-cli.py search <github_username>
```
Fetch Github Events Info:
```bash
python github-cli.py event <github_username> <flag(s)>
```

### Available flags:
- `--help`: Show the help message.
- `--default-events`: Fetch only the main events (Push, PullRequest, Issues, Fork, Watch).
- `--all-events`: Fetch every type of event.
- `--push`: Fetch Push events.
- `--pullrequest`: Fetch Pull Request events.
- `--issues`: Fetch Issues events.
- `--fork`: Fetch Fork events.
- `--watch`: Fetch Watch events.
- `--create`: Fetch Create events.
- `--release`: Fetch Release events.
- `--delete`: Fetch Delete events.

### Examples:
1. To fetch user profile info:
   ```bash
   python github-cli.py search <github_username>
   ```
2. To fetch the standard events:
   ```bash
   python github-cli.py event <github_username> --default-events
   ```
3. To fetch every event:
   ```bash
   python github-cli.py event <github_username> --all-events
   ```
4. To fetch only push events:
   ```bash
   python github-cli.py event <github_username> --push
   ```
5. To fetch pull request and issues events:
   ```bash
   python github-cli.py event <github_username> --pullrequest --issues
   ```

# Notes:
- This program fetches events from GitHub, so a **valid internet connection** is required.
- The events are displayed with **rich text formatting** for better readability.

## Author

**Lethios**
- Github: [@Lethios](https://github.com/Lethios)
- Twitter: [@LethiosDev](https://x.com/LethiosDev)

## License

Copyright © 2025 [Lethios](https://github.com/Lethios).  
This project is licensed under the [MIT License](LICENSE).
