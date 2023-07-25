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
