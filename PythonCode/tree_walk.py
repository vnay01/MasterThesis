### This code is meant to operate as a tree-walker somehow!

# Listing 1: Walking through a connected Component of a Graph : represented Using Adjacency Sets

def walk(G,s, S=set()):                     # Walk the graph from node s
    P,Q = dict(), set()                     # Predecessors + "to do" queue
    P[s] = None                             # s has no predecessor
    Q.add(s)                                # We plan on starting with s
    while Q:                                # Still nodes to visit
        u = Q.pop()                         # Pick one, arbitrarily
        for v in G[u].difference(P,S):      # New nodes?
            Q.add(v)                        # We plan to visit them!
            P[v] = u                        # Remember where we came from
    return P                                # The traversal tree

''' The walk function will traverse a single connected component. To find all the components, we need to wrap it in a loop over the nodes'''

# Finding connected components:
def components(G):                          # The connected components
    comp = []
    seen = set()                            # Nodes we've already seen
    for u in G:                             # Try every starting point      Looping for all nodes
        if u in seen : continue             # Seen? Ignore it
        C = walk(G,u)                       # Traverse component           
        seen.update(C)                      # Add keys of C to seen
        comp.append(C)                      # Collect the components
    return comp




class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

def generate_graph(root):
    graph = {}
    visited = set()

    def dfs(node):
        if node in visited:
            return

        visited.add(node)
        graph[node.value] = []

        for child in node.children:
            graph[node.value].append(child.value)
            dfs(child)

    dfs(root)
    return graph

# Example usage
root_node = Node("(Bind dest:usb_test.tx_valid tree:(Branch Cond:(Operator Eq Next:(Terminal usb_test.current_state),(Terminal usb_test.IDLE)) True:(Branch Cond:(Terminal usb_test.send_data) True:(IntConst 1'b1) False:(IntConst 1'b1)) False:(Branch Cond:(Operator Eq Next:(Terminal usb_test.current_state),(Terminal usb_test.CRC1)) True:(Branch Cond:(Operator Ulnot Next:(Terminal usb_test.tx_ready)) True:(IntConst 1'b1) False:(IntConst 1'b1)) False:(Branch Cond:(Operator Eq Next:(Terminal usb_test.current_state),(Terminal usb_test.CRC2)) True:(Branch Cond:(Terminal usb_test.tx_ready) True:(IntConst 1'b0) False:(IntConst 1'b0)) False:(Branch Cond:(IntConst 1) True:(IntConst 1'b0))))))")
# Build the tree structure based on the provided input
# Add child nodes to root_node.children based on the input

graph = generate_graph(root_node)
print(graph)








''' Example Usage'''
