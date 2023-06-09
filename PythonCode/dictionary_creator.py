""" This function will be used to create a nested dictionary """

input_string = '{Bind dest:usb_test.next_state tree:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.IDLE}} True:{Branch Cond:{Terminal usb_test.send_data} True:{Terminal usb_test._rn1_next_state} False:{Terminal usb_test._rn2_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.CRC1}} True:{Branch Cond:{Terminal usb_test.tx_ready} True:{Terminal usb_test._rn4_next_state} False:{Terminal usb_test._rn5_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.CRC2}} True:{Branch Cond:{Terminal usb_test.tx_ready} True:{Terminal usb_test._rn7_next_state} False:{Terminal usb_test._rn8_next_state}} False:{Branch Cond:{IntConst 1} True:{Terminal usb_test._rn9_next_state}}}}}}'

input_string = '(Bind dest:usb_test.next_state tree:(Branch Cond:(Operator Eq Next:(Terminal usb_test.current_state),(Terminal usb_test.IDLE)) True:(Branch Cond:(Terminal usb_test.send_data) True:(Terminal usb_test._rn1_next_state) False:(Terminal usb_test._rn2_next_state)) False:(Branch Cond:(Operator Eq Next:(Terminal usb_test.current_state),(Terminal usb_test.CRC1)) True:(Branch Cond:(Terminal usb_test.tx_ready) True:(Terminal usb_test._rn4_next_state) False:(Terminal usb_test._rn5_next_state)) False:(Branch Cond:(Operator Eq Next:(Terminal usb_test.current_state),(Terminal usb_test.CRC2)) True:(Branch Cond:(Terminal usb_test.tx_ready) True:(Terminal usb_test._rn7_next_state) False:(Terminal usb_test._rn8_next_state)) False:(Branch Cond:(IntConst 1) True:(Terminal usb_test._rn9_next_state))))))'

#### Create a list?? 
'''Use string matching to {Branch Cond: /some text/ }}'''

## String which I need to match


def dict_creator(string):

    string = string.replace('(' , '{').replace(')', '}')     ## replace all unnecessary characters
    pairs =  string.split()     ## Splits at white spaces
    return string


""" Example Usage """
print('\n*****************************************************************\n')

print(dict_creator(input_string))