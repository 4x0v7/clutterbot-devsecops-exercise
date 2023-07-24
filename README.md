# Clutterbot DevSecOps Exercise

> .NET web app deployment with Terraform and GitHub Actions CI/CD

---

## Local development environment setup

> These instructions assume Windows 10 utilising the `scoop` package manager, see <https://scoop.sh>

### Prerequisites

- scoop: <https://scoop.sh>
- .NET SDK 7

    `scoop install dotnet-sdk`

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

## Init and run a new .NET web app

```powershell
task dotnet:init
task dotnet:run
```
