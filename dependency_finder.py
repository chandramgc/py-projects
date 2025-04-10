import os
import re
import sys
from collections import defaultdict


def get_tao_files(root_dir):
    """
    Recursively collect all Tao (.tao) files starting from root_dir.
    """
    tao_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            # print(f"Found file: {filename}")
            if filename.endswith('.tao'):
                tao_files.append(os.path.join(dirpath, filename))
    return tao_files


def module_name_from_path(file_path, root_dir):
    """
    Convert a file path into a module name relative to root_dir.
    The module name is the file’s relative path (with forward slashes)
    with the ".tao" extension removed.

    For example, if file_path is "/path/to/code/task.tao" and
    root_dir is "/path/to/code", the module name becomes "task".
    For a nested file like "/path/to/code/lib/util.tao", the module name
    becomes "lib/util".
    """
    rel_path = os.path.relpath(file_path, root_dir)
    # Normalize OS-specific separators to forward slashes
    rel_path = rel_path.replace(os.sep, "/")
    if rel_path.endswith(".tao"):
        rel_path = rel_path[:-len(".tao")]
    return rel_path


def parse_imports(file_content):
    """
    Parse the content of a Tao file and return a set of imported module names.
    This function looks for lines like:
      import "filename.tao";
    and extracts the file name (without the .tao extension).
    """
    pattern = re.compile(r'import\s+"([^"]+\.tao)"')
    matches = pattern.findall(file_content)
    imported = set()
    for m in matches:
        # Remove the ".tao" extension and normalize path separators.
        if m.endswith(".tao"):
            m = m[:-len(".tao")]
        m = m.replace("\\", "/")
        imported.add(m)
    return imported


def build_dependency_graph(root_dir):
    """
    Build a dependency graph for all Tao files under root_dir.
    Each key is a module (computed from the file path) and its value is a set of
    modules it directly depends on (i.e. that it imports).
    """
    tao_files = get_tao_files(root_dir)
    file_to_module = {}
    module_to_file = {}

    # Create mappings between file paths and module names.
    for file in tao_files:
        mod = module_name_from_path(file, root_dir)
        file_to_module[file] = mod
        module_to_file[mod] = file

    local_modules = set(module_to_file.keys())
    dependencies = defaultdict(set)

    for file in tao_files:
        mod = file_to_module[file]
        try:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file}: {e}")
            continue

        imports = parse_imports(content)
        # Record the dependency if an imported module is local.
        for imp in imports:
            if imp in local_modules:
                dependencies[mod].add(imp)
        # Ensure the module appears in the graph even if it has no imports.
        if mod not in dependencies:
            dependencies[mod] = set()

    return dependencies, module_to_file


def print_dependency_graph(dependencies):
    """
    Print the dependency graph in a human-readable format.
    """
    for mod in sorted(dependencies.keys()):
        print(f"Module: {mod}")
        deps = dependencies[mod]
        if deps:
            for dep in sorted(deps):
                print(f"  depends on: {dep}")
        else:
            print("  no dependencies")
        print()


def main():
    if len(sys.argv) < 2:
        print("Usage: python dependency_finder.py <relative_path_to_code_folder>")
        sys.exit(1)
    root_dir = sys.argv[1]
    # Convert the relative path to an absolute path.
    root_dir = os.path.dirname(__file__) + "\\" + root_dir
    dependencies, module_to_file = build_dependency_graph(root_dir)
    print("Dependency Graph:")
    print("-----------------")
    print_dependency_graph(dependencies)


if __name__ == "__main__":
    main()
