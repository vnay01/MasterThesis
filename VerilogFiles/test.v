//// Module for initial tests
//////// DO NOT USE ///////////

module test( clk, reset, last, crc, data_in, data_out );

    // Port direction

    input clk;
    input reset;
    input last;
    input crc;
    input data_in;
    output reg data_out;


    // Behavioral description

    always @(posedge clk) begin
        if (!reset)
        data_out <= 1'b0;
        else if (last)
        data_out <= 1'b0;
        else if (crc)
            data_out <= data_in;
            else
            data_out <= 1'b0;
    end

    initial begin
        $display("Compilation...done");
    end
endmodule
