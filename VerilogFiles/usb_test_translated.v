   /*
    Test code to verify the operation of ADD generation
    The code is self-explanatory
    */


module usb_test (clk, reset, send_data, tx_ready, tx_valid);

input clk;
input reset;
input send_data;
input tx_ready;

output reg tx_valid;


localparam IDLE=3'b000,
           CRC1=3'b001,
           CRC2=3'b011;
reg [2:0] current_state;
reg [2:0] next_state;


always@(posedge clk)
    if(!reset) 
        begin
        current_state<= IDLE;
        end
    else 
        begin
        current_state <= next_state;
        end

always@(*)
    begin
        next_state <= current_state;

        case(current_state)
            IDLE: begin tx_valid <= 1'b1;
                  if(send_data) next_state<=CRC1;
            end

            CRC1: begin tx_valid <= 1'b1;
                  if(tx_ready) next_state<=CRC2;                  
            end

            CRC2: begin tx_valid <= 1'b0;
                if(tx_ready)  
                    next_state<=IDLE;
                end
            default: begin
                tx_valid <= 1'b0;
                next_state<=IDLE;
                end 
        endcase
    end
endmodule


