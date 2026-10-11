"""Load the same physical parameters used by MATLAB and the report."""

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(frozen=True)
class LabParameters:
    A: float
    tau: float
    ks: float
    kp: float
    hover_v: float
    identification_step_v: float
    reference_m: float
    end_s: float
    interval_s: float

    @property
    def b(self):
        return 1 / self.tau

    @property
    def kT(self):
        return self.A / self.tau

    @classmethod
    def load(cls, project_root: Path):
        values = json.loads((project_root / "config/lab_parameters.json").read_text())
        return cls(
            values["A"],
            values["tau_s"],
            values["sensor_gain_V_per_m"],
            values["controller_gain"],
            values["hover_command_V"],
            values["identification_step_V"],
            values["reference_step_m"],
            values["simulation_end_s"],
            values["simulation_interval_s"],
        )
