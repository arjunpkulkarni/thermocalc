# Thermo-Calc Project - Complete Setup Summary

## 🎯 Project Overview

This project implements a complete solution for **Module 3: Engineering Design of Carbon and Stainless Steels** using **pycalphad**, the open-source Python alternative to Thermo-Calc.

## 📁 Project Structure

```
THERMOCALC/
├── README.md                      # Main project documentation
├── INSTALLATION.md                # Detailed installation guide
├── PROJECT_SUMMARY.md            # This file - complete overview
├── ANSWERS_REFERENCE.md          # Quick reference for all deliverables
│
├── requirements.txt              # Python dependencies
├── run_all.py                    # Master script to run everything
│
├── utils.py                      # Helper functions
├── part_a_carbon_steel.py       # Part A: Fe-C binary system
├── part_b_stainless_steel.py    # Part B: Fe-Cr-C ternary system
│
├── fe_c.tdb                      # Fe-C database (auto-generated)
├── fe_cr_c.tdb                   # Fe-Cr-C database (auto-generated)
│
└── outputs/                      # Generated plots and data
    ├── A1_phase_diagram_with_graphite.png
    ├── A2_phase_diagram_without_graphite.png
    ├── A5_austenite_boundary_fits.png
    ├── A9_steel_microstructure_vs_carbon.png
    ├── A9_steel_properties.csv
    ├── B1_Fe12.5Cr_XC_phase_diagram.png
    ├── B1_phase_diagram_data.csv
    ├── B2_Fe_Cr_C_ternary_diagram.png
    └── B2_ternary_compositions.csv
```

## 🚀 Quick Start Guide

### Step 1: Install Dependencies

```bash
# Option 1: Using pip
pip install -r requirements.txt

# Option 2: Using pip3
pip3 install -r requirements.txt

# Option 3: Using Python module
python3 -m pip install -r requirements.txt

# Option 4: Install individually
pip install pycalphad numpy matplotlib scipy pandas
```

### Step 2: Run the Analysis

```bash
# Interactive menu
python3 run_all.py

# Or run individual parts
python3 part_a_carbon_steel.py    # Part A only
python3 part_b_stainless_steel.py # Part B only
```

### Step 3: Review Results

All outputs are saved in the `outputs/` directory:
- **PNG files**: Phase diagrams and plots for your report
- **CSV files**: Numerical data and calculations

## 📊 What Each Script Does

### `part_a_carbon_steel.py`

Implements all Part A deliverables:

**A1:** Fe-C phase diagram WITH graphite
- Generates binary phase diagram
- Includes all phases: Liquid, BCC, FCC, Cementite, Graphite

**A2:** Fe-C phase diagram WITHOUT graphite
- More engineering-relevant diagram
- Explains why graphite is excluded

**A3:** Eutectic point analysis
- Identifies eutectic temperature and composition
- Calculates maximum operating temperatures

**A4:** Eutectoid point analysis
- Identifies eutectoid temperature and composition
- Determines eutectoid reaction

**A5:** Austenite boundary fitting
- Quadratic regression on phase boundaries
- Provides equations for integration into simulators

**A6:** Eutectoid steel (0.76 wt% C)
- Cooling pathway analysis
- Lever rule calculations
- Pearlite formation

**A7:** Hypoeutectoid steel (0.52 wt% C)
- Proeutectoid ferrite formation
- Phase fraction evolution
- Microstructure prediction

**A8:** Hypereutectoid steel
- Reverse calculation from eutectoid cementite
- Room temperature analysis
- Cementite decomposition discussion

**A9:** Steel series design
- Analysis of 6 different carbon contents
- Properties vs composition
- Design recommendations

### `part_b_stainless_steel.py`

Implements all Part B deliverables:

**B1:** Binary Fe-12.5Cr-XC phase diagram
- Fixed Cr content at 12.5 wt%
- Variable C content 0-5 wt%
- Carburization analysis
- Maximum C before cementite formation

**B2:** Ternary Fe-Cr-C diagram at 1500 K
- Triangular phase diagram
- Analysis of 4 specific compositions
- Phase identification and compositions
- Tie line determination

