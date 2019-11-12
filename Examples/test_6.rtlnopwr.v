module test_6 (a, b, c, y);

input [1:0] a;
input [1:0] b;
input [1:0] c;
output y;

wire vdd = 1'b1;
wire gnd = 1'b0;

NOR2X1 NOR2X1_1 ( .A(a[1]), .B(a[0]), .Y(_0_) );
AND2X2 AND2X2_1 ( .A(b[1]), .B(b[0]), .Y(_1_) );
OAI21X1 OAI21X1_1 ( .A(_1_), .B(_2_), .C(c[0]), .Y(_3_) );
NAND2X1 NAND2X1_1 ( .A(_3_), .B(c[1]), .Y(y) );
endmodule

