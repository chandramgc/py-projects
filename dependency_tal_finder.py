import os
import re


def find_tal_dependencies(directory):
    """
    Scan all TAL files in the specified directory and build a dependency map.

    Each TAL file is expected to use the directive:
        ?SOURCE "filename.tal"
    which indicates a dependency on another file.

    Parameters:
        directory (str): The path to the folder containing the TAL files.

    Returns:
        dict: A mapping from each TAL file to a list of dependent files.
    """
    dependencies = {}

    # List all files in the given directory that end with .tal
    for filename in os.listdir(directory):
        if filename.endswith('.tal'):
            file_path = os.path.join(directory, filename)
            dependencies[filename] = []
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Use a regex to capture dependencies declared as: ?SOURCE "filename.tal"
                    matches = re.findall(r'^\?SOURCE\s+"([^"]+)"', content, flags=re.MULTILINE)
                    dependencies[filename].extend(matches)
            except Exception as e:
                print(f"Error processing file {filename}: {e}")

    return dependencies


def print_dependency_graph(dependency_map):
    """
    Print the dependency graph from the dependency map.

    Parameters:
        dependency_map (dict): Mapping from TAL file names to list of dependencies.
    """
    print("TAL Files Dependency Graph:\n")
    for file, deps in dependency_map.items():
        if deps:
            print(f"{file} depends on:")
            for dep in deps:
                print(f"  - {dep}")
        else:
            print(f"{file} has no dependencies.")
        print()


if __name__ == '__main__':
    # Set the relative directory path to the folder containing your TAL code files.
    directory_path = './code_tal'  # Use './code_tal' if the folder is in your current working directory
    dependency_map = find_tal_dependencies(directory_path)
    print_dependency_graph(dependency_map)
