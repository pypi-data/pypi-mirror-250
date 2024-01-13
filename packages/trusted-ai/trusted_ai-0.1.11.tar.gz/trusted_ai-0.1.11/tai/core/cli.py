import argparse
import shutil
import sys
from git import Repo
from pathlib import Path
import subprocess


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def main():
    """Main function with running commands.

    :param mode: `new` for creation new package and `help` for text description
    :type organization: str

    :param org_pkg_name: name of your <organization>/<package name> (for mode `new`)
    :type organization: str

    :param --local-repo-path: path to folder where you want to create repo
    :type organization: str

    :param --config-path: path to config file with your creds
    :type organization: str
    """
    parser = argparse.ArgumentParser(prog="trusted-ai")
    parser.add_argument("mode", type=str, choices=["new", "help"])
    parser.add_argument("org_pkg_name", type=str)
    parser.add_argument("--local-repo-path", type=str, default=Path.cwd())
    parser.add_argument("--config-path", type=str, default=".")

    args = parser.parse_args()

    if args.mode == "help":
        print("Hello! \n It's TAI project, that will help you create your own little-package for MLM.")
        print(
            f"Type this command for creation new package:\n\t" + color.BOLD + color.GREEN + 
            f"tai new " + color.END + color.BLUE + color.BOLD +
            f"<organization/package_name> --local-repo-path <your path> --config-path <your config>"
            + color.END)
    elif args.mode == "new":
        org_pkg = args.org_pkg_name.split("/")
        if len(org_pkg) != 2:
            raise ValueError("Second argument (org_pkg_name) must be like 'organization/package_name' or 'user/package_name'.")
        organization, package_name = org_pkg[0], org_pkg[1]
        create_new_repo(organization=organization, package_name=package_name, local_repo_path=args.local_repo_path)
    else:
        raise ValueError("You can choose only these modes: new, main.")


def create_new_repo(organization, package_name, local_repo_path):
    """
    Create a new git repository with a package for your Model|Dataset|Executor.

    This function creates a repo in <local_repo_path> with the following structure::
        
        tai/
        ├── pyproject.toml  # pdm configuration file for your project
        ├── .gitignore
        ├── .venv           # virtual venv for your project
        └── contrib/
            └── <organization>/
                └── <package name>/
                    └── __init__.py

    :param organization: Organization name
    :type organization: str
    :param package_name: Package name
    :type package_name: str
    :param local_repo_path: path to folder where you want to create repo
    """
    file_path = Path(local_repo_path) / "tai" / "contrib" / organization / package_name
    file_path.mkdir(exist_ok=True, parents=True)
    open(file_path / "__init__.py", "a").close()

    shutil.copyfile(Path(__file__).parent / ".gitignore_template", Path(local_repo_path) / ".gitignore")

    Repo.init(local_repo_path)
    repo = Repo(local_repo_path)
    repo.index.add(['.gitignore'])

    command = ["pdm", "init"]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, text=True, cwd=local_repo_path)

    input_data_list = ["0", f"{package_name}",
                       "0.1.0", "y", "Some description...", "0", "MIT", organization, "test@test.com", "==3.12.*"]

    for input_data in input_data_list:
        process.stdin.write(input_data + "\n")
        process.stdin.flush()

    output = process.communicate()
    print("Output:", "\n".join(output))

    process.stdin.close()
    process.stdout.close()
    process.stderr.close()

    shutil.rmtree(Path(local_repo_path) / "src")
    shutil.rmtree(Path(local_repo_path) / "tests")

    # Provide a commit message
    # repo.index.commit('Initial commit.')


if __name__ == "__main__":
    main()