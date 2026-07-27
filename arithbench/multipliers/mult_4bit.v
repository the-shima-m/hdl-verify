// ArithBench-100: 4-bit Unsigned Multiplier
// Operation: multiplication
// Bit width: 4 (inputs), 8 (product)
// Source: standard textbook design (unsigned array multiplier behavior)
// Ground truth: product = a * b

module mult_4bit (
    input  [3:0] a,
    input  [3:0] b,
    output [7:0] product
);
    assign product = a * b;
endmodule