### `utils.py`

Helper functions used by both parts:
- `lever_rule()`: Phase fraction calculations
- `quadratic_fit()`: Polynomial regression
- `wt_to_mole_fraction()`: Composition conversions
- `mole_to_wt_fraction()`: Composition conversions
- `calculate_cementite_content()`: Fe₃C calculations
- `save_plot()`: Figure export with proper formatting
- `print_section_header()`: Formatted output

### `run_all.py`

Master execution script:
- Dependency checking
- Interactive menu system
- Runs Part A and/or Part B
- Progress tracking
- Result summary

## 🔬 Technical Details

### pycalphad vs Thermo-Calc

| Feature | Thermo-Calc | pycalphad |
|---------|-------------|-----------|
| Cost | Commercial (~$10k+) | Free & Open Source |
| Language | GUI/Console Mode | Python |
| Databases | TCBIN, TCFE, PTERN | Custom TDB files |
| Phase Diagrams | ✓ | ✓ |
| Gibbs Energy Min | ✓ | ✓ |
| Scheil Simulation | ✓ | ✓ |
| Diffusion | ✓ | Limited |
| Documentation | Excellent | Good |
| Automation | Scripting | Native Python |

### Thermodynamic Databases

The project includes **simplified educational databases**:

#### fe_c.tdb (Fe-C Binary)
- Phases: Liquid, BCC_A2, FCC_A1, Cementite, Graphite
- Based on literature data
- Suitable for educational purposes

#### fe_cr_c.tdb (Fe-Cr-C Ternary)
- Phases: Liquid, BCC_A2, FCC_A1, Cementite, M₂₃C₆, M₇C₃, M₃C
- Includes chromium carbides
- Type 410 stainless steel composition

**Important:** For research or industrial use, obtain validated commercial databases!

### Key Calculations Implemented

1. **Phase Equilibrium**
   - Gibbs energy minimization
   - Multi-phase stability
   - Composition determination

2. **Lever Rule**
   - Two-phase mass fractions
   - Used throughout Part A

3. **Critical Points**
   - Eutectic identification
   - Eutectoid identification
   - Composition and temperature extraction

4. **Curve Fitting**
   - Quadratic regression for phase boundaries
   - Scipy least-squares optimization

5. **Microstructure Prediction**
   - Proeutectoid phase formation
   - Eutectoid transformation
   - Pearlite fraction calculation

## 📝 Deliverables Checklist

### Report to GradeScope (PDF)

- [ ] A1: Phase diagram with graphite + labeled regions
- [ ] A2: Phase diagram without graphite + labeled regions + explanation
- [ ] A3: Eutectic point data + temperature restrictions
- [ ] A4: Eutectoid point data
- [ ] A5: Quadratic fit equations
- [ ] A6: Eutectoid steel analysis + sketch
- [ ] A7: Hypoeutectoid analysis + microstructure explanation
- [ ] A8: Hypereutectoid calculations + discrepancy explanation
- [ ] A9: Steel series table + trends + design recommendation
- [ ] B1: Fe-12.5Cr-XC diagram + phase regions + carburization analysis
- [ ] B2: Ternary diagram + composition analysis (4 steels)

### Submit to PrairieLearn (Numerical)

- [ ] A3: Eutectic T, composition, reaction
- [ ] A4: Eutectoid T, composition, reaction
- [ ] A5: Coefficients a, b, c (low and high branches)
- [ ] A6: Phase compositions and fractions
- [ ] A7: Mass fractions (3 questions)
- [ ] A8: Overall C content, pearlite fraction, ferrite at RT
- [ ] B1: Maximum C content at two temperatures
- [ ] B2: Phase compositions (4 steels)

## 🎓 Learning Outcomes

After completing this project, you will understand:

1. **Phase Diagrams**
   - Binary and ternary systems
   - Reading and interpreting phase regions
   - Tie lines and lever rule

2. **Steel Metallurgy**
   - Carbon steel classifications
   - Phase transformations
   - Microstructure-property relationships

