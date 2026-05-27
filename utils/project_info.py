import subprocess
import sys
import tomllib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


def get_package_version(package_name: str) -> str:
    try:
        return version(package_name)
    except PackageNotFoundError:
        return "not installed"


def run_command(command: list[str]) -> str:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False,
            encoding="utf-8",
        )

        if result.returncode != 0:
            return "unknown"

        return result.stdout.strip()
    except OSError:
        return "unknown"


def get_poetry_version() -> str:
    return run_command(["poetry", "--version"])


def get_git_branch() -> str:
    return run_command(["git", "rev-parse", "--abbrev-ref", "HEAD"])


def get_git_commit() -> str:
    return run_command(["git", "rev-parse", "--short", "HEAD"])


def get_git_commit_date() -> str:
    return run_command(["git", "log", "-1", "--format=%ci"])


def format_authors(authors: object) -> str:
    if not authors:
        return "unknown"

    if isinstance(authors, list):
        formatted_authors: list[str] = []

        for author in authors:
            if isinstance(author, str):
                formatted_authors.append(author)

            elif isinstance(author, dict):
                name = author.get("name")
                email = author.get("email")

                if name and email:
                    formatted_authors.append(f"{name} <{email}>")
                elif name:
                    formatted_authors.append(str(name))
                elif email:
                    formatted_authors.append(str(email))

        return ", ".join(formatted_authors) if formatted_authors else "unknown"

    return str(authors)


def get_project_metadata() -> dict[str, str]:
    pyproject_path = Path("pyproject.toml")

    if not pyproject_path.exists():
        return {
            "name": "unknown",
            "version": "unknown",
            "authors": "unknown",
        }

    with pyproject_path.open("rb") as file:
        pyproject = tomllib.load(file)

    project_config = pyproject.get("project", {})
    poetry_config = pyproject.get("tool", {}).get("poetry", {})

    name = project_config.get("name") or poetry_config.get("name", "unknown")
    project_version = (
        project_config.get("version")
        or poetry_config.get("version", "unknown")
    )

    authors_raw = project_config.get("authors") or poetry_config.get("authors", [])

    return {
        "name": str(name),
        "version": str(project_version),
        "authors": format_authors(authors_raw),
    }


def build_short_startup_info() -> tuple:
    metadata = get_project_metadata()

    return (
        f"{metadata['name']} version {metadata['version']}",
        f"Authors: {metadata['authors']}",
        f"- Python: {sys.version.split()[0]}",
        f"- Poetry: {get_poetry_version()}",
        f"- aiogram: {get_package_version('aiogram')}",
        f"- SQLAlchemy: {get_package_version('sqlalchemy')}",
        f"- asyncpg: {get_package_version('asyncpg')}",
        f"- Alembic: {get_package_version('alembic')}",
        f"-- Git: {get_git_branch()} {get_git_commit()}",
    )