`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: Vinay Singh
// 
// Create Date: 03/27/2023 03:30:49 PM
// Design Name: 
// Module Name: test_code
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


module test_code(
                clk, reset, data_in, data_out
    );
    
    //// Port direction
    
    input clk;
    input reset;
    input data_in;
    output reg data_out;
    
    //// FSM 
    localparam STATE_SIZE = 2;
    localparam S0 = 2'b00,
               S1 = 2'b01,
               S2 = 2'b10,
               S3 = 2'b11;
    reg [STATE_SIZE-1:0] current_state, next_state;
    
// register update
always@(posedge clk, posedge reset)
    begin
        if(reset)
            current_state <= S0;
            else
            current_state <= next_state;
    end

/// next state logic
always@(*)
    begin

    case(current_state)
    S0 : if(data_in)
            next_state <= S1;
            else
            next_state <= current_state;
            
    
    S1 : if(data_in)
           next_state <= S2;
           else
           next_state <= current_state;
           
    
    S2 : if(data_in)
          next_state <= S3;
         else
          next_state <= current_state;
    
    S3 : if(data_in)
          next_state <= S0;
           else
          next_state <= current_state;
    default: next_state <= current_state;          
    endcase
    end                  
   
//// Output logic;

always@(*)
begin

case(current_state)
    S0 : data_out = 1'b0;
    S1 : data_out = 1'b1;
    S2 : data_out = 1'b0;
    S3 : data_out = 1'b1;
    default : data_out = 1'b0;
endcase    
end

    
endmodule
