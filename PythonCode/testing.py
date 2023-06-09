
# Example usage
input_string = '''{Bind dest:usb_test.next_state tree:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.IDLE}} True:{Branch Cond:{Terminal usb_test.send_data} True:{Terminal usb_test._rn1_next_state} False:{Terminal usb_test._rn2_next_state}} 
                False:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.CRC1}} True:{Branch Cond:{Terminal usb_test.tx_ready} True:{Terminal usb_test._rn4_next_state} False:{Terminal usb_test._rn5_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.CRC2}} True:{Branch Cond:{Terminal usb_test.tx_ready} True:{Terminal usb_test._rn7_next_state} False:{Terminal usb_test._rn8_next_state}} False:{Branch Cond:{IntConst 1} True:{Terminal usb_test._rn9_next_state}}}}}}'''
# input_string = '{Bind dest:controller.next_state tree:{Branch Cond:{Operator Eq Next:{Terminal controller.current_state},{Terminal controller.INIT}} True:{Branch Cond:{Terminal controller.START} True:{Terminal controller._rn6_next_state} False:{Terminal controller._rn0_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal controller.current_state},{Terminal controller.LOAD}} True:{Branch Cond:{Operator Eq Next:{Terminal controller.count},{IntConst 1}} True:{Terminal controller.MULT}} False:{Branch Cond:{Operator Eq Next:{Terminal controller.current_state},{Terminal controller.MULT}} True:{Branch Cond:{Operator Eq Next:{Terminal controller.count},{IntConst 15}} True:{Terminal controller.L1_ADD}} False:{Branch Cond:{Operator Eq Next:{Terminal controller.current_state},{Terminal controller.L1_ADD}} True:{Branch Cond:{Operator Eq Next:{Terminal controller.count},{IntConst 7}} True:{Terminal controller._rn13_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal controller.current_state},{Terminal controller.L2_ADD}} True:{Branch Cond:{Operator Eq Next:{Terminal controller.count},{IntConst 7}} True:{Terminal controller._rn15_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal controller.current_state},{Terminal controller.L3_ADD}} True:{Branch Cond:{Operator Eq Next:{Terminal controller.count},{IntConst 7}} True:{Terminal controller._rn17_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal controller.current_state},{Terminal controller.L4_ADD}} True:{Branch Cond:{Operator Eq Next:{Terminal controller.count},{IntConst 7}} True:{Terminal controller._rn19_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal controller.current_state},{Terminal controller.MEM_STORE}} True:{Branch Cond:{Operator Eq Next:{Terminal controller.state_counter},{IntConst 256}} True:{Terminal controller._rn21_next_state} False:{Branch Cond:{Operator Eq Next:{Terminal controller.count},{IntConst 10}} True:{Terminal controller._rn23_next_state}}} False:{Branch Cond:{IntConst 1} True:{Terminal controller._rn26_next_state}}}}}}}}}}}'

print('\n***********************\n')

print(len(input_string))
"""Extract text between two strings"""

start_string = 'Branch Cond:'
end_string = 'False:{Branch'

## 1. Search and save the index where Branch Cond is encountered.
start_index = input_string.index(start_string)
end_index = input_string.index(end_string)


## 2. Save this end index.
### Done in previous step
""" Print out information to see if using index methods works
print(start_index)
print(input_string[start_index:end_index ])         ## Works!!
"""
print(start_index)
print(end_index)
## 3. Copy everything in between the start and end index extracted from above
copy_branch_1 = input_string[start_index : end_index]
print('Printing copied branch : \n', copy_branch_1)


## 4. Go back to step 1 to 5, until we reach the end of the string

## Start searching from end_index
input_string = input_string[end_index:]

print('Remaining Branches: \n', input_string)

start_index = input_string.index(start_string)

end_index = input_string.index(end_string, start_index , )

print(start_index)
print(end_index)

copy_branch_2 = input_string[start_index : end_index]


print('\n Printing copied branch_2: \n', copy_branch_2)

#### Update string again
input_string = input_string[end_index:]
print('\n')
print('\n Updated Branches: \n')
print(input_string)

start_index = input_string.index(start_string)

end_index = input_string.index(end_string, start_index , )

copy_branch_3 = input_string[start_index : end_index]



print('\n Main tree structure ... \n', input_string)
print('\n')
print('\n Branches: \n')
print('\n Branch 1: \n',copy_branch_1)
print('\n****************************\n')
print('\n Branch 2: \n',copy_branch_2)
print('\n****************************\n')
print('\n Branch 3: \n',copy_branch_3)
print('\n****************************\n')
print('\n****************************\n')

print(start_index)
print(end_index)
print(len(input_string))