import os
import subprocess
import sys
import typing

from tree_extractor import tree_extractor



def call_dataflow_analyzer(script_path, arguments ):
    """ This function calls data_flow_analyzer from Pyverilog and returns file for further processing"""
    command = ['python3', script_path] + arguments
    subprocess.call(command)
    



def extract_module_name(file_path):
    """Takes RTL file and produces module name """
    module_name = None
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('module'):
                parts = line.split(' ') ## Stores module <module_name> as indexed list
                if len(parts) > 1:
                    module_name = parts[1]
                break
    return module_name

def module_name_clean(module_name_unclean):
    """Cleans extracted module name"""
    if "#" in module_name_unclean:
        index = module_name_unclean.index("#")

    elif "(" in module_name_unclean:
        index = module_name_unclean.index("(")
        
    else:
        return module_name_unclean
    return module_name_unclean[:index]
    


####### Working Test code ########
#### Module name extractor #####
# rtl_file_path = "/Users/vinaysingh/Desktop/NeuralNetworks/DesignFiles/Convolution/"  # Replace with the actual RTL file path
rtl_file_path = "/home/vnay01/Desktop/MasterThesis/VerilogFiles/"
rtl_file_name = "USB_test.v"
file_path = rtl_file_path + rtl_file_name

module_name = extract_module_name(rtl_file_path+rtl_file_name)
module_name_new = module_name_clean(module_name)

script_path="/home/vnay01/Desktop/Pyverilog/examples/example_dataflow_analyzer.py"
arguments = ['-t ', module_name_new , file_path]
##### Calling Data Flow Analyzer module #####

data_flow=call_dataflow_analyzer(script_path, arguments) 

if module_name:
    print('\n')
    print("Module name:", module_name_new)
else:
    print("No module found in the RTL file.")
