module test_2 (a, b, ci, co);

output co;
input ci;
input a;
input b;

wire vdd = 1'b1;
wire gnd = 1'b0;

BUFX2 BUFX2_1 ( .A(a), .Y(_0_) );
NAND2X1 NAND2X1_1 ( .A(ci), .B(_0_), .Y(_1_) );
NAND3X1 NAND3X1_1 ( .A(_1_), .B(a), .C(b), .Y(co) );
endmodule

