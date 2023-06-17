`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Engineer: Vinay Singh
// Create Date: 05/13/2023 01:33:38 PM 
// Module Name: controller
/*  
Signal brief:
    Inputs : START  // comes from external pin - manual or microcontroller
            
             
    Output : status signals
                BUSY :: HIGH: : Indicates accelerator is busy 
                                No new computation must be allowed unless BUSY signal is deasserted.
            control signals:
                
        */

module controller(  
                    clk,
                    reset,  // ACTIVE LOW reset
                    START,
                    MEM_READ,         
                    BUSY,
                    DONE,
                    input_matrix_ram_en,
                    input_matrix_ram_read_en,
                    input_matrix_ram_address,
                    filter_matrix_rom_en,
                    filter_matrix_rom_read_en,
                    filter_matrix_rom_address,
                    data_path_signal,
                    fifo_command                             
    );
    
/// Port directions

input clk;
input reset;
input START;      
input MEM_READ;   
output reg BUSY;
output reg DONE;
output reg input_matrix_ram_en;
output reg input_matrix_ram_read_en;
output reg [9:0] input_matrix_ram_address;
output reg filter_matrix_rom_en;
output reg filter_matrix_rom_read_en;
output reg filter_matrix_rom_address;
output reg [4:0] data_path_signal;          // concatnation of signals which control different sections of datapath
output reg [1:0] fifo_command;

// Internal counters
parameter counter_size = 10;

reg [counter_size-1:0] count, count_next;
reg [counter_size-1:0] state_counter, state_counter_next; 
reg [9:0] w_input_matrix_ram_address, w_input_matrix_ram_address_next; 
reg w_filter_matrix_rom_address, w_filter_matrix_rom_address_next;
reg [1:0] w_fifo_command, w_fifo_command_next;
    
// State variables
   parameter STATE_SIZE = 8;
   parameter INIT = 8'd0,
             LOAD = 8'd1,
             MULT = 8'd2,
             L1_ADD = 8'd3,
             L2_ADD = 8'd4,
             L3_ADD = 8'd5,
             L4_ADD = 8'd6,
             MEM_STORE = 8'd7;
             
reg [STATE_SIZE-1: 0] current_state, next_state;

// Register update

always@(posedge clk)
    begin
    if(!reset) begin
        current_state <= INIT;
        
        count <= {counter_size{1'b0}};
        state_counter <= {counter_size{1'b0}};
        
        w_input_matrix_ram_address <= {10{1'b0}};
        w_filter_matrix_rom_address <= 1'b0;
        
        input_matrix_ram_address <= {10{1'b0}};
        filter_matrix_rom_address <= 1'b0; 
        
        w_fifo_command <= {2{1'b0}}; 
        end
        else
        begin
        current_state <= next_state;
        
        count <= count_next;
        state_counter <= state_counter_next;
        w_input_matrix_ram_address <= w_input_matrix_ram_address_next;
        w_filter_matrix_rom_address <= w_filter_matrix_rom_address_next;
        
        input_matrix_ram_address <= w_input_matrix_ram_address;
        filter_matrix_rom_address <= w_filter_matrix_rom_address;
        w_fifo_command <= w_fifo_command_next;
        end  
        end           
    
// State change logic starts here::::

always@(*)
begin
    // default values
    next_state <= current_state;      // preserve current state
    
    count_next = count + 1;          // increment counter by 1
    state_counter_next = state_counter;    // For testing, I am updating this counter only when MEM_STORE state is reached. Will have to be reused 
   
    w_input_matrix_ram_address_next = w_input_matrix_ram_address;  // 
    w_filter_matrix_rom_address_next = w_filter_matrix_rom_address;    
    w_fifo_command_next <= w_fifo_command;
    
    
    DONE = 1'b0;
    
    case(current_state)
    
    INIT: if(START) begin
            next_state <= LOAD;          // State change
            w_input_matrix_ram_address_next = {10{1'b0}}; /// Initial RAM address
            state_counter_next = {counter_size{1'b0}}; 
            count_next <= {counter_size{1'b0}}; 
          end  
    
    LOAD: begin
            w_filter_matrix_rom_address_next = w_filter_matrix_rom_address + 1 ; 
            w_input_matrix_ram_address_next = w_input_matrix_ram_address + 1;
            w_fifo_command_next <= {2{1'b0}};
            
            // Optimization candidate
            // count signal is used here to change states.
            
            if(count == 1) begin
            
            next_state <= MULT;                          // change state to MULT
            count_next = {counter_size{1'b0}};          // reset counter to 0s
           end 
           end
           
           
    MULT: 
            // Optimization candidate
            // Since at this moment, I have not selected the architecutre
            // of multiplier to be used, I am using internal counter value for state transition logic
            if(count == 15) begin
            next_state <= L1_ADD;
            count_next = {counter_size{1'b0}};
            end

    L1_ADD: if (count == 7)begin
            next_state <= L2_ADD;
            count_next = {counter_size{1'b0}};
            end
            
    L2_ADD: if (count == 7)begin
            next_state <= L3_ADD;
            count_next = {counter_size{1'b0}};
            end

    L3_ADD: if (count == 7)begin
            next_state <= L4_ADD;
            count_next = {counter_size{1'b0}};
            end
    
    L4_ADD: if (count == 7)begin
            next_state <= MEM_STORE;
            count_next = {counter_size{1'b0}};
            end


   MEM_STORE: // Optimization candidate -- Can be eliminated entirely
                // Total number of mem_store operations is decided by the 
                // size of the convoluted matrix.
                // Keeping it a fixed number of 256 for the sake of testing 
            if (state_counter == 256) begin
                next_state <= INIT;
                DONE = 1'b1;
                w_fifo_command_next <= 2'b01;       // enable READ operation
                
                end
                else
                    begin
                        
                        if (count == 10)begin           // this is not required later on
                        next_state <= LOAD;
                        state_counter_next = state_counter + 1; 
                        count_next = {counter_size{1'b0}};
                        w_fifo_command_next <= 2'b10;       // enable WRITE
                        end
                        end
                    
   default: next_state <= INIT;
    endcase
end



/// State - dependent control signals


always@(*)
begin
    
    // default values
    BUSY <= 1'b1;
    
    // Input Matrix RAM signals
    input_matrix_ram_en = 1'b0;
    input_matrix_ram_read_en = 1'b0;
    
    // Filter Coefficient ROM signals
    filter_matrix_rom_en = 1'b0;
    filter_matrix_rom_read_en = 1'b0;  // Not used in this ROM from Xilinx
    
    // data_path control signals
    data_path_signal = 5'b00000;   
    
    // FIFO commands
    fifo_command = w_fifo_command; 
    
    // Value assignment logic
    case(current_state)
    
    INIT: begin
          BUSY <= 1'b0;
//          input_matrix_ram_en = 1'b0;
          end
          
    LOAD: 
           begin           
           input_matrix_ram_en = 1'b1;
           filter_matrix_rom_en = 1'b1;
           data_path_signal = 5'b00000;
           end  
    MULT:
            
           begin          
           data_path_signal = 5'b10000;          
           end           
    L1_ADD:
           begin
           data_path_signal = 5'b01000;
           end 
    L2_ADD:
           begin
           data_path_signal = 5'b00100;
           end 
    L3_ADD:
           begin
           data_path_signal = 5'b00010;
           end 
    L4_ADD:
           begin
           data_path_signal = 5'b00001;
           end 
    MEM_STORE:
           begin
           data_path_signal = 5'b00000;
           //// fifo_command will need to be made such that MEM_STORE can be eliminated 
           end              
    default : 
           begin
           data_path_signal = 5'b00000;   
           end                                                                      
    
    endcase
end

endmodule   
