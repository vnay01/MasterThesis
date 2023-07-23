## New file to test if import Pyverilog works
## Uncomment while using within CITRIX
'''
#! /proj/cot/conda/envs/cot_py0/bin/python
# #! /proj/cot/conda/envs/iverilog0/bin/iverilog
'''

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

@profile


def main():
    start = timer()
    timestr = time.strftime("%Y/%m/%d- %H hr-%M m.-%S s")

    print('Starting Flow at...', timestr)
    ### Globals -- These need to be changed as arguments later
    rtl_file_name = "USB_test.v"
    top_module = 'usb_test'
    """ Work starts here"""

    ####### Working Test code ########
    ########## Book Keeping and setting up directory ######
    system = platform.system()
    if system == "Linux":
        parent_dir = "/home/" + os.getlogin() +'/'
        working_dir = parent_dir + "Desktop/MasterThesis/"
        output_dir = working_dir + "TestOutputs/"
        if not os.path.exists('temp'):
            os.mkdir('temp')
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
    elif system=="Windows":
        parent_dir = "/home/vnay01/"
        working_dir = parent_dir + "Desktop/MasterThesis/"
        output_dir = working_dir + "TestOutputs/"
        temp = working_dir + "temp/"
        data_flow_dir = output_dir + "data_flow/"
        translated_verilog_dir = output_dir + "translated_verilog/"
    else:
        print("What the hell!? Which system are you on!!?")


    """ RTL file details & node selection"""
    rtl_file_path = working_dir + 'VerilogFiles/'
    file_path = rtl_file_path + rtl_file_name
    translated_file_path = rtl_file_path + rtl_file_name +'_translated.v'
    input_file = file_path
    output_file = translated_file_path

    module_name = top_module

    if not os.path.exists('Properties'):
        os.mkdir('Properties')
    property_file_name = 'property_' + module_name + '.sva'
    property_file_path = os.path.abspath('Properties') +'/'+ property_file_name

    ### Call this function to modify assignment oeprators
    replace_assignment_operator(input_file, output_file)
#    preprocess_include= '-I'


    data_flow = VerilogDataflowAnalyzer(output_file,top_module)         ## Create a dataflow object.
#    print(data_flow)                      ## Expecting an object of class VerilogDataflowAnalyzer()
    
    ## Using generate() to get an object of type  'VerilogDataflowAnalyzer'
    data_flow.generate()

    directives = data_flow.get_directives()         ## Checks for directives ( i.e. #define , `include etc. )
    
    terms = data_flow.getTerms()                    ## This returns a dictionary of all terms in RTL
    terms_keys = terms.keys()                       ## Returns a dict_key type object. This can be used to select root nodes of dataflow tree
    # Since dict_key is non-subscriptable, we convert it into subscriptable type - either a list or tuple
    terms_keys_list=list(terms_keys)

    '''
    ## Checker code
    for i in range(len(terms_keys)):
        print('\n', [i] ,'List of keys: ' ,terms_keys_list[i])
    print('\n')
    '''    
    # Binding information
    binddict = data_flow.getBinddict()
    binddict_keys = list(binddict.keys())
    print('\n These are the nodes for which dataflow trees can be generated : ')
    for i in range(len(binddict_keys)):
        print('\n', [i] ,'List of Binding keys: ' ,binddict_keys[i])
    
    #### Pass the index of desired root node:
    root_node = int(6)                                         #### Use with caution. Works for state transition only.
    print('\n\n Generating tree structure for selected node : ')
    a=''
    for i in binddict.get(binddict_keys[root_node]):                   ## Use 'keys' for generating properties for cycling through root nodes. This is required to increase Formal Coverage
        print(' Pyverilog function call')
        print('\n',i._assign())                        # actual. To be removed 
        print(' modified function call')
        #print('\n',i._assign_mod())                        ## tostr() is a recursive function
        a = i._always_combination_mod()                # calling method() on object of Bind class
        '''
        # checker code
        print('\n PRINITNG data stored in a :', (a))
        '''
    print('\n Prinitng length of a: ',len(a))
