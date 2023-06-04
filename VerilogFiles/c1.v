//# 4 inputs


module c1 (a,b,c,d,e,z);

input a,b,c,d,e;
output z;
wire f,g,h,i;

not not1 (f,b);
and and1 (g,a,f);
or or1 (h,c,d);
nand nand1 (i,h,e);
nor nor1(z,g,i);

endmodule
