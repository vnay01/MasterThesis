import os
import subprocess
from subprocess import call
import sys
import typing


def call_dataflow_analyzer(script_path, module_name_new, arguments):
    """ This function calls data_flow_analyzer from Pyverilog and returns file for further processing"""
    command = ['python3', script_path, '-t', module_name_new] + arguments
    call(command)
    print(sys.argv)


def extract_module_name(file_path):
    """Takes RTL file and produces module name """
    module_name = None
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('module'):
                parts = line.split(' ')  ## Stores module <module_name> as indexed list
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
