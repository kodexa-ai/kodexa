"""
Utilities to support generating documentation based on the metadata in a kodexa.yml
"""
import json
import os
import jinja2
from addict import Dict


def get_path():
    """Gets the path of the documentation
    
    :return: the path of this module file

    Args:

    Returns:

    """
    return os.path.abspath(__file__)


def get_template_env():
    """Get the Jinja2 template environmnet
    
    :return:

    Args:

    Returns:

    """
    cli_path = os.path.dirname(get_path())
    package_location = os.path.join(cli_path, "templates")
    template_loader = jinja2.FileSystemLoader(searchpath=package_location)
    return jinja2.Environment(loader=template_loader, autoescape=True)


def generate_documentation(metadata):
    """Given the metadata object from a kodexa.yml generate the documentation

    Args:
      metadata:Dict: A dictionary of the metadata

    """
    os.makedirs('docs', exist_ok=True)

    if metadata.type == 'action':
        options = metadata.metadata.options
        print(json.dumps(options, indent=2))
        write_template("options.j2", f"docs/{metadata.type}-{metadata.slug}/docs/", "options.md", metadata, options)
        write_template("index.j2", f"docs/{metadata.type}-{metadata.slug}/docs/", "index.md", metadata, options)
        write_template("mkdocs.j2", f"docs/{metadata.type}-{metadata.slug}/", "mkdocs.yaml", metadata, options)

    if 'services' in metadata:
        for service in metadata['services']:
            generate_documentation(service)


def write_template(template, output_location, output_filename, service, options):
    """
    Write the given template out to a file

    Args:
      template: the name of the template
      output_location: the location to write the output
      output_filename: the name of the output file
      service: the service metadata
      options: the options for the service

    """
    if service is None:
        service = {}
    template = get_template_env().get_template(template)
    from kodexa.model.objects import Option
    complete_options = [Option.parse_obj(option) for option in options]
    processed_template = template.render({"service": service, "options": complete_options})

    from pathlib import Path
    Path(output_location).mkdir(parents=True, exist_ok=True)
    with open(output_location + "/" + output_filename, "w") as text_file:
        text_file.write(processed_template)
