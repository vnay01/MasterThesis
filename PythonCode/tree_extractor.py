import os
import sys

def search_pattern_in_file(file_path, pattern, module_name, root_node):
    """Takes .txt file as input and find tree """
    try:
        sys.stdout=open('data_flow_tree_' + root_node +'.txt',"w") 
        with open(file_path, 'r') as file:
            line_number = 0
            found = False
            for line in file:
                line_number += 1
                if pattern in line:
                    print(line.strip())
                    found = True
                    
            
            if not found:
                print("Pattern not found in the file.")
        sys.stdout.close()                
    except FileNotFoundError:
        print("File not found.")

# Example usage
module_name="usb_test"
root_node = "current_state"
 # Replace with the actual file path
file_path = '/Users/vinaysingh/Desktop/MasterThesis/data_flow_usb_test.txt'
pattern = "(Bind dest:"+ module_name + '.' + root_node
search_pattern_in_file(file_path, pattern, module_name, root_node)
