import argparse
import shutil
import sys
from git import Repo
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(prog="trusted-ai")
    parser.add_argument("mode", type=str, choices=["new", "main"])
    parser.add_argument("--organization", type=str)
    parser.add_argument("--package_name", type=str)
    parser.add_argument("--local-repo-path", type=str, default=Path.cwd())

    args = parser.parse_args()

    print(args)

    if args.mode == "main":
        print("Hello world!")
    elif args.mode == "new":
        create_new_repo(args)
    else:
        raise ValueError("You can choose only these modes: new, main.")

def create_new_repo(args):
    file_path = Path(args.local_repo_path) / "tai" / "contrib" / args.organization / args.package_name
    file_path.mkdir(exist_ok=True, parents=True)
    open(file_path / "__init__.py", "a").close()

    shutil.copyfile('tai/core/.gitignore_template', Path(args.local_repo_path) / ".gitignore")

    Repo.init(args.local_repo_path)
    repo = Repo(args.local_repo_path)
    repo.index.add(['.gitignore'])
    # Provide a commit message
    # repo.index.commit('Initial commit.')


# if __name__ == "__main__":
#     main()