# Rubric review and submission checks

This checklist is separate from the report. It does not guarantee marks.

| Rubric criterion | Report evidence | Remaining limitation |
| --- | --- | --- |
| Velocity conversion explained | Motion equation, integrator removal, difference formula, velocity figure | None in the retained-run calculation |
| Correct step test | Hover convention, finite transition, clock-reset handling, full long record | Only one retained trial |
| Repeated tests and aggregation | No fictitious repeats claimed | Supply at least three real trial records; aggregate gains/time constants and their ranges |
| Identification validation | Fit-window and held-out residuals, position-domain cross-check | Held-out interval is from the same run; no independent validation trial |
| Model and units | Free-body diagram, voltage/metre block diagram, input and sensor mappings | Transfer-function checker acceptance record absent |
| Logical root-locus design | Correct locus, gain bound, poles, damping, manual peak calculation | Previous-year numerical mistakes corrected |
| Plausibility of specifications | 30 s pole target distinguished from actual brief; joint uncertainty bound | Original gain has little aerodynamic margin |
| Sensible simulations | 5 m step, initial conditions, 0–5 V saturation, analytic/numerical agreement | MATLAB/Simulink scripts need execution in MATLAB |
| Component robustness | 2,048 documented loop-resistor/drag corner cases, ratio mismatch analysis | Original board does not guarantee all component corners |
| Experimental evaluation | Display readouts, digitised peak with resolution, model comparison | Screenshot metrics approximate; raw command and position logs absent |
| Demonstration plot and hardware | Retained screenshot, 5 m simulation, three-op-amp Veroboard photograph | Signed demonstration record absent; an awarded mark cannot be established |
| Fully labelled circuit | Clean redrawn design schematic and nominal values | Solder-side continuity and actual measured values are unverified |
| Recommendations | Match ratios, reduce gain, trim loaded hover, repeat/disturbance tests | Proposed changes have not been physically tested |
| Professional presentation | LaTeX, vector plots, referenced figures, captions, equations, concise methods | Final page count must remain ≤15 main-report pages |
| Git folder links | Local Git bundle, internal PDF evidence links, folder map and central remote URL setter | GitHub account connected; requested hosted repository remains unavailable. No live folder URL asserted |

## Highest-priority additions before submission

1. Real repeated Session 1 trials (the clock reset is not a repeat).
2. Raw Session 2 command, reference and altitude logs, plus a defined disturbance test.
3. Measured resistor values, readable chip model and solder-side netlist/bias feed confirmation.
4. Final demonstration marking/acceptance record where available.
5. Hosted repository URL and marker access, then rebuild the clickable online links.

The original supplied design meets the observed nominal accuracy and overshoot bounds. Full independent ±10% resistor robustness cannot honestly be stated. Strong technical reporting includes this finding and its correction.
