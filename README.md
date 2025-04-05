![github-info-fetcher](https://socialify.git.ci/Lethios/github-info-fetcher/image?custom_description=A+simple+and+powerful+CLI+tool+to+explore+GitHub+profiles%2C+events%2C+and+popular+repositories+with+customizable+filters.&description=1&language=1&name=1&owner=1&pattern=Formal+Invitation&theme=Auto)

## Features
- **GitHub User Lookup**  
  View detailed profile information about any GitHub user with a single command.  
- **Event Fetcher**  
  Retrieve user activity with options to:
  - Show default events (Push, Pull Request, Issues, Fork, Watch)
  - Show all available GitHub events (including Create, Delete, Release)
  - Filter by one or more event types using flags  
- **Popular Repositories Explorer**  
  Discover trending repositories with filters for language, topic, creation date, stars, and more.  
- **Rich Terminal Output**  
  All data is beautifully displayed using color-coded formatting for clarity and ease of reading.
  
- **Flexible CLI**  
  Combine multiple flags for custom output. Designed with argparse for intuitive command-line usage.
  
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
Discover Popular Repositories:
```bash
python github-cli.py popular [flag(s)]
```

### Available flags:

General:
- `--help`: Show the help message.
  
Events Filtering:
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
  
Popular Repositories Filtering:
- `--language <name>`: Filter by programming language.
- `--topic <name>`: Filter by topic.
- `--after <YYYY-MM-DD>`: Filter repositories created after a specific date.
- `--min-stars <number>`: Filter by minimum star count.
- `--limit <number>`: Limit the number of results.

### Examples:
1. To fetch user profile info:
   ```bash
   python github-cli.py search Lethios
   ```
2. To fetch the standard events:
   ```bash
   python github-cli.py events Lethios --default-events
   ```
3. To fetch pull request, issues  and create events:
   ```bash
   python github-cli.py events Lethios --pullrequest --issues --create
   ```
4. To discover popular Python CLI repos with 200+ stars since 2023:
   ```bash
   python github-cli.py popular --language python --topic cli --min-stars 200 --since 2023-01-01
   ``` 

## Author
**Lethios**
- Github: [@Lethios](https://github.com/Lethios)
- Twitter: [@LethiosDev](https://x.com/LethiosDev)

## License
Copyright © 2025 [Lethios](https://github.com/Lethios).  
This project is licensed under the [MIT License](LICENSE).
