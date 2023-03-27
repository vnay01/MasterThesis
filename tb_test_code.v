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
`ifndef clockperiod
    `define clockperiod 5
    `endif
    
module tb_test_code( );


// signals

reg tb_clk;
reg tb_reset;
reg tb_data_in;
wire tb_data_out;


//// Module under test
test_code dut_0(
                .clk(tb_clk), 
                .reset(tb_reset), 
                .data_in(tb_data_in), 
                .data_out(tb_data_out)
    );
/// Simulating clock
always
#`clockperiod tb_clk <= ~tb_clk;

initial
begin

tb_clk = 1'b0;
tb_reset = 1'b1;

#5 tb_reset = 1'b0;
   tb_data_in = 1'b1;
#15 tb_data_in = 1'b0;
#25 tb_data_in = 1'b1;
#35 tb_data_in = 1'b0;
#45 tb_data_in = 1'b1;
#55 tb_data_in = 1'b0;
#65 tb_data_in = 1'b1;
#75 tb_data_in = 1'b0;

#100 $stop;

end


endmodule
