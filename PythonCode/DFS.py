class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_edge(self, start_node, end_node):
        if start_node not in self.adjacency_list:
            self.adjacency_list[start_node] = []
        self.adjacency_list[start_node].append(end_node)

    def dfs(self, start_node):
        visited = set()

        def dfs_recursive(node):
            visited.add(node)
            print(node)  # Replace this line with your desired processing of the node

            if node in self.adjacency_list:
                for neighbor in self.adjacency_list[node]:
                    if neighbor not in visited:
                        dfs_recursive(neighbor)

        dfs_recursive(start_node)


# Create an instance of the graph
graph = Graph()

# Add edges based on the given DOT code
graph.add_edge("controller.next_state_graphrename_0", "Branch_graphrename_1")
graph.add_edge("Branch_graphrename_1", "Eq_graphrename_2")
graph.add_edge("Branch_graphrename_1", "Branch_graphrename_4")
# Add more edges based on the remaining DOT code

# Perform DFS starting from a specific node
start_node = "controller.next_state_graphrename_0"
graph.dfs(start_node)
