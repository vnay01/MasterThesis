import re

edge_pattern = re.compile(r'"(.+?)"\s*->\s*"(.+?)"')

def convert_edges_to_nodes(edge_str):
    nodes = set()
    edges = []
    
    lines = edge_str.strip().split('\n')
    for line in lines:
        match = edge_pattern.search(line)
        if match:
            source_node = match.group(1)
            target_node = match.group(2)
            nodes.add(source_node)
            nodes.add(target_node)
            edges.append((source_node, target_node))
    
    nodes_str = '\n'.join(f'\t"{node}" [label="{node}"]' for node in nodes)
    edges_str = '\n'.join(f'\t"{source}" -> "{target}"' for source, target in edges)
    
    converted_str = f'strict digraph "" {{\n{nodes_str}\n{edges_str}\n}}'
    return converted_str

# Example usage
graph_str = "/home/vnay01/Desktop/MasterThesis/usb_test.txt"

converted_graph_str = convert_edges_to_nodes(graph_str)
print(converted_graph_str)
