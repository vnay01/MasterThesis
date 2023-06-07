
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
  property T1;
    @(posedge clk)
      ((state == init) && (count40 == 39)) |=> (state == load_command);
  endproperty

  property T2;
    @(posedge clk)
      (state == load_command) |=> (state ==start_frame);
  endproperty

  property T3;
    @(posedge clk)
      (state == start_frame) |=> (state == wrc_low);
  endproperty

  property T4;
    @(posedge clk)
      (state == wrc_low) |=> (state == wrc_high);
  endproperty

  property T5;
    @(posedge clk)
      ((state == wrc_high) && (count40 != 17)) |=> (state == wrc_low);
  endproperty

  property T6;
    @(posedge clk)
      ((state == wrc_high) && (count40 == 17)) |=> (state == rdc_low);
  endproperty

  property T7;
    @(posedge clk)
      (state == rdc_low) |=> (state == rdc_high);
  endproperty

  property T8;
    @(posedge clk)
      ((state == rdc_high) && (count40 != 35)) |=> (state == rdc_low);
  endproperty

  property T9;
    @(posedge clk)
      ((state == rdc_high) && (count40 == 35)) |=> (state == end_frame);
  endproperty

  property T10;
    @(posedge clk)
      ((state == end_frame) && (count40 == 39)) |=> (state == load_command);
  endproperty

  AST_T1: assert property(T1); 
  AST_T2: assert property(T2); 
  AST_T3: assert property(T3); 
  AST_T4: assert property(T4); 
  AST_T5: assert property(T5);
  AST_T6: assert property(T6); 
  AST_T7: assert property(T7); 
  AST_T8: assert property(T8); 
  AST_T9: assert property(T9); 
  AST_T10: assert property(T10);
  // outputs

  property OP1;
   @(posedge clk)
     (state == init) |-> (ops == 4'b1000);
  endproperty

  property OP2;
   @(posedge clk)
     (state == load_command) |-> (ops == 4'b1000);
  endproperty

  property OP3;
   @(posedge clk)
     (state == start_frame) |-> (ops == 4'b1100);
  endproperty

  property OP4;
   @(posedge clk)
     (state == wrc_low)  |-> (ops == 4'b0111);
  endproperty

  property OP5;
   @(posedge clk)
     (state == wrc_high)  |-> (ops == 4'b1110);
  endproperty

  property OP6;
   @(posedge clk)
     (state == rdc_low)  |-> (ops == 4'b0101);
  endproperty

  property OP7;
   @(posedge clk)
     (state == rdc_high)  |-> (ops == 4'b1100);
  endproperty

  property OP8;
   @(posedge clk)
     (state == end_frame)  |-> (ops == 4'b1000);
  endproperty

 AST_OP1: assert property(OP1); 
 AST_OP2: assert property(OP2); 
 AST_OP3: assert property(OP3); 
 AST_OP4: assert property(OP4); 
 AST_OP5: assert property(OP5); 
 AST_OP6: assert property(OP6); 
 AST_OP7: assert property(OP7); 
 AST_OP8: assert property(OP8);
//#### END OF EDIT ###

endmodule
