   /* Written in accordance to System Verilog Specifications
    Test code to verify the operation of ADD generation
    The code is self-explanatory
    */


module usb_test (clk, reset, send_data, tx_ready, tx_valid, buff);

input logic clk;
input logic reset;
input logic send_data;
input logic tx_ready;
output logic tx_valid;
output logic [9:0] buff;


typedef enum logic[2:0] { IDLE, CRC1, CRC2} state_t;

state_t current_state, next_state;
          


always@(posedge clk)
    if(!reset) current_state<= IDLE;
    else current_state <= next_state;

always@(*)
    begin
        case(current_state)
            IDLE: begin tx_valid = 1'b1;
                  if(send_data) next_state=CRC1;
                  else next_state=IDLE;
            end

            CRC1: begin tx_valid = 1'b1;
                  if(!tx_ready) next_state=CRC2;
                  else next_state=CRC1;
            end

            CRC2: begin tx_valid = 1'b0;
            if(tx_ready ) next_state=IDLE;
            else next_state=CRC2;
            end
            default: begin
                tx_valid = 1'b0;
                next_state=IDLE;
                end 
        endcase
    end


always@(posedge clk)
    begin
        if (!reset) buff = 0;
        else
            begin
            buff[0] <= tx_valid;                 
            buff[9:1] <= buff[8:0];
            end
    end



initial begin
    $display("Done Compilation...");
end
endmodule
