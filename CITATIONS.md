# Tools Used by HDL-Verify — Citations and Acknowledgements

HDL-Verify orchestrates several external open-source tools. It calls them as
separate command-line programs; it does not copy or embed their source code.
Each tool is credited below with its license and how to cite it. If you use
HDL-Verify in academic work, please also cite the underlying tools you relied
on (at minimum Yosys and ABC for the formal check, and Icarus Verilog and
cocotb if you used the fuzzing flow).

---

## Yosys — formal synthesis and equivalence checking

- **What it does here:** reads the Verilog, builds the miter circuit, runs the
  SAT-based equivalence proof.
- **License:** ISC
- **Project:** https://yosyshq.net/yosys/
- **Cite:** C. Wolf, J. Glaser, and J. Kepler. "Yosys — A Free Verilog Synthesis
  Suite." In *Proceedings of the 21st Austrian Workshop on Microelectronics
  (Austrochip)*, 2013.

## ABC — SAT solver / logic optimization back end

- **What it does here:** performs the underlying formal proof; ships bundled
  with Yosys as `yosys-abc`.
- **License:** MIT-style license from the University of California, Berkeley.
- **Project:** Berkeley Logic Synthesis and Verification Group, ABC: A System
  for Sequential Synthesis and Verification.
  https://people.eecs.berkeley.edu/~alanmi/abc/
- **Cite:** R. Brayton and A. Mishchenko. "ABC: An Academic Industrial-Strength
  Verification Tool." In *Computer Aided Verification (CAV)*, LNCS 6174,
  Springer, 2010, pp. 24–40.

## Icarus Verilog — simulation (fuzz testing)

- **What it does here:** compiles and runs both designs on random inputs to
  compare their outputs (the fuzz test).
- **License:** GPL-2.0-or-later. (HDL-Verify calls it as a separate program and
  does not link its code, so HDL-Verify itself is not GPL.)
- **Project / author:** Stephen Williams. https://steveicarus.github.io/iverilog/
- **Cite:** S. Williams. "Icarus Verilog." https://steveicarus.github.io/iverilog/
  (software).

## cocotb — Python co-simulation framework (Month 2 fuzzer)

- **What it does here:** drives the random-input fuzzing harness from Python.
- **License:** BSD-3-Clause
- **Project:** https://www.cocotb.org/
- **Cite:** cocotb contributors. "cocotb: A coroutine-based co-simulation
  testbench environment for verifying VHDL and Verilog RTL using Python."
  https://www.cocotb.org/ (software).

## OSS CAD Suite — pre-built tool distribution

- **What it does here:** the packaged binary distribution used to install Yosys,
  ABC, and Icarus Verilog together (used because Homebrew could not build Yosys
  on macOS 12).
- **License:** mixed — each bundled tool keeps its own license (see above).
- **Project:** https://github.com/YosysHQ/oss-cad-suite-build

---

## Python development tools (not shipped to users)

Used only for development, all MIT-licensed: black, ruff, pytest, pre-commit.

## Reference-circuit provenance (ArithBench-100)

Each benchmark circuit records its own origin in its header comment and in the
`source` metadata field. Circuits are reimplemented from published
architectures or textbook descriptions rather than copied verbatim; the source
is cited per circuit. See NOTICE.md for the full provenance policy.
