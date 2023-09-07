# script to read 'README.md' file from a github repo using 'rich' library
import sys
try:
    import requests
    from github import Github
    from rich.console import Console
    from debug import logger
    from rich.markdown import Markdown
except ImportError as e:
    from debug import logger
    logger.error(f"Failed importing dependencies ({e})")
    sys.exit(0)

console = Console()

def ReadMD(repo : str) -> None:
    # get repo details
    gitty = Github()
    try:
        Repo = gitty.get_repo(repo.split("/")[-2]+"/"+repo.split("/")[-1]) # get 'owner/repo'
        # Fetch the README.md content from GitHub
        response = requests.get(Repo.get_readme().download_url)
        response.raise_for_status()

        # Read the content as markdown and display it using rich
        MdContent = response.text
        console.print(
            Markdown(
                MdContent
            )
        )
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch README.md from GitHub ({e})")
        sys.exit(0)

    except Exception as e:
        logger.error(f"Unexpected error ! ({e})")
        sys.exit(0)


try:
    repo = sys.argv[1]
    ReadMD(repo)
except IndexError:
    console.print("[yellow]Usage:[/yellow] \n py [green]readMd.py[/green] <REPO>")

