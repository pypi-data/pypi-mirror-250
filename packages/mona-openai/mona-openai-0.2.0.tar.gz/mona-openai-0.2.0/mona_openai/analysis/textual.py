"""
A module to derive text-related metrics such as text length, usage of
specific grammatical words, text repetition, etc...

These analyses can be used to detect significant drifts that could be
caused by hallucinations or bugs.

NOTE: There are many more analyses that can be added here.
"""

from collections.abc import Iterable
from typing import Optional

from .analyzer import Analyzer
from .util import get_analyzers

PREPOSITIONS = set(
    (
        "aboard",
        "about",
        "above",
        "across",
        "after",
        "against",
        "along",
        "amid",
        "among",
        "around",
        "as",
        "at",
        "before",
        "behind",
        "below",
        "beneath",
        "beside",
        "between",
        "beyond",
        "but",
        "by",
        "concerning",
        "considering",
        "despite",
        "down",
        "during",
        "except",
        "for",
        "from",
        "in",
        "inside",
        "into",
        "like",
        "near",
        "of",
        "off",
        "on",
        "onto",
        "out",
        "outside",
        "over",
        "past",
        "regarding",
        "round",
        "since",
        "through",
        "throughout",
        "till",
        "to",
        "toward",
        "under",
        "underneath",
        "until",
        "unto",
        "up",
        "upon",
        "with",
        "within",
        "without",
    )
)


class TextualAnalyzer(Analyzer):
    """
    An analyzer class that takes a text and provides methods to get analysis
    on that text such as length, word count, etc...
    """

    def __init__(self, text: str) -> None:
        self._text = text
        self._splitted_text = text.split()
        self._prepositions = tuple(
            x for x in self._splitted_text if x in PREPOSITIONS
        )

    def _none_init(self) -> None:
        self._text = None
        self._splitted_text = ()
        self._prepositions = ()

    def get_length(self) -> int:
        """
        Returns the length of the text.
        """
        return len(self._text)

    def get_word_count(self) -> int:
        """
        Returns the number of the words in the text.
        """
        return len(self._splitted_text)

    def get_preposition_count(self) -> int:
        """
        Returns the number of prepositions in the text.
        """
        return len(self._prepositions)

    def get_preposition_ratio(self) -> float:
        """
        Returns the ratio of prepositions in the text.
        """
        word_count = self.get_word_count()
        return self.get_preposition_count() / word_count if word_count else 0

    def get_words_not_in_others_count(
        self, others: Iterable["TextualAnalyzer"]
    ) -> int:
        """
        Returns the number of the words in the text that do not appear in the
        given other texts.
        """
        others_words_set = set().union(
            *tuple(other._splitted_text for other in others)
        )
        return len(
            [
                word
                for word in self._splitted_text
                if word not in others_words_set
            ]
        )


def get_textual_analyzers(
    texts: Iterable[Optional[str]],
) -> tuple[TextualAnalyzer, ...]:
    """
    Returns a tuple of TextualAnalyzers for all the given texts.
    """
    return get_analyzers(texts, TextualAnalyzer)
