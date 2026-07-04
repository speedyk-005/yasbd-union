from functools import cache
from importlib import import_module
from itertools import chain

import regex as re

from yasbd.rules import _LANG_PACK_REGISTRY, get_supported_langs
from yasbd.rules.base import Rules, build_abbr_pattern

# fmt: off
_RULE_SET_NAMES = {
    "TERMINATORS",
    "TITLE_ABBRVS",
    "DOTTED_GEOPOL_ABBRVS",
    "REFERENCE_ABBRVS",
    "SECTION_MARKERS",
    "INLINE_ONLY_ABBRVS",
    "NAMES_WITH_EXCLAMATION",
    "DATE_ABBRVS",
    "COMMON_SENT_STARTERS",
    "POST_QUOTATIVE_PARTICLES",
    "REPORTING_WORDS",

    # Specials
    "DISCOURSE_FINAL_PARTICLES",
    "STREET_ABBRVS",
    "ORG_PROPER_NOUNS",
    "DATE_WORDS",
}
# fmt: on


@cache
def _get_all_rules():
    """Return a list of all Rules subclasses from supported languages"""
    rules = []
    for lang in get_supported_langs():
        if lang == "xx":
            continue

        # Prioritize registered lang packs
        if lang in _LANG_PACK_REGISTRY:
            _, cls = _LANG_PACK_REGISTRY[lang]
        else:
            rule_mod = import_module(f"yasbd.rules.{lang}")
            cls = getattr(rule_mod, f"{lang.capitalize()}Rules")

        rules.append(cls)
    return rules


def _get_rule_set(set_name):
    """Union a named attribute from all Rules subclasses into a single set."""
    rule_set = set()
    for cls in _get_all_rules():
        if found_set := getattr(cls, set_name, None):
            rule_set.update(found_set)
    return rule_set


# fmt: off
class XxRules(Rules):


    @classmethod
    def _compile_regex_dynamically(cls):
        """Aggregate all languages' rule sets, then compile regex from the merged data."""
        for set_name in _RULE_SET_NAMES:
            setattr(cls, set_name, _get_rule_set(set_name))
        super()._compile_regex_dynamically()

        cls.MID_SENTENCE_FINDER_LST.extend(
            [
                # Spaced three-dot ellipsis mid-thought (e.g., ". . . she didn't")
                # Consecutive dots "..." or "...." still create sentence boundaries.
                re.compile(r"(?<!\.)\.(?:\s\.){2}"),

                # Ordinal numbers
                # https://learngerman.dw.com/en/ordinal-numbers/l-57731450/gr-60885529
                re.compile(r"\s\d{1,3}\."),

                # Multi-part abbreviations with spaces (like "d. h.", "z. B.", "i. d. R.")
                re.compile(r"\b[a-zA-Z]\.(?!\s+\w{2,})"),

                # Number/Time abbreviations followed by a date token (e.g., 9 a.m. Monday)
                re.compile(
                    rf"""
                        (?:\d\.|(?:(?<=\d)|\b)(?i:[ap]\.m\.))
                        (?=
                            \s+(?i:{build_abbr_pattern(cls.DATE_ABBRVS | cls.DATE_WORDS)})
                            (?:\.|\s|$)
                        )
                    """, re.X,
                ),

                # Geopolitical abbrv is followed by a common org noun (e.g., U.S.A Army)
                re.compile(
                    rf"""
                        \b(?i:{cls.DOTTED_GEOPOL_ABBRVS_PATTERN})\.
                        (?=\s+(?:{build_abbr_pattern(cls.ORG_PROPER_NOUNS)}))
                    """, re.X,
                ),

                # Full-width geopolitical abbreviations
                re.compile(r"(?:[\uFF21-\uFF3A\uFF41-\uFF5A\uFF10-\uFF19]．){1,5}"),

                # Time abbreviations followed by a date token (e.g., 9 a.m. Monday)
                re.compile(
                    rf"""
                        (?:(?<=\d)|\b)(?i:[ap]\.m\.)
                        (?=
                            \s+(?i:{build_abbr_pattern(cls.DATE_ABBRVS | cls.DATE_WORDS)})
                            (?:\.|\s|$)
                     )
                     """, re.X,
                 ),

                # Ud./Vd. pronoun abbreviation not followed by a proper name
                re.compile(
                    rf"""
                        \b(?i:{build_abbr_pattern({"ud", "uds", "vd", "vds"})})\.
                        (?!\s+(?:{cls.COMMON_STARTERS_PATTERN})\b)
                    """, re.X,
                ),
            ]
        )

        # Street abbrv followed by a common starters
        cls.ENDING_STREET_ABBRVS_FINDER = re.compile(
            rf"""
            (?:\b(?i:{build_abbr_pattern(cls.STREET_ABBRVS)})\.)
            (?=\s+(?:{cls.COMMON_STARTERS_PATTERN})\b)
           """, re.X,
        )

        # Discourse final particles that should not end a sentence (Thai, Burmese, etc.)
        cls.FINAL_PARTICLES_FINDER = re.compile(
            rf"{build_abbr_pattern(cls.DISCOURSE_FINAL_PARTICLES)}(?![\s]*[.?!;:๚๛])"
        )

    # fmt: on
    def _post_process_boundaries(self, main_boundaries: set[int], text: str) -> None:
        main_boundaries.update(
            m.end()
            for m in chain(
                self.FINAL_PARTICLES_FINDER.finditer(text),
                self.ENDING_STREET_ABBRVS_FINDER.finditer(text),
            )
        )
