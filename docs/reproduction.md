# Reproducing the simulations

## Requirements

The recorded runs used **LTspice 26.0.2 for macOS**. Use LTspice with its standard diode and MOSFET libraries. The MOSFET cases require **IPP600N25N3** in `standard.mos`; if your installation lacks it, obtain the model from an authorized source before running. Do not silently substitute a different MOSFET when comparing results.

## Run a case

1. Open a schematic from `ltspice/` in LTspice.
2. Check the pulse width and transient directive against the table below.
3. Run the transient analysis through **400 ms**.
4. Plot `V(n007)` for output, `I(L1)` and `I(L2)` for currents. In MOSFET cases, `V(n010)` is gate voltage and `V(n008)` is drain voltage.
5. Display **399.95-400 ms** to see five settled switching periods. Use **0-400 ms** for startup.
6. Open the simulation log and compare `.meas` results with `results/measurements.csv`.

| Schematic | Pulse width | Max timestep | Purpose |
|---|---:|---:|---|
| P08_baseline50_recovered.asc | 4.99 us | 100 ns | Near-ideal 50% duty |
| P08_duty30.asc | 2.99 us | 100 ns | Near-ideal 30% duty |
| P08_duty60.asc | 5.99 us | 100 ns | Near-ideal 60% duty |
| P08_loss_model.asc | 4.99 us | 100 ns | Assumed conduction losses |
| P08_mosfet_model.asc | 4.99 us | 100 ns | MOSFET substitution |
| P08_mosfet_check.asc | 4.99 us | 50 ns | MOSFET, compression disabled |

Average/minimum measurements use **390-400 ms**. Peak-to-peak ripple uses **399.9-400 ms**. Node numbers are those of the archived circuit; recheck them after rewiring. The baseline's saved log/netlist retains the earlier `P08_schematic` name.

## Recorded evidence and packaging changes

The logs record the October 2026 runs, not new runs performed for the GitHub release. Two stale duty-case schematic pulse widths were previously corrected to agree with the recorded netlists (2.99 us and 5.99 us). For this release, micro symbols were normalized to SPICE `u`, local user paths were removed from logs, and absolute standard-library references in archived netlists were made relative. No reported measurement values were edited. Open the `.asc` files to regenerate fresh netlists using your installed libraries.

`python3 scripts/check_results.py` checks pulse widths, transient settings, and matching measurement directives against the archived netlists, extracts the saved log measurements, and checks the headline numerical comparisons. It does **not** run LTspice or prove fresh-run reproducibility.

## Build the report

From `report/`, run `tectonic report.tex`, or use a LaTeX installation with the packages listed in `report.tex`. The report includes source screenshots so figure crops can be reproduced. The final PDF is `report/report.pdf`.

## Limits

No hardware was built for this project. Efficiency reflects the chosen models, not measured prototype efficiency. Timestep and compression changed together in the final numerical check; a controlled convergence study is still needed. Core loss, thermal rise, full diode recovery, and layout parasitics are outside the model. The quadruple/hextuple variants and closed-loop control were not simulated.
