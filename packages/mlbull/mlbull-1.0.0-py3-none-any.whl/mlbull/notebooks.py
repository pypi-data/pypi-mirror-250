from logging import getLogger
import types
from IPython.core.interactiveshell import InteractiveShell
from IPython.core.getipython import get_ipython
from nbformat import read
from nbconvert import HTMLExporter

from mlbull.utils import reload_mlbull_dummies

from .print_logger import PrintLogger
from .precomputed import restore_precomputed, save_precomputed


logger = getLogger(__file__)


class MockShell(InteractiveShell):
    pass

    def enable_gui(self, gui=None):
        pass

    def enable_matplotlib(self, gui=None):
        pass


class NotebookLoader(object):
    """Module Loader for Jupyter Notebooks"""

    def __init__(self, path=None):
        self.shell = MockShell.instance()
        self.path = path

    def load_module(self, fullname: str, fullpath: str):
        """import a notebook as a module"""
        logger.info(f"Loading notebook {fullpath}")
        reload_mlbull_dummies()

        # load the notebook object
        with open(fullname, "r", encoding="utf-8") as f:
            nb = read(f, 4)

        mod = types.ModuleType(fullname)
        mod.__file__ = fullpath
        mod.__loader__ = self
        mod.__dict__["get_ipython"] = get_ipython
        print_logger = PrintLogger(fullpath)
        mod.__dict__["print"] = print_logger

        restore_precomputed(mod)

        # extra work to ensure that magics that would affect the user_ns
        # actually affect the notebook module's ns
        save_user_ns = self.shell.user_ns
        self.shell.user_ns = mod.__dict__

        try:
            for cell_number, cell in enumerate(nb.cells):
                if cell.cell_type != "code":
                    continue
                # transform the input to executable Python
                code = self.shell.input_transformer_manager.transform_cell(
                    cell.source
                )
                # run the code in the module
                compiled = compile(
                    code,
                    f"{fullpath} - Cell number {cell_number}",
                    mode="exec",
                )
                exec(compiled, mod.__dict__)
        finally:
            self.shell.user_ns = save_user_ns

        save_precomputed(mod)

        exporter = HTMLExporter()
        html, _ = exporter.from_notebook_node(nb)

        return mod, print_logger, html


loader = NotebookLoader()


def get_notebook_as_module(filename: str, fullpath: str):
    module, logger, html = loader.load_module(filename, fullpath)
    return module, logger, html
