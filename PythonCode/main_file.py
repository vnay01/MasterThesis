import os
import subprocess
from subprocess import call
import sys
import typing
import platform
## Module to find time elapsed in running this code
import time
from timeit import default_timer as timer


### My modules ###
from module_extractor import *
from tree_generator import *
from branch_extractor import *
from graph_generator import *
from rtl_modifier import * 
from sva_file_maker import *
start = timer()
timestr = time.strftime("%Y/%m/%d- %H hr-%M m.-%S s")

print('Starting Flow at...', timestr)
### Globals -- These need to be changed as arguments later
rtl_file_name = "USB_test.v"
root_node = "next_state"



""" Work starts here"""

####### Working Test code ########
########## Book Keeping and setting up directory ######
system = platform.system()
if system == "Linux":
    parent_dir = "/home/vnay01/"
    working_dir = parent_dir + "Desktop/MasterThesis/"
    output_dir = working_dir + "TestOutputs/"
    data_flow_dir = output_dir + "data_flow/"
    translated_verilog_dir = output_dir + "translated_verilog/"
elif system == "Darwin":
    parent_dir = "/Users/vinaysingh/"
    working_dir = parent_dir + "Desktop/MasterThesis/"
    output_dir = working_dir + "TestOutputs/"
    data_flow_dir = output_dir + "data_flow/"
    translated_verilog_dir = output_dir + "translated_verilog/"
elif system=="Windows":
    parent_dir = "/home/vnay01/"
    working_dir = parent_dir + "Desktop/MasterThesis/"
    output_dir = working_dir + "TestOutputs/"
    data_flow_dir = output_dir + "data_flow/"
    translated_verilog_dir = output_dir + "translated_verilog/"
else:
    print("What the hell!? Which system are you on!!?")


""" RTL file details & node selection"""
rtl_file_path = working_dir + "VerilogFiles/"
file_path = rtl_file_path + rtl_file_name


### Setting main script path ###
script_path=parent_dir + "Desktop/Pyverilog/examples/example_dataflow_analyzer.py"
# arguments = [ file_path]





#### Main work starts here #### 

module_name = extract_module_name(file_path)
module_name = module_name_clean(module_name)

print(module_name)
### Changing all blocking statements to non-blocking
output_file = working_dir + module_name +'_translated.v'
replace_assignment_operator( file_path , output_file)

file_path=os.path.abspath(output_file)
arguments = [ file_path]
##### Calling Data Flow Analyzer module #####
call_dataflow_analyzer(script_path, module_name, arguments) 

pattern = "(Bind dest:"+ module_name + '.' + root_node

data_flow_file_path = os.getcwd()+'/data_flow_'+ module_name + '.txt'

## This function extracts target node tree and returns the path to file where the tree is stored
tree_path = data_flow(data_flow_file_path, pattern, module_name, root_node)
# print(tree_path)

## This extracts tree for selected node
root_node = root_node_extractor(tree_path)
# print('\n Root Node :', root_node)

## Once tree is extracted, we need to separate sub-trees
branch_list, new_string, count = tree_extractor(tree_path)      ## tree_extractor() calls branch_extractor()
print('\n')
print('Generating sub_branches for target node : \n')
# print(branch_list)
print('\n*******************\n')
print('\n Number of branches :', count)
print('\n*******************\n')
#print(new_string)
for i in range(count):
    print(branch_list[i])
########################################################
#### Lets extract information from each sub-tree########
########################################################



"""
print('\n*******************\n')
operator = operator_extractor(branch)
# print('\n Operator: ', operator)
Operator = operator_type(operator)

#terminal = 'Branch Cond:(Operator Eq Next:(Terminal controller.current_state),(Terminal controller.INIT))) True:(Branch Cond:(Terminal controller.START) True:(Terminal controller._rn6_next_state) False:(Terminal controller._rn0_next_state)) '
LHS, RHS = terminal_extractor(branch)
print('\n*******************\n')
print('\nLHS: ', LHS)
print('\n*******************\n')
print('\nRHS: ',RHS)

antecedant_tuple = (LHS, RHS, Operator)
ant_1 = generate_antecedant(antecedant_tuple)

true_path = True_path(branch)
#print(true_path)
antecedant_2 = test_antecdant_generator(true_path)

antecedant = ant_1 + operator_type('Land') + antecedant_2 

true_value, false_value = true_cond_value(true_path)
consequent = generate_consequent(root_node, operator_type('Eq'), true_value)

## Printing Properties 

prop = property_writer(antecedant, consequent)
print('\n Property ')
print(prop)
"""

#print(cons_1)
# test_antecdant_generator(True_path(branch_list[0]))
#######################################################################################
###### vnay01: This section is required only for generating graphs in a proper way using Pyverilog's graphgen() function
if system == "Linux":
    print('\n*******************\n')
    print('\nprinting graph_generator_info: \n')
    print('\n*******************\n')
    output_file = working_dir + module_name +'_translated.v'
    script_path = parent_dir + "Desktop/Pyverilog/examples/example_graphgen.py"
    replace_assignment_operator( file_path , output_file)
    arguments = [output_file]
#### Generate graph only if the detected system is Linux
    graph_generator(script_path, module_name, root_node, arguments)
    print('\n*******************\n')
else:
    pass

#######################################################################################


""" SVA file maker"""


property_file_name = 'prop_' + module_name + '_.sva'
property_file_path = working_dir + property_file_name

''' property_genrator() calls
    1) root_node_extractor()
    2) operator_extractor()
    3) operator_type()
    4) terminal_extractor()     ## this is where single terminal values need to be handled
'''
print('\nprinting branches ::: \n ')
for i in range(count):    
    print(str(branch_list[i]).strip(']').strip('[').strip("'"))

print('\n *****************************\n')
prop = []
for i in range(count):       ## Calls property_generator (no. of branch ) times
    print('\n \t \t *** Calling property_generator( ) *** \t', i)
    property = property_generator(branch_list[i],tree_path)     ## takes one branch at a time and returns a property for the branch
    prop.append(property)

module_info_extractor(file_path, property_file_path)
property_add(property_file_path, count, prop)


## Run Time  information
end = timer()
print('\n The total run time for this code is : ',end - start, 'seconds')
