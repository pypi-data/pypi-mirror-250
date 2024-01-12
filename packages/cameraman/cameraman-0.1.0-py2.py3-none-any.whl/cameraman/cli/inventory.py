import re
import os
import yaml

import click

from .main import *
from .config import *


@main.group(context_settings=CONTEXT_SETTINGS)
@click.pass_obj
def inventory(env):
    """subcommands for manae workspaces for cameraman"""
    # banner("User", env.__dict__)
    pass


@inventory.command()
# @click.option("--addreses", default="192.168.22.[0-256]")
@click.option("--addreses", default="192.168.6.200")
@click.pass_obj
def reset(env, addreses):
    """Create a new inventory for cameraman"""
    # force config loading
    config.callback()
    INVENTORY = env.inventory
    API = env.api

    import requests
    from requests.auth import HTTPDigestAuth, HTTPBasicAuth

    def expand(addreses):
        return [addreses]

    def find_setting(host):
        for pattern, settings in INVENTORY.items():
            m = re.match(pattern, host)
            if m:
                cfg = m.groupdict()
                cfg.update(settings)
                return cfg

    def get_auth(settings):
        auth = settings.get("auth", "digest")
        username = settings.get("username", "")
        password = settings.get("password", "")

        return {
            "digest": HTTPDigestAuth(username, password),
            "basic": HTTPBasicAuth(username, password),
        }.get(auth)

    def get_api(settings):
        api = API.get(settings.get("api", "bosh"), {})
        return api

    def get_url(settings, cmd):
        url = settings.get("url", "https://{host}{command}")

        return url

    def get_command(settings, cmd):
        return get_api(settings).get(cmd)

    for host in expand(addreses):
        settings = find_setting(host)
        auth = get_auth(settings)
        url = get_url(settings, "reset")
        method, command = get_command(settings, "reset")
        _url = url.format(**locals())
        func = getattr(requests, method, requests.get)
        response = func(
            _url,
            auth=auth,
            verify=False,
        )

        # Check the response
        if response.status_code == 200:
            print("Request successful!")
            print("Response content:", response.text)
        else:
            print("Request failed. Status code:", response.status_code)


@inventory.command()
@click.pass_obj
def list(env):
    """List existing workspaces for cameraman"""
    # force config loading
    config.callback()

    # TODO: add your new workspace configuratoin folder here ...
