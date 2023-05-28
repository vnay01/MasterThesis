""" Read a Verilog file and extract module information"""

def module_info_extractor(input_file, output_file):
    """Reading file"""
    with open(input_file, 'r') as file:
        rtl_code = file.read()

    copied_block = ""
    module_flag = False

    lines = rtl_code.split('\n')
    for line in lines:
        if 'module' in line:
            module_flag = True
        elif line.startswith(')'):
            module_flag = False

        if (module_flag == True):
            copied_block += line + '\n'
            
        if module_flag and ')' in line:
            module_flag = False
    
    with open(output_file, 'w') as file:
        file.write(copied_block)


def port_direction(input_file, output_file):
    """Copies the module information and makes each port as input"""
    with open(input_file, 'r') as file:
        rtl_code = file.read()
    
    copied_block = ""
    module_flag = False

    lines= rtl_code.split('\n')
    for line in lines:
        
        if '(' in line:
            module_flag = True
        elif (line.startswith(')') or line.endswith(')')):
            module_flag = False

