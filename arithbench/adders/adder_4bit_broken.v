// Deliberately incorrect 4-bit adder — ignores carry_in.
// Used to confirm the formal checker can detect a real bug.
module adder_4bit_broken (
    input  [3:0] a,
    input  [3:0] b,
    input        carry_in,
    output [3:0] sum,
    output       carry_out
);
    assign {carry_out, sum} = a + b;
endmodule