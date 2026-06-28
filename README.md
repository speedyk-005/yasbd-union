# yasbd-xx 

[![Python Version](https://img.shields.io/badge/Python-3.11%20--%203.14-blue)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/yasbd-xx?kill_cache=1)](https://pypi.org/project/yasbd-xx)
[![Tests](https://img.shields.io/github/actions/workflow/status/speedyk-005/yasbd-xx/build-and-test.yml?branch=main&label=tests)](https://github.com/speedyk-005/yasbd-xx/actions)
[![Stability](https://img.shields.io/badge/stability-alpha-red)](https://github.com/speedyk-005/yasbd-xx)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)
[![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

**sentence splitting for when you have no idea what language that is.**

An experimental lang pack for [yasbd-lib](https://github.com/speedyk-005/yasbd) that
merges every known abbreviation set into one chaotic union. Sometimes it works.
Sometimes it doesn't. That's the deal.

---

## `auto` vs `xx`

**`auto`** is a concierge. It sniffs the first paragraph, decides whether you're
writing in French or Swahili, and dispatches to the precise rules for that language.
It's clean. It's correct. It knows what it's doing.

**`xx`** is a Swiss Army knife that lost the corkscrew. It takes every abbreviation,
every sentence starter, every discourse particle from every installed language, throws
them into a blender, and hopes the result works on your mixed-language train wreck.

|                    | `auto`               | `xx`                      |
|--------------------|----------------------|---------------------------|
| Detects language   | ✅ yes               | ❌ nope                   |
| Correct per lang   | ✅ almost always     | 🎲 depends on the phase of the moon |
| Handles mixed text | ❌ no (detects once) | ✅ yes (everything at once) |
| False splits       | rarely               | regularly (German `Es` leaks into Spanish — ask us how) |
| Best for           | clean, single-lang   | messy, mixed, "I'll fix it later" |

`xx` is not a language. It's a probabilistic overlay of your entire language ecosystem.
Use it when you need to get the job done and don't mind if a few sentences get
beheaded along the way.

---

## Installation

```bash
pip install yasbd-xx
```

## Usage

```python
from yasbd import BoundaryDetector
from yasbd.rules import register_lang_packs

register_lang_packs(["yasbd_xx"])

detector = BoundaryDetector("xx")
sentences = list(detector.segment(
    "Dr. Wang said 你好世界。Prof. Li replied 是的。"
))
# ["Dr. Wang said 你好世界。", "Prof. Li replied 是的。"]
```

Will it always work? No.
Will you survive? Probably.

---

## When NOT to use xx

- You need production-grade accuracy
- Your text is clean single-language
- You don't want to explain to your boss why "Ud. Es" got split in half

In those cases, use the language-specific code or `auto`.

---

## Caveat emptor

- False splits guaranteed. The more languages installed, the more creative they get.
- Cross-contamination is a feature, not a bug. German starters will leak into
  Spanish, Thai particles into French, your mileage will vary.
- Not deterministic across environments — depends on what lang packs you have installed.

You have been warned. Proceed anyway.

---

## License

MIT. You break it, you buy it. (You won't buy it. But you were warned.)
