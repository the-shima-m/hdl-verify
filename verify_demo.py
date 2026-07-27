"""
Demo script: run verify() on a known-good circuit pair.
Month 1 milestone: verify() prototype on a 4-bit adder.
"""

from hdl_verify import verify

report = verify(
    reference="arithbench/adders/adder_4bit.v",
    candidate="arithbench/adders/adder_4bit.v",  # same file = should PASS
)

print(report)
