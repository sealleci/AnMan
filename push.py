import argparse
import subprocess
import sys
from dataclasses import dataclass


@dataclass
class PushArgs:
    message: str


def run_git_command(command_parts: list[str]):
    try:
        result = subprocess.run(command_parts, check=True, text=True, capture_output=True)
        print(result.stdout)
    except Exception as e:
        print(f"Error occurred while running {' '.join(command_parts)}: {e}")
        sys.exit(1)


def parse_args() -> PushArgs:
    parser = argparse.ArgumentParser(description="Git automation script")
    parser.add_argument("-m", "--message", required=True, help="Commit message")

    return PushArgs(**vars(parser.parse_args()))


def main(commit_message: str):
    print("> Pulling the latest changes from remote")
    run_git_command(["git", "pull"])

    print("> Adding changes")
    run_git_command(["git", "add", "."])

    print(f"> Committing changes with message: {commit_message}")
    run_git_command(["git", "commit", "-m", commit_message])

    print("> Pushing changes")
    run_git_command(["git", "push"])


if __name__ == "__main__":
    main(parse_args().message)
