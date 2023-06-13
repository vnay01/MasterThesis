/* @vnay01
    Test code to verify the operation of ADD generation
    The code is self-explanatory
    */


module usb_test (clk, reset, send_data, tx_ready, tx_valid, buff);

// Port direction
input clk;
input reset;
input send_data;
input tx_ready;
output reg tx_valid;
output reg [9:0] buff;

// State definitions
parameter IDLE=3'b000,
          CRC1=3'b001,
          CRC2=3'b011;
reg [2:0] current_state, next_state;

// FSM Starts here
// Register update
always@(posedge clk)
    if(!reset) current_state<= IDLE;
    else current_state <= next_state;

// State change logic
//always@(current_state or send_data or tx_ready)
always@(*)
    begin
        case(current_state)
            IDLE: begin tx_valid <= 1'b1;
                  if(send_data) next_state<=CRC1;
                  else next_state<=IDLE;
            end

            CRC1: begin tx_valid <= 1'b1;
                  if(tx_ready) next_state<=CRC2;
                  else next_state<=CRC1;
            end

            CRC2: begin tx_valid <= 1'b0;
            if(tx_ready) next_state<=IDLE;
            else next_state<=CRC2;
            end
            default: begin next_state <= current_state;
                           tx_valid <= 1'b0;
                           end 
        endcase
    end

// FSM Ends here

// Adding a register buffer // use it to check the quality of FSM extraction
always@(posedge clk)
    begin
        if (!reset) buff <= 0;
        else
            begin
            buff[0] <= tx_valid;     // sample value of yx_valid
            buff[9:1] <= buff[8:0]; // Left shift    
            end
            
    end



initial begin
    $display("Done Compilation...");
end
endmodule

