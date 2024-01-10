"""
Copyright 2023 Erdinc Kaya
DESCRIPTION:
    Simple CLI tool to deploy my lab VMs
USAGE EXAMPLE:
    > python main.py create template|vm --target pve --host <target-host>
"""


# ::IMPORTS ------------------------------------------------------------------------ #

# cli framework - https://pypi.org/project/typer/
import os
from typing import Annotated, List
import typer

import urllib3

# package for reading details about this package
from .common import prepare_vm

from . import config
from . import create
from . import delete
from . import ezua
from . import ezdf
from .parameters import ez_product

app = typer.Typer(add_completion=True, no_args_is_help=True)

# ::SETUP -------------------------------------------------------------------------- #
app = typer.Typer(add_completion=True, no_args_is_help=True)

# ::SETUP SUBPARSERS --------------------------------------------------------------- #
app.add_typer(
    config.app,
    no_args_is_help=True,
    name="config",
    short_help="manage deployment settings",
)
app.add_typer(
    create.app,
    no_args_is_help=True,
    name="create",
    short_help="create templates and VMs",
)
app.add_typer(
    delete.app,
    no_args_is_help=True,
    name="delete",
    short_help="delete templates and VMs",
)

app.add_typer(
    ezua.app,
    no_args_is_help=True,
    name="ezua",
    short_help="Manage Ezmeral Unified Analytics installation",
)

app.add_typer(
    ezdf.app,
    no_args_is_help=True,
    name="ezdf",
    short_help="Manage Ezmeral Data Fabric installation",
)


# ::GLOBALS --------------------------------------------------------------------- #
PKG_NAME = "ezlab"


# ::CORE LOGIC --------------------------------------------------------------------- #
# ::CLI ---------------------------------------------------------------------------- #


@app.command()
def info():
    """print usage"""
    print(
        """
        Manage lab VMs for various platforms
        Select <target> parameters: 'pve' | 'vmware'
        Provide credentials: <host> <username> <password>
        <config> get/set: manage preferences and network/storage,
        <create> vm/template: deploy VMs based on template,
        <delete> vm/template: delete selected VMs and templates,
        <install> df/ua: install Ezmeral product,
        <prepare>: prepare VM(s) for Ezmeral product,
        <info>: print this message
        """
    )


@app.command()
def prepare(
    vm_ip: Annotated[str, typer.Option("--ip", "-i")],
    vm_name: Annotated[
        str, typer.Option("--name", "-n", help="short name for the host")
    ],
    product: Annotated[
        ez_product,
        typer.Option(
            "--product",
            "-p",
        ),
    ],
):
    """
    configure vm for given product
    """
    if prepare_vm(
        vm_name=vm_name,
        vm_ip=vm_ip,
        product_code=product,
    ):
        print(f"{vm_name} configured")


# ::EXECUTE ------------------------------------------------------------------------ #
def main() -> None:
    # Strongly discouraged
    urllib3.disable_warnings()
    # ensure the system is configured
    if not os.path.isfile("config.ini"):
        print("Configuration is required.")
        config.set()
    app()


# if __name__ == "__main__":  # ensure importing the script will not execute
#     main()
