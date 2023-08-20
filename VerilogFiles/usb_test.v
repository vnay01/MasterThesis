   /*
    Test code to verify the operation of ADD generation
    The code is self-explanatory
    */


module usb_test (clk, reset, send_data, tx_ready, tx_valid, buff, a, b, sum);

input clk;
input reset;
input send_data;
input tx_ready;
input a;
input b;
output reg tx_valid;
output reg [9:0] buff;
output reg [1:0] sum;

localparam IDLE=3'b000,
          CRC1=3'b001,
          CRC2=3'b011;
reg [2:0] current_state;
reg [2:0] next_state;

// Internal counters

reg [9:0] counter, counter_next;
reg [9:0] shift_reg;


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
        counter_next = counter;
        next_state = current_state;

        case(current_state)
            IDLE: begin tx_valid = 1'b1;
                  counter_next = counter + 1;
                  if(send_data) next_state=CRC1;
            end

            CRC1: begin tx_valid = 1'b1;
                  counter_next = counter + 1;
                  if(!tx_ready) next_state=CRC2;
                  
            end

            CRC2: begin tx_valid = 1'b0;
            counter_next = counter + 1;

            if(tx_ready) 
                begin
                    if (counter < 9) 
                    next_state=CRC1;
                end
            else begin
            if (counter == 10) begin
            next_state=IDLE;
            counter_next = {10{1'b0}}; 
            end
            end
            end
            default: begin
                tx_valid = 1'b0;
                counter_next = counter;
                next_state=IDLE;
                end 
        endcase
    end

// Shift registers
always@(posedge clk)
    begin
        if (!reset) buff = 0;
        else
            begin
            buff[0] <= tx_valid;                 
            buff[9:1] <= buff[8:0];
            end
    end

// Non state dependent logic

reg [1:0] node;

always@(*)
    begin
    case(counter)

    10'd0: node = 2'b00;
    10'd4: node = 2'b01;
    10'd6: node = 2'b10;
    10'd9: node = 2'b11;
    default: node = 2'b00;
    endcase
    end

always@(posedge clk)
    begin
        if (!reset) 
            sum <= {2{1'b0}};
        else
            sum <= a + b;        
    end
    // Shift Registers
always@(posedge clk)    
    begin
        if(!reset)
        shift_reg = {5{{1'b0},{1'b1}}};
        else
        shift_reg[9:1] <= shift_reg[8:0]; 
    end

initial begin
    $display("Done Compilation...");
    $display(shift_reg);
end
endmodule


// Testbench

module tb();

reg tb_tx_send_data;
reg tb_send_data;
reg tb_tx_ready;
reg tb_tx_valid;
reg [9:0] tb_buff;
reg tb_a;
reg tb_b;
reg [1:0] tb_sum;


v_usb_test usb_test (.clk(tb_clk), 
                     .reset(tb_reset), 
                     .send_data(tb_send_data), 
                     .tx_ready(tb_tx_ready), 
                     .tx_valid(tb_tx_valid), 
                     .buff(tb_buff), 
                     .a(tb_a), 
                     .b(tb_b), 
                     .sum(tb_sum));

endmodule
