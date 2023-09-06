import sys
try:
    from tqdm import tqdm
    import time
    import pyperclip
    import webbrowser
    import requests
    from test_utils.data import testModel
    import typer
    from enum import Enum
    from rich.console import Console
    from rich.panel import Panel
    from rich.box import SIMPLE_HEAVY
    from pathlib import Path
    import typing
    import subprocess
except ImportError as e:
    from test_utils.debug import logger
    logger.error(f"Failed importing dependencies ({e})")
    sys.exit(0)

# import logging 
from test_utils.debug import logger

# init rich console
console = Console()

# change all '--' to '-'
def token_normalize_func(value):
    if value.startswith('-'):
        return value.lstrip('-')
    return value

CONTEXT_SETTINGS = dict(help_option_names=['-h', '-help'], token_normalize_func=token_normalize_func)

cli = typer.Typer(
    help=' CLI tool 🛠️ to test sentzi backend ',
    add_completion=False,
    rich_markup_mode="rich",
    context_settings=CONTEXT_SETTINGS,
    epilog="Made with ❤️ by [bright_cyan]sreezx[/bright_cyan] [bright_green]@github.com/sreezx[/bright_green]"
    )

# create output mode class
class OutputMode(str, Enum):
    show = "show"
    hidden = "hidden"
    scroll = "scroll"

# create open class
class Open(str, Enum):
    st_app_local = "st-app:local"
    st_app_cloud = "st-app:cloud"
    repo = "repo"
    hg_space = "hgf-space"

def opens(
        method : Open,
        log : bool
) -> (typing.Callable | None):
    def on_enter(link : str, again : bool = False) -> None:
        """ Open webbrowser on enter """
        if not again:
            console.print(
                Panel("To [blue]locate[/blue] the link in your default webbrowser press '[yellow]enter[/yellow]' . "
                "Press '[yellow]q[/yellow]' to exit ."
                ,box=SIMPLE_HEAVY)
                )
        def Prompt() -> str:
            ask = console.input(" : ")
            return ask
        prompt = Prompt()
        if prompt in [""]:
            webbrowser.open(link)
            if log:
                logger.success("Link opened in browser ! ✨")

        elif prompt.lower() in ["q"]:
            sys.exit(0)

        else:
            on_enter(link,again=True)
    def if_repo() -> None:
        pyperclip.copy("https://github.com/sreezx/Sentzi")
        logger.success("Repo link copied to clipboard [link : https://github.com/sreezx/Sentzi] ✨")
        on_enter("https://github.com/sreezx/Sentzi")
    def if_st_local() -> None:
        logger.debug("Running bat file to connect with 'run.ps1' ... ")
        subprocess.run(f'{Path().cwd() / "bin/do.bat"}') # run the bat file
    def if_st_cloud() -> None:
        pyperclip.copy("https://sentzi.streamlit.app/")
        logger.success("App link copied to clipboard [link : https://sentzi.streamlit.app/] ✨")
        on_enter("https://sentzi.streamlit.app/")
    def HgF() -> None:
        pyperclip.copy("https://huggingface.co/spaces/Sreezx/Sentzi")
        logger.success("Hugging Face Space link copied to clipboard [link : https://huggingface.co/spaces/Sreezx/Sentzi] ✨")
        on_enter("https://huggingface.co/spaces/Sreezx/Sentzi")
    
    FuncsDict = {
        "st-app:local" : lambda : if_st_local(),
        "st-app:cloud" : lambda : if_st_cloud(),
        "repo" : lambda : if_repo(),
        "hgf-space" : lambda : HgF()
    }
    return FuncsDict.get(method.value, lambda : None)

