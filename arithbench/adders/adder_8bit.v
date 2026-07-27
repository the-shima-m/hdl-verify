// ArithBench-100: 8-bit Ripple Carry Adder
// Operation: addition
// Bit width: 8
// Source: standard textbook design (ripple carry)
// Ground truth: a + b + carry_in = {carry_out, sum}

module adder_8bit (
    input  [7:0] a,
    input  [7:0] b,
    input        carry_in,
    output [7:0] sum,
    output       carry_out
);
    assign {carry_out, sum} = a + b + carry_in;
endmodule
