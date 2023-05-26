
def replace_assignment_operator(input_file, output_file):
    with open(input_file, 'r') as file:
        rtl_code = file.read()

    lines = rtl_code.split('\n')
    modified_lines = []
    for line in lines:
        if '<=' in line:
            modified_lines.append(line)
        else:
            modified_lines.append(line.replace('=', '<='))

    modified_code = '\n'.join(modified_lines)

    with open(output_file, 'w') as file:
        file.write(modified_code)

# Example usage

parent_dir = "/home/vnay01/"
working_dir = parent_dir + "Desktop/MasterThesis/"

rtl_file_path = working_dir + "VerilogFiles/"

rtl_file_name = "USB_test.v"
file_path = rtl_file_path + rtl_file_name



input_file = file_path
output_file = working_dir + 'output_file.v'
replace_assignment_operator(input_file, output_file)
