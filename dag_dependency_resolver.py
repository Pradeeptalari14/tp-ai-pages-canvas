"""Topological Dependency Resolver for Dynamic Canvas.

Orders cell execution into a Directed Acyclic Graph (DAG) ensuring all reactive
upstream dependencies resolve prior to downstream evaluation.
"""

from collections import defaultdict, deque
import logging
from typing import Dict, List, Set

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("dag_dependency_resolver")


class CanvasDAGResolver:
    """Computes topological evaluation ordering for reactive canvas graphs."""

    def __init__(self):
        self.adj_list: Dict[str, List[str]] = defaultdict(list)
        self.in_degree: Dict[str, int] = defaultdict(int)
        self.all_nodes: Set[str] = set()

    def add_dependency(self, upstream_node: str, downstream_node: str) -> None:
        self.adj_list[upstream_node].append(downstream_node)
        self.in_degree[downstream_node] += 1
        self.all_nodes.add(upstream_node)
        self.all_nodes.add(downstream_node)

    def compute_evaluation_order(self) -> List[str]:
        queue: deque[str] = deque([node for node in self.all_nodes if self.in_degree[node] == 0])
        order: List[str] = []
        current_in_degree = dict(self.in_degree)

        while queue:
            node = queue.popleft()
            order.append(node)
            for neighbor in self.adj_list[node]:
                current_in_degree[neighbor] -= 1
                if current_in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) != len(self.all_nodes):
            raise ValueError("Cycle detected in Dynamic Canvas reactive DAG!")

        logger.info("Computed valid topological evaluation order: %s", order)
        return order


def run_demo() -> None:
    resolver = CanvasDAGResolver()
    resolver.add_dependency("query_database", "compute_stats")
    resolver.add_dependency("compute_stats", "render_chart")
    resolver.add_dependency("compute_stats", "export_pdf_report")

    order = resolver.compute_evaluation_order()
    logger.info("DAG Execution Pipeline: %s", " -> ".join(order))


if __name__ == "__main__":
    run_demo()
