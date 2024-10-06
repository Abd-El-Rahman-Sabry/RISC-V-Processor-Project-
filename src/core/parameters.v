`ifndef PARAMS
`define PARAMS 

    `define     RF_WIDTH            16 
    `define     DB_WIDTH            32
    `define     AB_WIDTH            $clog2(`DB_WIDTH)
    `define     FUNCT_WIDTH         4
    `define     STATUS_REG_WIDTH    3


    // ALU functions 

    `define     ALU_ADD     4'b0000
    `define     ALU_SUB     4'b0001
    `define     ALU_NOT     4'b0010
    `define     ALU_AND     4'b0011
    `define     ALU_XOR     4'b0100
    `define     ALU_A       4'b0101
    `define     ALU_B       4'b0111

    // Flags 

    `define     N_FLG       0 
    `define     Z_FLG       1 
    `define     C_FLG       2 


    // Register file 

    `define RF_SIZE 8

`endif 
