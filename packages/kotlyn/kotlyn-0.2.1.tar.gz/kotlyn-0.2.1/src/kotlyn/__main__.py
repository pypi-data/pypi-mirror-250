import os
import sys
import zenyx
from zenyx import printf
import requests
import zipfile
import random
import time
import termcolor


ARGS = zenyx.Arguments(sys.argv)
HOME_DIRECTORY = os.path.expanduser("~")
MODULE_DIR = "kotlyn"


def get_latest_release_tag(repo_owner, repo_name):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(api_url)

    if response.status_code == 200:
        release_info = response.json()
        return release_info["tag_name"]
    else:
        print(
            f"Failed to retrieve latest release information. Status code: {response.status_code}"
        )
        return None


def download_url(url, save_path, chunk_size=128):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(save_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)


def download_github_release(repo_owner, repo_name, download_path="."):
    latest_release_tag = get_latest_release_tag(repo_owner, repo_name)

    if latest_release_tag:
        api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/tags/{latest_release_tag}"
        response = requests.get(api_url)

        if response.status_code == 200:
            release_info = response.json()
            assets = release_info["assets"]

            for asset in assets:
                asset_url = asset["browser_download_url"]
                asset_name = asset["name"]
                download_url(asset_url, os.path.join(download_path, asset_name))

            printf(f"  @!Kotlyn$&/download_github_release\n   @~Latest release ({latest_release_tag}) downloaded successfully.$&")
        else:
            printf(
                f"  @!Kotlyn$&/download_github_release\n   @!Failed to retrieve release information. Status code: {response.status_code}$&"
            )


def create_folder(folder_name) -> None:
    global HOME_DIRECTORY
    folder_path = os.path.join(HOME_DIRECTORY, folder_name)

    try:
        os.makedirs(folder_path)
        printf(f"  @!Kotlyn$&/create_folder\n   @~Folder '{folder_name}' created successfully$&")
    except FileExistsError:
        printf(f"  @!Kotlyn$&/create_folder\n   @~Folder '{folder_name}' already exists$&")
    except Exception as e:
        printf(f"An error occurred: {e}")


def find_kotlin_compiler_zip(directory_path):
    try:
        files = os.listdir(directory_path)
        matching_files = [
            file
            for file in files
            if file.startswith("kotlin-compiler-") and file.endswith(".zip")
        ]

        if matching_files:
            return matching_files[0]
        else:
            printf("  @!Kotlyn$&/find_kotlin_compiler_zip\n   @~No matching file found.$&")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def list_not_entry_kt(entry: str, path: str):
    files = os.listdir(os.path.realpath(path))
    return " ".join([file for file in files if file != entry and file.endswith(".kt")])


def delete_files_in_folder(folder_path):
    try:
        # Get the list of files in the folder
        files = os.listdir(folder_path)

        # Iterate through the files and delete each one
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)

        print(f"  @!Kotlyn$&/delete_files_in_folder\n   @~All files in {folder_path} have been deleted.$&")
    except Exception as e:
        print(f"An error occurred: {e}")


def unpack_zip(zip_path, output_directory):
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(output_directory)
        print(f"  @!Kotlyn$&/unpack_zip\n   @~Zip file unpacked successfully$&")
    except zipfile.BadZipFile:
        print(f"  @!Kotlyn$&/unpack_zip\n   @~The file '{zip_path}' is not a valid zip archive.$&")
    except Exception as e:
        print(f"An error occurred: {e}")


def path(path: str) -> str:
    return os.path.join(*(path.split("/")))


def create_file(filepath: str) -> None:
    if os.path.exists(filepath):
        return
    with open(filepath, "w") as wf:
        wf.write("")


def write_file(path: str, content: str) -> None:
    with open(path, "w") as wf:
        wf.write(content)


def read_file(path: str) -> str:
    res = ""
    with open(path, "r") as rf:
        res = rf.read()
    return res


# ---------------------------------- MAIN ----------------------------------


