   /*
    Test code to verify the operation of ADD generation
    The code is self-explanatory
    */


module usb_test (clk, reset, send_data, tx_ready, tx_valid, buff);

input clk;
input reset;
input send_data;
input tx_ready;
output reg tx_valid;
output reg [9:0] buff;

localparam IDLE=3'b000,
          CRC1=3'b001,
          CRC2=3'b011;
reg [2:0] current_state;
reg [2:0] next_state;

// Internal counters

reg [9:0] counter, counter_next;


always@(posedge clk)
    if(!reset) 
        begin
        current_state<= IDLE;
        counter <= {10{1'b0}};          // reset value of counter
        end
    else 
        begin
        current_state <= next_state;
        counter <= counter_next;
        end

always@(*)
    begin
        counter_next <= counter;
        next_state <= current_state;

        case(current_state)
            IDLE: begin tx_valid <= 1'b1;
                  counter_next <= counter + 1;
                  if(send_data) next_state<=CRC1;
            end

            CRC1: begin tx_valid <= 1'b1;
                  counter_next <= counter + 1;
                  if(!tx_ready) next_state<=CRC2;
                  
            end

            CRC2: begin tx_valid <= 1'b0;
            counter_next <= counter + 1;

            if(tx_ready) 
                begin
                    if (counter < 9) 
                    next_state<=CRC1;
                end
            else begin
            if (counter == 10) begin
            next_state<=IDLE;
            end
            end
            end
            default: begin
                tx_valid <= 1'b0;
                counter_next <= counter;
                next_state<=IDLE;
                end 
        endcase
    end


always@(posedge clk)
    begin
        if (!reset) buff <= 0;
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

