import base64
import os
import sys
from datetime import datetime

import anyio
import dagger
import hcl2
from graphql import GraphQLError

# pin the base image to its sha256 for build environment reproducibility
base_image = "mcr.microsoft.com/dotnet/sdk:7.0@sha256:24f22e1142432dea3a34d350686be77be5e454ccb9fab7c00d67cd03c6e000a6"
webapp_deployed_image_name = os.getenv("WEBAPP_DEPLOYED_IMAGE_NAME")

REGISTRY_PUBLISH = os.getenv("REGISTRY_PUBLISH") not in {None, "0", "false"}

GH_PUBLISH = REGISTRY_PUBLISH and os.getenv("GH_PUBLISH") not in {None, "0", "false"}
GCP_PUBLISH = REGISTRY_PUBLISH and os.getenv("GCP_PUBLISH") not in {None, "0", "false"}


def get_tf_variable(variables, key):
    for variable in variables:
        if key in variable:
            return variable[key]["default"]
    return None


def read_secret_from_file(filename):
    try:
        with open(filename, "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"Warning: {filename} not found.")
        return None


async def publish_to_registry(ctr, registry, tag):
    if registry["publish"] is True:
        await ctr.with_registry_auth(
            registry["url"], registry["user"], registry["token"]
        ).publish(f"{registry['url']}/{registry['image_name']}:{tag}")


async def main():
    cfg = dagger.Config(log_output=sys.stderr)

    # loading the .tf variables to get values
    with open("variables.tf", "r") as f:
        tf_variables = hcl2.load(f)

    project_id = get_tf_variable(tf_variables["variable"], "project_id")
    repository_id = get_tf_variable(
        tf_variables["variable"], "gcp_artifcat_registry_name"
    )

    async with dagger.Connection(cfg) as dagger_client:
        src = dagger_client.host().directory(
            path=".",
            exclude=[
                "modules/*",
                ".git/*",
                ".terraform/*",
                "ctr_registry/*",
                "image.tar",
            ],
        )

        dagger_client = dagger_client.pipeline(".NET build")

        gh_psh_tkn = None
        if GH_PUBLISH:
            gh_token_filename = os.getenv("GH_TOKEN_SECRET_FILE")
            gh_psh_tkn = read_secret_from_file(gh_token_filename)
            gh_psh_tkn = dagger_client.set_secret("gh-token", gh_psh_tkn)

        gcp_psh_tkn = None
        if GCP_PUBLISH:
            gcp_psh_tkn_file = os.getenv("GCP_CTR_PUSHER_TOKEN_FILE")
            gcp_psh_tkn = read_secret_from_file(gcp_psh_tkn_file)
            gcp_psh_tkn = dagger_client.set_secret(
                "gcp-token",
                base64.b64decode(gcp_psh_tkn).decode("utf-8"),
            )

        # import or build container
        if os.getenv("LOCAL_TAR_IMPORT") not in {None, "0", "false"}:
            tar_file: dagger.File = (
                dagger_client.host().directory(".").file("image.tar")
            )
            imported_ctr: dagger.Container = dagger_client.container().import_(
                source=tar_file
            )
            docker_dotnet_build_ctr = imported_ctr
        else:
            # build using Dockerfile
            docker_dotnet_build_ctr: dagger.Container = src.docker_build()

        # define tags
        webapp_deployed_tag = (
            os.environ["WEBAPP_DEPLOYED_TAG"]
            if os.getenv("LOCAL_TAR_EXPORT") in {None, "0", "false"}
            else None
        )
        tags = (
            [webapp_deployed_tag, "latest"]
            if os.getenv("LOCAL_TAR_EXPORT") in {None, "0", "false"}
            else None
        )

        # define registries
        registries = [
            {
                "registry": "github",
                "url": "ghcr.io",
                "user": "4x0v7",
                "token": gh_psh_tkn,
                "image_name": f"4x0v7/{webapp_deployed_image_name}",
                "publish": GH_PUBLISH,
            },
            {
                "registry": "gcp",
                "url": "australia-southeast1-docker.pkg.dev",
                "user": "_json_key",
                "token": gcp_psh_tkn,
                "image_name": f"{project_id}/{repository_id}/{webapp_deployed_image_name}",
                "publish": GCP_PUBLISH,
            },
        ]

        async with anyio.create_task_group() as tg:
            tg.start_soon(docker_dotnet_build_ctr.export, "./image.tar") if os.getenv(
                "LOCAL_TAR_EXPORT"
            ) not in {None, "0", "false"} else None

            # push to registries concurrently
            for registry in registries:
                if registry["publish"] is True:
                    for tag in tags:
                        tg.start_soon(
                            publish_to_registry, docker_dotnet_build_ctr, registry, tag
                        )


if __name__ == "__main__":
    try:
        anyio.run(main)
    except GraphQLError as e:
        print(e.message, file=sys.stderr)
        sys.exit(1)
