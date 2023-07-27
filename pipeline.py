import base64
import os
import sys
from datetime import datetime

import anyio
import dagger
from graphql import GraphQLError

# pin the base image to its sha256 for build environment reproducibility
base_image = "mcr.microsoft.com/dotnet/sdk:7.0@sha256:24f22e1142432dea3a34d350686be77be5e454ccb9fab7c00d67cd03c6e000a6"


async def main():
    cfg = dagger.Config(log_output=sys.stderr)

    async with dagger.Connection(cfg) as dagger_client:
        # get reference to the local project
        src = dagger_client.host().directory(
            path=".", exclude=["modules/*", ".git/*", ".terraform/*", "ctr_registry/*"]
        )

        dagger_client = dagger_client.pipeline(".NET build")

        # read secret from host env variable
        gh_token_secret = dagger_client.set_secret(
            "gh-token", os.environ["GH_TOKEN_SECRET"]
        )

        webapp_deployed_tag = os.environ["WEBAPP_DEPLOYED_TAG"]

        # build using Dockerfile
        docker_dotnet_build_ctr: dagger.Container = src.docker_build()

        # define tags
        tags = [webapp_deployed_tag, "latest"]

        # define registries
        registries = [
            {
                "publish": os.getenv("GH_PUBLISH"),
                "url": "ghcr.io",
                "user": "4x0v7",
                "token": gh_token_secret,
                "image_name": "4x0v7/clutterbot-webapp",
            },
            {
                "publish": os.getenv("GCLOUD_PUBLISH"),
                "url": "australia-southeast1-docker.pkg.dev",
                "user": "_json_key",
                "token": base64.b64decode(
                    os.environ.get("GLCLOUD_CTR_PUSHER_TOKEN", "")
                ).decode("utf-8")
                if os.getenv("GCLOUD_PUBLISH") not in {"0", "false"}
                else None,
                "image_name": "maximal-relic-394118/cbot/clutterbot-webapp",
            },
        ]

        async with anyio.create_task_group() as tg:
            tg.start_soon(docker_dotnet_build_ctr.export, "./image.tar") if os.getenv(
                "LOCAL_TAR_EXPORT"
            ) not in {"0", "false"} else None

            async def publish_to_registry(registry, tag):
                await docker_dotnet_build_ctr.with_registry_auth(
                    registry["url"], registry["user"], registry["token"]
                ).publish(f"{registry['url']}/{registry['image_name']}:{tag}")

            for registry in registries:
                if registry["publish"] not in {"0", "false"}:
                    for tag in tags:
                        tg.start_soon(publish_to_registry, registry, tag)


if __name__ == "__main__":
    try:
        anyio.run(main)
    except GraphQLError as e:
        print(e.message, file=sys.stderr)
        sys.exit(1)
