module test_1 (a, b, c, y);

input [1:0] a;
input [1:0] b;
input [1:0] c;
output y;

wire vdd = 1'b1;
wire gnd = 1'b0;

AND2X2 AND2X2_1 ( .A(a[0]), .B(b[0]), .Y(_0_) );
AOI22X1 AOI22X1_1 ( .A(_0_), .B(a[1]), .C(b[1]), .D(c[0]), .Y(_1_) );
NAND2X1 NAND2X1_1 ( .A(_1_), .B(c[1]), .Y(y) );
endmodule
