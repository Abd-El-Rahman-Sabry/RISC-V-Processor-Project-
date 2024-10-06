`ifndef _HLT

`define _HLT

`include "parameters.v"

module HLT (
    input  wire             clk,
    input  wire             rstn,
    input  wire             in,
    output reg              out
);

always @(posedge clk or negedge rstn) begin
    if (!rstn) begin
        out <= 0;
    end else if(in) begin
        out <= 1;
    end
end

endmodule

`endif 