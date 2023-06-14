import os


def dict_creator(string):
    """ Function to change () into {} .
            Seems to be completely redundant"""

    string = string.replace('(', '{').replace(')', '}')  ## replace all unnecessary characters
    pairs = string.split()  ## Splits at white spaces
    return string


def branch_extractor(input_string):
    """ Takes input as a string and spits out tuple of the form ([branches], remaining_string)"""
    start_string = 'Branch Cond:'
    end_string = 'False:(Branch'
    copy_branch = []  ## holds extracted tree

    try:
        start_index = input_string.index(start_string)
        end_index = input_string.index(end_string)
        copy_branch.append(input_string[start_index: end_index])  ## copy between indices
        input_string = input_string[end_index:].strip('False:')  ## Update string
        return copy_branch, input_string
    except FileNotFoundError:
        print('No input file')


## Lets decide how many times do I need to call this function
## From analyzing the graph, whenever False:{Branch is encountered 
## A new branch is created
## So lets count the number of times this happens and use it to decide
## how many function calls should be made


""" Example Usage"""


def tree_extractor(input_file):
    """Takes tree of selected node and returns a list of sub-branches"""
    file_object = open(input_file, 'r')
    input_string = file_object.read()
    end_string = 'False:(Branch'

    branch_list = []  ## holds extracted tree
    #    branch_list = branch_extractor(input_string)[0]
    #    input_string = branch_extractor(input_string)[1]
    count = input_string.count(end_string)  ## This decides the number of branch_extractor() calls
    print(count)
    i = 0
    string = input_string
    while i < count:
        branch, string = branch_extractor(string)
        branch_list.append(branch)
        i = i + 1
    return branch_list, input_string, count


def operator_extractor(branch_list):
    '''Takes sub-tree and returns operator type  used in COND block'''
    branch = ""
    copied_line = ""
    start_string = 'Operator'
    end_string = 'Next:'  ## this does not work for inner terminals!! Needs to be fixed

    branch = str(branch_list).strip('[').strip(']')
    start_index = branch.index(start_string)
    end_index = branch.index(end_string)
    copied_line = branch[start_index + 8:end_index]
    print(copied_line.strip())
    return copied_line.strip()


def operator_type(operator):
    ''' This block returns operators'''
    match operator:
        case 'Eq':
            op_code = '=='
        case 'GreaterEq':
            op_code = '>='
        case 'GreaterThan':
            op_code = '>'
        case 'LessThan':
            op_code = '<'
        case 'LessEq':
            op_code = '<='
        case 'NotEq':
            op_code = '!='
        case 'Ulnot':
            op_code = '!'
        case 'Lor':
            op_code = '||'
        case _:
            op_code = None
    return op_code


## Function to extract terminals within COND branch
# Read sub-tree

# index Operator & first TRUE

# copy everything between these two indices

# First Terminal goes into LHS

# Second Terminal goes into RHS

####### This section reads each list object and produces Antecedants. How many antecedants will be there?? and what will be the relation between these antecedant terms?? 

# Steps:
def terminal_extractor(input_list):
    '''Takes sub-tree as input and extracts terminal to put into LHS and RHS'''
    input_string = str(input_list).strip('[').strip(']')
    LHS = ""
    RHS = ""
    start_string = 'Operator'
    end_string = ') True'
    start_index = input_string.index(start_string)
    end_index = input_string.index(end_string, start_index)
    input_string = input_string[start_index: end_index + 1]
    print('\n Printing copied string :\n', input_string)
    terminal_index = input_string.index('Terminal', start_index)
    input_string = input_string[terminal_index - 1:]
    LHS = input_string[: input_string.index(',')]
    start_string = '.'
    LHS = LHS[LHS.index(start_string) + 1:].strip(')').strip('(')
    RHS = input_string[input_string.index(','):]
    RHS = RHS[RHS.index(start_string) + 1:].strip('(').strip(')')
    return LHS, RHS


""" Function to generate Antecedants """


def generate_antecedant(antecedant_tuple):
    """ This function takes LHS, RHS and Operator and returns antecedant """
    LHS,RHS,Operator = antecedant_tuple
    antecedant = '(' + LHS + Operator + RHS + ')'
    print('\n', antecedant)
    return antecedant

def root_node_extractor(input_file):
    """Takes the complete tree as input and returns root_node name"""
    file_object = open(input_file, 'r')
    input_string = file_object.read()
    start_string = 'dest:'
    end_string = 'tree'
    start_index = input_string.index(start_string)
    end_index = input_string.index(end_string, start_index) ## Look for end_string only after start_string has been indexed
    root_string = input_string[start_index:end_index].strip()
    root_node = root_string[root_string.index('.') : ].strip('.')
    print(root_node)
    return root_node


def generate_consequent(root_node , operator, value):
    """ Produces consequent in the form of < root_node == value >"""
    consequent = '(' + root_node + operator + value + ')'
    return consequent


#input_string = '(Bind dest:usb_test.next_state tree:(Branch Cond:(Operator Eq Next:(Terminal usb_test.current_state),(Terminal usb_test.IDLE)) True:(Branch Cond:(Operator Lor Next:(Terminal usb_test.send_data),(Terminal usb_test._rn0_tx_valid)) True:(Terminal usb_test._rn1_next_state) False:(Terminal usb_test._rn2_next_state)) False:(Branch Cond:(Operator Eq Next:(Terminal usb_test.current_state),(Terminal usb_test.CRC1)) True:(Branch Cond:(Terminal usb_test.tx_ready) True:(Terminal usb_test._rn4_next_state) False:(Terminal usb_test._rn5_next_state)) False:(Branch Cond:(Operator Eq Next:(Terminal usb_test.current_state),(Terminal usb_test.CRC2)) True:(Branch Cond:(Terminal usb_test.tx_ready) True:(Terminal usb_test._rn7_next_state) False:(Terminal usb_test._rn8_next_state)) False:(Branch Cond:(IntConst 1) True:(Terminal usb_test._rn9_next_state))))))'

#root_node_extractor(input_string)
