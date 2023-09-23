## New file to test if import Pyverilog works
""" Author : ESNIVIN / vnay01"""
#! /proj/cot/conda/envs/cot_py0/bin/python
# #! /proj/cot/conda/envs/iverilog0/bin/iverilog


from __future__ import absolute_import
from __future__ import print_function

import os
import subprocess
from subprocess import call
import sys
import typing
import platform
from optparse import OptionParser

from memory_profiler import profile


# import pyverilog
from pyverilog import *
from pyverilog.dataflow import *
from pyverilog.dataflow.dataflow_analyzer import *
from pyverilog.dataflow.optimizer import *
from pyverilog.dataflow.graphgen import *
from pyverilog.dataflow.dataflow_codegen import *

from pyverilog.dataflow.optimizer import *
from pyverilog.dataflow.graphgen import *

import pyverilog.vparser.ast as vast
from pyverilog.vparser.parser import *
from pyverilog.ast_code_generator.codegen import *


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

# @profile


def main():
    start = timer()
    timestr = time.strftime("%Y/%m/%d- %H hr-%M m.-%S s")

    print("Starting Flow at...", timestr)
    ### Globals -- These need to be changed as arguments later
    rtl_file_name = "test.v"
    top_module = "test"

    ##### reset type info #####
    """
        0 -> active_low reset
        1 -> active_high reset
    """
    reset_name = "reset"  # give reset name here
    reset_type = 1  # Active_low or Active_high ?? refer comment above for details

    if reset_type == 0:
        reset_name = "!" + reset_name
    else:
        reset_name = reset_name

    print("\n RESET Name: ", reset_name)

    #### Pass the index of desired root node(s):
    root_node_list = [5]

    """ Work starts here"""
    ####### Working Test code ########
    ########## Book Keeping and setting up directory #####
    system = platform.system()
    if system == "Linux":
        parent_dir = "/home/" + os.getlogin() + "/"
        working_dir = parent_dir + "Desktop/MasterThesis/"
        if not os.path.exists("TestOutputs"):
            os.mkdir("TestOutputs")
        output_dir = working_dir + "TestOutputs/"
        if not os.path.exists("temp"):
            os.mkdir("temp")
        temp = working_dir + "temp/"
        data_flow_dir = output_dir + "data_flow/"
        translated_verilog_dir = output_dir + "translated_verilog/"
    elif system == "Darwin":
        parent_dir = "/Users/vinaysingh/"
        working_dir = parent_dir + "Desktop/MasterThesis/"
        output_dir = working_dir + "TestOutputs/"
        temp = working_dir + "temp/"
        data_flow_dir = output_dir + "data_flow/"
        translated_verilog_dir = output_dir + "translated_verilog/"
    elif system == "Windows":
        parent_dir = "/home/vnay01/"
        working_dir = parent_dir + "Desktop/MasterThesis/"
        output_dir = working_dir + "TestOutputs/"
        temp = working_dir + "temp/"
        data_flow_dir = output_dir + "data_flow/"
        translated_verilog_dir = output_dir + "translated_verilog/"
    else:
        print("What the hell!? Which system are you on!!?")

    """ RTL file details & node selection"""

    rtl_file_path = working_dir + "VerilogFiles/"
    # /home/vnay01/Desktop/MasterThesis/VerilogFiles/usb/trunk/rtl/verilog/usbf_top.v
    # /home/vnay01/Desktop/MasterThesis/VerilogFiles/fpga-median/trunk/rtl/state_machine.v

    file_path = rtl_file_path + rtl_file_name
    translated_file_path = rtl_file_path + top_module + "_translated.v"
    input_file = file_path
    output_file = translated_file_path

    module_name = top_module

    if not os.path.exists("Properties"):
        os.mkdir("Properties")
    property_file_name = "property_" + module_name + ".sva"
    property_file_path = os.path.abspath("Properties") + "/" + property_file_name

    ### Call this function to modify assignment oeprators
    replace_assignment_operator(input_file, output_file)

    ## Add bind information
    bind_adder(file_path, property_file_path)

    port_name=module_info_extractor(file_path, property_file_path)
    start_string='('
    end_string = ')'
    start_index = port_name.index(start_string)
    end_index = port_name.index(end_string)
    port_name = port_name[start_index+1:end_index]
    
    # create a list of port names
    port_name_list = port_name.split(', ')
    print("Printing extracted port names " + str(port_name_list))

    data_flow = VerilogDataflowAnalyzer(output_file, top_module)  ## Create a dataflow object.
    #    print(data_flow)                                                   ## Expecting an object of class VerilogDataflowAnalyzer()

    ## Using generate() to get an object of type  'VerilogDataflowAnalyzer'
    data_flow.generate()

    directives = (data_flow.get_directives())  ## Checks for directives ( i.e. #define , `include etc. )

    terms = data_flow.getTerms()  ## This returns a dictionary of all terms in RTL
    # checker code to determine the type of nodes
    print("\nTerm:")
    for tk, tv in sorted(terms.items(), key=lambda x: str(x[0])):
        print(tv.tostr())

    terms_keys = (terms.keys())  ## Returns a dict_key type object. This can be used to select root nodes of dataflow tree
    # Since dict_key is non-subscriptable, we convert it into subscriptable type - either a list or tuple
    terms_keys_list = list(terms_keys)

    """
    ## Checker code
    for i in range(len(terms_keys)):
        print('\n', [i] ,'List of keys: ' ,terms_keys_list[i])
    print('\n')
    """
    # Binding information
    binddict = data_flow.getBinddict()  # returns a dict object
    binddict_keys = list(binddict.keys())  # create a list of keys from previous dictionary
    print("\n These are the nodes for which dataflow trees can be generated : ")
    for i in range(len(binddict_keys)):
        print("\n", [i], "List of Binding keys: ", binddict_keys[i])

    """
    #### get root_node_name from keys
    root_node_name = str(binddict_keys[root_node])
    root_node_name = root_node_name[root_node_name.find('.')+1:]
    print('\n Root Node Name : ', root_node_name)
    print('\n ********** \n')
    """
    """
    for bk, bv in sorted(binddict.items(), key=lambda x: str(x[0]), reverse=False):
        for bvi in bv:
            #print(bvi.tostr())
            print(bvi.tostr())  
    """

    print("\n\n Generating tree structure for selected node : ")
    a = ""

    ## Looping through list of root_nodes

    for j in root_node_list:
        for i in binddict.get(binddict_keys[j]):  ## Use 'keys' for generating properties for cycling through root nodes. This is required to increase Formal Coverage
            print(i.tostr_mod(), "\n i is printed")  ## Converts object into string & helps in debugging
            print("\n", i.tostr(), "\n ***********\n\n")  ## Converts object into string & helps in debugging
            print(" Pyverilog function call")
            print("\n This is how Pyverilog creates a tree internally \n    ", i._assign())  # actual. To be removed
            print(" *****modified function call *****")
            a = i._always_combination_mod()  # calling method() on object of Bind class

            # checker code
            # print('\n PRINITNG data stored in a :', (a))
        print("\n ***** Root Node Index : ", j)

        line_buff = ""
        line_buff = a[:-1].strip()
        line_buff = (line_buff.splitlines())  # This creates a list of all properties but also includes empty items within the list
        print("\n Printing line_buff \n:", line_buff)
        # We need to remove all empty items from the list
        #    line_buff = [value for value in line_buff if value != '']
        print("\n Modified Line_buff \n", line_buff)

        ## Check number of items in the list
        print("\n\n Number of items in line_buff \n: ", len(line_buff))
        #    prop = create_property(line_buff[0])
        #    print('\n XY :: ',prop)
        prop_list = list_pair(line_buff)  # Split property list
        #    print('prop_list \n',prop_list)
        print("\n\n True_condition_property: ")  # Check correctness
        for i in range(len(prop_list[0])):
            print([i], " ", prop_list[0][i])

        print("\n\n False_condition_property: ", prop_list[1])  # Check correctness

        true_part = ""
        false_part = ""

        ## ammend the antecedant part of false_condition
        # def prop_make(prop_list):
        print("\ length of prop_list : ", len(prop_list[0]))
        ## Open an sva file:
        true_path_list = []
        false_path_list = []

        for i in range(len(prop_list[0])):  # Use this to control the number of properties generated
            true_part = str(prop_list[0][i])
            print("Printing TRUE PART of branch properties ::  \n" + true_part)
            false_part = str(prop_list[1][i])
            ## search for |-> string
            if "|->" in true_part:  # Normal Operation
                start_index = true_part.index("|->")
                antecedant_part = (true_part[:start_index].strip(" &&").strip("&&").strip("&& ").strip(" && ").strip())
                true_part = (antecedant_part + true_part[start_index:].strip(" &&").strip("&&").strip("&& ").strip(" && ").strip())
                false_part = (antecedant_part+ "|->"+ " ("+ false_part.strip(";").strip(" &&").strip("&&").strip("&& ")+ " )")
                true_path_list.append(true_part)
                false_path_list.append(false_part)
                print([i], " True part", true_part)
                print([i], " False Part", false_part)
            else:  ## Nested condition management : TO DO
                print("\n Handle logic for nested conditions here")
                """ Generally, the nested condition will appear without (current_state == xxxx )
                    So, just copy antecedant of the previous list item and append it with antecedant of the current list
                """
                i += 1
        print("\n\n true_part : ", true_path_list)
        print("\n\n false_part : ", false_path_list)

        #    print('\n Copied Antecedant :',antecedant_part)
        count = len(true_path_list)
        path_list = true_path_list, false_path_list
        #### get root_node_name from keys
        root_node_name = str(binddict_keys[j])
        root_node_name = root_node_name[root_node_name.find(".") + 1 :]
        print("\n Root Node Name : ", root_node_name)
        print("\n ********** \n")

        true_property_add(property_file_path, count, path_list[0], root_node_name, reset_name)

        print("\n Adding false properties*******\n")
        false_property_add(property_file_path, count, path_list[1], root_node_name, reset_name)
        # property_add(property_file_path,count , false_path_list)

    ## Closing SVA file
    endmodule(property_file_path)
    print("\n RESET Name: ", reset_name)
    #### Drawing graph


