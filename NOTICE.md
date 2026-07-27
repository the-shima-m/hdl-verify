# Third-Party Tools and Licenses

HDL-Verify is an orchestration layer: it calls external open-source tools
as separate programs (via the command line) rather than copying their code
into this package. Each tool keeps its own license, listed below. Because
HDL-Verify invokes these tools as separate processes and does not bundle or
link their source, HDL-Verify itself can be released under a permissive
license (see LICENSE).

None of the tools below are redistributed as part of this package. Users
install them separately (for example via the OSS CAD Suite).

## Verification and simulation tools

| Tool | Purpose in HDL-Verify | License |
|------|----------------------|---------|
| Yosys | Reads Verilog, builds the miter circuit for equivalence checking | ISC |
| ABC | SAT-based formal proof engine (bundled with Yosys as `yosys-abc`) | MIT-style (UC Berkeley) |
| Icarus Verilog | Simulator used for the random-input fuzz test | GPL-2.0-or-later |
| cocotb | Python co-simulation framework for the fuzzer (Month 2) | BSD-3-Clause |
| OSS CAD Suite | Pre-built distribution that packages the above tools together | Mixed (see each tool) |

Note on Icarus Verilog: it is licensed under the GPL, but HDL-Verify runs it
as a separate command-line program and does not incorporate its code, so
using it here does not place HDL-Verify under the GPL.

## Python libraries

| Library | Purpose | License |
|---------|---------|---------|
| (list runtime dependencies here as they are added) | | |

Development-only tools (not shipped to users): black (MIT), ruff (MIT),
pytest (MIT), pre-commit (MIT).

## ArithBench-100 reference circuits

Each circuit in the benchmark records its own origin in the circuit's header
comment and in the benchmark metadata (the `source` field). Provenance rules
for the collection:

- **Reimplemented from published architectures** (including the author's own
  ISCAS 2020 and TCAS-II 2022 finite-field multiplier papers): the Verilog is
  written fresh from the design description. Circuit designs and algorithms are
  not themselves copyrightable; only a specific code listing is. The source
  paper is cited in the circuit header.
- **Textbook designs:** reimplemented from the description, never copied
  verbatim from a published listing. The textbook is cited.
- **Open-source designs:** included only where the upstream license permits
  redistribution; the upstream license and a link are recorded in the circuit's
  metadata. GPL-licensed sources are avoided in the redistributed collection so
  the benchmark can stay permissively licensed.

## How to cite the tools

If you use HDL-Verify in academic work, please also cite the underlying tools:
Yosys (C. Wolf, YosysHQ) and ABC (Berkeley Logic Synthesis and Verification
Group), plus Icarus Verilog and cocotb where the fuzzing flow is used.
