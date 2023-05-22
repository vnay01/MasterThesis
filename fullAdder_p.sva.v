bind fulladder fullAdder_p fv_inst (.clk(clk), 
									.reset(reset),
					.				a(a), .b(b));


module fullAdder_p(
				clk, reset,
				a, b
					
);

input clk;
input reset;
input [7:0]a, b;
//input c_in;
logic [8:0] sum;


//// Assertions 


property reset_output;
	@(posedge clk) (reset == 1'b1 |-> (sum == 8'd0));
//	@(posedge clk)((a == 8'h02 || b == 8'h02) |-> (sum == 8'h04));
endproperty

a_sum_is_HIGH: assert property(reset_output);


property norm_output;
	@(posedge clk)((reset == 0) |-> (sum == (a+b)));
endproperty

a_norm_output : assert property(norm_output);

endmodule