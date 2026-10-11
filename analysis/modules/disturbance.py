"""Illustrative actuator-bias simulation; this is a prediction, not an experiment."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from .plot_style import BLUE, ORANGE, GREEN, RED, exporter


def run(project_root, parameters):
    ROOT = project_root
    FIG = ROOT / "report/figures"
    RES = ROOT / "results"
    A, tau, ks, kp = (parameters.A, parameters.tau, parameters.ks, parameters.kp)
    b, kt = (parameters.b, parameters.kT)
    blue, orange, green, red = (BLUE, ORANGE, GREEN, RED)
    save = exporter(FIG)
    metrics = {}
    di = 0.002
    dtime = 70

    def simdist(t, z):
        yy, vv = z
        bias = di if t >= dtime else 0
        cmd = np.clip(2.5 + kp * ks * (5 - yy) + bias, 0, 5)
        return [vv, kt * (cmd - 2.5) - b * vv]

    s = solve_ivp(
        simdist,
        [0, 180],
        [0, 0],
        t_eval=np.linspace(0, 180, 3601),
        rtol=1e-09,
        atol=1e-10,
        max_step=0.02,
    )
    fig, ax = plt.subplots(figsize=(7.1, 3.1))
    ax.plot(s.t, s.y[0], color=blue)
    ax.axhline(5, color="k", ls="--")
    ax.axvline(dtime, color=orange, ls=":")
    ax.axhspan(4.6, 5.4, color=green, alpha=0.12)
    ax.set(xlabel="Time (s)", ylabel="Position (m)")
    ax.text(80, 5.85, "Illustrative +2 mV actuator bias at 70 s")
    save(fig, "disturbance_prediction")
    metrics["input_bias_limit_for_5m_8percent_v"] = 0.08 * 5 * kp * ks
    metrics["illustrative_bias_error_m"] = di / (kp * ks)
    return metrics
