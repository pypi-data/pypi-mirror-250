#!/usr/bin/env python3
"""
Collection of reusable helper functions
"""

import concurrent.futures
import json
import os
from typing import Dict, List, Union

from dotenv import load_dotenv
from iap_cli.commands.config.add import add_credentials, add_server
from iap_cli.config import APP_DIR, CREDENTIALS_FILEPATH, INVENTORY_FILEPATH
from iap_cli.enums import Applications
from iap_sdk import Iap


def clear_screen() -> None:
    """Clears terminal screen."""
    os.system("clear")


def complete_application_name(incomplete: str):
    """
    Function used for Typer-cli autocompletion of application names.

    :param incomplete: Beginning character(s) of the application name
    """
    for app in Applications:
        if app.name.startswith(incomplete):
            yield (app.name)


def complete_server_name(incomplete: str):
    """
    Function used for Typer-cli autocompletion of server names.

    :param incomplete: Beginning character(s) of the server name
    """
    SERVERS = get_all_servers_from_inventory()
    for name in SERVERS.keys():
        if name.startswith(incomplete):
            yield (name)


def get_all_servers_from_inventory() -> Dict:
    """
    Helper function to load the entire inventory.json file
    """
    APP_DIR.mkdir(parents=False, exist_ok=True)
    if not INVENTORY_FILEPATH.exists():
        add_server()
    with open(f"{INVENTORY_FILEPATH}", "r") as file:
        inventory = json.load(file)
    return inventory


def get_client(host: str) -> Iap:
    """Create Iap connection instance"""
    # load environment vars
    APP_DIR.mkdir(parents=False, exist_ok=True)
    if not CREDENTIALS_FILEPATH.exists():
        add_credentials()
    load_dotenv(dotenv_path=CREDENTIALS_FILEPATH)
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    api = Iap(
        host=host,
        username=username,
        password=password,
        verify=False,
    )
    return api


def get_servers_from_inventory(server_group: str) -> List[str]:
    """
    Helper function to load the IAP server name(s) from inventory.json

    :param server_group: Friendly name of the server/cluster as defined in your inventory.json file
    """
    APP_DIR.mkdir(parents=False, exist_ok=True)
    if not INVENTORY_FILEPATH.exists():
        add_server()
    with open(f"{INVENTORY_FILEPATH}", "r") as file:
        inventory = json.load(file)
        servers = inventory[server_group]
        if isinstance(servers, str):
            servers = [servers]
    return servers


def runner(function: str, hosts: Union[List[str], str], args=None) -> List[Dict]:
    """
    Generic function that allows for running other functions in parallel.
    Will return the following response format: [{"host": "servername": "response":[]}]

    :param function: The name of the target function to be run concurrently.
    :param hosts: List of IAP/IAG hostnames.
    :param args: Arguments to be provided to the target function.
    """
    # check if single host or multiple hosts. Turn single host str into list
    if isinstance(hosts, str):
        hosts = [hosts]
    output_data_list = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        if args:
            future_to_host = {
                executor.submit(function, host, args): host for host in hosts
            }
        else:
            future_to_host = {executor.submit(function, host): host for host in hosts}
        for future in concurrent.futures.as_completed(future_to_host):
            host = future_to_host[future]
            try:
                data = future.result()
                output_data_list.append({"host": host, "response": data})
            except Exception as exc:
                print("%r generated an exception: %s" % (host, exc))
    return output_data_list
