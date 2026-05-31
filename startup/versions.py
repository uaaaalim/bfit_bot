import logging
import sys
import tomllib
from pathlib import Path

import aiogram
import alembic
import asyncpg
import sqlalchemy

logger = logging.getLogger(__name__)

def aiogram_version() -> str:
    return str(aiogram.__version__)

def python_version() -> str:
    version = sys.version_info
    return str(version.major)+"."+str(version.minor)+"."+str(version.micro)+" for "+str(sys.platform)

def alembic_version() -> str:
    return str(alembic.__version__)

def asyncpg_version() -> str:
    return str(asyncpg.__version__)

def sqlalchemy_version() -> str:
    return str(sqlalchemy.__version__)

def get_git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()[:6]
    except Exception as err:
        logger.error(f"Failed to get git commit: %s".format(err))
        return "unknown"

def read_pyproject() -> dict:
    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"

    with pyproject_path.open("rb") as file:
        return tomllib.load(file)

def get_project_info() -> dict[str, object]:
    data = read_pyproject()

    project = data.get("project", {})

    return {
        "name": project.get("name", "unknown"),
        "version": project.get("version", "unknown"),
        "authors": project.get("authors", []),
    }

def get_project_name() -> str:
    return str(get_project_info()["name"])
def get_project_version() -> str:
    return str(get_project_info()["version"])
def get_project_authors() -> object:
    return get_project_info()["authors"]

import subprocess


def get_poetry_version() -> str:
    try:
        result = subprocess.run(
            ["poetry", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )

        return result.stdout.strip()

    except FileNotFoundError:
        return "poetry not found"

    except subprocess.CalledProcessError:
        return "unknown"
