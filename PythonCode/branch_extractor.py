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
    copy_branch = []            ## this list object holds extracted branches
    try:

        start_index = input_string.index(start_string)  
        end_index = input_string.index(end_string)
        copy_branch.append(input_string[start_index : end_index])
        input_string = input_string[end_index:].strip('False:')   

        return copy_branch, input_string
    except FileNotFoundError: 
        print('No input file')


    
## Lets decide how many times do I need to call this function
## From analyzing the graph, whenever False:{Branch is encountered 
## A new branch is created
## So lets count the number of times this happens and use it to decide
## how many function calls should be made


""" Example Usage"""
# input_string = '(Bind dest:usb_test.next_state tree:(Branch Cond:(Operator Eq Next:(Terminal usb_test.current_state),(Terminal usb_test.IDLE)) True:(Branch Cond:(Terminal usb_test.send_data) True:(Terminal usb_test._rn1_next_state) False:(Terminal usb_test._rn2_next_state)) False:(Branch Cond:(Operator Eq Next:(Terminal usb_test.current_state),(Terminal usb_test.CRC1)) True:(Branch Cond:(Terminal usb_test.tx_ready) True:(Terminal usb_test._rn4_next_state) False:(Terminal usb_test._rn5_next_state)) False:(Branch Cond:(Operator Eq Next:(Terminal usb_test.current_state),(Terminal usb_test.CRC2)) True:(Branch Cond:(Terminal usb_test.tx_ready) True:(Terminal usb_test._rn7_next_state) False:(Terminal usb_test._rn8_next_state)) False:(Branch Cond:(IntConst 1) True:(Terminal usb_test._rn9_next_state))))))'

## Read file
input_file = '/home/vnay01/Desktop/MasterThesis/data_flow_tree_state.txt'
file_object = open(input_file,'r')
input_string = file_object.read()


end_string = 'False:(Branch'
count = input_string.count(end_string)      ## count the total number of requried function calls

branch_list = []    ## holds extracted tree

for i in range(count):
    branch_list.append(branch_extractor(input_string)[0])
    input_string = branch_extractor(input_string)[1]

"""
for i in range(count):
    print(branch_list[i])
"""
# print(len(branch_list))



####### This section reads each list object and produces Antecedants. How many antecedants will be there?? and what will be the relation between these antecedant terms?? 

# Steps:

# Read each index from the list
new_branch = str(branch_list[0]).strip('[').strip(']')

print((new_branch))
# Extract Conditions . What should I do to extract this information. 
## Search for Operator __ Next:(Terminal  string . Save its index
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