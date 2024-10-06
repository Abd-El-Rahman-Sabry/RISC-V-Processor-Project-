`ifndef _INST_MEM

`define _INST_MEM


`include "parameters.v"


module instuction_memory #(parameter memory_width = `INSTRUCTION_WIDTH, memory_depth = `INSTRUCTION_DEPTH)(
    input  wire                              clk,
    input  wire                              rstn,
    input  wire  [$clog2(memory_depth)-1:0]  adress,
    input  wire                              re,   
    input  wire   [memory_width-1:0]         data_in,
    output reg  [memory_width-1:0]           data_out
);

reg [memory_width-1:0] internal_mem [$clog2(memory_depth)-1:0];


integer i;

always @(posedge clk or negedge rstn) begin
    if (!rstn) begin
        data_out <= 0;
        for (i=0; i<memory_depth; i=i+1) begin
        internal_mem[i] <= 0;
        end
    end else 
    begin 
        if (re) begin
            data_out <= internal_mem[adress];
        end else begin
            internal_mem[adress] <= data_in;
        end
    end
end

endmodule
 
`endif