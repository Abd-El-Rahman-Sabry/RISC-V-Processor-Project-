`ifndef _FETCH_STAGE

`define _FETCH_STAGE

`include "parameters.v"

module fetch_stage #(parameter memory_width = `INSTRUCTION_WIDTH, memory_depth = `INSTRUCTION_DEPTH, pc_width = $clog2(`INSTRUCTION_DEPTH), sp_width = `SP_WIDTH)(
    input                           clk,
    input                           rstn,
    input  [1:0]                    i_pc_i_type,
    input  [pc_width-1:0]           i_r_dst,
    input  [pc_width-1:0]           i_m_index,
    input  [pc_width-1:0]           i_x_sp,
    input  [pc_width-1:0]           i_m_2_3,
    input  [pc_width-1:0]           i_m_4_5,
    input                           i_hlt,
    input                           i_sp_step_sign,
    input                           i_sp_step_value,
    input  [15:0]                   i_mem_address,
    output [memory_width-1:0]       o_instruction,
    output [pc_width-1:0]           o_pc,
    output [pc_width-1:0]           o_pc_1,
    output [sp_width-1:0]           o_sp
);

wire [pc_width-1:0] i_types_mux_o;
wire [pc_width-1:0] m_types_mux_o;
wire [pc_width-1:0] pc_i_mux_o;
wire [pc_width-1:0] pc_o;
wire [pc_width-1:0] pc_adder_o;
wire                hlt_o;

wire [sp_width-1:0] sp_steps_mux_o;
wire [sp_width-1:0] sp_adder_o;
wire [sp_width-1:0] sp_o;

wire exception;
wire exc_type;

adder #(.width(pc_width)) pc_adder (.in1(pc_o), .in2(1), .out(pc_adder_o));

mux_4x1 #(.width(pc_width)) i_types_mux (.in1(pc_adder_o), .in2(i_r_dst), .in3(i_m_index), .in4(i_x_sp), .control(i_pc_i_type), .out(i_types_mux_o));

mux_2x1 #(.width(pc_width)) m_types_mux (.in1(i_m_2_3), .in2(i_m_2_3), .control(exc_type), .out(m_types_mux_o));

mux_2x1 #(.width(pc_width)) pc_i_mux (.in1(i_types_mux_o), .in2(m_types_mux_o), .control(hlt_o), .out(pc_i_mux_o));

HLT HLT1 (.clk(clk), .rstn(rstn), .in(i_hlt), .out(hlt_o)); 

PC #(.width(pc_width)) pc1 (.clk(clk), .rstn(rstn), .en(hlt_o), .in(pc_i_mux_o), .out(pc_o));

EPC #(.width(pc_width)) epc1 (.clk(clk), .rstn(rstn), .en(exception), .in(pc_o), .out());

instuction_memory #(.memory_width(memory_width), .memory_depth(memory_depth)) instuction_memory1 (.clk(clk), .rstn(rstn), .adress(pc_o), .data_out(o_instruction));

mux_4x1 #(.width(sp_width)) sp_steps_mux (.in1(1), .in2(2), .in3(-1), .in4(-2), .control({i_sp_step_sign,i_sp_step_value}), .out(sp_steps_mux_o));

adder #(.width(sp_width)) sp_adder (.in1(sp_o), .in2(sp_steps_mux_o), .out(pc_adder_o));

sp #(.width(sp_width)) sp1 (.clk(clk), .rstn(rstn), .en(en), .in(pc_adder_o), .out(sp_o));

mux_2x1 #(.width(sp_width)) sp_o_mux (.in1(pc_adder_o), .in2(sp_o), .control(i_sp_step_sign), .out(o_sp));

exception_detector #(.sp_width(sp_width)) exception_detector1 (.sp_o(sp_o), .sp_step_sign(i_sp_step_sign), .mem_address(i_mem_address), .exception(exception), .exc_type(exc_type));



 
endmodule

`endif