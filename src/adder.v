`ifndef _ADDER

`define _ADDER

`include "parameters.v"

module adder #(
    parameter width = `INSTRUCTION_WIDTH
) (
    input  [width-1:0] in1,
    input  [width-1:0] in2,
    output [width-1:0] out
);

assign out = in1 + in2;
    
endmodule

`endif 