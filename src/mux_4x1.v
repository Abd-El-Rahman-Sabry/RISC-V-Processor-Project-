`ifndef _MUX_4X1

`define _MUX_4X1

`include "parameters.v"

module mux_4x1 #(
   parameter width = `INSTRUCTION_WIDTH
) (
    input  wire [1:0]       control,
    input  wire [width-1:0] in1,
    input  wire [width-1:0] in2,
    input  wire [width-1:0] in3,
    input  wire [width-1:0] in4,
    output wire [width-1:0] out
);
    
    assign out = control[1]?(control[0]? in4 : in3):(control[0]? in2 : in1);

endmodule

`endif 