# Clutterbot DevSecOps Exercise

> .NET web app deployment with Terraform and GitHub Actions CI/CD

---

## Local development environment setup

> These instructions assume Windows 10 utilising the `scoop` package manager, see <https://scoop.sh>

### Prerequisites

- scoop: <https://scoop.sh>
- .NET SDK 7

    `scoop install dotnet-sdk@7.0.306`

    Confirm .NET is installed correctly

    ```powershell
    dotnet --list-sdks
    7.0.306 [C:\Users\user\scoop\apps\dotnet-sdk\current\sdk]
    ```

- task (optional but recommended, see <https://taskfile.dev>)

    `scoop install task`

    Confirm task is installed correctly

    ```powershell
    task --version
    Task version: v3.27.1 (h1:cftsoOqUo7/pCdtO7fDa4HreXKDvbrRhfhhha8bH9xc=)
    ```

- Terraform

    `scoop install terraform`

    Confirm Terraform is installed correctly

    ```powershell
    terraform --version
    Terraform v1.5.4
    on windows_amd64
    ```

- vendir

    `scoop install vendir`

    Confirm vendir is installed correctly

    ```powershell
    vendir version
    vendir version 0.34.3

    Succeeded
    ```

### Local CI/CD development prerequisites

- Docker

    Rancher Desktop is recommended, but Docker Desktop will work fine

    `scoop install rancher-desktop`

    Start the Docker daemon

    Confirm Docker is installed correctly

    ```powershell
    docker version
    Client:
     Version:           24.0.5
     API version:       1.42 (downgraded from 1.43)
     Go version:        go1.20.6
     Git commit:        ced0996
     Built:             Fri Jul 21 20:36:24 2023
     OS/Arch:           windows/amd64
     Context:           mbx
    
    Server:
     Engine:
      Version:          23.0.6
      API version:      1.42 (minimum version 1.12)
      Go version:       go1.20.4
      Git commit:       9dbdbd4b6d7681bd18c897a6ba0376073c2a72ff
      Built:            Fri May 12 13:54:36 2023
      OS/Arch:          linux/amd64
      Experimental:     false
     containerd:
      Version:          v1.7.2
      GitCommit:        0cae528dd6cb557f7201036e9f43420650207b58
     runc:
      Version:          1.1.7
      GitCommit:        860f061b76bb4fc671f0f9e900f7d80ff93d4eb7
     docker-init:
      Version:          0.19.0
      GitCommit:
    ```

- Python 3.11

    `scoop install python311`

    Confirm Python is installed correctly

    ```powershell
    python -VV
    Python 3.11.4 (tags/v3.11.4:d2340ef, Jun  7 2023, 05:45:37) [MSC v.1934 64 bit (AMD64)]
    ```

- Pipenv

    `pip install --upgrade pipenv`

    Confirm Pipenv is installed correctly

    ```powershell
    pipenv --version
    pipenv, version 2023.7.23
    ```

- Dagger

    `scoop install dagger@0.6.4`

    Confirm Dagger is installed correctly

    ```powershell
    dagger version
    dagger v0.6.4 windows/amd64
    ```

## Init and run a new .NET web app

```powershell
task dotnet:init
task dotnet:run
```

## Configure local CI/CD development environment

> Local CI/CD prerequisites must be installed first

```powershell
task cicd:deps:install
```

## Build the .NET web app

```powershell
task dotnet:build
```

## Push the Docker image to GitHub Packages

### Local configuration

To push the built Docker image to GitHub Packages Container registry from a local development environment
you will need to create a personal access token.

Follow the [GitHub documentation](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry#authenticating-with-a-personal-access-token-classic) to create a personal access token.

Put the token into a text file named `github_token.txt` in the root of the repository.
This file is is ignored by the `.gitignore` file, to prevent accidentally committing it.

#### Modify the Taskfile

The `dotnet:build` task in the `Taskfile.yml` has 2 configurable ENV variables to control where the built Docker image is pushed.

```yaml
LOCAL_TAR_EXPORT: false
REGISTRY_PUBLISH: true
```

#### Configure for a local Docker daemon

By default, the image is published via GitHub Actions to the Container registry on push.
For local development, you can instead opt to export the built image as a `tar` file.
The tar file can then be loaded into a Docker daemon.

```sh
task dotnet:build
docker load --input image.tar
Loaded image ID: sha256:644249ebf40a41a568fbeaeacbe81414ecd838a7f792b6c64d25a6dbf2521813
```

Once the image is loaded, tag it

```sh
docker tag sha256:644249ebf40a41a568fbeaeacbe81414ecd838a7f792b6c64d25a6dbf2521813 ghcr.io/4x0v7/clutterbot-webapp:v0.0.0
```

Confirm the image was tagged successfully

```sh
docker image ls
REPOSITORY                         TAG       IMAGE ID       CREATED              SIZE
ghcr.io/4x0v7/clutterbot-webapp    v0.0.0    644249ebf40a   About a minute ago   318MB
```

You can now run the image as usual

```sh
docker run -it --rm -p 5001:80 ghcr.io/4x0v7/clutterbot-webapp:v0.0.0
```
