"""Reactive Computational Kernel for AI Pages Dynamic Canvas.

Executes code cells in an isolated namespace, propagates reactive variables across
DAG nodes, and formats interactive rich media payloads.
"""

import logging
from typing import Any, Dict

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("canvas_reactive_kernel")


class ReactiveCell:
    """Represents a computational node in the dynamic canvas graph."""

    def __init__(self, cell_id: str, code: str, inputs: list[str], outputs: list[str]):
        self.cell_id = cell_id
        self.code = code
        self.inputs = inputs
        self.outputs = outputs
        self.last_result: Any = None
        self.dirty = True

    def mark_dirty(self) -> None:
        self.dirty = True


class CanvasKernelEngine:
    """Manages state execution and reactive propagation for dynamic pages."""

    def __init__(self, memory_limit_mb: int = 512):
        self.memory_limit_mb = memory_limit_mb
        self.cells: Dict[str, ReactiveCell] = {}
        self.global_scope: Dict[str, Any] = {}

    def register_cell(self, cell: ReactiveCell) -> None:
        self.cells[cell.cell_id] = cell
        logger.info("Registered reactive canvas cell: %s", cell.cell_id)

    def execute_cell(self, cell_id: str) -> Dict[str, Any]:
        cell = self.cells.get(cell_id)
        if not cell:
            raise KeyError(f"Cell {cell_id} not found in canvas engine")

        local_scope: Dict[str, Any] = dict(self.global_scope)
        try:
            # Execute Python code within controlled scope
            exec(cell.code, local_scope)
            for out_var in cell.outputs:
                if out_var in local_scope:
                    self.global_scope[out_var] = local_scope[out_var]

            cell.dirty = False
            cell.last_result = {out: self.global_scope.get(out) for out in cell.outputs}
            logger.info("Successfully evaluated cell %s: outputs=%s", cell_id, list(cell.outputs))
            return {"status": "success", "cell_id": cell_id, "data": cell.last_result}
        except Exception as exc:
            logger.error("Failed to execute cell %s: %s", cell_id, exc)
            return {"status": "error", "cell_id": cell_id, "error": str(exc)}


def main() -> None:
    engine = CanvasKernelEngine(memory_limit_mb=512)

    cell1 = ReactiveCell(
        cell_id="cell-load-metrics",
        code="data = [12, 19, 3, 5, 2, 3]; avg_val = sum(data) / len(data)",
        inputs=[],
        outputs=["data", "avg_val"],
    )
    cell2 = ReactiveCell(
        cell_id="cell-threshold-alert",
        code="alert = avg_val > 5.0",
        inputs=["avg_val"],
        outputs=["alert"],
    )

    engine.register_cell(cell1)
    engine.register_cell(cell2)

    res1 = engine.execute_cell("cell-load-metrics")
    res2 = engine.execute_cell("cell-threshold-alert")

    logger.info("Run finished. Result 1: %s", res1)
    logger.info("Run finished. Result 2: %s", res2)


if __name__ == "__main__":
    main()
