import os


def dict_creator(string):

    """ Function to change () into {} . 
            Seems to be completely redundant"""

    string = string.replace('(' , '{').replace(')', '}')     ## replace all unnecessary characters
    pairs =  string.split()     ## Splits at white spaces
    return string






def branch_extractor(input_string):
    """ Takes input as a string and spits out tuple of the form ([branches], remaining_string)"""
    start_string = 'Branch Cond:'
    end_string = 'False:(Branch'
    copy_branch = []    ## holds extracted tree

    try:        
        start_index = input_string.index(start_string)  
        end_index = input_string.index(end_string)
        copy_branch.append(input_string[start_index : end_index])       ## copy between indices
        input_string = input_string[end_index:].strip('False:')         ## Update string
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
    file_object = open(input_file,'r')
    input_string = file_object.read() 
    end_string = 'False:(Branch'

    branch_list = []    ## holds extracted tree
#    branch_list = branch_extractor(input_string)[0]
#    input_string = branch_extractor(input_string)[1]
    count = input_string.count(end_string)          ## This decides the number of branch_extractor() calls
    print(count)
    i = 0
    string = input_string
    while ( i < count):
        
        branch, string = branch_extractor(string)
        branch_list.append(branch)
        i = i + 1
#        print('tree_extractor_new_string \n',input_string)
#        print('\n i : ', i, string)

    return branch_list, input_string, count



def sub_tree(branch_list):
    branch = ""
    copied_line = ""
    start_string ='Operator'
    end_string = '))'               ## this does not work for inner terminals!! Needs to be fixed
    branch = str(branch_list).strip('[').strip(']')
    start_index = branch.index(start_string)
    end_index = branch.index(end_string)
    copied_line = branch[start_index:end_index+1]
    return copied_line


####### This section reads each list object and produces Antecedants. How many antecedants will be there?? and what will be the relation between these antecedant terms?? 

# Steps:

# Read each index from the list

# new_branch = str(branch_list[0]).strip('[').strip(']')

# Extract Conditions . What should I do to extract this information. 
## Search for Operator __ Next:(Terminal  string . Save its index
"""
start_string = 'Operator'
end_string = '))'

start_index = new_branch.index(start_string)


## Look for ending )). Save its index
end_index = new_branch.index(end_string)
print('\n*******************\n')
print(start_index)
print(new_branch[end_index-2])

## Copy everything in between these two indices
copied_line = new_branch[start_index:end_index+1]           ## Just to look more symmetrical
print('\nPrinting copied line: \n')
print(copied_line)


###### Deciding what to put in op_code
######################3
print('Printing new_branch line: \n')
print((new_branch).split(copied_line))

op_code = ''

operator_index_start = copied_line.find('Operator')
operator_index_end = copied_line.find('Next')
operator = copied_line[operator_index_start+9:operator_index_end]
print(operator)

if 'Eq' in operator:
    op_code = '=='


## Look for (Terminal and ), .Copy everything between these two indices into LHS and the second occurrence into RHS
start_string = '(Terminal'
end_string = ')'

start_index = copied_line.index(start_string)
end_index = copied_line.index(end_string)

print(start_index)
print(end_index)

# Save as a tuple (LHS, operator ,RHS) 
lhs_copy = copied_line[start_index:end_index+1]
copied_line = copied_line[end_index+2: ]
print(copied_line)
start_index = copied_line.index(start_string)
end_index = copied_line.index(end_string)
print(start_index)
print(end_index)

rhs_copy = copied_line[start_index:end_index+1]
start_index = lhs_copy.index('.')
end_index = lhs_copy.index(')')

lhs_copy=lhs_copy[start_index+1: end_index]

rhs_copy = rhs_copy[start_index+1: end_index].strip(')').strip('(')

print(lhs_copy)
print(rhs_copy)



antecedant = '(' + lhs_copy + op_code + rhs_copy + ')'

print('Antecedant : ', antecedant)
# Extract Branch Cond: ::: This will also go into antecedant 


## Use TRUE & False branches to assign values to (consequent)
"""