import os
import subprocess
from subprocess import call
import sys
import typing

### My modules ###
from module_extractor import *
from tree_generator import *
from branch_extractor import *
from graph_generator import graph_generator
from rtl_modifier import replace_assignment_operator 
from sva_file_maker import module_info_extractor



""" Work starts here"""

####### Working Test code ########
########## Book Keeping and setting up directory ######
parent_dir = "/home/vnay01/"
working_dir = parent_dir + "Desktop/MasterThesis/"
output_dir = working_dir + "TestOutputs/"
data_flow_dir = output_dir + "data_flow/"
translated_verilog_dir = output_dir + "translated_verilog/"

""" RTL file details & node selection"""
rtl_file_path = working_dir + "VerilogFiles/"
rtl_file_name = "controller.v"
file_path = rtl_file_path + rtl_file_name
root_node = "next_state"




### Setting main script path ###
script_path=parent_dir + "Desktop/Pyverilog/examples/example_dataflow_analyzer.py"
arguments = [ file_path]


#### Main work starts here #### 

module_name = extract_module_name(file_path)
module_name = module_name_clean(module_name)


##### Calling Data Flow Analyzer module #####
call_dataflow_analyzer(script_path, module_name, arguments) 

pattern = "(Bind dest:"+ module_name + '.' + root_node

data_flow_file_path = os.getcwd()+'/data_flow_'+ module_name + '.txt'

## This function extracts target node tree and returns the path to file where the tree is stored
tree_path = data_flow(data_flow_file_path, pattern, module_name, root_node)

## This extracts tree for selected node

# input_file = os.getcwd() + '/'
## Once tree is extracted, we need to separate sub-trees
## branch_extractor() does this. It returns a list of all sub-branches
# sub_branch_extractor() returns a tuple of (list of sub-trees, number of sub-trees)
branch_list, new_string, count = tree_extractor(tree_path)
print('\n')
print('Generating sub_branches for target node : \n')
#print(branch_list)
print('\n*******************\n')
print('\n*******************\n')
print(new_string)
print(count)

for i in range(count):
    print(branch_list[i])
    


#### Lets extract information from each sub-tree


print('\n*******************\n')

#######################################################################################

###### vnay01: This section is required only for generating graphs in a proper way using Pyverilog's graphgen() function
output_file = working_dir + module_name +'_translated.v'
script_path = parent_dir + "Desktop/Pyverilog/examples/example_graphgen.py"
replace_assignment_operator( file_path , output_file)
arguments = [output_file]

#### Generate graph 
# graph_generator(script_path, module_name, root_node, arguments)
#######################################################################################

""" SVA file maker"""
output_file = working_dir + module_name +'_p.sva'

# module_info_extractor(file_path, output_file)