3. **Computational Thermodynamics**
   - Gibbs energy minimization
   - Phase equilibrium calculations
   - CALPHAD methodology

4. **Materials Design**
   - Composition-property optimization
   - Trade-offs (hardness vs toughness)
   - Engineering constraints

5. **Stainless Steel**
   - Passivation and corrosion resistance
   - Carburization effects
   - Chromium carbide formation

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'pycalphad'"
**Solution:** Install dependencies
```bash
pip3 install pycalphad
```

### Issue: Calculations are slow
**Solution:** Ternary systems are computationally expensive. Reduce grid resolution in code:
```python
temps = np.linspace(1000, 1800, 50)  # Instead of 300
```

### Issue: Phase diagram doesn't show expected regions
**Solution:** Check database phases. Simplified databases may not include all phases.
For production work, use commercial databases like TCFE or PTERN.

### Issue: "EquilibriumError" during calculation
**Solution:** Some compositions may not converge. This is normal at phase boundaries.
The code includes try-except blocks to handle these cases.

### Issue: Plots not displaying in SSH session
**Solution:** Use non-interactive backend:
```bash
export MPLBACKEND=Agg
```
Or add to Python script:
```python
import matplotlib
matplotlib.use('Agg')
```

## 📚 Additional Resources

### pycalphad Documentation
- Official docs: https://pycalphad.org/docs/latest/
- Examples: https://github.com/pycalphad/pycalphad/tree/develop/examples
- Paper: Otis & Liu (2017), J. Open Res. Software

### Thermodynamic Databases
- pycalphad-databases: https://github.com/pycalphad/pycalphad-databases
- NIST databases: https://www.nist.gov/mml/acmd/thermodynamic-databases
- ThermoCalc databases: https://www.thermocalc.com/products/databases/

### Steel Metallurgy References
- Callister & Rethwisch: *Materials Science and Engineering* (textbook)
- ASM Handbook Vol. 3: *Alloy Phase Diagrams*
- Porter & Easterling: *Phase Transformations in Metals and Alloys*

### Phase Diagram Resources
- ASM Alloy Phase Diagram Database
- SpringerMaterials phase diagrams
- MatWeb materials database

## 🤝 Support

For issues with:
- **This project**: Check ANSWERS_REFERENCE.md or contact course instructor
- **pycalphad**: https://github.com/pycalphad/pycalphad/issues
- **Python/dependencies**: Stack Overflow or Python documentation

## ⚖️ Citation

If you use this code for academic work:

```bibtex
@software{pycalphad2017,
  author = {Otis, Richard and Liu, Zi-Kui},
  title = {pycalphad: CALPHAD-based Computational Thermodynamics in Python},
  year = {2017},
  url = {https://pycalphad.org},
  doi = {10.5334/jors.140}
}
```

## 📅 Timeline

Recommended schedule:

- **Day 1**: Install dependencies, run scripts, generate all plots
- **Day 2**: Part A calculations (A1-A5)
- **Day 3**: Part A calculations (A6-A9)
- **Day 4**: Part B calculations (B1-B2)
- **Day 5**: Compile report, format plots, write explanations
- **Day 6**: Review, proofread, submit to PrairieLearn
- **Day 7**: Final report submission to GradeScope

**Deadline**: December 12, 2025 at 11:59 PM

## ✅ Final Checklist

Before submission:

- [ ] All plots generated and properly labeled
- [ ] All calculations shown with algebraic work
- [ ] All numerical answers checked
- [ ] Report formatted as single PDF
- [ ] All sections clearly labeled (A1, A2, ..., B2)
- [ ] PrairieLearn submissions completed
- [ ] Report uploaded to GradeScope
- [ ] Submission confirmed before deadline

## 🎉 Good Luck!

You now have a complete, production-ready solution for the Thermo-Calc project using open-source tools. The code is well-documented, modular, and follows best practices for scientific computing in Python.

Remember: **Show your work!** Points are deducted for numerical answers without algebraic support.

---

*Project created for MSE/MatSE Module 3: Engineering Design of Carbon and Stainless Steels*


