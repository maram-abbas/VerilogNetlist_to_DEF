module test_5 (a, b, c, y);

input [1:0] a;
input [1:0] b;
input c;
output y;

wire vdd = 1'b1;
wire gnd = 1'b0;

NAND3X1 NAND3X1_1 ( .A(a[0]), .B(a[1]), .C(b[0]), .Y(_0_) );
NAND3X1 NAND3X1_2 ( .A(b[1]), .B(c), .C(_0_), .Y(y) );
endmodule

