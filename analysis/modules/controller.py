"""Nominal closed-loop model, root locus, and step-response predictions."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import TransferFunction
from scipy.signal import step
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
    tt = np.linspace(
        0, parameters.end_s, round(parameters.end_s / parameters.interval_s) + 1
    )

    def closed(k=kp, drag=b, amp=5):
        _, yn = step(TransferFunction([kt * k * ks], [1, drag, kt * k * ks]), T=tt)
        return amp * yn

    def step_metrics(yy, amp=5):
        z = np.flatnonzero(np.abs(yy - amp) > 0.02 * abs(amp))
        return {
            "overshoot_percent": float(max(0, (yy.max() - amp) / amp * 100)),
            "peak_m": float(yy.max()),
            "peak_time_s": float(tt[np.argmax(yy)]),
            "settling_2percent_s": (
                float(tt[min(z[-1] + 1, len(tt) - 1)]) if len(z) else 0
            ),
            "terminal_error_m": float(amp - yy[-1]),
        }

    nom = closed()
    metrics["simulation_nominal"] = step_metrics(nom)
    wn = np.sqrt(kt * kp * ks)
    zeta = b / (2 * wn)
    wd = np.sqrt(wn**2 - (b / 2) ** 2)
    metrics.update(
        {
            "wn": wn,
            "zeta": zeta,
            "wd": wd,
            "sigma": b / 2,
            "overshoot_analytic_percent": 100
            * np.exp(-np.pi * zeta / np.sqrt(1 - zeta * zeta)),
            "peak_time_analytic_s": np.pi / wd,
            "settling_envelope_s": -np.log(0.02 * np.sqrt(1 - zeta * zeta)) / (b / 2),
        }
    )
    zmin = -np.log(0.3) / np.sqrt(np.pi**2 + np.log(0.3) ** 2)
    metrics["zeta_min_30percent"] = zmin
    metrics["kp_max_nominal"] = b * b / (4 * kt * ks * zmin * zmin)
    metrics["kp_max_joint_scalar10"] = (0.9 * b) ** 2 / (
        4 * kt * ks * zmin * zmin * 1.1
    )
    metrics["breakaway_gain"] = b * b / (4 * kt * ks)
    gg = np.linspace(0, 0.035, 1200)
    roots = np.array([np.roots([1, b, kt * k * ks]) for k in gg])
    fig, ax = plt.subplots(figsize=(7.1, 3.8))
    for i in range(2):
        ax.plot(roots[:, i].real, roots[:, i].imag, color=blue)
    ax.plot([0, -b], [0, 0], "x", ms=8, color="k", label="Open-loop poles")
    pp = np.roots([1, b, kt * kp * ks])
    ax.plot(pp.real, pp.imag, "o", color=orange, label="Kp = 0.01432")
    ax.axvline(-b / 2, color=green, ls=":", label="Re = −1/(2τ) = −0.06173")
    xx = np.linspace(-0.16, 0, 100)
    slope = np.sqrt(1 - zmin * zmin) / zmin
    ax.plot(xx, -xx * slope, "--", color="gray", label="30% overshoot boundary")
    ax.plot(xx, xx * slope, "--", color="gray")
    ax.axvline(-4 / 30, color=red, ls="--", label="30 s envelope target (unreachable)")
    ax.set(
        xlim=(-0.16, 0.012),
        ylim=(-0.25, 0.25),
        xlabel="Real part (s⁻¹)",
        ylabel="Imaginary part (s⁻¹)",
    )
    ax.legend(fontsize=9, loc="upper left")
    save(fig, "root_locus")
    fig, axs = plt.subplots(2, 1, figsize=(7.1, 3.8), sharex=True)
    axs[0].plot(tt, nom, color=blue, label="5 m step; nominal controller")
    axs[0].axhline(5, color="k", ls="--", label="Reference 5 m")
    axs[0].axhspan(4.9, 5.1, color=green, alpha=0.12, label="2% band")
    axs[0].plot(
        [metrics["simulation_nominal"]["peak_time_s"]], [nom.max()], "o", color=orange
    )
    axs[0].annotate(
        f"Peak {nom.max():.3f} m\nOvershoot {metrics['simulation_nominal']['overshoot_percent']:.2f}%",
        (metrics["simulation_nominal"]["peak_time_s"], nom.max()),
        xytext=(42, 6.0),
        arrowprops={"arrowstyle": "->"},
        fontsize=10,
    )
    axs[0].set_ylabel("Position (m)")
    axs[0].legend(fontsize=9, loc="lower right")
    cmd = 2.5 + kp * ks * (5 - nom)
    axs[1].plot(tt, cmd, color=orange)
    axs[1].axhline(2.5, color="gray", ls=":")
    axs[1].set(
        xlim=(0, 100), xlabel="Time from reference step (s)", ylabel="Command (V)"
    )
    fig.tight_layout()
    save(fig, "nominal_response")
    pd.DataFrame(
        {"time_s": tt, "reference_m": 5, "nominal_position_m": nom, "command_v": cmd}
    ).to_csv(RES / "nominal_simulation.csv", index=False)
    return metrics


def closed_response(time_s, parameters, gain=None, drag=None, amplitude=5):
    """Return a linear position step response with the sensor gain included."""
    gain = parameters.kp if gain is None else gain
    drag = parameters.b if drag is None else drag
    coefficient = parameters.kT * gain * parameters.ks
    _, response = step(
        TransferFunction([coefficient], [1, drag, coefficient]), T=time_s
    )
    return amplitude * response


def response_metrics(time_s, output_m, amplitude=5):
    """Measure overshoot and the final entry into the reference-based 2% band."""
    outside = np.flatnonzero(np.abs(output_m - amplitude) > 0.02 * abs(amplitude))
    return {
        "overshoot_percent": float(
            max(0, (output_m.max() - amplitude) / amplitude * 100)
        ),
        "peak_m": float(output_m.max()),
        "peak_time_s": float(time_s[np.argmax(output_m)]),
        "settling_2percent_s": (
            float(time_s[min(outside[-1] + 1, len(time_s) - 1)]) if len(outside) else 0
        ),
        "terminal_error_m": float(amplitude - output_m[-1]),
    }
