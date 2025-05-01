import yaml
import os
import glob
import logging
import json
from kodexa import KodexaClient

logger = logging.getLogger(__name__)


class ManifestManager:
    """
    A class to manage the manifests for deploying and monitoring
    Kodexa use-cases
    """

    def __init__(self, kodexa_client: KodexaClient):
        self.kodexa_client = kodexa_client

    @staticmethod
    def read_manifest(manifest_path: str) -> list:
        """
        Read and parse a YAML manifest file and extract resource paths.

        Args:
            manifest_path (str): Path to the YAML manifest file.

        Returns:
            list: List of resource paths extracted from the manifest file.
                  Returns an empty list if 'resource-paths' key is not present
                  or the file doesn't exist.
        """
        if not os.path.exists(manifest_path):
            logger.warning(f"Manifest file not found: {manifest_path}")
            return []
        try:
            with open(manifest_path, 'r') as file:
                manifest = yaml.safe_load(file)
            # Support 'resource-paths' as the primary key
            return manifest.get('resource-paths', [])
        except Exception as e:
            logger.error(
                f"Failed to read or parse manifest {manifest_path}: {e}",
                exc_info=True
            )
            return []

    def deploy_from_manifest(self, manifest_path: str,
                             org_slug: str | None = None):
        """
        Deploys all resources listed in a manifest file.

        Args:
            manifest_path (str): The path to the manifest file.
            org_slug (str | None): The organization slug to deploy to. If None,
                                   uses the default org from the client.
        """
        logger.info(
            f"Starting deployment from manifest {manifest_path} "
            f"to organization {org_slug}"
        )
        resource_paths = self.read_manifest(manifest_path)
        abs_manifest_path = os.path.abspath(manifest_path)
        manifest_dir = os.path.dirname(abs_manifest_path)
        original_cwd = os.getcwd()
        deployed_count = 0

        try:
            # Change to manifest directory to resolve relative paths
            os.chdir(manifest_dir)

            for resource_pattern in resource_paths:
                # Use glob to find matching files
                resource_files = glob.glob(resource_pattern, recursive=True)

                if not resource_files:
                    logger.warning(
                        f"No files found matching pattern '{resource_pattern}' "
                        f"relative to {manifest_dir}"
                    )
                    continue

                for rel_path in resource_files:
                    # Resolve absolute path based on current directory
                    abs_path = os.path.abspath(rel_path)
                    logger.info(f"Processing resource file: {abs_path}")
                    resource_dir = os.path.dirname(abs_path)

                    # Temporarily change to resource file's directory
                    # This helps with relative paths in the resource definition
                    os.chdir(resource_dir)

                    try:
                        with open(abs_path, 'r') as f:
                            path_lower = abs_path.lower()
                            if path_lower.endswith(".json"):
                                obj = json.load(f)
                            elif path_lower.endswith((".yaml", ".yml")):
                                obj = yaml.safe_load(f)
                            else:
                                logger.warning(
                                    f"Skipping unsupported file type: {abs_path}"
                                )
                                continue

                        components = []
                        if isinstance(obj, list):
                            logger.info(f"Found {len(obj)} components in {abs_path}")
                            components.extend(obj)
                        elif isinstance(obj, dict):
                            components.append(obj)
                        else:
                            logger.warning(
                                f"Skipping unexpected object type in {abs_path}"
                            )
                            continue

                        for comp_obj in components:
                            # Ensure component object is a dictionary
                            if not isinstance(comp_obj, dict):
                                logger.warning(
                                    f"Skipping non-dictionary item in {abs_path}"
                                )
                                continue

                            try:
                                if "deployed" in comp_obj:
                                    # Remove deployment state if present
                                    del comp_obj["deployed"]

                                component = self.kodexa_client.deserialize(comp_obj)
                                # Ensure correct org slug
                                component.org_slug = target_org_slug

                                logger.info(
                                    "Deploying component %s:%s",
                                    component.slug, component.version
                                )
                                log_details = component.deploy(update=True)
                                deployed_count += 1
                                for log_detail in log_details:
                                    logger.info(log_detail)
                            except Exception as e:
                                comp_id = comp_obj.get('slug', 'unknown')
                                logger.error(
                                    "Failed to deploy component %s from %s: %s",
                                    comp_id, abs_path, e, exc_info=True
                                )
                                # Option: stop deployment on first error
                                # raise

                    except Exception as e:
                        logger.error(
                            "Failed to process resource file %s: %s",
                            abs_path, e, exc_info=True
                        )
                    finally:
                        # Return to manifest directory for next file
                        os.chdir(manifest_dir)

        finally:
            # Return to original working directory
            os.chdir(original_cwd)

        logger.info(
            f"Deployment completed from manifest {manifest_path}. "
            f"Deployed {deployed_count} components."
        )

    def undeploy_from_manifest(self, manifest_path: str,
                               org_slug: str | None = None):
        """
        Undeploys all resources listed in a manifest file.

        Args:
            manifest_path (str): The path to the manifest file.
            org_slug (str | None): The organization slug to undeploy from.
                                   If None, uses the default org from client.
        """
        target_org_slug = org_slug or self.kodexa_client.get_org_slug()
        if not target_org_slug:
            msg = "Organization slug must be provided or set in the client."
            raise ValueError(msg)

        logger.info(
            f"Starting undeployment from manifest {manifest_path} "
            f"for organization {target_org_slug}"
        )
        resource_paths = self.read_manifest(manifest_path)
        abs_manifest_path = os.path.abspath(manifest_path)
        manifest_dir = os.path.dirname(abs_manifest_path)
        original_cwd = os.getcwd()
        undeployed_count = 0

        try:
            # Change to manifest directory to resolve relative paths
            os.chdir(manifest_dir)

            for resource_pattern in resource_paths:
                resource_files = glob.glob(resource_pattern, recursive=True)

                if not resource_files:
                    logger.warning(
                        f"No files found matching pattern '{resource_pattern}' "
                        f"relative to {manifest_dir}"
                    )
                    continue

                for rel_path in resource_files:
                    # Resolve absolute path based on current directory
                    abs_path = os.path.abspath(rel_path)
                    logger.info(f"Processing for undeployment: {abs_path}")

                    try:
                        with open(abs_path, 'r') as f:
                            path_lower = abs_path.lower()
                            if path_lower.endswith(".json"):
                                obj = json.load(f)
                            elif path_lower.endswith((".yaml", ".yml")):
                                obj = yaml.safe_load(f)
                            else:
                                logger.warning(
                                    f"Skipping unsupported file type: {abs_path}"
                                )
                                continue

                        components = []
                        if isinstance(obj, list):
                            logger.info(f"Found {len(obj)} components in {abs_path}")
                            components.extend(obj)
                        elif isinstance(obj, dict):
                            components.append(obj)
                        else:
                            logger.warning(
                                f"Skipping unexpected object type in {abs_path}"
                            )
                            continue

                        for comp_obj in components:
                            # Ensure component object is a dictionary
                            if not isinstance(comp_obj, dict):
                                logger.warning(
                                    f"Skipping non-dictionary item in {abs_path}"
                                )
                                continue

                            slug = comp_obj.get('slug')
                            version = comp_obj.get('version')

                            if not slug or not version:
                                logger.warning(
                                    "Skipping component in %s (missing slug/version)",
                                    abs_path
                                )
                                continue

                            try:
                                # Get component object to call undeploy
                                # Note: This assumes get_object method exists
                                # with appropriate parameters and return value
                                component = self.kodexa_client.get_object(
                                    target_org_slug, slug, version
                                )
                                if component:
                                    logger.info(
                                        "Undeploying component %s:%s",
                                        slug, version
                                    )
                                    component.undeploy()
                                    undeployed_count += 1
                                else:
                                    logger.warning(
                                        "Component %s:%s not found in org %s",
                                        slug, version, target_org_slug
                                    )
                            except Exception as e:
                                logger.error(
                                    "Failed to undeploy component %s:%s: %s",
                                    slug, version, e, exc_info=True
                                )
                                # Option: stop on first error
                                # raise

                    except Exception as e:
                        logger.error(
                            "Failed to process file %s for undeployment: %s",
                            abs_path, e, exc_info=True
                        )

        finally:
            # Return to original working directory
            os.chdir(original_cwd)

        logger.info(
            f"Undeployment completed from manifest {manifest_path}. "
            f"Undeployed {undeployed_count} components."
        )

    def sync_from_instance(self, manifest_path: str, org_slug: str | None = None):
        """
        Syncs resources from a Kodexa instance to the filesystem based on a manifest.

        This reads a manifest file and for each resource defined:
        1. Retrieves the resource from the Kodexa instance
        2. Saves it to the corresponding file on the filesystem

        Args:
            manifest_path (str): The path to the manifest file.
            org_slug (str | None): The organization slug to sync from.
                                  If None, uses the default org from client.
        """
        target_org_slug = org_slug or self.kodexa_client.get_org_slug()
        if not target_org_slug:
            msg = "Organization slug must be provided or set in the client."
            raise ValueError(msg)

        logger.info(
            f"Starting sync from instance to filesystem using manifest "
            f"{manifest_path} for organization {target_org_slug}"
        )
        resource_paths = self.read_manifest(manifest_path)
        abs_manifest_path = os.path.abspath(manifest_path)
        manifest_dir = os.path.dirname(abs_manifest_path)
        original_cwd = os.getcwd()
        synced_count = 0

        try:
            # Change to manifest directory to resolve relative paths
            os.chdir(manifest_dir)

            for resource_pattern in resource_paths:
                resource_files = glob.glob(resource_pattern, recursive=True)

                if not resource_files:
                    logger.warning(
                        f"No files found matching pattern '{resource_pattern}' "
                        f"relative to {manifest_dir}"
                    )
                    continue

                for rel_path in resource_files:
                    # Resolve absolute path based on current directory
                    abs_path = os.path.abspath(rel_path)
                    logger.info(f"Processing for sync: {abs_path}")

                    try:
                        # Read the file to get component information
                        with open(abs_path, 'r') as f:
                            path_lower = abs_path.lower()
                            if path_lower.endswith(".json"):
                                file_obj = json.load(f)
                            elif path_lower.endswith((".yaml", ".yml")):
                                file_obj = yaml.safe_load(f)
                            else:
                                logger.warning(
                                    f"Skipping unsupported file type: {abs_path}"
                                )
                                continue

                        components = []
                        if isinstance(file_obj, list):
                            logger.info(
                                f"Found {len(file_obj)} components in {abs_path}"
                            )
                            components.extend(file_obj)
                        elif isinstance(file_obj, dict):
                            components.append(file_obj)
                        else:
                            logger.warning(
                                f"Skipping unexpected object type in {abs_path}"
                            )
                            continue

                        for comp_obj in components:
                            # Ensure component object is a dictionary
                            if not isinstance(comp_obj, dict):
                                logger.warning(
                                    f"Skipping non-dictionary item in {abs_path}"
                                )
                                continue

                            slug = comp_obj.get('slug')
                            version = comp_obj.get('version')

                            if not slug or not version:
                                logger.warning(
                                    "Skipping component (missing slug/version) in %s",
                                    abs_path
                                )
                                continue

                            try:
                                # Get the component from the Kodexa instance
                                logger.info(
                                    f"Retrieving component {slug}:{version} "
                                    f"from org {target_org_slug}"
                                )
                                component = self.kodexa_client.get_object(
                                    target_org_slug, slug, version
                                )
                                
                                if not component:
                                    logger.warning(
                                        f"Component {slug}:{version} not found "
                                        f"in org {target_org_slug}"
                                    )
                                    continue

                                # Serialize the component to data
                                updated_obj = component.serialize()
                                
                                # Write the updated data back to the file
                                write_format = "json"
                                if path_lower.endswith((".yaml", ".yml")):
                                    write_format = "yaml"
                                
                                with open(abs_path, 'w') as f:
                                    if write_format == "json":
                                        json.dump(updated_obj, f, indent=2)
                                    else:
                                        yaml.dump(updated_obj, f)
                                
                                logger.info(
                                    f"Synced component {slug}:{version} to {abs_path}"
                                )
                                synced_count += 1
                                
                            except Exception as e:
                                logger.error(
                                    "Failed to sync component %s:%s: %s",
                                    slug, version, e, exc_info=True
                                )
                    except Exception as e:
                        logger.error(
                            "Failed to process file %s for sync: %s",
                            abs_path, e, exc_info=True
                        )

        finally:
            # Return to original working directory
            os.chdir(original_cwd)

        logger.info(
            f"Sync completed from instance to filesystem using manifest "
            f"{manifest_path}. Synced {synced_count} components."
        )

