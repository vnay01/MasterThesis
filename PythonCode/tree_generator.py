class TreeNode:
    def __init__(self, label):
        self.label = label
        self.children = []

def generate_tree(expression):
    stack = []
    current_node = None
    i = 0

    while i < len(expression):
        if expression[i] == '(':
            node_label = ''
            i += 1

            while i < len(expression) and expression[i] != ' ' and expression[i] != ':':
                node_label += expression[i]
                i += 1

            new_node = TreeNode(node_label)

            if current_node:
                current_node.children.append(new_node)

            current_node = new_node
            stack.append(current_node)

        elif expression[i] == ')':
            if stack:
                stack.pop()
            if stack:
                current_node = stack[-1]
            i += 1

        elif expression[i] == ' ':
            i += 1

        elif expression[i].isalpha():
            node_label = ''

            while i < len(expression) and expression[i] != ' ' and expression[i] != ')':
                node_label += expression[i]
                i += 1

            new_node = TreeNode(node_label)
            current_node.children.append(new_node)

        else:
            i += 1

    return current_node

expression = "(Bind dest:usb_test.next_state tree:(Branch Cond:(Operator Eq Next:(Terminal usb_test.current_state),(Terminal usb_test.IDLE)) True:(Branch Cond:(Terminal usb_test.send_data) True:(Terminal usb_test._rn1_next_state) False:(Terminal usb_test._rn2_next_state)) False:(Branch Cond:(Operator Eq Next:(Terminal usb_test.current_state),(Terminal usb_test.CRC1)) True:(Branch Cond:(Terminal usb_test.tx_ready) True:(Terminal usb_test._rn4_next_state) False:(Terminal usb_test._rn5_next_state)) False:(Branch Cond:(Operator Eq Next:(Terminal usb_test.current_state),(Terminal usb_test.CRC2)) True:(Branch Cond:(Terminal usb_test.tx_ready) True:(Terminal usb_test._rn7_next_state) False:(Terminal usb_test._rn8_next_state)) False:(Branch Cond:(IntConst 1) True:(Terminal usb_test._rn9_next_state))))))"
tree = generate_tree(expression)
print((tree.label))
print((tree.children))