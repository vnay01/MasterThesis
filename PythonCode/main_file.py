import os
import subprocess
from subprocess import call
import sys
import typing

### My modules ###
from module_extractor import *

from tree_extractor import search_pattern_in_file
from graph_generator import graph_generator

from rtl_modifier import replace_assignment_operator 
from sva_file_maker import module_info_extractor



""" Work starts here"""

####### Working Test code ########
########## Book Keeping and setting up directory ######
parent_dir = "/home/vnay01/"
working_dir = parent_dir + "Desktop/MasterThesis/"

rtl_file_path = working_dir + "VerilogFiles/"

rtl_file_name = "USB_test.v"
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


##### Exracting root node is not fixes yet. This needs to be made automatic


output_file = working_dir + module_name +'_translated.v'
# search_pattern_in_file(output_file_path, pattern, module_name_new, root_node)
script_path = parent_dir + "Desktop/Pyverilog/examples/example_graphgen.py"

replace_assignment_operator( file_path , output_file)
arguments = [output_file]

#### Generate graph 
graph_generator(script_path, module_name, root_node, arguments)


""" SVA file maker"""
output_file = working_dir + module_name +'_p.sva'

module_info_extractor(file_path, output_file)