def show_version(
        log : bool,
):
    version_url = "https://cdn.jsdelivr.net/gh/sreezx/Sentzi/version"
    if log:
        logger.debug(f"Called 'sentzi-test.py {sys.argv[1:]}' ")
        logger.info(f"Getting version info from : '{version_url}'")

    # Create a tqdm progress bar
    try:
        version = requests.get(version_url, stream=True)
    except (requests.HTTPError or requests.ConnectionError):
        if log:
            logger.error("Failed connecting to server ! Make sure you have an active internet connection .")
        sys.exit(0)
    total_size = int(version.headers.get('content-length', 0))

    with tqdm(total=total_size, unit='B', unit_scale=True, desc="Getting version info",ncols=80) as pbar:
        with open('temp_version.txt', 'wb') as f:
            for data in version.iter_content(chunk_size=1024):
                time.sleep(0.5) # delay the bar
                pbar.update(len(data))  # Update the progress bar
                f.write(data) # write the version

    # show as a panel
    console.print(
        Panel(
            f"[blue]sentzi[/blue] 🏷️ [yellow]{Path('temp_version.txt').read_text(encoding='utf-8')}[/yellow] "
            ,expand=False,box=SIMPLE_HEAVY)
                )
    if log:
        logger.info('Deleting the temporary version file (temp_version.txt)')
    # delete the file
    Path('temp_version.txt').unlink(missing_ok=True)


# flags
@cli.callback(invoke_without_command=True,no_args_is_help=True)
def no_cmds(
    version : typing.Optional[bool] = typer.Option(
        None,
        '-version',
        '-v',
        is_eager=True,
        is_flag=True,
        help='Show version and exit .'
        ),
    log : typing.Optional[bool] = typer.Option(
        True,
        '-log/-no-log','-L/-nL',
        is_eager=True,
        is_flag=True,
        help="Enable or disable logging .", 
        show_default=True
        ),
    With : typing.Optional[str] = typer.Option(
        None,
        '-with',
        '-W',
        help="Get the sentiment of a text or from a text file. To analyze "
        "external datasets enter '[magenta]ext.data[/magenta]'",
        show_default=False,
        metavar=" PATH | STR | 'ext.data' ",
        rich_help_panel="'With' Options"
    ),
    save_json : typing.Optional[bool] = typer.Option(
        None,
        '-save',
        '-S',
        is_eager=False,
        is_flag=True,
        help="Save '[blue]With[/blue]' result to a '[magenta]json[/magenta]' file .",
        rich_help_panel="'With' Options"
        ),
    output : typing.Optional[OutputMode] = typer.Option(
        OutputMode.show.value,
        '-output',
        '-o',
        case_sensitive=False,
        show_default=True,
        help="Different modes to display the '[blue]With[/blue]' result. "
        "The default way is '[yellow]show[/yellow]'. '[yellow]hidden[/yellow]' hides"
        " the result completely. To view large results give '[yellow]scroll[/yellow]' as the mode . ",
        rich_help_panel="'With' Options"
    ),
    N : typing.Optional[int] = typer.Option(
        1,
        '-n',
        '-N',
        show_default=True,
        max=20,
        min=1,
        help="Number of reviews to select from the external dataset . Max is '20' and Min '1' .",
        rich_help_panel="'With' Options"
    ),
    _open : typing.Optional[Open] = typer.Option(
        None,
        '-open',
        '-!',
        case_sensitive=False,
        help="To run main application locally just enter '[yellow]-! st-app:local[/yellow]' . "
        " To run from the [magenta]Streamlit[/magenta] cloud use '[yellow]-! st-app:cloud[/yellow]' ."
        "For opening the official [magenta]github[/magenta] repo enter '[yellow]-! repo[/yellow]'"
        ". Another site you can open is the official [magenta]Hugging Face Space[/magenta] of '[cyan]sentzi[/cyan]' , using '[yellow]-! hg-space[/yellow]' ")
):
    flags = {
        version : lambda : show_version(log),
        With : lambda : testModel(With, log,save_json,output,N),
        _open : lambda : opens(_open, log)(),
    }
    # parse the flags
    for flag in flags.keys():
        if flag:
            flags.get(flag,lambda : None)() # execute the flag






    