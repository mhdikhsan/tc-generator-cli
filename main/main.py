import sys
from py2cfg import CFGBuilder
from sklearn.cluster import KMeans
import numpy as np
import json
import os
import time
import warnings

warnings.filterwarnings("ignore")


start_time = time.time()


class Object:
    def __init__(self, _gvid, name, label):
        self._gvid = _gvid
        self.name = name
        self.label = label


class Edge:
    def __init__(self, tail, head):
        self.tail = tail
        self.head = head


class Node:
    def __init__(self, name, id, label, targets=None, predecessors=None, paths=None):
        self.name = name
        self.id = id
        self.label = label
        self.targets = targets or []
        self.predecessors = predecessors or []
        self.paths = paths or []


class NodeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Node):
            return {
                'name': obj.name,
                'id': obj.id,
                'label': obj.label,
                'targets': obj.targets,
                'predecessors': obj.predecessors,
                'paths': obj.paths
            }
        return super().default(obj)

def separate_functions(file_path):
    functions = []
    current_function = ""
    indent_level = 0
    inside_class = False

    with open(file_path, "r") as file:
        for line in file:
            line = line.rstrip()  # Remove trailing whitespace

            # Check if the line starts with "class"
            if line.startswith("class"):
                # Save the previously collected function
                if current_function:
                    functions.append(current_function)

                current_function = line
                indent_level = line.index("class")
                inside_class = True
                
            # Check if the line starts with "def", "async def", or "@"
            elif line.startswith("def") or line.startswith("async def") or line.startswith("@"):
                # Save the previously collected function
                if current_function:
                    functions.append(current_function)

                current_function = line
                indent_level = line.index("def") if line.startswith("def") or line.startswith("async def") else line.index("@") + 1
                inside_class = False

            else:
                # Append the line to the current function with indentation
                if current_function:
                    current_function += "\n" + " " * indent_level + line

    # Append the last function after reaching the end of the file
    if current_function:
        functions.append(current_function)

    return functions



def generate_basis_set(cfg):
    basis_set = []
    visited = set()

    def get_path(node, current_path):
        current_path.append(node.id)
        visited.add(node.id)

        if not node.targets:
            if len(current_path) > 1:  # Exclude single-node paths
                basis_set.append(current_path[:])
        else:
            for target_id in node.targets:
                if target_id not in visited:
                    get_path(cfg[target_id], current_path[:])

        visited.remove(node.id)

    for start_node in cfg.values():
        get_path(start_node, [])

    return basis_set


def generate_coverage_report(cfg, function_id, basis_set):
    # Define the paths
    paths = basis_set

    # Get all unique branches from the paths
    unique_branches = set()
    for path in paths:
        for branch in path:
            unique_branches.add(branch)

    # Convert paths to feature vectors
    feature_vectors = []
    for path in paths:
        vector = [1 if branch in path else 0 for branch in unique_branches]
        feature_vectors.append(vector)

    # Convert feature vectors to numpy array
    X = np.array(feature_vectors)

    # Automatically calculate the number of clusters
    if (len(paths) <= 0):
        return
    k = int(np.sqrt(len(paths)))
    kmeans = KMeans(n_clusters=k, random_state=0).fit(X)

    # Get cluster labels
    labels = kmeans.labels_

    # Create a dictionary to store the highest coverage in each cluster along with the nodes
    cluster_coverage = {}

    # Calculate coverage percentage for each path and find the highest coverage in each cluster
    for i, path in enumerate(paths):
        covered_branches = set(path)
        coverage_percentage = (len(covered_branches) /
                               len(unique_branches)) * 100
        cluster_id = labels[i]

        if cluster_id not in cluster_coverage:
            cluster_coverage[cluster_id] = [(i, coverage_percentage, path)]
        else:
            if coverage_percentage > cluster_coverage[cluster_id][0][1]:
                cluster_coverage[cluster_id] = [(i, coverage_percentage, path)]
            elif coverage_percentage == cluster_coverage[cluster_id][0][1]:
                cluster_coverage[cluster_id].append(
                    (i, coverage_percentage, path))

    # Calculate the overall average percentage
    average_percentages = []
    for cluster_id, test_cases in cluster_coverage.items():
        highest_coverage = max(test_cases, key=lambda x: x[1])
        average_percentages.append(highest_coverage[1])

    overall_average_percentage = sum(
        average_percentages) / len(average_percentages)

    end_time = time.time()
    execution_time = end_time - start_time

    # Create a text file to save the output
    output_file = open(f"output {function_id}.txt", 'w')

    # Write the test cases with the highest coverage in each cluster to the output file
    output_file.write("Test Cases with Highest Coverage in Each Cluster:\n")
    for cluster_id, test_cases in cluster_coverage.items():
        output_file.write(f"Cluster {cluster_id + 1}:\n")
        for test_case_id, coverage_percentage, nodes in test_cases:
            output_file.write(
                f"Test Case {test_case_id + 1}: Coverage = {coverage_percentage:.2f}%\n")
            output_file.write("Nodes: " + ", ".join(str(node)
                                                    for node in nodes) + "\n")
            output_file.write("\n")

    output_file.write(
        f"Overall Average Percentage = {overall_average_percentage:.2f}%\n")
    output_file.write(f"Program execution time: {execution_time} seconds\n")

    output_file.close()

    # print test cases
    testcase_directory = f"test_cases function {function_id}"
    if not os.path.exists(testcase_directory):
        os.makedirs(testcase_directory)

    for cluster_id, test_cases in cluster_coverage.items():
        for test_case_id, coverage_percentage, nodes in test_cases:
            output_file_path = os.path.join(
                testcase_directory, f"Test Case {test_case_id + 1}.py")
            output_file = open(output_file_path, 'w')
            for node in nodes:
                output_file.write(cfg[node].label + "\n")
            output_file.close()


folder_path = sys.argv[1]
id = 0
# Get all files with .py extension in the folder
py_files = [file for file in os.listdir(folder_path) if file.endswith('.py')]

# Iterate over each .py file
for file_name in py_files:
    file_path = os.path.join(folder_path, file_name)
    function_list = separate_functions(file_path)

    # Iterate over each function in the file
    for function in function_list:
        id += 1
        try:
            cfg = CFGBuilder().build_from_src('cfg', function)
        except SyntaxError:
            continue
        cfg_visual = cfg.build_visual(
            f'cfgvisual {id}', 'json', build_keys=False, calls=False)
        cfg.build_visual(
            f'cfg_visual/cfgvisual {id}', 'png', build_keys=False, calls=False , show=False)

        try:
            with open(f'cfgvisual {id}.json') as json_file:
                data = json.load(json_file)

            cfg = {}

            for obj in data['objects']:
                cfg[obj['_gvid']] = Node(
                    obj['name'], obj['_gvid'], obj['label'].replace("\\l", "\n"))

            for edge in data['edges']:
                cfg[edge['tail']].targets.append(edge['head'])
                cfg[edge['head']].predecessors.append(edge['tail'])

            basis_set = generate_basis_set(cfg)

            generate_coverage_report(cfg, id, basis_set)

        except KeyError:
            continue
