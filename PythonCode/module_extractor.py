import subprocess
import sys
import typing

def call_dataflow_analyzer(script_path, arguments ):
    command = ['python3', script_path] + arguments
    subprocess.call(command)
    return 




def extract_module_name(file_path):
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

def remove_parentheses(string):
    return string.replace("(", "")




####### Working code ########
#### Module name extractor #####
rtl_file_path = '/Users/vinaysingh/Desktop/NeuralNetworks/DesignFiles/SystolicArchitectureDesign/'  # Replace with the actual RTL file path
rtl_file_name = 'controller.v'

module_name = extract_module_name(rtl_file_path + rtl_file_name)
module_name_new = remove_parentheses(module_name)
output_file =  'dataflow_'+ module_name_new +'.txt'

#### calling Dataflow analyzer module from pyverilog ####
script_path = '/Users/vinaysingh/Desktop/Pyverilog/examples/example_dataflow_analyzer.py'
arguments = ['-t' , module_name_new, rtl_file_path+rtl_file_name ]

##### generates dataflow #######
sys.stdout= open(output_file,'w+')
data_flow = call_dataflow_analyzer(script_path, arguments)




if module_name:
    print('\n')
    print("Module name:", module_name_new)
else:
    print("No module found in the RTL file.")
