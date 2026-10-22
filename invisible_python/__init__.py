import importlib.abc
import importlib.machinery
import importlib.util
import sys
from pathlib import Path

from .codec import decode, encode


class InvisibleLoader(importlib.abc.Loader):
    def __init__(self, filename):
        self.filename = filename

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        source = decode(self.filename.read_bytes())
        exec(compile(source, str(self.filename), "exec"), module.__dict__)


class InvisibleFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        ordinary = importlib.machinery.PathFinder.find_spec(fullname, path)
        if ordinary is not None and ordinary.loader is not None:
            return None
        name = fullname.rsplit(".", 1)[-1]
        for directory in sys.path if path is None else path:
            if not isinstance(directory, str):
                continue
            base = Path(directory or ".").resolve()
            package = base / name / "__init__.ipy"
            module = base / f"{name}.ipy"
            for filename, locations in ((package, [str(package.parent)]), (module, None)):
                if filename.is_file():
                    return importlib.util.spec_from_file_location(
                        fullname,
                        filename,
                        loader=InvisibleLoader(filename),
                        submodule_search_locations=locations,
                    )
        return None


def install():
    if not any(isinstance(finder, InvisibleFinder) for finder in sys.meta_path):
        index = sys.meta_path.index(importlib.machinery.PathFinder)
        sys.meta_path.insert(index, InvisibleFinder())
