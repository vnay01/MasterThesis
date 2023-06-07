""" This function will be used to create a nested dictionary """
import re

input_string = '{Bind dest:usb_test.next_state tree:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.IDLE}} True:{Branch Cond:{Terminal usb_test.send_data} True:{Terminal usb_test._rn1_next_state} False:{Terminal usb_test._rn2_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.CRC1}} True:{Branch Cond:{Terminal usb_test.tx_ready} True:{Terminal usb_test._rn4_next_state} False:{Terminal usb_test._rn5_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.CRC2}} True:{Branch Cond:{Terminal usb_test.tx_ready} True:{Terminal usb_test._rn7_next_state} False:{Terminal usb_test._rn8_next_state}} False:{Branch Cond:{IntConst 1} True:{Terminal usb_test._rn9_next_state}}}}}}'

input_string = '{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.IDLE}} True:{Branch Cond:{Terminal usb_test.send_data} True:{Terminal usb_test._rn1_next_state} False:{Terminal usb_test._rn2_next_state}}' 

#### Create a list?? 
'''Use string matching to {Branch Cond: /some text/ }}'''

## String which I need to match
search_string='{Branch Cond:{'
end_string = '\}\}'
## Main string in which I need to find the pattern mentioned previously
regex_object = re.compile(r'({Branch Cond:){1,}')
mo = re.search("^\{Branch Cond:.*\}\}$", input_string)


copy_flag = False

if (mo):
    """Set a flag to start copy"""
    copy_flag = True

else: 
    copy_flag = False


print('copy_flag :', copy_flag)

## Logic to start copying

