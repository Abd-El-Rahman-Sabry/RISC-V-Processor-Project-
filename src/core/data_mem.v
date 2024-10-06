`include "parameters.v"


module data_mem #(
  parameter DWIDTH = `DB_WIDTH,  
  parameter AWIDTH = `AB_WIDTH  
)(
    input wire [DWIDTH - 1 : 0] i_data_in, 
    input wire [AWIDTH - 1 : 0] i_add,
    
    input wire i_clk , i_rst,

    output reg [DWIDTH - 1 : 0] o_data_low,
    output reg [DWIDTH - 1 : 0] o_data_high
    
);
endmodule 