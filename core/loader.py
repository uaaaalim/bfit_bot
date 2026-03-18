import importlib
import inspect
from pathlib import Path


def load_instances_from_directory(
    directory: str,
    package_name: str,
    base_class: type,
    *args,
):
    instances = []
    for path in sorted(Path(directory).glob("*.py")):
        if path.name.startswith("__"):
            continue

        module = importlib.import_module(f"{package_name}.{path.stem}")
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if obj is base_class:
                continue
            if not issubclass(obj, base_class):
                continue
            instances.append(obj(*args))
    return instances
