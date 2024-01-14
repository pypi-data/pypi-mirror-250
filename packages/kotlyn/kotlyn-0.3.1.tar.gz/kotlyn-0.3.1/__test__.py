import os


def write_file(path: str, content: str) -> None:
    with open(path, "w") as wf:
        wf.write(content)


def path(path: str) -> str:
    return os.path.join(*(path.split("/")))


HOME_DIRECTORY = os.path.expanduser("~")

write_file(
    path(f"{HOME_DIRECTORY}/kotlin-builder/setup_env.ps1"),
    "\n".join(
        [
            "# Test folder",
            f'$InstallLocation = "%KOTLIN_HOME%\\bin"',
            "# To add folder to PATH",
            "$persistedPath = [Environment]::GetEnvironmentVariable('Path', [EnvironmentVariableTarget]::User) -split ';'",
            "if ($persistedPath -notcontains $InstallLocation) {",
            "   $persistedPath = $persistedPath + $InstallLocation | where { $_ }",
            "   [Environment]::SetEnvironmentVariable('Path', $persistedPath -join ';', [EnvironmentVariableTarget]::User)",
            "   }",
            "#To verify if PATH isn't already added",
            "$envPaths = $env:Path -split ';'",
            "if ($envPaths -notcontains $InstallLocation) {",
            "   $envPaths = $envPaths + $InstallLocation | where { $_ }",
            "   $env:Path = $envPaths -join ';'",
            "}",
        ]
    ),
)
