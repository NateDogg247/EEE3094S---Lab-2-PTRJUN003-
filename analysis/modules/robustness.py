"""Aerodynamic uncertainty, loaded circuit gain, and independent resistor corners."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import brentq
import itertools
from .plot_style import BLUE, ORANGE, GREEN, RED, exporter
from .controller import closed_response, response_metrics


def run(project_root, parameters):
    ROOT = project_root
    FIG = ROOT / "report/figures"
    RES = ROOT / "results"
    A, tau, ks, kp = (parameters.A, parameters.tau, parameters.ks, parameters.kp)
    b, kt = (parameters.b, parameters.kT)
    blue, orange, green, red = (BLUE, ORANGE, GREEN, RED)
    save = exporter(FIG)
    metrics = {}
    tt = np.linspace(
        0, parameters.end_s, round(parameters.end_s / parameters.interval_s) + 1
    )

    def closed(k=kp, drag=b, amp=5):
        return closed_response(tt, parameters, k, drag, amp)

    def step_metrics(y, amp=5):
        return response_metrics(tt, y, amp)

    fig, ax = plt.subplots(figsize=(7.1, 3.7))
    rows = []
    for factor in [0.9, 1, 1.1]:
        yc = closed(drag=factor * b)
        mm = step_metrics(yc)
        rows.append({"b_factor": factor, **mm})
        ax.plot(tt, yc, label=f"b × {factor:.1f}; Mp={mm['overshoot_percent']:.2f}%")
    ax.axhline(5, color="k", ls="--")
    ax.set(xlim=(0, 115), xlabel="Time (s)", ylabel="Position (m)")
    ax.legend(fontsize=10)
    save(fig, "aerodynamic_robustness")
    metrics["aerodynamic_corners"] = rows
    scalar = []
    for bf, kf in itertools.product([0.9, 1.1], [0.9, 1.1]):
        scalar.append(
            {
                "b_factor": bf,
                "kp_factor": kf,
                **step_metrics(closed(k=kp * kf, drag=b * bf)),
            }
        )
    metrics["scalar_corners"] = scalar
    Rnom = np.array(
        [100000, 1000, 100000, 1000, 4700, 10000, 100000, 100000, 100000, 100000], float
    )

    def bias_thevenin(w):
        r11, r12, r13, pot = (3900.0, 1200.0, 22000.0, 10000.0)
        pa, pb = (pot * w, pot * (1 - w))
        parallel = 1 / (1 / pot + 1 / r12)
        current = -15 / (r11 + parallel + r13)
        va = current * r11
        vb = current * (r11 + parallel)
        matrix = np.array(
            [
                [1 / r11 + 1 / r12 + 1 / pa, -1 / r12, -1 / pa],
                [-1 / r12, 1 / r13 + 1 / r12 + 1 / pb, -1 / pb],
                [-1 / pa, -1 / pb, 1 / pa + 1 / pb],
            ]
        )
        rth = float(np.linalg.solve(matrix, [0, 0, 1])[2])
        vth = va + w * (vb - va)
        return (vth, rth, -vth * 100000 / (100000 + rth))

    wpot = brentq(lambda w: bias_thevenin(w)[2] - 2.5, 0.01, 0.99)
    vth, rth, ubias = bias_thevenin(wpot)
    metrics["bias_network"] = {
        "w_fraction": wpot,
        "open_wiper_v": vth,
        "thevenin_ohm": rth,
        "loaded_hover_v": ubias,
        "loaded_kp": 0.01 * 1.47 * (1 + 100000 / (100000 + rth)) / 2,
    }
    corners = []
    for factors in itertools.product([0.9, 1.1], repeat=10):
        R = Rnom * np.array(factors)
        r1, r2, r3, r4, r5, r6, r7, r8, r9, r10 = R
        af = r4 / r3
        ar = (1 + af) * r2 / (r1 + r2)
        g2 = 1 + r5 / r6
        r = r10 / (r9 + rth)
        g3 = (1 + r) * r8 / (r7 + r8)
        K = af * g2 * g3
        ratio = ar / af
        for bf in [0.9, 1.1]:
            ze = bf * b / (2 * np.sqrt(kt * K * ks))
            os = 0 if ze >= 1 else 100 * np.exp(-np.pi * ze / np.sqrt(1 - ze * ze))
            corners.append([bf, K, ratio, abs(1 - ratio) * 100, os])
    co = pd.DataFrame(
        corners,
        columns=[
            "b_factor",
            "feedback_kp",
            "reference_feedback_ratio",
            "tracking_error_percent",
            "overshoot_percent",
        ],
    )
    co.to_csv(RES / "independent_resistor_corners.csv", index=False)
    metrics["resistor_corners"] = {
        "number": len(co),
        "kp_min": co.feedback_kp.min(),
        "kp_max": co.feedback_kp.max(),
        "worst_tracking_error_percent": co.tracking_error_percent.max(),
        "reference_ratio_min": co.reference_feedback_ratio.min(),
        "reference_ratio_max": co.reference_feedback_ratio.max(),
        "worst_overshoot_percent": co.overshoot_percent.max(),
        "nominal_loaded_prediction": 0.01 * 1.47 * (1 + 100000 / (100000 + rth)) / 2,
        "nominal_pot_fraction": wpot,
        "nominal_pot_thevenin_ohm": rth,
    }
    fig, axs = plt.subplots(1, 2, figsize=(7.1, 3.2))
    axs[0].hist(co.overshoot_percent, bins=28, color=blue)
    axs[0].axvline(30, color=red, ls="--")
    axs[0].set(xlabel="Overshoot (%)", ylabel="Corner count")
    axs[1].hist(co.tracking_error_percent, bins=28, color=orange)
    axs[1].axvline(8, color=red, ls="--")
    axs[1].set(xlabel="Tracking error after bias trim (%)", ylabel="Corner count")
    fig.tight_layout()
    save(fig, "component_robustness")
    newkp = 0.0068 * 1.47 * (1 + 100000 / (100000 + rth)) / 2
    metrics["recommended_kp"] = newkp
    metrics["recommended_worst_scalar_overshoot_percent"] = step_metrics(
        closed(k=newkp * 1.1, drag=0.9 * b)
    )["overshoot_percent"]
    return metrics
