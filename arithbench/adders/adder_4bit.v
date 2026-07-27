// ArithBench-100: 4-bit Ripple Carry Adder
// Operation: addition
// Bit width: 4
// Source: standard textbook design
// Ground truth: a + b = sum, with carry_out

module adder_4bit (
    input  [3:0] a,
    input  [3:0] b,
    input        carry_in,
    output [3:0] sum,
    output       carry_out
);
    assign {carry_out, sum} = a + b + carry_in;
endmodule