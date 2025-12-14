# Installation and Setup Guide

## Quick Start

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- **pycalphad**: Computational thermodynamics library (Thermo-Calc alternative)
- **numpy**: Numerical computing
- **matplotlib**: Plotting and visualization
- **scipy**: Scientific computing (for curve fitting)
- **pandas**: Data analysis and CSV export

### 2. Verify Installation

```bash
python run_all.py
```

Select option 4 to test that all dependencies are correctly installed.

### 3. Run Analysis

#### Option A: Run Everything
```bash
python run_all.py
```
Then select option 3 to run both parts.

#### Option B: Run Individual Parts
```bash
# Part A only
python part_a_carbon_steel.py

# Part B only
python part_b_stainless_steel.py
```

## Detailed Installation Steps

### macOS / Linux

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run project
python run_all.py
```

### Windows

```cmd
# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run project
python run_all.py
```

## Troubleshooting

### Issue: "No module named 'pycalphad'"

**Solution:**
```bash
pip install pycalphad
```

### Issue: "ImportError: cannot import name 'Database'"

**Solution:** Update pycalphad to latest version
```bash
pip install --upgrade pycalphad
```

### Issue: Plots not displaying

**Solution:** Make sure matplotlib backend is configured
```bash
pip install --upgrade matplotlib
```

On macOS, if using SSH or remote connection:
```bash
export MPLBACKEND=Agg
```

### Issue: "No such file or directory: 'outputs'"

**Solution:** The scripts automatically create the outputs directory. If you see this error, manually create it:
```bash
mkdir outputs
```

## Database Information

### Thermodynamic Databases (TDB Files)

The project includes simplified thermodynamic databases for educational purposes:

- **fe_c.tdb**: Fe-C binary system (created automatically)
- **fe_cr_c.tdb**: Fe-Cr-C ternary system (created automatically)

### For Production Use

For research or industrial applications, obtain validated databases:

1. **Open-Source Options:**
   - [pycalphad-databases](https://github.com/pycalphad/pycalphad-databases)
   - NIST databases
   
2. **Commercial Databases:**
   - **TCBIN**: Binary systems (ThermoCalc)
   - **TCFE**: Iron-based systems (ThermoCalc)
   - **PTERN**: Ternary systems
   - **SSOL**: Solution databases

To use a custom database, replace the database loading code:
```python
db = Database('your_custom_database.tdb')
```

## Output Files

After running the analysis, you'll find:

```
outputs/
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

## Performance Notes

- **Part A** (Binary Fe-C): ~1-2 minutes
- **Part B** (Ternary Fe-Cr-C): ~5-10 minutes

Ternary calculations are computationally intensive. For faster results, reduce the number of grid points in the code.

## Support

For issues with:
- **pycalphad**: https://github.com/pycalphad/pycalphad/issues
- **This project**: Check README.md or contact your course instructor

## Citations

If using this code for academic work, cite:

```bibtex
@software{pycalphad,
  title = {pycalphad: Python library for computational thermodynamics},
  author = {Otis, Richard and Liu, Zi-Kui},
  year = {2017},
  url = {https://pycalphad.org}
}
```

## License

This educational project is provided as-is for academic use.
pycalphad is licensed under the MIT License.


