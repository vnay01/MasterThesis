import os
import subprocess
from subprocess import call
import sys
import typing

### My modules ###
from module_extractor import *

from tree_extractor import search_pattern_in_file



""" Work starts here"""

####### Working Test code ########
########## Book Keeping and setting up directory ######
parent_dir = "/Users/vinaysingh/"
working_dir = parent_dir + "Desktop/MasterThesis/"

rtl_file_path = working_dir + "VerilogFiles/"

rtl_file_name = "USB_test.v"
file_path = rtl_file_path + rtl_file_name

### Setting main script path ###
script_path=parent_dir + "Desktop/Pyverilog/examples/example_dataflow_analyzer.py"
arguments = [ file_path]


#### Main work starts here #### 

module_name = extract_module_name(file_path)
module_name_new = module_name_clean(module_name)



##### Calling Data Flow Analyzer module #####
data_flow=call_dataflow_analyzer(script_path, module_name_new, arguments) 


##### Exracting root node is not fixes yet. This needs to be made automatic
root_node = "next_state"

pattern = "(Bind dest:"+ module_name + '.' + root_node
output_file_path = working_dir+"data_flow_"+ module_name_new +".txt"

search_pattern_in_file(output_file_path, pattern, module_name_new, root_node)
