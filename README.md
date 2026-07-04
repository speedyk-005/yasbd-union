# yasbd-union

[![Python Version](https://img.shields.io/badge/Python-3.11%20--%203.14-blue)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/yasbd-union?kill_cache=2)](https://pypi.org/project/yasbd-union)
[![Tests](https://img.shields.io/github/actions/workflow/status/speedyk-005/yasbd-union/build-and-test.yml?branch=main&label=tests)](https://github.com/speedyk-005/yasbd-union/actions)
[![Stability](https://img.shields.io/badge/stability-alpha-red)](https://github.com/speedyk-005/yasbd-union)
[![License: MIT](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://opensource.org/licenses/MIT)

**Sentence splitting for when you genuinely have no idea what language you're looking at.**

---

## What this is

`yasbd-union` is an experimental add-on for [yasbd-lib](https://github.com/speedyk-005/yasbd).

It takes sentence-splitting rules from every installed language pack and throws them into one shared space.

Sometimes it behaves nicely.
Sometimes it makes bold assumptions.
Sometimes it surprises even you.

That's basically the whole deal.

---

## `auto` vs `xx`

**`auto`** tries to be smart about it.

It looks at your text, decides what language it is, and uses the right rules for the job. Clean and structured.

**`xx`** doesn't bother with that step.

It assumes your text is already a mix of everything and just applies all available rules at once.

|                    | `auto`              | `xx`                                   |
|--------------------|---------------------|----------------------------------------|
| Language handling  | Detects first       | Doesn't care                           |
| Accuracy           | Stable              | Depends on what rules are installed     |
| Mixed text         | Not ideal           | Basically its natural habitat          |
| False splits       | Rare                | Happens sometimes                      |
| Personality        | Careful             | A bit chaotic, but trying its best     |
| Best for           | Clean text          | Mixed-language messes     |

---

## Install

```bash
pip install yasbd-union
```

Then register it:

```python
from yasbd.rules import register_lang_packs
from yasbd import BoundaryDetector

register_lang_packs(["yasbd_union"])

detector = BoundaryDetector("xx")
```

---

Example
```python
sentences = list(detector.segment(
    "Dr. Wang said 你好世界。Prof. Li replied 是的。"
))

print(sentences)
```
Output:
```bash
["Dr. Wang said 你好世界。", "Prof. Li replied 是的。"]
```

---

## When to use xx

Use it when:

- You don't know what language your text is in
- Your input is messy, mixed, or unpredictable
- You're dealing with logs, chats, or scraped text
- You just want something that "tries its best"

---

## When not to use xx

Avoid it when:

- You need strict, repeatable results
- Your text is single-language
- You don't want surprises in sentence boundaries
- You're trying to explain results to someone very literal

In those cases, auto or a specific language pack will behave better.

---

## A few honest notes

- Some sentence splits will be slightly unexpected
- Results can change depending on installed language packs
- It is not fully predictable by design

If that sounds like a problem, xx is probably not what you want.

---

## License

**MIT:** If it breaks, it's still yours.
