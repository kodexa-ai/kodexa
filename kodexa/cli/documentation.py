import errno
import json
import os
from shutil import copyfile

import jinja2
from addict import Dict


def get_path():
    return os.path.abspath(__file__)


def get_template_env():
    cli_path = os.path.dirname(get_path())
    package_location = os.path.join(cli_path, "templates")
    template_loader = jinja2.FileSystemLoader(searchpath=package_location)
    return jinja2.Environment(loader=template_loader)


def generate_documentation(metadata):
    os.makedirs('docs', exist_ok=True)
    for service in metadata.services:
        write_template("action.j2", f"docs/{service.slug}.md", Dict(metadata), Dict(service))

        # additional_docs = "metadata/" + metadata['organizationSlug'] + "-" + service['slug'] + ".md"
        # if path.exists(additional_docs):
        #     with open(additional_docs, 'r') as additional_docs:
        #         additional_docs_md = additional_docs.read()
        #
        #         text_file.write("\n\n")
        #         text_file.write(additional_docs_md)

    write_template("readme.j2", "README.md", Dict(metadata))


def write_template(template, output_location, metadata, service=None):
    if service is None:
        service = {}
    template = get_template_env().get_template(template)
    processed_template = template.render({"metadata": metadata, "service": service})
    with open(output_location, "w") as text_file:
        text_file.write(processed_template)


def generate_site(metadata: Dict, base_dir: str, output_filename: str, url: str, output_json: str):
    import os
    try:
        os.makedirs(os.path.join(base_dir, metadata['version']))
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    releases = []

    release_file_path = os.path.join(base_dir, 'releases.json')
    if os.path.exists(release_file_path):
        with open(release_file_path) as f:
            releases = json.load(f)

    from datetime import datetime
    now = datetime.now()

    releases.append({
        'version': metadata['version'],
        'date': now.strftime("%d/%m/%Y %H:%M:%S")
    })

    copyfile(output_filename, os.path.join(base_dir, metadata['version'], os.path.basename(output_filename)))
    copyfile(output_json, os.path.join(base_dir, metadata['version'], os.path.basename(output_json)))

    write_template("releases.j2.html", os.path.join(base_dir, 'index.html'),
                   {'metadata': Dict(metadata), 'releases': releases})

    write_template("release.j2.html", os.path.join(base_dir, metadata['version'], 'index.html'),
                   {'metadata': Dict(metadata), 'releases': releases, 'path': os.path.basename(output_filename)})
