import os
from types import ModuleType

import mlbull_dummies

ROOT_CACHE_DIR = os.path.expanduser("~/.cache/mlbull")

try:
    os.mkdir(ROOT_CACHE_DIR)
except FileExistsError:
    pass


def save_precomputed(module: ModuleType):
    cache_file_name = os.path.join(ROOT_CACHE_DIR, module.__name__)

    with open(cache_file_name, "wb+") as f:
        f.write(mlbull_dummies.precompute_function.export_results())


def restore_precomputed(module: ModuleType):
    cache_file_name = os.path.join(ROOT_CACHE_DIR, module.__name__)

    try:
        with open(cache_file_name, "rb+") as f:
            cached = f.read()
            gatherer = mlbull_dummies.PrecomputeGatherer(cached)
            # This is necessary to ensure the object is available from the
            # external module
            module.__dict__["precompute_function"] = gatherer
            mlbull_dummies.precompute_function = gatherer
    except FileNotFoundError:
        print(f"No cache for {module.__name__} found!")
        return
