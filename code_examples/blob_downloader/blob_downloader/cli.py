import click
from blob_downloader.version import __version__
from blob_downloader.settings import S
from typing import Any

logo = f"""

  ____  _       _       _____                      _                 _           
 |  _ \| |     | |     |  __ \                    | |               | |          
 | |_) | | ___ | |__   | |  | | _____      ___ __ | | ___   __ _  __| | ___ _ __ 
 |  _ <| |/ _ \| '_ \  | |  | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
 | |_) | | (_) | |_) | | |__| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   
 |____/|_|\___/|_.__/  |_____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   
                                                                                 
                                                                        v{__version__}                                                                              
    """


@click.version_option(package_name="blob_downloader", message=logo)
@click.group()
def cli(): ...


@click.group()
def settings():
    "Commands for the settings management"


@settings.command(name="set", short_help="Set a setting value")
@click.argument("name", type=str, required=True)
@click.argument("value", required=True)
def _set(name: str, value: Any):
    if name in S.model_fields:
        try:
            S.model_validate({name: value})
        except Exception as e:
            click.secho(e, fg="red")
            click.get_current_context().exit(2)
        else:
            ...


cli.add_command(settings)
