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
import json
import logging
import os
import os.path
import tarfile

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
@click.argument('ref')
@click.option('--url', default=KodexaPlatform.get_url(), help='The URL to the Kodexa server')
@click.option('--token', default=KodexaPlatform.get_access_token(), help='Access token')
@pass_info
def get(_: Info, object_type: str, ref: str, url: str, token: str):
    """List the instance of the object type"""
    KodexaPlatform.set_url(url)
    KodexaPlatform.set_access_token(token)
    KodexaPlatform.get(object_type, ref)


@cli.command()
@click.argument('object_type')
@click.argument('ref')
@click.option('--url', default=KodexaPlatform.get_url(), help='The URL to the Kodexa server')
@click.option('--token', default=KodexaPlatform.get_access_token(), help='Access token')
@pass_info
def delete(_: Info, object_type: str, ref: str, url: str, token: str):
    """Delete object from the platform"""

    KodexaPlatform.set_url(url)
    KodexaPlatform.set_access_token(token)
    KodexaPlatform.delete(object_type, ref)


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
    print("Extension documentation has been successfully built :tada:")


@cli.command()
@click.option('--path', default=os.getcwd(), help='Path to folder container kodexa.yml (defaults to current)')
@click.option('--output', default=os.getcwd() + "/dist",
              help='Path to the output folder (defaults to dist under current)')
@click.option('--version', default=os.getenv('VERSION'), help='Version number (defaults to 1.0.0)')
@pass_info
def package(_: Info, path: str, output: str, version: str):
    """Load metadata"""
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
