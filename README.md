# HDL-Verify

A validation and reproducibility toolkit for AI-generated Hardware Description Code.

## What it does

- **Formal check** — mathematically proves two circuits are equivalent (Yosys + ABC). Working.
- **Fuzz test** — throws random inputs at both circuits and compares outputs (Icarus Verilog). Working.
- (On going) **Reproducibility fingerprint** — logs every tool version and prompt so results can be replayed.

## Quick Start

Install from source (not yet on PyPI):

```bash
git clone https://github.com/the-shima-m/hdl-verify.git
cd hdl-verify
pip install -e .
```

```python
from hdl_verify import verify

report = verify("my_reference.v", "ai_generated.v")
print(report)
```

## Requirements

- Python 3.10+
- [Yosys](https://yosyshq.net/yosys/) (for formal checking)
- [Icarus Verilog](https://steveicarus.github.io/iverilog/) (for fuzz testing)

## Project Status

Under active development.

## Acknowledgment

This work was supported by the US Research Software Sustainability Institute
(URSSI) via grant G-2022-19347 from the Sloan Foundation.