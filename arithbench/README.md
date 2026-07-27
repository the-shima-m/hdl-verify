# ArithBench-100

A benchmark of reference arithmetic circuits with verified, unambiguous
ground truth, used to evaluate AI-generated Verilog against a known-correct
standard.

## Scope

All circuits here are **combinational** (no clock, no registers): the output
depends only on the current inputs. This is deliberate — combinational
arithmetic has a single unambiguous correct answer for every input, which is
exactly what makes it good ground truth. Sequential (clocked/pipelined)
designs are future work.

## Layout

    arithbench/
      adders/         addition circuits
      multipliers/    multiplication circuits
      subtractors/    subtraction circuits
      dividers/       division circuits
      TEMPLATE.v      copy this to start a new circuit
      metadata.csv    catalog of every circuit (one row each)

For circuits used to test the checker itself, a matching `*_broken.v` may
sit beside the correct version (a deliberately incorrect variant).

## How to add a circuit (3 steps)

1. Copy `TEMPLATE.v` into the right folder and rename it, e.g.
   `multipliers/mult_8bit.v`. Fill in the header comment (especially the
   `Source:` line) and write the module.

2. Verify it is correct using the tool itself. The simplest check is that a
   circuit is equivalent to itself, but the real test is running a candidate
   against it:

       hdl-verify adders/adder_8bit.v adders/adder_8bit.v

   For a genuine ground-truth check, compare against an independent
   reference implementation of the same operation.

3. Add one row to `metadata.csv` describing the circuit, then commit.

## Provenance and licensing

Circuits are **reimplemented** from published descriptions, never copied
verbatim from a copyrighted listing. The `Source:` header records where each
design came from. See the top-level NOTICE.md for the full policy.
