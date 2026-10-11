"""Run the documented stages in order and save one consolidated result file."""

import json
from .parameters import LabParameters
from .plot_style import configure
from . import identification, controller, robustness, hardware, disturbance, simulink_evidence


def run_all(project_root):
    parameters = LabParameters.load(project_root)
    (project_root / "results").mkdir(exist_ok=True)
    configure()
    metrics = {}
    stages = [identification, controller, robustness, hardware, disturbance, simulink_evidence]
    for stage in stages:
        print("Running " + stage.__name__.split(".")[-1] + "...")
        metrics.update(stage.run(project_root, parameters))
    (project_root / "results/metrics.json").write_text(
        json.dumps(metrics, indent=2) + "\n"
    )
    return metrics
