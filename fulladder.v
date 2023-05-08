/* Code to test operation of JG

	Behavioral code of a Full Adder
*/

module fulladder ( clk, reset, a, b, sum);

input clk;		// dummy
input reset;	// dummy
input [7:0]a,b;
output reg [7:0]sum;

wire [7:0] w_sum;

assign w_sum = a + b ;


always@(posedge clk)
	begin
		if(reset) begin
		sum <= {8{1'b0}};
		end
		else		
		begin
		sum <= w_sum;
		end
	end
endmodule