`ifndef _MEMORY_STAGE

`define _MEMORY_STAGE

`include "parameters.v"

module memory_stage #(parameter memory_width = `MEMORY_WIDTH, memory_depth = `MEMORY_DEPTH, rf_width = `RF_WIDTH, pc_width = $clog2(`INSTRUCTION_DEPTH), sp_width = `SP_WIDTH) (
    input                                      i_rstn,
    input                                      i_clk,
    input      [rf_width-1:0]                  i_alu_o,
    input      [rf_width-1:0]                  i_r_r_scr1,
    input      [pc_width-1:0]                  i_pc,
    input      [pc_width-1:0]                  i_pc_1,
    input      [sp_width-1:0]                  i_sp,
    input                                      i_address_c,
    input      [1:0]                           i_data_in_c,
    input                                      i_we,
    input                                      i_re,
    output reg [memory_width/2-1:0]            o_mem_l,
    output reg [memory_width-1:memory_width/2] o_mem_h
);

wire [pc_width-1:0]             mem_data_in;
wire [$clog2(memory_depth)-1:0] mem_address;

mux_4x1 #(.width(pc_width)) mem_data_in_mux (.control(i_data_in_c), .in1(i_r_r_scr1), .in2(i_pc), .in3(i_pc_1), .in4(0), .out(mem_data_in));

mux_2x1 #(.width($clog2(memory_depth))) mem_addres_mux (.control(i_address_c), .in1(i_alu_o), .in2(i_sp), .out(mem_address));

data_memory #(.memory_width(memory_width), .memory_depth(memory_depth)) data_mem (.rstn(rstn), .clk(clk), .we(i_we), .re(i_re), .address(mem_address), .data_in(mem_data_in), .data_out_l(o_mem_l), .data_out_h(o_mem_h)); 

endmodule

`endif