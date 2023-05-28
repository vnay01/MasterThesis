import os
import sys
from subprocess import call

def graph_generator(script_path, module_name, root_node ,arguments):
    """ This function calls graph_generator script from Pyverilog"""
    """Usage : python3 <path to script> -s module_name.root_node"""
    root = module_name + '.' + root_node
    command = ['python3', script_path, '-t', module_name, '-s', root] + arguments
    call(command)
    print("Graph generationn completed...")
    