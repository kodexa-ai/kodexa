#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the Kodexa CLI, it can be used to allow you to work with an instance of the Kodexa platform.

It supports interacting with the API, listing and viewing components.  Note it can also be used to login and logout
"""
import json
import logging
import os
import os.path
import sys
import tarfile
from getpass import getpass
from typing import Optional

import click
import yaml
from rich import print

logging.root.addHandler(logging.StreamHandler(sys.stdout))

from kodexa import KodexaClient
from kodexa.platform.kodexa import ExtensionHelper, KodexaPlatform

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels


class Info(object):
    """An information object to pass data between CLI functions."""

    def __init__(self):  # Note: This object must have an empty constructor.
        """Create a new instance."""
        self.verbose: int = 0


# pass_info is a decorator for functions that pass 'Info' objects.
#: pylint: disable=invalid-name
pass_info = click.make_pass_decorator(Info, ensure=True)


def merge(a, b, path=None):
    "merges dictionary b into dictionary a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a


# Change the options to below to suit the actual options for your task (or
# tasks).
@click.group()
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
@pass_info
def cli(info: Info, verbose: int):
    # Use the verbosity count to determine the logging level...
    if verbose > 0:
        logging.root.setLevel(
            LOGGING_LEVELS[verbose]
            if verbose in LOGGING_LEVELS
            else logging.DEBUG
        )
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.root.getEffectiveLevel()})",
                fg="yellow",
            )
        )
    info.verbose = verbose


@cli.command()
@click.argument('id', required=True)
@click.option('--url', default=KodexaPlatform.get_url(), help='The URL to the Kodexa server')
@click.option('--token', default=KodexaPlatform.get_access_token(), help='Access token')
@pass_info
def project(_: Info, project_id: str, token: str, url: str):
    """
    Get all the details for a specific project
    """
    client = KodexaClient(url=url, access_token=token)
    project_instance = client.get_project(project_id)
    print(f"Name: [bold]{project_instance.name}[/bold]")
    print(f"Description: [bold]{project_instance.description}[/bold]\n")

    print("[bold]Document Stores[/bold]")
    project_instance.document_stores.print_table()
    print("[bold]Data Stores[/bold]")
    project_instance.data_stores.print_table()
    print("[bold]Data Structures[/bold]")
    project_instance.taxonomies.print_table()
    print("[bold]Assistants[/bold]")
    project_instance.assistants.print_table()


@cli.command()
@click.argument('ref', required=True)
@click.argument('path', required=True)
@click.option('--url', default=KodexaPlatform.get_url(), help='The URL to the Kodexa server')
@click.option('--token', default=KodexaPlatform.get_access_token(), help='Access token')
@pass_info
def upload(_: Info, ref: str, path: str, token: str, url: str):
    """
    Upload the contents of a file or directory to a Kodexa platform instance
    """

    client = KodexaClient(url=url, access_token=token)
    document_store = client.get_object_by_ref('store', ref)

    from kodexa.platform.client import DocumentStoreEndpoint
    if isinstance(document_store, DocumentStoreEndpoint):
        import glob
        for path_match in glob.glob(path):

            print(f"Uploading {path_match}")
            document_store.upload_file(path_match)

        print("Upload complete :tada:")
    else:
        print(f"{ref} is not a document store")


@cli.command()
@click.option('--org', help='The slug for the organization to deploy to', required=False)
@click.option('--slug', help='Override the slug for component (only works for a single component)', required=False)
@click.option('--version', help='Override the version for component (only works for a single component)',
              required=False)
@click.option('--file', help='The path to the file containing the object to apply')
@click.option('--update/--no-update', help='The path to the file containing the object to apply',
              default=False)
@click.option('--url', default=KodexaPlatform.get_url(), help='The URL to the Kodexa server')
@click.option('--token', default=KodexaPlatform.get_access_token(), help='Access token')
@click.option('--format', default=None, help='The format to input if from stdin (json, yaml)')
@click.option('--overlay', default=None, help='A JSON or YAML file that will overlay the metadata')
@pass_info
def deploy(_: Info, org: Optional[str], file: str, url: str, token: str, format=None, update: bool = False,
           version=None, overlay: Optional[str] = None, slug=None):
    """
    Deploy a component to a Kodexa platform instance from a file or stdin
    """

    client = KodexaClient(access_token=token, url=url)

    obj = None
    if file is None:
        print("Reading from stdin")
        if format == 'yaml' or format == 'yml':
            obj = yaml.safe_load(sys.stdin.read())
        elif format == 'json':
            obj = json.loads(sys.stdin.read())
        else:
            raise Exception("You must provide a format if using stdin")
    else:
        print("Reading from file", file)
        with open(file, 'r') as f:
            if file.lower().endswith('.json'):
                obj = json.load(f)
            elif file.lower().endswith('.yaml') or file.lower().endswith('.yml'):
                obj = yaml.safe_load(f)
            else:
                raise Exception("Unsupported file type")

    overlay_obj = None

    if overlay is not None:
        print("Reading overlay")
        if overlay.endswith('yaml') or overlay.endswith('yml'):
            overlay_obj = yaml.safe_load(sys.stdin.read())
        elif overlay.endswith('json'):
            overlay_obj = json.loads(sys.stdin.read())
        else:
            raise Exception("Unable to determine the format of the overlay file, must be .json or .yml/.yaml")

    if isinstance(obj, list):
        print(f"Found {len(obj)} components")
        for o in obj:

            if overlay_obj:
                o = merge(o, overlay_obj)

            component = client.deserialize(o)
            if org is not None:
                component.org_slug = org
            print(f"Deploying component {component.slug}:{component.version}")
            component.deploy(update=update)

    else:

        if overlay_obj:
            obj = merge(obj, overlay_obj)

        component = client.deserialize(obj)

        if version is not None:
            component.version = version
        if slug is not None:
            component.slug = slug
        if org is not None:
            component.org_slug = org
        print(f"Deploying component {component.slug}:{component.version}")
        log_details = component.deploy(update=update)
        for log_detail in log_details:
            print(log_detail)
    print("Deployed :tada:")


@cli.command()
@click.argument('execution_id', required=True)
@click.option('--url', default=KodexaPlatform.get_url(), help='The URL to the Kodexa server')
@click.option('--token', default=KodexaPlatform.get_access_token(), help='Access token')
@pass_info
def logs(_: Info, execution_id: str, url: str, token: str):
    """
    Get logs for an execution
    """
    client = KodexaClient(url=url, access_token=token)


@cli.command()
@click.argument('object_type', required=True)
@click.argument('ref', required=False)
@click.option('--url', default=KodexaPlatform.get_url(), help='The URL to the Kodexa server')
@click.option('--token', default=KodexaPlatform.get_access_token(), help='Access token')
@click.option('--query', default="*", help='Limit the results using a query')
@click.option('--path', default=None, help='JQ path to content you want')
@click.option('--format', default=None, help='The format to output (json, yaml)')
@click.option('--page', default=1, help='Page number')
@click.option('--pageSize', default=10, help='Page size')
@click.option('--sort', default=None, help='Sort by (ie. startDate:desc)')
@pass_info
def get(_: Info, object_type: str, ref: Optional[str], url: str, token: str, query: str, path: str = None, format=None,
        page: int = 1, pagesize: int = 10, sort: str = None):
    """
    List the instance of the object type
    """
    client = KodexaClient(url=url, access_token=token)

    from kodexa.platform.client import resolve_object_type
    object_name, object_metadata = resolve_object_type(object_type)

    if 'global' in object_metadata and object_metadata['global']:
        objects_endpoint = client.get_object_type(object_type)
        if ref and not ref.isspace():
            object_instance = objects_endpoint.get(ref)
            from rich.syntax import Syntax
            if format == 'json':
                print(Syntax(object_instance.json(indent=4), "json"))
            elif format == 'yaml':
                print(Syntax(object_instance.yaml(indent=4), "yaml"))
        else:
            objects_endpoint.print_table(query=query, page=page, pagesize=pagesize, sort=sort)
    else:

        if ref and not ref.isspace():

            if '/' in ref:
                object_instance = client.get_object_by_ref(object_metadata['plural'], ref)
                from rich.syntax import Syntax
                if format == 'json':
                    print(Syntax(object_instance.json(indent=4), "json"))
                elif format == 'yaml' or not format:
                    print(Syntax(object_instance.yaml(indent=4), "yaml"))
            else:

                organization = client.organizations.find_by_slug(ref)
                objects_endpoint = client.get_object_type(object_type, organization)
                objects_endpoint.print_table(query=query, page=page, pagesize=pagesize, sort=sort)
        else:

            print(f"You must provide a ref to get a specific object")


@cli.command()
@click.argument('ref', required=True)
@click.argument('query', default="*")
@click.option('--url', default=KodexaPlatform.get_url(), help='The URL to the Kodexa server')
@click.option('--token', default=KodexaPlatform.get_access_token(), help='Access token')
@click.option('--download/--no-download', default=False, help='Download the KDDB for the latest in the family')
@click.option('--download-native/--no-download-native', default=False, help='Download the native file for the family')
@click.option('--page', default=1, help='Page number')
@click.option('--pageSize', default=10, help='Page size')
@click.option('--sort', default=None, help='Sort by ie. name:asc')
@pass_info
def query(_: Info, query: str, ref: str, url: str, token: str, download: bool, download_native: bool, page: int,
          pagesize: int, sort: None):
    """
    Query the documents in a given document store
    """
    client = KodexaClient(url=url, access_token=token)
    from kodexa.platform.client import DocumentStoreEndpoint

    document_store: DocumentStoreEndpoint = client.get_object_by_ref('store', ref)
    if isinstance(document_store, DocumentStoreEndpoint):
        results = document_store.query(query, page, pagesize, sort)

    else:
        raise Exception("Unable to find document store with ref " + ref)

@cli.command()
@click.argument('project_id', required=True)
@click.option('--url', default=KodexaPlatform.get_url(), help='The URL to the Kodexa server')
@click.option('--token', default=KodexaPlatform.get_access_token(), help='Access token')
@click.option('--output', help='The path to export to')
@pass_info
def export_project(_: Info, project_id: str, url: str, token: str, output: str):
    client = KodexaClient(url, token)
    project_endpoint = client.projects.get(project_id)
    client.export_project(project_endpoint, output)


@cli.command()
@click.argument('org_slug', required=True)
@click.argument('path', required=True)
@click.option('--url', default=KodexaPlatform.get_url(), help='The URL to the Kodexa server')
@click.option('--token', default=KodexaPlatform.get_access_token(), help='Access token')
@pass_info
def import_project(_: Info, org_slug: str, url: str, token: str, path: str):
    print("Importing project from {}".format(path))

    client = KodexaClient(url, token)
    organization = client.organizations.find_by_slug(org_slug)

    print("Organization: {}".format(organization.name))
    client.import_project(organization, path)

    print("Project imported")


@cli.command()
@click.argument('project_id', required=True)
@click.argument('assistant_id', required=True)
@click.option('--url', default=KodexaPlatform.get_url(), help='The URL to the Kodexa server')
@click.option('--token', default=KodexaPlatform.get_access_token(), help='Access token')
@click.option('--file', help='The path to the file containing the event to send')
@click.option('--format', default=None, help='The format to use if from stdin (json, yaml)')
@pass_info
def send_event(_: Info, project_id: str, assistant_id: str, url: str, file: str, event_format: str, token: str):
    """Send an event to an assistant
    """

    client = KodexaClient(url, token)

    obj = None
    if file is None:
        print("Reading from stdin")
        if event_format == 'yaml':
            obj = yaml.parse(sys.stdin.read())
        elif event_format == 'json':
            obj = json.loads(sys.stdin.read())
        else:
            raise Exception("You must provide a format if using stdin")
    else:
        print("Reading event from file", file)
        with open(file, 'r') as f:
            if file.lower().endswith('.json'):
                obj = json.load(f)
            elif file.lower().endswith('.yaml'):
                obj = yaml.full_load(f)
            else:
                raise Exception("Unsupported file type")

    print("Sending event")
    from kodexa.platform.client import AssistantEndpoint
    assistant_endpoint: AssistantEndpoint = client.get_project(project_id).assistants.get(assistant_id)
    assistant_endpoint.send_event(obj)
    print("Event sent :tada:")


@cli.command()
@pass_info
@click.option('--python/--no-python', default=False, help='Print out the header for a Python file')
def platform(_: Info, python: bool):
    """
    Get the details for the Kodexa instance we are logged into
    """
    platform_url = KodexaPlatform.get_url()

    if platform_url is not None:
        print(f"Kodexa URL: {KodexaPlatform.get_url()}")
        print(f"Access Token: {KodexaPlatform.get_access_token()}")
        kodexa_version = KodexaPlatform.get_server_info()
        print(f"Version: {kodexa_version['version']}")
        print(f"Release: {kodexa_version['release']}")
        if python:
            print("\nPython example:\n\n")
            print(f"from kodexa import *")
            print(f"client = KodexaClient('{KodexaPlatform.get_url()}', '{KodexaPlatform.get_access_token()}')")
    else:
        print("Kodexa is not logged in")


@cli.command()
@click.argument('object_type')
@click.argument('ref')
@click.option('--url', default=KodexaPlatform.get_url(), help='The URL to the Kodexa server')
@click.option('--token', default=KodexaPlatform.get_access_token(), help='Access token')
@pass_info
def delete(_: Info, object_type: str, ref: str, url: str, token: str):
    """
    Delete the given resource (based on ref)
    """
    client = KodexaClient(url, token)
    client.get_object_by_ref(object_type, ref).delete()


@cli.command()
@pass_info
def login(_: Info):
    """Logs into the specified platform environment using the email address and password provided,
    then downloads and stores the personal access token (PAT) of the user.
    Once successfully logged in, calls to remote actions, pipelines, and workflows will be made to the
    platform that was set via this login function and will use the stored PAT for authentication.

    """
    try:
        kodexa_url = input("Enter the Kodexa URL (https://platform.kodexa.com): ")
        if kodexa_url == "":
            print("Using default as https://platform.kodexa.com")
            kodexa_url = "https://platform.kodexa.com"
        username = input("Enter your email: ")
        password = getpass("Enter your password: ")
    except Exception as error:
        print('ERROR', error)
    else:
        KodexaPlatform.login(kodexa_url, username, password)


@cli.command()
@pass_info
def version(_: Info):
    import pkg_resources
    print("Kodexa Version:", pkg_resources.get_distribution("kodexa").version)


@cli.command()
@click.option('--path', default=os.getcwd(), help='Path to folder container kodexa.yml (defaults to current)')
@click.option('--output', default=os.getcwd() + "/dist",
              help='Path to the output folder (defaults to dist under current)')
@click.option('--version', default=os.getenv('VERSION'), help='Version number (defaults to 1.0.0)')
@pass_info
def package(_: Info, path: str, output: str, version: str):
    """
    Package an extension pack based on the kodexa.yml file
    """
    metadata_obj = ExtensionHelper.load_metadata(path)
    print("Preparing to pack")
    try:
        os.makedirs(output)
    except OSError as e:
        import errno
        if e.errno != errno.EEXIST:
            raise

    metadata_obj['version'] = version if version is not None else '1.0.0'

    if 'source' in metadata_obj and 'location' in metadata_obj['source']:
        metadata_obj['source']['location'] = metadata_obj['source']['location'].format(**metadata_obj)

    versioned_metadata = os.path.join(output, f"{metadata_obj['slug']}-{metadata_obj['version']}.json")

    unversioned_metadata = os.path.join(output, "kodexa.json")
    with open(versioned_metadata, 'w') as outfile:
        json.dump(metadata_obj, outfile)

    from shutil import copyfile
    copyfile(versioned_metadata, unversioned_metadata)

    output_filename = f"{metadata_obj['slug']}-{metadata_obj['version']}.tar.gz"
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(output, arcname=os.path.basename(output))

    os.rename(output_filename, os.path.join(output, output_filename))

    print("Extension has been packaged :tada:")