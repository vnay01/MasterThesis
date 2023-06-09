
# Example usage
input_string = '''{Bind dest:usb_test.next_state tree:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.IDLE}} True:{Branch Cond:{Terminal usb_test.send_data} True:{Terminal usb_test._rn1_next_state} False:{Terminal usb_test._rn2_next_state}} 
                False:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.CRC1}} True:{Branch Cond:{Terminal usb_test.tx_ready} True:{Terminal usb_test._rn4_next_state} False:{Terminal usb_test._rn5_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.CRC2}} True:{Branch Cond:{Terminal usb_test.tx_ready} True:{Terminal usb_test._rn7_next_state} False:{Terminal usb_test._rn8_next_state}} False:{Branch Cond:{IntConst 1} True:{Terminal usb_test._rn9_next_state}}}}}}'''
# input_string = 'abc'

print('\n***********************\n')

"""Extract text between two strings"""

start_string = 'Branch Cond'
end_string = 'False Branch'

## 1. Search for the index where Branch Cond is encountered.
print(input_string.find(start_string))


## 2. Save this start index. We will start copying text from this index
## 3. continue searching for end_string ( False:{Branch)
## 4. Save this end index.
## 5. Copy everything in between the start and end index extracted from above
## 6. Go back to step 1 to 5, until we reach the end of the string
