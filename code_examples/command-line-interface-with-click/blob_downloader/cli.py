import click
from blob_downloader.version import __version__
from blob_downloader.settings import S
from blob_downloader.cli_utils import read_settings_file, update_settings_file
from typing import Any
logo = fr""" 

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
    """Groups of commands for settings management"""

@settings.command(name="set", help="Set a setting value")
@click.argument("name", type=str)
@click.argument("value")
def _set(name, value):
    if name in S.model_fields:
        try:
            S.model_validate({name: value})
        except Exception as e:
            click.secho(e, fg="red")
            click.get_current_context().exit(2)
        else:
            update_settings_file(name, value)
            click.secho(f"Setting '{name}' successfully updated!", fg="green")
    else:
        click.secho(f"Setting '{name}' is not listed among the available settings.", fg="red")
        click.get_current_context().exit(2)

@settings.command(help="Show the current values")
def show():
    ...

@settings.command(help="Unset a setting value")
def unset():
    ...

cli.add_command(settings)
