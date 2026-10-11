"""Session 1: differentiate position, identify the model, and validate it."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
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
    raw = pd.read_csv(ROOT / "data/session1/PTRJUN003_raw.csv")
    reset = np.flatnonzero(raw["Time(s)"].diff().to_numpy() < 0)
    start = int(reset[-1]) if len(reset) else 0
    d = raw.iloc[start:, :4].copy().reset_index(drop=True)
    t, u, sv, y = [d.iloc[:, i].to_numpy(float) for i in range(4)]
    if not np.all(np.diff(t) > 0):
        raise ValueError("Non-monotonic retained time")
    v = np.r_[np.nan, np.diff(y) / np.diff(t)]
    vmid = np.r_[np.nan, (t[:-1] + t[1:]) / 2]
    ss = float(np.mean(v[t >= 120]))
    Ass = ss / parameters.identification_step_v
    target = 0.632 * ss
    idx = np.flatnonzero(v >= target)[0]
    t63 = float(
        t[idx - 1]
        + (target - v[idx - 1]) / (v[idx] - v[idx - 1]) * (t[idx] - t[idx - 1])
    )
    sel = (t >= 17) & (t <= 60)
    fit = least_squares(
        lambda p: p[0] * (1 - np.exp(-(t[sel] - p[2]) / p[1])) - v[sel],
        [ss, 8.1, 15.9],
        bounds=([30, 3, 15.5], [40, 15, 16.2]),
        xtol=1e-12,
        ftol=1e-12,
        gtol=1e-12,
    )
    Vfit, taufit, t0fit = map(float, fit.x)
    cal = (sv > 0) & (sv < 9.9) & (y > 0)
    ksfit = float(y[cal] @ sv[cal] / (y[cal] @ y[cal]))

    def pred_vel(tt):
        return (
            A
            * parameters.identification_step_v
            * (1 - np.exp(-np.maximum(tt - t0fit, 0) / tau))
        )

    def pred_pos(tt):
        q = np.maximum(tt - t0fit, 0)
        return A * parameters.identification_step_v * (q - tau * (1 - np.exp(-q / tau)))

    vv = pred_vel(t)
    yy = pred_pos(t)
    # Independent input treatment: retain the measured finite transition.
    # Initial velocity is zero at 15.7 s, immediately before the manual change.
    measured_times = t[t >= 15.7]
    measured_input = solve_ivp(
        lambda tt, state: [(A * (np.interp(tt, t, u) - parameters.hover_v) - state[0]) / tau],
        [15.7, float(t[-1])], [0.0], t_eval=measured_times,
        rtol=1e-8, atol=1e-9, max_step=0.05,
    )
    if not measured_input.success:
        raise RuntimeError(measured_input.message)
    measured_v = measured_input.y[0]
    measured_fit = (measured_times >= 17) & (measured_times <= 60)
    measured_valid = measured_times > 60
    pd.DataFrame({'time_s': measured_times, 'velocity_from_measured_input_mps': measured_v}).to_csv(
        RES / 'session1_measured_input_validation.csv', index=False)
    train = (t >= 17) & (t <= 60)
    valid = t > 60

    def rmse(a, b):
        return float(np.sqrt(np.mean((a - b) ** 2)))

    metrics = {
        "retained_rows": len(d),
        "discarded_rows": start,
        "sample_interval_s": 0.1,
        "v_infinity_mps": ss,
        "A_from_tail": Ass,
        "v_63p2_mps": target,
        "t_63p2_absolute_s": t63,
        "tau_63p2_from_15p9_s": t63 - 15.9,
        "fit_v_infinity": Vfit,
        "fit_tau": taufit,
        "fit_step_time": t0fit,
        "ks_fit": ksfit,
        "calibration_points": int(cal.sum()),
        "velocity_rmse_fit_window": rmse(v[train], vv[train]),
        "velocity_rmse_holdout": rmse(v[valid], vv[valid]),
        "position_rmse_holdout": rmse(y[valid], yy[valid]),
        "nominal_A": A,
        "nominal_tau": tau,
        "nominal_ks": ks,
        "nominal_kp": kp,
        "b": b,
        "kT": kt,
        "measured_input_velocity_rmse_fit_window": rmse(v[t >= 15.7][measured_fit], measured_v[measured_fit]),
        "measured_input_velocity_rmse_holdout": rmse(v[t >= 15.7][measured_valid], measured_v[measured_valid]),
        "parameter_checker": {"A_score_percent":100, "tau_score_percent":96, "sensor_score_percent":100,
                              "provenance":"Supplied Helicopter Parameter Check screenshot; not confidence intervals"},
    }
    d["Velocity(m/s)"] = v
    d["Velocity_time_midpoint(s)"] = vmid
    d["Model_velocity(m/s)"] = vv
    d["Model_position(m)"] = yy
    d.to_csv(RES / "session1_processed.csv", index=False)
    fig, axs = plt.subplots(3, 1, figsize=(7.1, 4.5), sharex=True)
    axs[0].plot(t, u, color=blue)
    axs[0].axhline(2.5, ls=":", color="gray")
    axs[0].set_ylabel("Input u (V)")
    axs[0].axvline(15.9, color=orange, ls="--")
    axs[0].text(25, 3.3, "Hover 2.5 V; final 5 V; Δu = 2.5 V")
    axs[1].plot(t, y, color=blue, label="Position channel (m)")
    axs[1].set_ylabel("Altitude y (m)")
    axs[2].plot(t, sv, color=green)
    axs[2].axhline(10, color=red, ls="--")
    axs[2].set_ylabel("Sensor (V)")
    axs[2].set_xlabel("Retained run time (s)")
    axs[2].text(45, 4.5, "Voltage clips at 10 V; metre channel keeps increasing")
    fig.tight_layout()
    save(fig, "identification_record")
    fig, ax = plt.subplots(figsize=(7.1, 2.3))
    zoom = (t >= 14.5) & (t <= 17.5)
    ax.plot(t[zoom], u[zoom], 'o-', ms=3, color=blue, label='Logged manual input')
    ax.plot([14.5,15.9,15.9,17.5], [2.5,2.5,5,5], '--', color=orange,
            label='Ideal step approximation, 2.5 V increment')
    ax.set(xlabel='Retained run time (s)', ylabel='Input command (V)', xlim=(14.5,17.5), ylim=(2.35,5.15))
    ax.legend(fontsize=9, loc='lower right')
    save(fig, 'step_input_transition')
    fig, ax = plt.subplots(figsize=(7.1, 3.5))
    q = t - 15.9
    ax.plot(q, v, color=blue, lw=1, label="Backward difference of position")
    ax.plot(q, vv, "--", color=orange, label="First-order model")
    ax.plot(measured_times-15.9, measured_v, ':', color=red, lw=1.2,
            label='Model driven by recorded input')
    ax.axhline(target, color=green, ls=":", label=f"63.2% = {target:.3f} m/s")
    ax.axvline(t63 - 15.9, color=green, ls=":")
    ax.axhline(ss, color="gray", ls=":")
    ax.set(
        xlim=(0, 60), ylim=(0, 39), xlabel="Time from step (s)", ylabel="Velocity (m/s)"
    )
    ax.text(12, 16, f"τ ≈ {t63 - 15.9:.2f} s; A ≈ {Ass:.4f} m/(s V)")
    ax.legend(loc="lower right", fontsize=10)
    save(fig, "velocity_identification")
    fig, axs = plt.subplots(1, 2, figsize=(7.1, 3.1))
    axs[0].plot(y[cal], sv[cal], "o", ms=3, color=blue, label="Unsaturated pairs")
    xx = np.array([0, 10.5])
    axs[0].plot(xx, ksfit * xx, color=orange, label=f"ks = {ksfit:.6f} V/m")
    axs[0].set(xlabel="Altitude (m)", ylabel="Sensor output (V)")
    axs[0].legend(fontsize=9)
    axs[1].plot(
        t[valid], v[valid] - vv[valid], color=blue, label="Held-out velocity residual"
    )
    axs[1].set(xlabel="Run time (s)", ylabel="Residual (m/s)")
    axs[1].legend(fontsize=9)
    fig.tight_layout()
    save(fig, "validation_sensor")
    fig, axs = plt.subplots(2, 1, figsize=(7.1, 3.8), sharex=True)
    axs[0].plot(t, y, color=blue, label="Recorded position")
    axs[0].plot(t, yy, "--", color=orange, label="Rounded model")
    axs[0].set_ylabel("Altitude (m)")
    axs[0].legend(fontsize=10)
    axs[1].plot(t, y - yy, color=green)
    axs[1].set(xlabel="Run time (s)", ylabel="Position residual (m)")
    fig.tight_layout()
    save(fig, "position_validation")
    return metrics
