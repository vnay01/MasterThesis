def branch_extractor(input_string, loop_count):
    """ Takes input as a string and spits out branches"""
    start_string = 'Branch Cond:'
    end_string = 'False:{Branch'
    copy_branch = []            ## this list object holds extracted branches
#    start_index = input_string.index(start_string)  
#    end_index = input_string.index(end_string)
    start_index = input_string.index(start_string)  
    end_index = input_string.index(end_string)
    copy_branch.append(input_string[start_index : end_index])
    input_string = input_string[end_index:]
    loop_count = loop_count -1    
    if loop_count > 0:
        branch_extractor(input_string, loop_count)
        print(loop_count)
    else:
        print(input_string)
    return copy_branch
"""    for i in range(2):
        branch_extractor(input_string)

    print('\n', input_string)
"""   
    


input_string = '''{Bind dest:usb_test.next_state tree:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.IDLE}} True:{Branch Cond:{Terminal usb_test.send_data} True:{Terminal usb_test._rn1_next_state} False:{Terminal usb_test._rn2_next_state}} 
                False:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.CRC1}} True:{Branch Cond:{Terminal usb_test.tx_ready} True:{Terminal usb_test._rn4_next_state} False:{Terminal usb_test._rn5_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.CRC2}} True:{Branch Cond:{Terminal usb_test.tx_ready} True:{Terminal usb_test._rn7_next_state} False:{Terminal usb_test._rn8_next_state}} False:{Branch Cond:{IntConst 1} True:{Terminal usb_test._rn9_next_state}}}}}}'''

end_string = 'False:{Branch'

count = input_string.count(end_string)      ## count the total number of requried function calls
print('\n Count : ', count)

print(branch_extractor(input_string, count))

## Lets decide how many time do I need to call this function
## From analyzing the graph, whenever False:{Branch is encountered 
## A new branch is created
## So lets count the number of times this happens and use it to decide
## how many function calls should be made


