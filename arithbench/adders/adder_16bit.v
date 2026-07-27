// ArithBench-100: 16-bit Ripple Carry Adder
// Operation: addition
// Bit width: 16
// Source: standard textbook design (ripple carry)
// Ground truth: a + b + carry_in = {carry_out, sum}

module adder_16bit (
    input  [15:0] a,
    input  [15:0] b,
    input         carry_in,
    output [15:0] sum,
    output        carry_out
);
    assign {carry_out, sum} = a + b + carry_in;
endmodule
