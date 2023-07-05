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










''' Example Usage'''
