
def dict_creator(string):
    """ Function to change () into {} . 
        Seems to be completely redundant"""

    string = string.replace('(' , '{').replace(')', '}')     ## replace all unnecessary characters
    pairs =  string.split()     ## Splits at white spaces
    return string






def branch_extractor(input_string):
    """ Takes input as a string and spits out tuple of the form ([branches], remaining_string)"""
    start_string = 'Branch Cond:'
    end_string = 'False:{Branch'
    copy_branch = []            ## this list object holds extracted branches
    try:

        start_index = input_string.index(start_string)  
        end_index = input_string.index(end_string)
        copy_branch.append(input_string[start_index : end_index])
        input_string = input_string[end_index:].strip('False:')   

        return copy_branch, input_string
    except: 
        if (len(input_string) < 1):
            print('No input string')


    
## Lets decide how many times do I need to call this function
## From analyzing the graph, whenever False:{Branch is encountered 
## A new branch is created
## So lets count the number of times this happens and use it to decide
## how many function calls should be made


""" Example Usage"""
input_string = '''{Bind dest:usb_test.next_state tree:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.IDLE}} True:{Branch Cond:{Terminal usb_test.send_data} True:{Terminal usb_test._rn1_next_state} False:{Terminal usb_test._rn2_next_state}} 
                False:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.CRC1}} True:{Branch Cond:{Terminal usb_test.tx_ready} True:{Terminal usb_test._rn4_next_state} False:{Terminal usb_test._rn5_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal usb_test.current_state},{Terminal usb_test.CRC2}} True:{Branch Cond:{Terminal usb_test.tx_ready} True:{Terminal usb_test._rn7_next_state} False:{Terminal usb_test._rn8_next_state}} False:{Branch Cond:{IntConst 1} True:{Terminal usb_test._rn9_next_state}}}}}}'''

input_string = '{Bind dest:controller.next_state tree:{Branch Cond:{Operator Eq Next:{Terminal controller.current_state},{Terminal controller.INIT}} True:{Branch Cond:{Terminal controller.START} True:{Terminal controller._rn6_next_state} False:{Terminal controller._rn0_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal controller.current_state},{Terminal controller.LOAD}} True:{Branch Cond:{Operator Eq Next:{Terminal controller.count},{IntConst 1}} True:{Terminal controller.MULT}} False:{Branch Cond:{Operator Eq Next:{Terminal controller.current_state},{Terminal controller.MULT}} True:{Branch Cond:{Operator Eq Next:{Terminal controller.count},{IntConst 15}} True:{Terminal controller.L1_ADD}} False:{Branch Cond:{Operator Eq Next:{Terminal controller.current_state},{Terminal controller.L1_ADD}} True:{Branch Cond:{Operator Eq Next:{Terminal controller.count},{IntConst 7}} True:{Terminal controller._rn13_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal controller.current_state},{Terminal controller.L2_ADD}} True:{Branch Cond:{Operator Eq Next:{Terminal controller.count},{IntConst 7}} True:{Terminal controller._rn15_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal controller.current_state},{Terminal controller.L3_ADD}} True:{Branch Cond:{Operator Eq Next:{Terminal controller.count},{IntConst 7}} True:{Terminal controller._rn17_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal controller.current_state},{Terminal controller.L4_ADD}} True:{Branch Cond:{Operator Eq Next:{Terminal controller.count},{IntConst 7}} True:{Terminal controller._rn19_next_state}} False:{Branch Cond:{Operator Eq Next:{Terminal controller.current_state},{Terminal controller.MEM_STORE}} True:{Branch Cond:{Operator Eq Next:{Terminal controller.state_counter},{IntConst 256}} True:{Terminal controller._rn21_next_state} False:{Branch Cond:{Operator Eq Next:{Terminal controller.count},{IntConst 10}} True:{Terminal controller._rn23_next_state}}} False:{Branch Cond:{IntConst 1} True:{Terminal controller._rn26_next_state}}}}}}}}}}}'

input_string = '(Bind dest:usb_test.next_state tree:(Branch Cond:(Operator Eq Next:(Terminal usb_test.current_state),(Terminal usb_test.IDLE)) True:(Branch Cond:(Terminal usb_test.send_data) True:(Terminal usb_test._rn1_next_state) False:(Terminal usb_test._rn2_next_state)) False:(Branch Cond:(Operator Eq Next:(Terminal usb_test.current_state),(Terminal usb_test.CRC1)) True:(Branch Cond:(Terminal usb_test.tx_ready) True:(Terminal usb_test._rn4_next_state) False:(Terminal usb_test._rn5_next_state)) False:(Branch Cond:(Operator Eq Next:(Terminal usb_test.current_state),(Terminal usb_test.CRC2)) True:(Branch Cond:(Terminal usb_test.tx_ready) True:(Terminal usb_test._rn7_next_state) False:(Terminal usb_test._rn8_next_state)) False:(Branch Cond:(IntConst 1) True:(Terminal usb_test._rn9_next_state))))))'


input_string = dict_creator(input_string)
end_string = 'False:{Branch'
count = input_string.count(end_string)      ## count the total number of requried function calls
# print('\n Count : ', count)

branch_list = []    ## holds extracted tree

for i in range(count):
    branch_list.append(branch_extractor(input_string)[0])
    input_string = branch_extractor(input_string)[1]


for i in range(count):
    print(branch_list[i])




