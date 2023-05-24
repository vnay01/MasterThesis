def extract_nodes(tree):
    if isinstance(tree, dict):
        nodes = []
        for key, value in tree.items():
            if key == "Next":
                nodes.extend(extract_nodes(value))
            elif key == "True" or key == "False":
                nodes.append(value)
            elif isinstance(value, dict):
                nodes.extend(extract_nodes(value))
        return nodes
    elif isinstance(tree, list):
        nodes = []
        for item in tree:
            nodes.extend(extract_nodes(item))
        return nodes
    else:
        return []


## Example
input_tree = "/home/vnay01/Desktop/MasterThesis/data_flow_tree_state.txt"
print(extract_nodes(input_tree))