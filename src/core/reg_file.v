`include "parameters.v"

module regfile #(
    parameter WIDTH = `RF_WIDTH,
    parameter SIZE = `RF_SIZE
) (
    input wire [$clog2(WIDTH) - 1 : 0] i_src_0 , i_src_1,
    input wire [$clog2(WIDTH) - 1 : 0] i_dst, 
    input wire [WIDTH - 1 : 0] i_wr_data,
    
    output wire [WIDTH - 1 : 0] o_a , o_b, 
    
    input wire i_clk , i_rst, i_w_en 

);

    reg [WIDTH - 1 : 0] rf [0 : SIZE - 1]; 

    integer i = 0; 

    always @(posedge i_clk or negedge i_rst) begin

        if (~i_rst)
            begin
                for (i = 0 ; i < SIZE ; i= i + 1)
                    begin
                        rf[i] <= {WIDTH{1'b0}}; 
                    end                
            end
        else 
            begin
                // Data in 
                if (i_w_en)
                    begin
                        rf[i_dst] <= i_wr_data;  
                    end
            end
        
    end

    // Data out ports  
    assign o_a = rf[i_src_0];
    assign o_b = rf[i_src_1];


endmodule 