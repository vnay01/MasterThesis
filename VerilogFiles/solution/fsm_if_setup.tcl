clear -all

analyze -sv09 fsm_if.v fsm_if_test.v
elaborate -top FSM_IF_TEST

clock clk
reset ~rst_n


visualize {1[*45]}
