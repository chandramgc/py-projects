import os
import re
import graphviz


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
                    # Use regex to capture dependency lines, e.g., ?SOURCE "common.tal"
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


def plot_dependency_graph(dependency_map, output_filename='tal_dependency_graph'):
    """
    Plot the dependency graph using Graphviz and save it as an image.

    Parameters:
        dependency_map (dict): Mapping from TAL file names to list of dependencies.
        output_filename (str): Base name for the output file (without extension).
    """
    # Create a directed graph
    dot = graphviz.Digraph(comment='TAL Files Dependency Graph')

    # Add all files as nodes to the graph.
    for file in dependency_map:
        dot.node(file, file)

    # For each file, add edges for its dependencies.
    for file, deps in dependency_map.items():
        for dep in deps:
            dot.edge(file, dep)

    # Render the graph to an output file (e.g., a PNG file) and optionally view it.
    output_path = dot.render(output_filename, format='png', view=True)
    print(f"Graph saved to: {output_path}")


if __name__ == '__main__':
    # Set the relative path to the TAL code files folder
    directory_path = './code_tal'
    dependency_map = find_tal_dependencies(directory_path)

    print_dependency_graph(dependency_map)
    plot_dependency_graph(dependency_map)
