// ArithBench-100: <SHORT NAME, e.g. "8-bit Ripple Carry Adder">
// Operation: <addition | multiplication | subtraction | division | ...>
// Bit width: <e.g. 8>
// Source: <where this came from — textbook title + author, paper, or "original">
// Ground truth: <the exact function, e.g. "a + b + carry_in = {carry_out, sum}">
//
// This circuit must be COMBINATIONAL (no clock, no registers) so that both
// the formal check and the fuzz test can run on it. Sequential designs are
// out of scope for the current version (see README).

module TEMPLATE (
    input  [7:0] a,
    input  [7:0] b,
    output [8:0] result
);
    assign result = a + b;
endmodule
