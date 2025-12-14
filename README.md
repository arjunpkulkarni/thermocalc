# Thermo-Calc Project: Engineering Design of Carbon and Stainless Steels

## Project Overview
This project uses **pycalphad** (open-source alternative to Thermo-Calc) to design:
- Part A: Fe-C carbon steels
- Part B: Fe-Cr-C martensitic stainless steels (Type 410)

## Setup Instructions

1. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

2. **Download Thermodynamic Database:**
The project requires a thermodynamic database (TDB file) for Fe-C-Cr systems.
- For academic use, you can download from: https://github.com/pycalphad/pycalphad-databases
- Or use the simplified database included in this project

3. **Run Scripts:**

### Part A - Carbon Steel Design
```bash
python part_a_carbon_steel.py
```

### Part B - Stainless Steel Design
```bash
python part_b_stainless_steel.py
```

## Project Structure
- `part_a_carbon_steel.py` - Binary Fe-C phase diagram calculations
- `part_b_stainless_steel.py` - Ternary Fe-Cr-C calculations
- `utils.py` - Helper functions for calculations
- `requirements.txt` - Python dependencies
- `outputs/` - Generated plots and results

## Features
- Binary and ternary phase diagram generation
- Eutectic and eutectoid point identification
- Phase fraction calculations (lever rule)
- Polynomial fitting for phase boundaries
- Steel microstructure predictions

## Output
All plots and calculation results will be saved in the `outputs/` directory.


# thermocalc
