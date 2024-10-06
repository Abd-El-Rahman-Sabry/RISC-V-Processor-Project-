`ifndef _MUX_2X1

`define _MUX_2X1

`include "parameters.v"

module mux_2x1 #(
   parameter width = `INSTRUCTION_WIDTH
) (
    input  wire           control,
    input  wire [width-1:0] in1,
    input  wire [width-1:0] in2,
    output wire [width-1:0] out
);
    
    assign out = control? in1 : in2;

endmodule

`endif 