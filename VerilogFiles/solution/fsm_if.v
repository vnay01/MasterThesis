
module FSM_IF   (input wire clk,
                 input wire rst_n,           // interface control
                 input wire [5:0] count40,   // cycle counter
                 output reg tclk, 
                 output reg trst,           // serial data control
                 output reg dq_en,         // tristate enable for serial data
                 output reg sr_en);        // serial to parallel shift enable

  // interface state machine states
  localparam init = 0, load_command = 1, start_frame = 2, wrc_low = 3, wrc_high = 4,
             end_frame = 5, rdc_low = 6, rdc_high = 7;
  reg [2:0] state;

  wire [3:0] ops;

 //
 // state machine for interface control 
 //

 assign ops = {tclk, trst, dq_en, sr_en};

  always@(posedge clk or negedge rst_n)
    if (~rst_n)
      state <= init;
    else
      case (state)
      
         init: 
           if (count40 == 39)
             state <= load_command;

         load_command:
           state <= start_frame;

         start_frame:
           state <= wrc_low;
 
         wrc_low:
           state <= wrc_high;

         wrc_high:
           if (count40 == 15) 
             state <= rdc_low;
           else
             state <= wrc_low;

         end_frame:
           if (count40 == 39) 
             state <= load_command;

         rdc_low:
           state <= rdc_high;

         rdc_high:
           if (count40 == 35)
             state <= end_frame;
           else
             state <= rdc_low;

         default: $display("Unexpected State %b", state);
      endcase

always@(state)
  begin
  // defaults
  dq_en = 1'b0;
  trst =  1'b1;
  sr_en = 1'b0;

  case (state)
    init, load_command: 
      begin
      trst = 1'b0;
      tclk = 1'b1;  // reset tclk high
      end

    start_frame:
      tclk = 1'b1;

    wrc_low:
      begin
      dq_en = 1'b1;
      tclk = 1'b0;
      sr_en = 1'b1;
      end
 
    wrc_high:
      begin
      dq_en = 1'b1;    
      tclk = 1'b1;
      end

    end_frame:
      begin
      trst = 1'b1;
      tclk = 1'b1;
      end

    rdc_low:
      begin
      tclk = 1'b0;
      sr_en = 1'b1;
      end

    rdc_high:
      tclk = 1'b1;

  endcase
  end

 // add assertions here
//#### EDIT ###











//#### END OF EDIT ###

endmodule
