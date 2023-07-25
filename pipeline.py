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
        src = dagger_client.host().directory(".")

        dagger_client = dagger_client.pipeline(".NET build")

        dotnet_deps_install_ctr: dagger.Container = (
            dagger_client.container()
            .from_(base_image)
            # mount local repository into image
            .with_mounted_directory("/src", src)
            # set current working directory for next commands
            .with_workdir("/src/ClutterbotWebApp")
            .with_entrypoint(["/bin/sh", "-c"])
            .with_exec(["dotnet restore"])
        )

        # reuse the same container (with installed dependencies) for building the app
        dotnet_build_ctr: dagger.Container = (
            dotnet_deps_install_ctr
            # bust the cache so build always runs
            .with_env_variable(
                "CACHEBUSTER", datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            )
            .with_exec(["dotnet build --no-restore"])
        )

        # Not concurrent
        #
        # await dotnet_build_ctr.stdout()

        # Concurrent
        #
        async with anyio.create_task_group() as tg:
            tg.start_soon(dotnet_build_ctr.stdout)


if __name__ == "__main__":
    try:
        anyio.run(main)
    except GraphQLError as e:
        print(e.message, file=sys.stderr)
        sys.exit(1)