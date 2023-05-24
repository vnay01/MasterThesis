class TreeNode:
    def __init__(self, data):
        self.data = data
        self.children = []

    def add_child(self, child):
        self.children.append(child)


def generate_tree(strings):
    root = None
    stack = []

    for string in strings:
        if string.startswith('('):
            node = TreeNode(string[1:])
            if root is None:
                root = node
            else:
                stack[-1].add_child(node)
            stack.append(node)

        elif string.endswith(')'):
            while stack and not string.endswith(')'):
                stack.pop()

        else:
            node = TreeNode(string)
            if root is None:
                root = node
            else:
                stack[-1].add_child(node)

    return root


def print_tree(root, level=0):
    indent = '  ' * level
    print(indent + root.data)

    for child in root.children:
        print_tree(child, level + 1)


# Example usage
strings = ['A', '(B', 'C', '(D', 'E', 'F)', '(G', 'H)', 'I)']
tree = generate_tree(strings)
print_tree(tree)