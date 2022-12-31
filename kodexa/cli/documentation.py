"""
Utilities to support generating documentation based on the metadata in a kodexa.yml
"""
import json
import os
import jinja2
from addict import Dict


def camel_to_kebab(s):
    """Convert a camel case string to a kebab case string

    Args:
      s: the string to convert

    Returns:

    """
    return ''.join(['-' + i.lower() if i.isupper() else i for i in s]).lstrip('-')


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
    components = document_component(metadata)

    write_template("index.j2", f"docs/overview", f"index.md", components)

    toc = "overview\n    index\n"

    toc = toc + "assistant\n"
    for assistantDefinition in components['assistantDefinitions']:
        toc += f"    {assistantDefinition}\n"

    toc = toc + "project-template\n"
    for projectTemplate in components['projectTemplates']:
        toc += f"    {projectTemplate}\n"

    toc = toc + "model-runtime\n"
    for projectTemplate in components['modelRuntimes']:
        toc += f"    {projectTemplate}\n"

    toc = toc + "taxonomy\n"
    for taxonomy in components['taxonomies']:
        toc += f"    {taxonomy}\n"

    toc = toc + "store\n"
    for store in components['stores']:
        toc += f"    {store}\n"

    toc = toc + "action\n"
    for action in components['actions']:
        toc += f"    {action}\n"

    toc = toc + "pipeline\n"
    for pipeline in components['pipelines']:
        toc += f"    {pipeline}\n"

    with open("docs/toc", "w") as text_file:
        text_file.write(toc)


def transform_taxons(taxons):
    """
    Transform the taxons into a format that works with our markdown helper

    Args:
      taxons: the taxons to transform

    Returns:

    """
    simple_taxons = []
    for taxon in taxons:
        simple_taxon = {
            'name': taxon['name'],
            'taxonType': taxon['type'],
            'description': taxon['description'] if 'description' in taxon else ''
        }

        if 'children' in taxon:
            simple_taxon['children'] = transform_taxons(taxon['children'])

        simple_taxons.append(simple_taxon)

    return simple_taxons


def transform_options(options):
    """
    Transform the options into a format that works with our markdown helper

    Args:
      options: the options to transform

    Returns:

    """
    simple_options = []
    for option in options:
        description = ""
        if option['required'] == True:
            description += "**Required**\n"

        if 'description' in option:
            description = description + option['description']

        if 'default' in option:
            description = description + f" \nDefault: {option['default']}"

        simple_option = {
            'name': option['name'],
            'description': description,
            'type': option['type']
        }

        if option['type'] == 'object':
            simple_option['children'] = transform_options(option['groupOptions'])

        simple_options.append(simple_option)

    return simple_options


def document_component(metadata):
    components = {
        'actions': [],
        'stores': [],
        'projectTemplates': [],
        'pipelines': [],
        'taxonomies': [],
        'assistantDefinitions': [],
        'modelRuntimes': [],
        'extensionPacks': []
    }

    if metadata.type == 'action':
        options = metadata.metadata.options
        print(json.dumps(options, indent=2))
        write_template("action.j2", f"docs/{camel_to_kebab(metadata.type)}", f"{metadata.slug}.md", metadata)
        components['actions'].append(f"{metadata.slug}")
        with open(f"docs/{camel_to_kebab(metadata.type)}/{metadata.slug}-options.json", "w") as options_file:
            options_file.write(json.dumps(transform_options(options), indent=2))

    if metadata.type == 'store':
        write_template("store.j2", f"docs/{camel_to_kebab(metadata.type)}", f"{metadata.slug}.md", metadata)
        components['stores'].append(f"{metadata.slug}")

    if metadata.type == 'projectTemplate':
        write_template("project-template.j2", f"docs/{camel_to_kebab(metadata.type)}", f"{metadata.slug}.md", metadata)
        components['projectTemplates'].append(f"{metadata.slug}")

    if metadata.type == 'extensionPack':
        write_template("extension-pack.j2", f"docs/{camel_to_kebab(metadata.type)}", f"{metadata.slug}.md", metadata)
        components['extensionPacks'].append(f"{metadata.slug}")

    if metadata.type == 'pipeline':
        write_template("pipeline.j2", f"docs/{camel_to_kebab(metadata.type)}", f"{metadata.slug}.md", metadata)
        components['pipelines'].append(f"{metadata.slug}")

    if metadata.type == 'taxonomy':
        write_template("taxonomy.j2", f"docs/{camel_to_kebab(metadata.type)}", f"{metadata.slug}.md", metadata)
        components['taxonomies'].append(f"{metadata.slug}")
        with open(f"docs/{camel_to_kebab(metadata.type)}/{metadata.slug}-structure.json", "w") as taxonomy_file:
            taxonomy_file.write(json.dumps(transform_taxons(metadata['taxons']), indent=2))

    if metadata.type == 'assistant':
        from kodexa.model.objects import AssistantDefinition
        write_template("assistant.j2", f"docs/{camel_to_kebab(metadata.type)}", f"{metadata.slug}.md",
                       AssistantDefinition.parse_obj(metadata))
        components['assistantDefinitions'].append(f"{metadata.slug}")
        with open(f"docs/{camel_to_kebab(metadata.type)}/{metadata.slug}-options.json", "w") as options_file:
            options_file.write(json.dumps(transform_options(metadata.options), indent=2))

        for event_type in metadata.eventTypes:
            with open(f"docs/{camel_to_kebab(metadata.type)}/{metadata.slug}-{event_type.name}-options.json",
                      "w") as options_file:
                options_file.write(json.dumps(transform_options(event_type.options), indent=2))

    if metadata.type == 'modelRuntime':
        write_template("model-runtime.j2", f"docs/{camel_to_kebab(metadata.type)}", f"{metadata.slug}.md", metadata)
        components['modelRuntimes'].append(f"{metadata.slug}")

    if 'services' in metadata:
        for service in metadata['services']:
            service_components = document_component(service)
            components['actions'] += service_components['actions']
            components['stores'] += service_components['stores']
            components['projectTemplates'] += service_components['projectTemplates']
            components['pipelines'] += service_components['pipelines']
            components['taxonomies'] += service_components['taxonomies']
            components['assistantDefinitions'] += service_components['assistantDefinitions']
            components['modelRuntimes'] += service_components['modelRuntimes']
            components['extensionPacks'] += service_components['extensionPacks']

    return components


def write_template(template, output_location, output_filename, service):
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
    processed_template = template.render({"service": service})

    from pathlib import Path
    Path(output_location).mkdir(parents=True, exist_ok=True)
    with open(output_location + "/" + output_filename, "w") as text_file:
        text_file.write(processed_template)
