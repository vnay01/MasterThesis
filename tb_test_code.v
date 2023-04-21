`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 03/27/2023 05:46:20 PM
// Design Name: 
// Module Name: tb_test_code
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////
`ifndef test_code
   `include "E:/MasterThesis/MasterThesis.srcs/sources_1/new/test_code.v"
    `endif

`ifndef clocked_mux
 `include "E:/MasterThesis/MasterThesis.srcs/sources_1/new/clocked_mux.sv"
 `endif    
`ifndef clockperiod
    `define clockperiod 5
    `endif
    
module tb_test_code( );


// signals

reg tb_clk;
reg tb_reset;
reg tb_data_in;
reg tb_sel;
reg tb_d_in0, tb_d_in1;

wire tb_data_out;



//// Module under test

/*
test_code dut_0(
                .clk(tb_clk), 
                .reset(tb_reset), 
                .data_in(tb_data_in), 
                .data_out(tb_data_out)
    );
    */
    
clocked_mux dut_0( .clk(tb_clk), 
             .reset(tb_reset), 
             .sel(tb_sel), 
             .d_in0(tb_d_in0), 
             .d_in1(tb_d_in1), 
             .d_out(tb_data_out)
             );    
/// Simulating clock
always
#`clockperiod tb_clk <= ~tb_clk;

initial
begin

tb_clk = 1'b0;
tb_reset = 1'b1;
tb_d_in0 = 1'b0;
tb_d_in1 = 1'b1;


#5 tb_reset = 1'b0;
   tb_sel = 1'b0;
#15 tb_sel = 1'b0;
#25 tb_sel = 1'b1;
#35 tb_sel = 1'b0;
#45 tb_sel = 1'b1;
#55 tb_sel = 1'b0;
#65 tb_sel = 1'b1;
#75 tb_sel = 1'b0;

#100 $stop;

end

/// toggle sel switch



endmodule
