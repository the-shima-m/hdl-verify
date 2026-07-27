# HDL-Verify: Project Timeline (July to December 2026)

**Project:** HDL-Verify: A Validation and Reproducibility Toolkit for AI Generated Hardware Description Code

**Fellow:** Shima Mohaghegh

**Duration:** July 2026 to December 2026 (6 months)

HDL-Verify is a free and open source Python tool. It checks whether two versions of a digital circuit are truly the same. One version is known to be correct, and the other is written by an AI model. The tool uses three methods together. It gives a formal mathematical proof, it runs a random input stress test, and it saves a full record of every run so the result can be repeated later.

Together with the tool, the project also releases ArithBench-100. This is a set of 100 reference arithmetic circuits with a correct and verified answer for each one.

The timeline below shows the planned deliverables for each month.

---

## Month 1, July 2026: Formal checker and project foundation

- Set up the public GitHub repository with automated testing.
- Connect the Yosys and ABC verification tools to a simple Python interface.


---

## Month 2, August 2026: Fuzz testing and benchmark growth

- Add the random input testing module using the Icarus Verilog simulator.
- Start the ArithBench collection with adder and multiplier circuits.

---

## Month 3, September 2026: Reproducibility record and first evaluation

- Build the reproducibility record. It saves the AI model, the prompt, and the version of every tool used, so any run can be repeated later.
- Extend ArithBench to larger circuits and more operations, such as subtraction and division.
- Evaluate one open weight language model on the benchmark.

---

## Month 4, October 2026: Comparative study

- Evaluate a second open weight language model.
- Compare the formal result with the simple test result, and measure the difference between them.

---

## Month 5, November 2026: Reproducibility study and feedback

- Repeat the Month 3 experiment after 30 days to see how much the AI output and the tools change over time.

---

## Month 6, December 2026: Release and sharing

- Release the hdl-verify package on the Python Package Index (PyPI).
- Publish user tutorials and a public results dashboard.
- Write up the results of the project and share them with the community.
