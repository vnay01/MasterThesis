
module FSM_IF_TEST;

wire 		clk, rst_n;                 
reg  [5:0] 	count40;  
wire 		tclk, 	trst, dq_en, sr_en; 


  FSM_IF U1 (.clk(clk), .rst_n(rst_n), .count40(count40), .tclk(tclk), .trst(trst), .dq_en(dq_en), .sr_en(sr_en));

  always @(posedge clk or negedge rst_n)    // generate the count
    if (~rst_n)  // active low reset
      //count40 <= 6'b0;
      count40 <= 38;
    else if (count40 == 39)
      count40 <= 6'b0;
    else
      count40 <= count40 + 6'b1;

     
endmodule
