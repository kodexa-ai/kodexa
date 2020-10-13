#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the entry point for the command-line interface (CLI) application.

Itcan be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.

.. currentmodule:: dharma_cli.cli
.. moduleauthor:: Kodexa, Inc <support@kodexa.com>
"""
import logging
import os
import sys

import click
from rich import print
from rich.table import Table

from kodexa.cloud.kodexa import ExtensionHelper, KodexaPlatform

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels

DEFAULT_COLUMNS = {
    'extensionPacks': [
        'orgSlug',
        'slug',
        'name',
        'description',
        'type',
        'status'
    ],
    'default': [
        'orgSlug',
        'slug',
        'name',
        'description',
        'type'
    ]
}

OBJECT_TYPES = {
    "extensionPacks": {
        "name": "extension pack",
        "plural": "extension packs"
    },
    "pipelines": {
        "name": "pipelines",
        "plural": "pipelines"
    },
    "actions": {
        "name": "action",
        "plural": "actions"
    }
}


def resolve_object_type(obj_type):
    hits = []
    keys = []
    for target_type in OBJECT_TYPES.keys():
        if obj_type in target_type:
            hits.append(OBJECT_TYPES[target_type])
            keys.append(target_type)

    if len(hits) == 1:
        return keys[0], hits[0]

    if len(hits) == 0:
        print(":exclaimation: Unable to find object type {obj_type}")
        sys.exit(1)
    else:
        print(f":exclaimation: To many potential matches for object type ({','.join(keys)}")
        sys.exit(1)


class Info(object):
    """An information object to pass data between CLI functions."""

    def __init__(self):  # Note: This object must have an empty constructor.
        """Create a new instance."""
        self.verbose: int = 0


# pass_info is a decorator for functions that pass 'Info' objects.
#: pylint: disable=invalid-name
pass_info = click.make_pass_decorator(Info, ensure=True)


# Change the options to below to suit the actual options for your task (or
# tasks).
@click.group()
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
@pass_info
def cli(info: Info, verbose: int):
    """Run Kodexa."""
    # Use the verbosity count to determine the logging level...
    if verbose > 0:
        logging.basicConfig(
            level=LOGGING_LEVELS[verbose]
            if verbose in LOGGING_LEVELS
            else logging.DEBUG
        )
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )
    info.verbose = verbose


@click.option('--path', default=os.getcwd(), help='Path to folder containing kodexa.yml')
@click.option('--url', default=KodexaPlatform.get_url(), help='The URL to the Kodexa server')
@click.option('--org', help='The slug for the organization to deploy to')
@click.option('--token', default=KodexaPlatform.get_access_token(), help='Access token')
@cli.command()
@pass_info
def deploy(_: Info, path: str, url: str, org: str, token: str):
    """Deploy extension pack to an Kodexa platform instance"""

    print("Starting deployment from path", path)
    KodexaPlatform.set_url(url)
    KodexaPlatform.set_access_token(token)

    if '://' in path:
        print("Deploying from URI", path)
        KodexaPlatform.deploy_extension_from_uri(path, org)
    else:
        print("Deploying local metadata from", path)
        metadata = ExtensionHelper.load_metadata(path)
        metadata['orgSlug'] = org;
        KodexaPlatform.deploy_extension(metadata)
    print("Deployed extension pack :tada:")


@cli.command()
@click.argument('object_type')
@click.argument('organization_slug')
@click.option('--url', default=KodexaPlatform.get_url(), help='The URL to the Kodexa server')
@click.option('--token', default=KodexaPlatform.get_access_token(), help='Access token')
@pass_info
def get(_: Info, object_type: str, organization_slug: str, url: str, token: str):
    """List the instance of the object type"""
    KodexaPlatform.set_url(url)
    KodexaPlatform.set_access_token(token)
    object_type, object_type_metadata = resolve_object_type(object_type)
    objects = KodexaPlatform.list_objects(organization_slug, object_type)

    cols = DEFAULT_COLUMNS['default']

    if object_type in DEFAULT_COLUMNS:
        cols = DEFAULT_COLUMNS[object_type]

    print("\n")
    table = Table(title=f"Listing {object_type_metadata['plural']}")
    for col in cols:
        table.add_column(col)
    for object_dict in objects['content']:
        row = []

        for col in cols:
            row.append(object_dict[col] if col in object_dict else '')
        table.add_row(*row)

    print(table)


@cli.command()
@click.argument('object_type')
@click.argument('organization_slug')
@click.argument('slug')
@click.option('--url', default=KodexaPlatform.get_url(), help='The URL to the Kodexa server')
@click.option('--token', default=KodexaPlatform.get_access_token(), help='Access token')
@pass_info
def delete(_: Info, object_type: str, organization_slug: str, slug: str, url: str, token: str):
    """Delete object from the platform"""
    object_type, object_type_metadata = resolve_object_type(object_type)

    print(f"Deleting {object_type_metadata['name']} [bold]{organization_slug}/{slug}[/bold]")
    KodexaPlatform.set_url(url)
    KodexaPlatform.set_access_token(token)
    try:
        KodexaPlatform.delete_object(organization_slug, slug, object_type)
        print(f"Deleted {object_type_metadata['name']} [bold]{organization_slug}/{slug}[/bold] :tada:")
    except:
        print(f"\n:exclamation: Failed to delete {object_type_metadata['name']} [{sys.exc_info()[0]}]")


@cli.command()
@click.option('--path', default=os.getcwd(), help='Path to folder container kodexa.yml')
@pass_info
def metadata(_: Info, path: str):
    """Load metadata"""
    metadata = ExtensionHelper.load_metadata(path)
    print(f"Metadata loaded")


@cli.command()
@click.option('--path', default=os.getcwd(), help='Path to folder container kodexa.yml')
@pass_info
def document(_: Info, path: str):
    """Load metadata"""
    metadata = ExtensionHelper.load_metadata(path)
    print("Metadata loaded")
    from kodexa.cli.documentation import generate_documentation
    generate_documentation(metadata)
    print("Documentation has been successfully built :tada:")
