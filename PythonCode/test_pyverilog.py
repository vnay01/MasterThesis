## New file to test if import Pyverilog works
from __future__ import absolute_import
from __future__ import print_function

import os
import subprocess
from subprocess import call
import sys
import typing
import platform
from optparse import OptionParser


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



def main():
    start = timer()
    timestr = time.strftime("%Y/%m/%d- %H hr-%M m.-%S s")

    print('Starting Flow at...', timestr)
    ### Globals -- These need to be changed as arguments later
    rtl_file_name = "USB_test.v"
    top_module = 'usb_test'
    root_node = "next_state"
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

    replace_assignment_operator(input_file, output_file)
#    preprocess_include= '-I'


    data_flow = VerilogDataflowAnalyzer(output_file,top_module)
    print(data_flow)                      ## Expecting an object of class VerilogDataflowAnalyzer()
    
    ## Using generate() to get an object of type  'VerilogDataflowAnalyzer'
    data_flow.generate()

    directives = data_flow.get_directives()
    
    terms = data_flow.getTerms()                    ## This returns a dictionary of all terms in RTL
    terms_keys = terms.keys()                         ## Returns a dict_key type object
    # Since dict_key is non-subscriptable, we convert it into subscriptable type - either a list or tuple
    terms_keys_list=list(terms_keys)
    ## Checker code
    for i in range(len(terms_keys)):
        print('\n', [i] ,'List of keys: ' ,terms_keys_list[i])
    print('\n')

    # Binding information
    binddict = data_flow.getBinddict()
    binddict_keys = list(binddict.keys())
    print('\n These are the nodes for which dataflow trees can be generated : ')
    for i in range(len(binddict_keys)):
        print('\n', [i] ,'List of Binding keys: ' ,binddict_keys[i])
    
    print('\n\n Generating tree structure for selected node : ')
    a=''
    for i in binddict.get(binddict_keys[5]):
        print(' Pyverilog function call')
        print('\n',i._assign())                        # actual 
        print(' modified function call')
        #print('\n',i._assign_mod())                        ## tostr() is a recursive function
        a = i._always_combination_mod()                # calling method() on object of Bind class
        
        #print('\n',i._always_combination_mod())
        print('\n PRINITNG data sotred in a :', (a))
    
    print('\n \n Does a still have value outside the loop ?? \n', (a))
    print('\n Data Type of a :', type(a))
    
    ## Lets write it to a file for manipulation!!
    prop_intermediate_file = temp + 'temp_prop_file.txt'
    file_object = open(prop_intermediate_file,'w')
    file_object.write(a[:-1])
#    file_object.close()

    ## proper formatting of property file  
    ## split into lines whenever ';' is encountered
    line_buff = ''
#    with open(file_object,'r'):
    line_buff = a[:-1].strip()
    line_buff = line_buff.splitlines()
    print('\n Printing line_buff :', line_buff)

#    for i in range(len(line_buff)):
#        print('\n List item of line_buff : ', type(line_buff[i]) , line_buff[i])


    xy = property_(line_buff[0])
    print('\n XY :: ',xy)
    '''
    for key, value in sorted(binddict.items(), key=lambda x: str(x[0]), reverse=False):
        for bvi in value:
            #print(bvi.tostr())             ## Recursive calls tostr() method of Bind object
            print(bvi.tostr())         ## My modified functions       
            print('\n')   
    '''
    # Working with codegen:: Work in Progress ----- Issues after this line


def property_(input_string):
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