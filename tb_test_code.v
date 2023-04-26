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
/*
`ifndef test_code
   `include "E:/MasterThesis/MasterThesis.srcs/sources_1/new/test_code.v"
    `endif

`ifndef clocked_mux
 `include "E:/MasterThesis/MasterThesis.srcs/sources_1/new/clocked_mux.sv"
 `endif   
 */
 `ifndef usb_test
   `include "/home/vnay01/Desktop/MasterThesis/USB_test.v"
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

wire tb_tx_valid;
wire [9:0] tb_buff;
reg tb_tx_ready;

integer  i;



//// Module under test

/*
test_code dut_0(
                .clk(tb_clk), 
                .reset(tb_reset), 
                .data_in(tb_data_in), 
                .data_out(tb_data_out)
    );
clocked_mux dut_0( .clk(tb_clk), 
             .reset(tb_reset), 
             .sel(tb_sel), 
             .d_in0(tb_d_in0), 
             .d_in1(tb_d_in1), 
             .d_out(tb_data_out)
             );    
    */

usb_test dut_0 (.clk(tb_clk),
                .reset(tb_reset), 
                .send_data(tb_data_in), 
                .tx_ready(tb_tx_ready), 
                .tx_valid(tb_tx_valid),
                .buff(tb_buff));    

/// Simulating clock
always
#`clockperiod tb_clk <= ~tb_clk;


initial
begin

tb_clk = 1'b0;
tb_reset = 1'b0;
tb_data_in = 1'b0;
tb_tx_ready = 1'b0;                                 // IDLE

#10 tb_reset   = 1'b1;
    tb_data_in = ~tb_data_in;         // 1          // IDLE -> CRC1
   
#10 tb_data_in = ~tb_data_in;       // 0            
    tb_tx_ready = ~tb_tx_ready;     //1             // CRC1 -> CRC2 
    
#10 tb_tx_ready = ~tb_tx_ready;       // 0          // CRC2 -> CRC2

#10 tb_tx_ready = ~tb_tx_ready;        // 1         // CRC2 -> IDLE

#10    
    for (i = 0 ; i < 10 ; i = i + 1) begin
        tb_data_in = 1'b1;
        tb_tx_ready = 1'b0;        
        #10
        tb_tx_ready = 1'b1;
        #10
        tb_tx_ready = 1'b0;
        #10
        tb_tx_ready = 1'b1;
        #10
        tb_tx_ready = 1'b0;
        #10
        tb_tx_ready = 1'b1;
        #10 ;
        end


#100 $stop;

end

initial
begin

end

/// toggle sel switch



endmodule
