input_list = ["((test.current_state==test.IDLE) ) && (test.send_data )|->  (test.tx_valid == 1'b1 )", "((test.current_state==test.CRC1) ) && (test.tx_ready )|->  (test.tx_valid == 1'b1 )", "((test.current_state==test.CRC2) ) && (test.tx_ready )|->  (test.tx_valid == 1'b0 )", "(1 )|->  (test.tx_valid == 1'b0 )"]

items_to_match = ["tx_valid", "send_data", "tx_ready"]

for i in range(len(input_list)):
    for item in items_to_match:
        input_list[i] = input_list[i].replace("test." + item, item)

# Print the modified list
for modified_string in input_list:
    print(modified_string)