def main() -> None:
    global ARGS
    original_path = os.path.realpath("./")

    os.system("@echo on")

    print(ARGS)

    if ARGS.normals[0] == "!setup":
        printf("@!Kotlyn - Kotlin | Setup$&")
        printf("@~Installing kotlin (.kt) language, creating environment variables...$&")
        # Creating folders
        create_folder(f"{MODULE_DIR}")
        create_folder(f"{MODULE_DIR}/shell")
        create_folder(f"{MODULE_DIR}/shell/bin")
        create_folder(f"{MODULE_DIR}/temp/install")

        # Creating files
        create_file(path(f"{HOME_DIRECTORY}/{MODULE_DIR}/{MODULE_DIR}.toml"))
        create_file(path(f"{HOME_DIRECTORY}/{MODULE_DIR}/.builder_install"))

        builder_install_info = read_file(
            path(f"{HOME_DIRECTORY}/{MODULE_DIR}/.builder_install")
        )
        if builder_install_info == "COMPLETE":
            zenyx.printf("@!Setup has been completed before!$&")
            return

        zenyx.printf("  @?Downloading Kotlin...$&", end="\r")

        # Downloading latest release
        download_github_release(
            "JetBrains", "kotlin", path(f"{HOME_DIRECTORY}/{MODULE_DIR}/temp/install")
        )
        zip_name: str = find_kotlin_compiler_zip(
            path(f"{HOME_DIRECTORY}/{MODULE_DIR}/temp/install")
        )
        compiler_zip_path = path(
            f"{HOME_DIRECTORY}/{MODULE_DIR}/temp/install/{zip_name}"
        )
        printf("  Kotlin Downloaded", end="\r")

        printf("  @?Unpacking ZIP Archive...$&", end="\r")
        unpack_zip(compiler_zip_path, path(f"{HOME_DIRECTORY}/{MODULE_DIR}/"))
        delete_files_in_folder(path(f"{HOME_DIRECTORY}/{MODULE_DIR}/temp/install"))
        printf("  Unpacked ZIP Archive", end="\r")

        kb_kotlin_home_path = path(f"{HOME_DIRECTORY}/{MODULE_DIR}/kotlinc")
        if not os.path.exists(kb_kotlin_home_path):
            raise Exception(
                "The path the builder would use for environment variables is not available"
            )

        write_file(
            path(f"{HOME_DIRECTORY}/{MODULE_DIR}/shell/setup_kotlin_env.ps1"),
            "\n".join(
                [
                    f"[Environment]::SetEnvironmentVariable(\"KOTLIN_HOME\", \"{path(f'{HOME_DIRECTORY}/{MODULE_DIR}/kotlinc')}\", [EnvironmentVariableTarget]::User)",
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
        os.system(f"powershell {path(f'{HOME_DIRECTORY}/{MODULE_DIR}/shell/setup_kotlin_env.ps1')}")
        
        write_file(
            path(f"{HOME_DIRECTORY}/{MODULE_DIR}/shell/bin/kotlyn.bat"),
            "\n".join(
                [
                    "@echo off",
                    "setlocal enabledelayedexpansion",
                    "rem Combine all arguments into a single string",
                    "set \"args=\"",
                    ":loop",
                    "if \"%1\"==\"\" goto endloop",
                    "set \"args=!args! %1\"",
                    "shift",
                    "goto loop",
                    ":endloop",
                    "rem Call the Python module with the combined arguments",
                    "python -m kotlyn %args%",
                    "endlocal"
                ]
            ),
        )
        write_file(
            path(f"{HOME_DIRECTORY}/{MODULE_DIR}/shell/setup_kotlyn_cmd.ps1"),
            "\n".join(
                [
                    # f"[Environment]::SetEnvironmentVariable(\"KOTLIN_HOME\", \"{path(f'{HOME_DIRECTORY}/{MODULE_DIR}/kotlinc/bin')}\")",
                    "# Test folder",
                    f'$InstallLocation = "{path(f"{HOME_DIRECTORY}/{MODULE_DIR}/shell/bin")}"',
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
        os.system(f"powershell {path(f'{HOME_DIRECTORY}/{MODULE_DIR}/shell/setup_kotlyn_cmd.ps1')}")

        delete_files_in_folder(f"{HOME_DIRECTORY}/{MODULE_DIR}/temp/")

        write_file(
            path(f"{HOME_DIRECTORY}/{MODULE_DIR}/.builder_install"), "COMPLETE"
        )

        printf("@!Kotlyn - Kotlin | Installed$&")
        return

    builder_install_info = read_file(
            path(f"{HOME_DIRECTORY}/{MODULE_DIR}/.builder_install")
        )
    if builder_install_info != "COMPLETE":
        zenyx.printf("@!Setup has not been completed!$&\nRun setup: python -m kotlyn --setup")
        return

    if ARGS.normals[0] == "!version":
        print("[Builder/CLI] \nKotlyn version 0.0.7")
        os.system("echo [JetBrains/Kotlin] && kotlin -version")
    
    if ARGS.normals[0] == "!update":
        os.system("python -m pip install --upgrade kotlyn")

    if ARGS.tagged("build"):
        if len(ARGS.normals) < 1 or ARGS.normals[0].startswith("!"):
            zenyx.printf("@!Missing param(s): <filename>$&")
            return
        
        os.system(f'cd {os.path.dirname(ARGS.normals[0])} && kotlinc {os.path.realpath(ARGS.normals[0])} -include-runtime -d Main.jar {list_not_entry_kt(ARGS.normals[0], os.path.dirname(ARGS.normals[0]))} && java -jar Main.jar')
    
    if ARGS.tagged("run"):
        if len(ARGS.normals) < 1 or ARGS.normals[0].startswith("!"):
            zenyx.printf("@!Missing param(s): <filename>$&")
            return
        
        jar_path = path(f"{HOME_DIRECTORY}/{MODULE_DIR}/temp/kotlyn-{time.time()}-{random.randint(100000, 999999)}-{random.randint(100000, 999999)}")

        os.system(f'cd {os.path.dirname(ARGS.normals[0])} && kotlinc {os.path.realpath(ARGS.normals[0])} -include-runtime -d {jar_path}.jar {list_not_entry_kt(ARGS.normals[0], os.path.dirname(ARGS.normals[0]))} && java -jar {jar_path}.jar')
        os.remove(f'{jar_path}.jar')

if __name__ == "__main__":
    main()
