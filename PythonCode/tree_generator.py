import os
import sys

def data_flow(file_path, pattern, module_name, root_node):
    """Takes .txt file as input and finds the required tree. 
     Also returns a pointer to the file where the extracted tree is written """
    try:
        ### Create a file object
        file_name = 'data_flow_tree_' + root_node + '.txt'
        file_object = open(file_name, 'w+')
        with open(file_path, 'r') as file:
            line_number = 0
            found = False
            for line in file:
                line_number += 1
                if pattern in line:
                    file_object.write(line.strip())
                    found = True            
            
            if not found:
                print("Pattern not found in the file.")
        file_object.close()        
        return os.path.abspath(file_name)    
    except FileNotFoundError:
        print("File not found.")

