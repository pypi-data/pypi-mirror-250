import os
import re
import sys
import importlib.util
import pkgutil
import json
import ast
import pkg_resources

mapping = {
    "PIL": "Pillow",
    "sklearn": "scikit-learn",
    "yaml": "PyYAML",
    "dateutil": "python-dateutil",
}


def check_if_in_mapping(module_name):
    return module_name in mapping.keys()


def get_install_name(import_name):
    return mapping.get(import_name, import_name)


def is_std_lib(module_name):
    """Check if module_name is a standard library module."""
    return (
        module_name in sys.builtin_module_names
        or pkgutil.find_loader(module_name) is not None
        and "site-packages" not in importlib.util.find_spec(module_name).origin
    )


def extract_imports(notebook_path):
    with open(notebook_path, "r", encoding="utf-8") as f:
        notebook_content = f.read()

    import_statements = []

    if notebook_path.endswith(".py"):
        import_statements = re.findall(
            r"^\s*(?:import|from)\s+.+", notebook_content, re.MULTILINE
        )

    elif notebook_path.endswith(".ipynb"):
        notebook = json.loads(notebook_content)
        cells = notebook["cells"]
        for cell in cells:
            if cell["cell_type"] == "code":
                code_lines = cell["source"]
                import_lines = [
                    line
                    for line in code_lines
                    if re.match(r"^\s*(?:import|from)\s+.+", line)
                ]
                import_statements.extend(import_lines)

    return import_statements


def get_imported_modules_from_statements(statements):
    imports = set()
    for statement in statements:
        node = ast.parse(statement)
        for n in ast.walk(node):
            if isinstance(n, ast.Import):
                for name in n.names:
                    imports.add(name.name.split(".")[0])
            elif isinstance(n, ast.ImportFrom):
                imports.add(n.module.split(".")[0])
    return imports


def get_installed_packages_versions():
    return {d.project_name: d.version for d in pkg_resources.working_set}


def generate_requirements(notebook, existing_requirements):
    notebook_path = os.path.abspath(notebook)
    notebook_dir = os.path.dirname(notebook_path)
    requirements_path = os.path.join(notebook_dir, "requirements.txt")

    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                existing_requirements.add(line.split("==")[0].strip())

    import_statements = extract_imports(notebook_path)
    imported_modules = get_imported_modules_from_statements(import_statements)
    installed_packages = get_installed_packages_versions()

    with open(requirements_path, "a", encoding="utf-8") as f:
        for module in imported_modules:
            if module not in existing_requirements:
                if module in installed_packages and not check_if_in_mapping(
                    module
                ):
                    f.write(f"{module}=={installed_packages[module]}\n")
                elif not re.match(r"^mlbull", module) and not is_std_lib(
                    module
                ):
                    f.write(f"{get_install_name(module)}\n")
                existing_requirements.add(module)


def make_requirements(foldername):
    existing_requirements = set()
    if os.path.isdir(foldername):
        for filename in os.listdir(foldername):
            if filename.endswith(".ipynb") or filename.endswith(".py"):
                generate_requirements(
                    os.path.join(foldername, filename), existing_requirements
                )
    else:
        generate_requirements(foldername, existing_requirements)
