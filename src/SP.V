`ifndef _SP

`define _SP

`include "parameters.v"

module SP #(parameter width = `SP_WIDTH) (
    input  wire             clk,
    input  wire             rstn,
    input  wire             en,
    input  wire [width-1:0] in,
    output reg  [width-1:0] out
);

always @(posedge clk or negedge rstn) begin
    if (!rstn) begin
        out <= 0;
    end else if(en) begin
        out <= in;
    end 
end

endmodule

`endif 