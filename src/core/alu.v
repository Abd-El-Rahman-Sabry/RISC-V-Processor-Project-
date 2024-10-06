
`include "parameters.v"

module alu #(
    parameter WIDTH = `RF_WIDTH 
) (
    //Main inputs 
    input wire [WIDTH - 1 : 0] i_a , i_b, 
    input wire [`FUNCT_WIDTH - 1 : 0] i_funct, 
    input wire i_rst , i_clk, 
    
    // control flags 

    input wire i_reserve_flg , i_restore_flg, 

    // Main outputs 
    output reg [`STATUS_REG_WIDTH - 1 : 0] o_stats, 
    output wire [WIDTH - 1 : 0] o_alu_r
);


    reg [`STATUS_REG_WIDTH - 1 : 0 ] store_flgs; 
    reg [WIDTH  : 0 ] alu_result; 


    // The status register 
    always @(posedge i_clk or negedge i_rst)  begin
        if (!i_rst)
            begin
                o_stats     <= 'b0;      
            end 
        else begin
            if (i_restore_flg)
                begin
                    o_stats <= store_flgs; 
                end
            else begin 
                    o_stats[`Z_FLG] <= alu_result == 'b0; 
                    o_stats[`N_FLG] <= alu_result < 'b0; 
                    o_stats[`C_FLG] <= alu_result[WIDTH];
            end 
        end
    end 
    

    // the store register 

    always @(posedge i_clk or negedge i_rst)
        begin
            
            if (~i_rst)
            begin
                store_flgs <= 'b0; 
            end
            else 
                begin
                    if (i_reserve_flg)
                        begin
                            store_flgs <= o_stats; 
                        end
                end
        end
    
    




    // ALU Operations 
    always @(*) begin
        case (i_funct) 
            
            `ALU_ADD: alu_result <= i_a + i_b; 
            `ALU_SUB: alu_result <= i_a - i_b; 
            `ALU_AND: alu_result <= i_a & i_b; 
            `ALU_XOR: alu_result <= i_a ^ i_b; 
            `ALU_NOT: alu_result <= ~i_a; 
            `ALU_A  : alu_result <= i_a; 
            `ALU_B  : alu_result <= i_b; 
            
            default : begin 
                alu_result <= {WIDTH{1'b0}};
            end 
                 
        endcase         
    end

    assign o_alu_r = alu_result;

    
endmodule