###################### Function definitions below ################################################################3
#### Break line_buff into two lists : true_list & false_list mapped as [true_list : false_list] = [odd_item : even_item]
def list_pair(line_buff):
    """Break line_buff into two lists : true_list & false_list mapped as [true_list : false_list] = [odd_item : even_item]"""
    # This mapping is too strict and leads to missing properties whenever nested conditions are encountered!!!
    # Short term remedy:: Do not remove emplty list items before calling this function
    list_true = []
    list_false = []
    print("\n type : ", type(list_true))
    for item in range(int(len(line_buff) / 2)):
        true_item = line_buff[(2 * item)]
        false_item = line_buff[(2 * item + 1)]
        list_true.append(true_item)  ## 0, 2, 4, 6 ....
        list_false.append(false_item.strip(";"))  # 1, 3, 5, ...
    #    print('\n True_list :', list_true)
    #    print('\n False_list :', list_false)
    return list_true, list_false


####### SVA File processing #######


###### Match antecedant for True and False conditions of the properties

## Take in two


def create_property(input_string):
    if input_string is not None:
        line = ""
        line = input_string
        print("Printing Input string to Create Property :: " + line)
        antecedant_list = line.split("|->")
        consequent_list = (antecedant_list[1].strip(" &&").strip("&&").strip(" && ").strip("&& "))
        property_list = (str(antecedant_list[0]).strip(" &&").strip("&&").strip(" && ").strip("&& ") + " |-> " + str(consequent_list).strip(" &&").strip("&&").strip(" && ").strip("&& "))
        return property_list
    else:
        return None


if __name__ == "__main__":
    main()
