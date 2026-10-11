# Retained test evidence

- `hardware_step_test.jpeg`: experimental display, uploaded WhatsApp Image 2026-10-09 at 10.22.36 AM.jpeg.
- `simulink_model.png`: supplied Simulink architecture screenshot, uploaded image(20261009-060141).png.
- `simulink_scope.png`: supplied simulation output, uploaded image(20261009-060203).png.

Only the first file is treated as an experimental controller response. No experimental Session 2 raw CSV or repeated-trial data was supplied. Pixel extraction is approximate and is saved separately in results; it is not relabelled as raw instrument data.

## Confirmed controller setup

The complete physical three-op-amp circuit remained connected as shown in the revised KiCad schematic during the controller test. The physical potentiometer was adjusted until the reported input was approximately 2.565 V to track the desired setpoint with minimal overshoot. No exact time, terminal or raw trace accompanies that recollection; it is recorded separately in `test_conditions.json` rather than relabelled as a new hover bias. The retained later command readout is 2.498 V.

`results/simulink_scope_digitised.csv` contains image-derived Simulink altitude and command samples. `results/simulink_reference_reconstruction.csv` contains the Python prediction for the same initial 2.5 m reference and 5 m final reference at approximately 2.5 s. These are not original exported Simulink solver logs.
