import click
from blob_downloader.version import __version__
from blob_downloader.settings import S
from typing import Any
from dotenv import set_key, unset_key, dotenv_values
from os.path import exists
from os import remove

logo = rf""" 

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
            set_key(S.model_config.get("env_file"), name, value)
            click.secho(f"Setting '{name}' successfully updated!", fg="green")
    else:
        click.secho(
            f"Setting '{name}' is not listed among the available settings.", fg="red"
        )
        click.get_current_context().exit(2)


@settings.command(help="Show the current values")
def show():
    click.echo("\n")
    for name, values in S.model_fields.items():
        default = values.default
        click.echo(f"{name}: ", nl=False)
        click.secho(getattr(S, name), fg="green", nl=False)
        click.echo(" (", nl=False)
        click.secho(f"{default}", fg="red", nl=False)
        click.echo(")")

    click.echo("\n")


def remove_env_file(ctx, param, value):
    """Remove the env file"""
    if not value or ctx.resilient_parsing:
        return
    if click.confirm("Are you sure you want to delete the .env file?", abort=True):
        env_path = S.model_config.get("env_file")
        if env_path and exists(env_path):
            remove(env_path)
            click.secho(f"File .env ({env_path}) removed correctly.")
        ctx.exit(0)


@settings.command(help="Unset a setting value")
@click.argument("name", type=str)
@click.option(
    "-a",
    "--all",
    is_flag=True,
    callback=remove_env_file,
    help="Restore all the settings.",
)
def unset(name):
    env_path = S.model_config.get("env_file")
    if name in S.model_fields:
        if name in dotenv_values(env_path):
            unset_key(env_path, name)
        click.secho(f"Setting '{name}' unset successfully.", fg="green")
    else:
        click.secho(f"Setting '{name}' does not exists.", fg="red")


cli.add_command(settings)
