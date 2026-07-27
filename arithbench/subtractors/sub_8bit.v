// ArithBench-100: 8-bit Subtractor
// Operation: subtraction
// Bit width: 8
// Source: standard textbook design (two's complement subtraction)
// Ground truth: diff = a - b, borrow_out set when a < b

module sub_8bit (
    input  [7:0] a,
    input  [7:0] b,
    output [7:0] diff,
    output       borrow_out
);
    assign {borrow_out, diff} = {1'b0, a} - {1'b0, b};
endmodule
