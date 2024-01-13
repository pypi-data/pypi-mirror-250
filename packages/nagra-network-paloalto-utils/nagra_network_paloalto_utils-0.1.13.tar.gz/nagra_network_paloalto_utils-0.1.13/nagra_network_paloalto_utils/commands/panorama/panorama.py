import ast
import logging

import click

from nagra_network_paloalto_utils.utils.locking_panorama import try_lock, unlock_pano
from nagra_network_paloalto_utils.utils.panorama import (
    Panorama,
    commit,
    push,
)

log = logging.getLogger(__name__)


@click.command(
    "lock",
    help="""\
Lock Palo Alto Panorama.
The command takes a json-formatted list of firewall to lock. (default to all)""",
)
@click.argument(
    "firewalls",
    envvar="FIREWALLS",
    type=ast.literal_eval,
    default="""["DG1_GLOBAL"]""",
)
@click.pass_obj
def cmd_lock(obj, firewalls):
    all_firewalls = "DG1_GLOBAL" in firewalls
    if not try_lock(
        obj.URL, obj.API_KEY, firewalls=firewalls, all_firewalls=all_firewalls
    ):
        exit(1)


@click.command(
    "unlock",
    help="""\
Unlock Palo Alto Panorama.
The command takes a json-formatted list of firewall to lock. (default to all)""",
)
@click.argument(
    "firewalls",
    envvar="FIREWALLS",
    type=ast.literal_eval,
    default="""["DG1_GLOBAL"]""",
)
@click.pass_obj
def cmd_unlock(obj, firewalls):
    panorama_instance = Panorama(obj.URL, api_key=obj.API_KEY)
    all_firewalls = "DG1_GLOBAL" in firewalls
    # firewalls = ["shared"] if "DG1_GLOBAL" in firewalls else firewalls  # TODO: check if it makes sense
    # comment=f"Terraform pipeline {obj.CI_COMMIT_REF_NAME} {obj.CI_PROJECT_TITLE}"
    if not unlock_pano(panorama_instance, firewalls, all_firewalls=all_firewalls):
        exit(1)


@click.command("commit", help="Commit changes to Palo Alto Panorama")
@click.option(
    "--admin-name",
    "commiter_name",
    envvar="PANOS_ADMIN_NAME",
    help="The admin name under which to commit",
    required=True,
)
@click.option(
    "--devicegroups", "devicegroups", type=ast.literal_eval, default="['DG1_GLOBAL']"
)
@click.option("--branch")
@click.option("--push", type=bool, is_flag=True, default=False)
@click.pass_obj
def cmd_commit(obj, commiter_name, devicegroups, branch, push):
    """
    makes a partial commit under the admin name

    :return:
    """
    description = "Automatic commit from {} {}.(Commit SHA : {})".format(
        obj.CI_PROJECT_TITLE,
        obj.CI_COMMIT_REF_NAME,
        obj.CI_COMMIT_SHA,
    )

    res = commit(
        obj.URL,
        obj.API_KEY,
        commiter_name,
        description=description,
    )
    if res in ("fail", "error"):
        log.error(
            "Error. This is most likely because someone else is performing maintenance on the firewall."
            " You will need to manually commit-all",
        )
        exit(1)
    if res == "success":
        log.info("Commit done.")
        if push:
            log.info(f"Pushing the config to {devicegroups} !")
            error = push(obj.URL, obj.API_KEY, devicegroups, branch)
            exit(1 if error else 0)
        return
    if res == "unchanged":
        log.info("Same configuration nothing to commit")
        # We should revert the changes..
        # revert_config(obj.URL, obj.API_KEY, commiter_name)
        return


@click.command("push", help="Push changes to Firewalls")
@click.option(
    "--devicegroups", "devicegroups", type=ast.literal_eval, default="['DG1_GLOBAL']"
)
@click.pass_obj
def cmd_push(obj, devicegroups):
    """
    makes a partial commit under the admin name

    :return:
    """
    # all_firewalls = not firewalls or "DG1_GLOBAL" in firewalls
    error = push(obj.URL, obj.API_KEY, devicegroups)
    exit(1 if error else 0)
