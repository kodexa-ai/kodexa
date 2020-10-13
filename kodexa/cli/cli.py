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

import click
from rich import print

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
    """Run dharma."""
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
    print("Deployed extension")


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
    objects = KodexaPlatform.list_objects(organization_slug, object_type)

    cols = DEFAULT_COLUMNS['default']

    if object_type in DEFAULT_COLUMNS:
        cols = DEFAULT_COLUMNS[object_type]

    from rich.table import Table

    table = Table(title=object_type)
    for col in cols:
        table.add_column(col)
    for object_dict in objects['content']:
        row = []

        for col in cols:
            row.append(object_dict[col] if col in object_dict else '')
        table.add_row(*row)

    from rich import print
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
    print(f"Deleting {object_type} {slug} in organization {organization_slug}")
    KodexaPlatform.set_url(url)
    KodexaPlatform.set_access_token(token)
    KodexaPlatform.delete_object(organization_slug, slug, object_type)
    click.echo(f"Deleted {object_type} {organization_slug}/{slug}")


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
    print("[green]Metadata loaded :tada: [/green]")
    from kodexa.cli.documentation import generate_documentation
    generate_documentation(metadata)
    print("[green]Documentation has been successfully built[/green]")
