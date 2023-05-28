
def replace_assignment_operator(input_file, output_file):
    """Call this function to translate RTL into format for graphgen.py"""
    with open(input_file, 'r') as file:
        rtl_code = file.read()

    modified_code = ""
    always_block = False

    lines = rtl_code.split('\n')
    for line in lines:
        if 'always@' in line:
            always_block = True
        elif line.startswith('end'):
            always_block = False

        if always_block and '<=' in line:
            modified_code += line + '\n'
        elif always_block and '==' in line:
            modified_code += line + '\n'
        elif always_block and '!=' in line:
            modified_code += line + '\n'
        elif (always_block == False ):
            modified_code += line + '\n'
        else:
            modified_line = line.replace('=', '<=')
            modified_code += modified_line + '\n'

    with open(output_file, 'w') as file:
        file.write(modified_code)

