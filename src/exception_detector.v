`ifndef _EXC_DETECTOR

`define _EXC_DETECTOR

`include "parameters.v"

module exception_detector #(parameter sp_width = `SP_WIDTH)(
    input  [sp_width-1:0] sp_o,
    input                 sp_step_sign,
    input  [15:0]         mem_address,
    output                exception,  
    output                exc_type
);

wire empty_stack_exc;
wire invalid_mem_address_exc;

assign empty_stack_exc = ~&sp_o&~sp_step_sign;

assign invalid_mem_address_exc = (mem_address > 'hFF00) ? 1:0; 

assign exception = empty_stack_exc | invalid_mem_address_exc;

assign exc_type = empty_stack_exc | ~invalid_mem_address_exc;


endmodule

`endif