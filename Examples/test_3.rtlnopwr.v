module test_3 (a, ci, co);

input ci;
output co;
input [3:0] a;

wire vdd = 1'b1;
wire gnd = 1'b0;

OR2X2 OR2X2_1 ( .A(a[0]), .B(a[1]), .Y(_0_) );
NAND2X1 NAND2X1_1 ( .A(_0_), .B(a[2]), .Y(_1_) );
NAND3X1 NAND3X1_1 ( .A(_1_), .B(a[3]), .C(ci), .Y(co) );
endmodule

