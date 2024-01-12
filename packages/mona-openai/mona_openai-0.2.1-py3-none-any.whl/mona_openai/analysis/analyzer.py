from abc import ABCMeta


class Analyzer(metaclass=ABCMeta):
    """
    A parent analyzer class for typing purposes and basic shared logic.
    """

    def is_none_analyzer(self) -> bool:
        return False

    def _none_init(self) -> None:
        """
        Child classes can override this to allow specific logic when
        converting an Analyzer to a NoneAnalyzer.
        """
        pass