#    print('\n \n Does a still have value outside the loop ?? \n', (a))
#    print('\n Data Type of a :', type(a))
    
    ## Lets write it to a file for manipulation!!
    #prop_intermediate_file = temp + 'temp_prop_file.txt'
    #file_object = open(prop_intermediate_file,'w')
    #file_object.write(a[:-1])
#    file_object.close()

    ## proper formatting of property file  
    ## split into lines whenever ';' is encountered
    line_buff = ''
#    with open(file_object,'r'):
    line_buff = a[:-1].strip()
    line_buff = line_buff.splitlines()                  # This creates a list of all properties but also includes empty items within the list
    print('\n Printing line_buff \n:', line_buff)         
# We need to remove all empty items from the list    
    line_buff = [value for value in line_buff if value != '']
    print('\n Modified Line_buff \n',line_buff)

## Check number of items in the list
    print('\n\n Number of items in line_buff \n: ',len(line_buff))
#    prop = create_property(line_buff[0])
#    print('\n XY :: ',prop)
    prop_list = list_pair(line_buff)                        # Split property list
    print('\n\n True_condition_property: ',prop_list[0])    # Check correctness
    print('\n\n False_condition_property: ',prop_list[1])   # Check correctness

    true_part = ''
    false_part = ''

    ## ammend the antecedant part of false_condition
#def prop_make(prop_list):    
    print('\ length of prop_list : ',len(prop_list[0]))
## Open an sva file:
    true_path_list = []
    false_path_list = []

    for i in range(len(prop_list[0]) - 2 ):
        true_part = str(prop_list[0][i])
        false_part = str(prop_list[1][i])
        ## search for |-> string 
        start_index = true_part.index('|->')
        antecedant_part = true_part[: start_index].strip(' &&').strip().strip('&&')
        #true_part = true_part.strip(' &&').strip().strip('&&').strip('&& ') + ' ;'
        true_part = antecedant_part  + true_part[start_index: ].strip(' &&').strip().strip('&&')
        false_part = antecedant_part + '|->' + ' ('+ false_part.strip(';') + ' )'
        true_path_list.append(true_part)
        false_path_list.append(false_part)
        print([i],' ',true_part)
        print([i],' ',false_part)

    print('\n\n true_part : ',true_path_list)
    print('\n\n false_part : ', false_path_list)
    bind_adder(file_path, property_file_path)
    module_info_extractor(file_path, property_file_path )
#    print('\n Copied Antecedant :',antecedant_part)
    count = len(true_path_list)
    lalala = true_path_list,false_path_list
    property_add(property_file_path,count , lalala)
    #property_add(property_file_path,count , false_path_list)




###################### Function definitions below ################################################################3
#### Break line_buff into two lists : true_list & false_list mapped as [true_list : false_list] = [odd_item : even_item]
def list_pair(line_buff):
    ''' Break line_buff into two lists : true_list & false_list mapped as [true_list : false_list] = [odd_item : even_item]'''
    list_true = []
    list_false = []
    print('\n type : ', type(list_true))
    for item in range(int(len(line_buff)/2)):
        true_item = line_buff[(2*item)]
        false_item = line_buff[(2*item + 1)]
        list_true.append(true_item)             ## 0, 2, 4, 6 ....      
        list_false.append(false_item.strip(';'))         # 1, 3, 5, ...
#    print('\n True_list :', list_true)
#    print('\n False_list :', list_false)        
    return list_true, list_false


####### SVA File processing #######


###### Match antecedant for True and False conditions of the properties

## Take in two 

def create_property(input_string):
    if input_string is not None:
        line = ''
        line = input_string
        antecedant_list = line.split('|->')
        consequent_list = antecedant_list[1]
        property_list = str(antecedant_list[0]).strip('&&  ') + ' |-> ' + str(consequent_list)
        return property_list
    else:
        return None

if __name__ == '__main__':
    main()
