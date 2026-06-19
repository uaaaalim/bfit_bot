import subprocess
import tomllib

with open("pyproject.toml", "rb") as f:
    data = tomllib.load(f)

project = data["project"]

project_name = project["name"]
project_version = project["version"]
project_authors = project.get("authors", [])

def get_branch_name() -> str:
    return subprocess.check_output(
        ["git", "branch", "--show-current"],
        text=True
    ).strip()

def get_commit() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "--short", "HEAD"],
        text=True
    ).strip()
