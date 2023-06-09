""" This function will be used to create a nested dictionary """
import re

input_string = '{Bind dest:usb_test.next_state tree:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.IDLE}} True:{Branch Cond:{Terminal usb_test.send_data} True:{Terminal usb_test._rn1_next_state} False:{Terminal usb_test._rn2_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.CRC1}} True:{Branch Cond:{Terminal usb_test.tx_ready} True:{Terminal usb_test._rn4_next_state} False:{Terminal usb_test._rn5_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.CRC2}} True:{Branch Cond:{Terminal usb_test.tx_ready} True:{Terminal usb_test._rn7_next_state} False:{Terminal usb_test._rn8_next_state}} False:{Branch Cond:{IntConst 1} True:{Terminal usb_test._rn9_next_state}}}}}}'

input_string = "{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.IDLE}} True:{Branch Cond:{Terminal usb_test.send_data} True:{Terminal usb_test._rn1_next_state} False:{Terminal usb_test._rn2_next_state}}"

#### Create a list?? 
'''Use string matching to {Branch Cond: /some text/ }}'''

## String which I need to match
"""
search_string='{Branch Cond:{'
end_string = '\}\}'
## Main string in which I need to find the pattern mentioned previously
regex_object = re.compile(r"[\:]")
mo = regex_object.findall(input_string)

print(mo)

print('Number of Branches : ', len(mo))
copy_flag = False

print('*****************************************************************\n')

## Logic to start copying
# When I encouner a Branch , split the current line into a newline
lines = input_string # capture input string

split_lines = re.split(r"Cond:", string=input_string)#using split() function to split lines whenever we encounter "Branch Cond"

print(split_lines)
print('\n List length : ' , len(split_lines))




print('\n*****************************************************************\n')
## printing the output
for split_line in split_lines:
    print(split_line)
"""

def parse_property(string):

    property_dict = {}

    string = string.replace('{' , '').replace('}', '').replace(':', '')     ## replace all unnecessary characters
    pairs =  string.split()     ## Splits at white spaces
    
print('\n*****************************************************************\n')