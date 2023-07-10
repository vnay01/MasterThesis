""" Read a Verilog file and extract module information"""
import time

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
    copied_block = rtl_code[start_index:end_index+2]
    
    print('copied_block: ', copied_block)
    with open(output_file, 'w') as file:
        file.write(copied_block)
    port_dir = port_direction(copied_block)
    with open(output_file,'a') as file:  
        file.write('\n')
        file.write('\n')
        file.write('// Setting Port direction //')
        file.write('\n')
        for i in range(len(port_dir)):
            file.write(port_dir[i]+'\n')
    return


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
        buff = "input " + copied_block[i].replace('input','').replace('output','').replace('reg','').replace('logic','') + ';'      # extract list item and add 'input ' 
        copied_block[i] = buff                  # modify the copied list item with previous step
    return copied_block



def property_add(input_file, count, property_list):
    '''Modifies .sva file. Adds property list and assert statements to the .sva file'''
    timestr = time.strftime("%Y/%m/%d- %H hr-%M m.-%S s")
    print('//////////////////////////////////////////////////\n')
    with open(input_file, 'a') as sva_file:
        sva_file.write('// Default Clocking and Reset\n')
        sva_file.write('//default clocking (@posedge clk); clocking')
        sva_file.write('\n// Property list \n')
        sva_file.write('\n//  Property Generated on Timestamp : ')
        sva_file.write(timestr)
#        sva_file.write('\n// TimeStamp: ', timestr)
        for i in range(count):
            prop_buff = property_list[0][i]
            sva_file.write('\n')
            sva_file.write('property t_Prop_'+ str(i) + '; \n')
            sva_file.write('\t@(posedge clk) ('+ prop_buff + ');')
            sva_file.write('\n')
            sva_file.write('endproperty \n')
            sva_file.write('\n')
            sva_file.write('assert_Prop_' + str(i) + ': assert property (t_Prop_' + str(i) +');')
            sva_file.write('\n') 
            sva_file.write('cover_prop_' + str(i) + ': cover property (t_Prop_'+str(i)+');')
            sva_file.write('\n')
        
        for i in range(count):
            prop_buff = property_list[1][i]
            sva_file.write('\n')
            sva_file.write('property f_Prop_'+ str(i) + '; \n')
            sva_file.write('\t@(posedge clk) ('+ prop_buff + ');')
            sva_file.write('\n')
            sva_file.write('endproperty \n')
            sva_file.write('\n')
            sva_file.write('assert_Prop_' + str(i) + ': assert property (f_Prop_' + str(i) +');')
            sva_file.write('\n') 
            sva_file.write('cover_prop_' + str(i) + ': cover property (f_Prop_'+str(i)+');')
            sva_file.write('\n')

        sva_file.write('\n')  
        sva_file.write('\n')     
        sva_file.write('endmodule')  
    sva_file.close()
    return 

def sva_module_info_extractor(input_file):
    '''Takes RTL file as input and writes module info. into SVA file'''
    file_object = open(input_file, 'r')
    