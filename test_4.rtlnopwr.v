module test_4 (a, ci, co);

input ci;
output co;
input [3:0] a;

wire vdd = 1'b1;
wire gnd = 1'b0;

NOR2X1 NOR2X1_1 ( .A(ci), .B(a[0]), .Y(_0_) );
AND2X2 AND2X2_1 ( .A(_0_), .B(a[1]), .Y(_1_) );
INVX1 INVX1_1 ( .A(a[2]), .Y(_2_) );
OR2X2 OR2X2_1 ( .A(_2_), .B(_1_), .Y(_3_) );
NAND2X1 NAND2X1_1 ( .A(_3_), .B(a[2]), .Y(_4_) );
NAND3X1 NAND3X1_1 ( .A(_4_), .B(a[3]), .C(ci), .Y(co) );
endmodule

