`ifndef _DATA_MEM

`define _DATA_MEM


`include "parameters.v"


module data_memory #(parameter memory_width = `MEMORY_WIDTH, memory_depth = `MEMORY_DEPTH)(
    input  wire                                  clk,
    input  wire                                  rstn,
    input  wire                                  we,
    input  wire                                  re,
    input  wire  [$clog2(memory_depth)-1:0]      adress,
    input  wire  [memory_width-1:0]              data_in,
    output reg   [memory_width/2-1:0]            data_out_l,
    output reg   [memory_width-1:memory_width/2] data_out_h
);

reg [memory_width-1:0] internal_mem [$clog2(memory_depth)-1:0];


integer i;

always @(posedge clk or negedge rstn) begin
    if (!rstn) begin
        {data_out_h,data_out_l} <= 0;
        for (i=0; i<memory_depth; i=i+1) begin
        internal_mem[i] <= 0;
        end
    end else 
    begin 
        assert (we & re == 1);
        if (we | re !=0) begin
            if (we) begin
            internal_mem[adress] <= data_in;
            end else if (re) begin
            {data_out_h,data_out_l} <= internal_mem[adress];
            end
        end
    end
end

endmodule
 
`endif