"""Session 2: digitise the retained screenshot and calculate experimental metrics."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
from .plot_style import BLUE, ORANGE, GREEN, RED, exporter
from .controller import closed_response


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
    nom = closed_response(tt, parameters)
    im = np.array(
        Image.open(ROOT / "data/session2/hardware_step_test.jpeg").convert("RGB")
    )
    xlo, xhi, ylo, yhi = (602, 1414, 60, 540)
    ts = []
    ys = []
    for x in range(xlo, xhi + 1):
        rgb = im[ylo : yhi + 1, x, :].astype(float)
        R, G, B = rgb.T
        mask = (B - R > 35) & (B - G > 20) & (B > 100) & (R < 200)
        ix = np.flatnonzero(mask)
        if len(ix):
            ts.append((x - xlo) * 120 / (xhi - xlo))
            ys.append((yhi - (ylo + np.median(ix))) * 20 / (yhi - ylo))
    td = np.array(ts)
    yd = np.array(ys)
    pd.DataFrame({"time_s_digitised": td, "altitude_m_digitised": yd}).to_csv(
        RES / "hardware_screenshot_digitised.csv", index=False
    )
    mask = td <= 86.2
    td = td[mask]
    yd = yd[mask]
    ref = 5.033
    final = 4.897
    err = ref - final
    metrics["hardware_screenshot"] = {
        "reference_m": ref,
        "final_height_m": final,
        "displayed_tracking_m": 0.137,
        "displayed_command_v": 2.498,
        "displayed_sensor_v": 4.553,
        "display_time_s": 86.1,
        "error_from_height_m": err,
        "tracking_accuracy_percent": 100 * (1 - abs(err) / ref),
        "digitised_peak_m": float(yd.max()),
        "digitised_peak_time_s": float(td[np.argmax(yd)]),
        "overshoot_relative_to_reference_percent": float((yd.max() - ref) / ref * 100),
        "pixel_height_resolution_m": 20 / (yhi - ylo),
        "pixel_time_resolution_s": 120 / (xhi - xlo),
    }
    outside = np.flatnonzero(abs(yd - ref) > 0.02 * ref)
    outside8 = np.flatnonzero(abs(yd - ref) > 0.08 * ref)
    metrics["hardware_screenshot"]["final_trace_within_2percent_reference"] = bool(
        abs(yd[-1] - ref) <= 0.02 * ref
    )
    metrics["hardware_screenshot"]["entry_8percent_band_s"] = (
        float(td[min(outside8[-1] + 1, len(td) - 1)]) if len(outside8) else 0
    )
    fig, ax = plt.subplots(figsize=(7.1, 3.0))
    ax.plot(td, yd, color=blue, label="Experimental trace digitised from screenshot")
    ax.plot(
        tt, 5.033 * nom / 5, "--", color=orange, label="Nominal model (0 → 5.033 m)"
    )
    ax.axhline(ref, color="k", ls=":", label="Displayed reference 5.033 m")
    ax.axhspan(0.92 * ref, 1.08 * ref, color=green, alpha=0.12, label="8% band")
    ax.axhline(final, color=red, ls=":", label="Terminal display 4.897 m")
    ax.set(xlim=(0, 88), ylim=(0, 7), xlabel="Graph time (s)", ylabel="Altitude (m)")
    ax.legend(fontsize=9, loc="lower right")
    save(fig, "hardware_comparison")
    return metrics
