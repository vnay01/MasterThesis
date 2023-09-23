###############################################################################################################

""" Read a Verilog file and extract module information"""
''' Author : ESNIVIN / vnay01'''

import time
from module_extractor import *


def bind_adder(input_file, output_file):
    ''' Simply adds binding information from main RTL file into SVA property file'''
    module_name = extract_module_name(input_file)
    module_name = module_name_clean(module_name)
    print('module_name : ',module_name)
    sva_module_name = 'v_'+ module_name
    bind_instance = 'i_' + module_name
    bind_construct = 'bind ' + module_name + ' ' + sva_module_name + ' ' + bind_instance + ' ( .* );'
### Time information ###
    timestr = time.strftime("%Y/%m/%d- %H hr-%M m.-%S s")
    with open(output_file,'w') as file:
        file.write('// DO NOT REMOVE //')
        file.write('\n// This file is a product of Master Thesis done by Vinay Singh (ESNIVIN) at Ericcson \n')
        file.write('\n/////////////////////////////////////////////////\n')
        file.write('/*')
        file.write('Author : ESNIVIN :: Vinay Singh \n')  
        file.write('Property File : ' + ' ' + module_name)
        file.write('\nFile Created at : ')
        file.write(timestr)
        file.write('\n*/')
        file.write('\n\n//////////////////////////////////////////////////\n')
        file.write(bind_construct)
        file.write('\n\n\n')
    return 

def module_info_extractor(input_file, output_file):
    """Reading file"""
    with open(input_file, 'r') as file:
        rtl_code = file.read()

    copied_block = ""
    module_flag = False

    start_string = 'module'
    end_string = ');'
    start_index = rtl_code.index(start_string)
    end_index = rtl_code.index(end_string)
    ##copied_block = start_string
    copied_block = start_string +' v_'+ rtl_code[start_index+6:end_index+2].strip()
    
    print('copied_block: ', copied_block)               ## Checker code
    with open(output_file, 'a') as file:
        file.write(copied_block)
    port_dir = port_direction(copied_block)
    with open(output_file,'a') as file:  
        file.write('\n')
        file.write('\n')
        file.write('// Setting Port direction //')
        file.write('\n')
        for i in range(len(port_dir)):
            line_buff = port_dir[i] 
            file.write(line_buff.strip())
            file.write('\n')
        file.write('\n\n /*')
        file.write(' // Add your ports here, for eg internal state registers and typedefs \n')
        file.write('\n'*10)
        file.write('*/\n')

    return copied_block


def port_direction(input_string):
    """ extract module name from copied block and assign port direction as input
        return a list 
        """
    start_string = '('
    end_string = ')'
    start_index = input_string.index(start_string)
    end_index = input_string.index(end_string, start_index)
    copied_block = input_string[start_index:end_index].replace('(','').replace(')','')
    copied_block = copied_block.split(',')      ## create a list of all port names
    ## assign all port direction as input
    for i in range(len(copied_block)):
        buff = copied_block[i].replace('output','input')+ ';'      # extract list item and add 'input ' 
        buff = 'input ' + buff
        copied_block[i] = buff                  # modify the copied list item with previous step
    return copied_block



def true_property_add(input_file, count, property_list, root_node_name, reset_name):
    '''Modifies .sva file. Adds property list and assert statements to the .sva file'''
    with open(input_file, 'a') as sva_file:
#        sva_file.write('// Default Clocking and Reset\n')
#        sva_file.write('//default clocking (@posedge clk); clocking')
        sva_file.write('\n// ***** True property list for selected node : ' + root_node_name + ' *****')
        sva_file.write('\n'*2)
#        sva_file.write('\n// TimeStamp: ', timestr)
        for i in range(count):
            prop_buff = property_list[i]
            sva_file.write('\n')
            sva_file.write('property t_Prop_'+ root_node_name + '_' + str(i) + '; \n')
            sva_file.write('\t@(posedge clk) disable iff (' + reset_name + ') ('+ prop_buff + ');')
            sva_file.write('\n')
            sva_file.write('endproperty \n')
            sva_file.write('\n')
            sva_file.write('// Asserting & Cover Statements \n\n')
            sva_file.write('assert_t_Prop_' + root_node_name + '_' + str(i) + ': assert property (t_Prop_' + root_node_name + '_' + str(i) +');')
            sva_file.write('\n') 
            #sva_file.write('// Covering Property\n\n')
            sva_file.write('cover_t_prop_' + root_node_name + '_' + str(i) + ': cover property (t_Prop_' + root_node_name + '_' + str(i) +');')
            sva_file.write('\n\n\n')
        sva_file.write('\n'*2)  
    sva_file.close()
    return

def false_property_add(input_file, count, property_list, root_node_name, reset_name):
    '''Modifies .sva file. Adds property list and assert statements to the .sva file'''
    with open(input_file, 'a') as sva_file:
        sva_file.write('\n// ***** Writing False condition properties for selected node : ' + root_node_name + ' *****')
        sva_file.write('\n'*2)
        sva_file.write('\n \n // When asserted, these properties will FAIL')
        for i in range(count):
            prop_buff = property_list[i]
            sva_file.write('\n')
            sva_file.write('property f_Prop_'+ root_node_name + '_' + str(i) + '; \n')
            sva_file.write('\t@(posedge clk) disable iff (' + reset_name + ') ('+ prop_buff + ');')
            sva_file.write('\n')
            sva_file.write('endproperty \n')
            sva_file.write('\n')
            sva_file.write('// Asserting & Cover Statements \n\n')
            sva_file.write('assert_f_Prop_'  + root_node_name + '_' + str(i) + ': assert property (f_Prop_' + root_node_name + '_' + str(i) +');')
            sva_file.write('\n')
            #sva_file.write('// Covering Property\n\n')
            sva_file.write('cover_f_prop_'  + root_node_name + '_' + str(i) + ': cover property (f_Prop_' + root_node_name + '_' + str(i)+');')
            sva_file.write('\n'*2)

        sva_file.write('\n'*2)  
        sva_file.write('\n // Add additional Properties here : \n')     

    sva_file.close()
    return

def endmodule(input_file):
    with open(input_file,'a') as sva_file:
        sva_file.write('\n\nendmodule')
    sva_file.close()

def sva_module_info_extractor(input_file):
    '''Takes RTL file as input and writes module info. into SVA file'''
    file_object = open(input_file, 'r')
