from typing import Dict, List

import typer
from iap_cli.models.iap import (
    AdaptersHealthGetResponse,
    AdaptersHealthResult,
    ApplicationsHealthGetResponse,
    ApplicationsHealthResult,
)
from iap_cli.utils import (
    complete_server_name,
    get_client,
    get_servers_from_inventory,
    runner,
)
from rich import print
from rich.console import Console
from rich.table import Table

get_app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Get resources from your IAP server.",
)
console = Console()


def get_adapters_health(host: str) -> AdaptersHealthResult:
    """
    Get the health of all adapters. Used for the Adapters Status Report

    :param host: Server hostname/FQDN.
    """
    api = get_client(host)
    try:
        response = api.core.get_adapters_health()
        results = AdaptersHealthGetResponse(**response)
        return results.results
    except Exception as e:
        print(e)


def get_applications_health(host: str) -> ApplicationsHealthResult:
    """
    Get the health of all applications. Used for the Applications Status Report

    :param host: Server hostname/FQDN.
    """
    api = get_client(host)
    try:
        response = api.core.get_applications_health()
        results = ApplicationsHealthGetResponse(**response)
        return results.results
    except Exception as e:
        print(e)


@get_app.command("adapters")
def adapters(
    hosts: str = typer.Argument(
        ..., help="The target IAP server(s).", autocompletion=complete_server_name
    )
) -> AdaptersHealthResult:
    """Get the health of all [bold]adapters[/bold] for one or more servers."""
    hosts = get_servers_from_inventory(hosts)
    try:
        data = runner(get_adapters_health, hosts)
        render_adapter_report(data)
    except Exception as e:
        print(e)


@get_app.command("applications")
def applications(
    hosts: str = typer.Argument(
        ..., help="The target IAP server(s).", autocompletion=complete_server_name
    )
) -> ApplicationsHealthResult:
    """Get the health of all [bold]applications[/bold] for one more servers."""
    hosts = get_servers_from_inventory(hosts)
    try:
        data = runner(get_applications_health, hosts)
        render_application_report(data)
    except Exception as e:
        print(e)


def render_adapter_report(data: List[Dict]) -> None:
    """
    Render Adapter Status Report table using the 'rich' package

    :param data: API results response returned by the 'runner' helper function.
    """
    columns = ["Package ID", "Adapter ID", "State", "Connection"]
    for d in data:
        table = Table(title=f"Adapter Status Report {d['host']}")
        td = d["response"]
        for column in columns:
            table.add_column(column, justify="left", no_wrap=True)
        for row in td:
            table.add_row(row.package_id, row.id, row.state, row.connection["state"])
        console.print()
        console.print(table)


def render_application_report(data: List[Dict]) -> None:
    """
    Render Application Status Report table using the 'rich' package

    :param data: API results response returned by the 'runner' helper function.
    """
    columns = ["Package ID", "App ID", "State"]
    for d in data:
        table = Table(title=f"Application Status Report {d['host']}")
        td = d["response"]
        for column in columns:
            table.add_column(column, justify="left", no_wrap=True)
        for row in td:
            table.add_row(row.package_id, row.id, row.state)
        console.print()
        console.print(table)
