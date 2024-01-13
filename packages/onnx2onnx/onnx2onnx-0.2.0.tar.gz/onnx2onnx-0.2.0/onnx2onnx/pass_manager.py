"""
Copyright Wenyi Tang 2023

:Author: Wenyi Tang
:Email: wenyitang@outlook.com

"""

from typing import Callable, List

from tabulate import tabulate

from .graph import OnnxGraph
from .passes import LEVEL1, LEVEL2, PASSES


class PassManager:
    """Ordered optimization pass list.

    Args:
        include (List[str], Optional): a list of pattern to select passes.
            Defaults to select all passes.
        exclude (List[str], Optional): a list of pattern to deselect passes.
            Defaults to None.
    """

    def __init__(self, include: List[str] = None, exclude: List[str] = None) -> None:
        self.activated: List[Callable[[OnnxGraph], OnnxGraph]] = []
        if not include:
            passes = [PASSES.get(i) for i in LEVEL1 + LEVEL2]
        else:
            passes = [PASSES.get(i) for i in include]
        if exclude:
            passes = list(filter(lambda i: i not in exclude, passes))
        self.activated = list(filter(lambda p: p is not None, passes))

    def optimize(self, graph: OnnxGraph, strict: bool = False) -> OnnxGraph:
        """Invoke passes on the input graph.

        Args:
            graph (OnnxGraph): See :class:`OnnxGraph`.
            strict (bool): Break if any pass fails.
        """
        for opt in self.activated:
            try:
                graph = opt(graph)
            except Exception as ex:  # pylint: disable=broad-exception-caught
                print(f"[E] {opt.__name__} failed: {ex}")
                if strict:
                    raise
        return graph

    @classmethod
    def print_all(cls):
        """Print the name of all passes."""
        print(PASSES, flush=True)

    def __repr__(self) -> str:
        return tabulate(
            [[i.__name__, i] for i in self.activated], ["PASS", "Func"], "grid"
        )
