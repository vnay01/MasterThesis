clear -all

analyze -sv09 fsm_if_w_props_rtl_errors.v fsm_if_test.v
elaborate -top FSM_IF_TEST

clock clk
reset ~rst_n


prove -all
