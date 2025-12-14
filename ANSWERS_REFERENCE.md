# Quick Reference Guide for Project Deliverables

## Part A: Carbon Steel Design

### A1 & A2: Phase Diagrams
- **A1**: Phase diagram WITH graphite
- **A2**: Phase diagram WITHOUT graphite (more engineering relevant)
  - Why? Cementite formation is kinetically favored even though graphite is thermodynamically stable
  - Cementite is metastable but practically stable on engineering timescales

### A3: Eutectic Point
- **Temperature**: ~1420 K (1147°C)
- **Composition**: ~4.3 wt% C
- **Reaction**: LIQUID → γ-AUSTENITE + CEMENTITE
- **Maximum Operating Temperatures**:
  - 1600 K: C < 4.3 wt% (above eutectic, some liquid present)
  - 1500 K: All compositions 0-5 wt% are solid
  - 1400 K: All compositions 0-5 wt% are solid

### A4: Eutectoid Point
- **Temperature**: ~1000 K (727°C)
- **Composition**: ~0.76 wt% C
- **Reaction**: γ-AUSTENITE → α-FERRITE + CEMENTITE
- Forms characteristic "pearlite" microstructure

### A5: Austenite Boundary Fits
Quadratic fits: T[K] = a[wt% C]² + b[wt% C] + c

**Low-carbon branch** (α + γ boundary):
- Fit points along lower boundary of austenite region
- Use data extraction from phase diagram

**High-carbon branch** (γ + Fe₃C boundary):
- Fit points along upper boundary of austenite region
- Use data extraction from phase diagram

### A6: Eutectoid Steel (0.76 wt% C)

**Cooling from 1100 K to below 1000 K:**

| Property | Value |
|----------|-------|
| Phases Present | α-ferrite, Cementite |
| Microstructure | Pearlite (lamellar) |
| α-ferrite composition | ~0.02 wt% C |
| Cementite composition | ~6.69 wt% C |
| α-ferrite mass fraction | ~0.89 (89%) |
| Cementite mass fraction | ~0.11 (11%) |

**Calculation (Lever Rule):**
```
W_cementite = (0.76 - 0.02) / (6.69 - 0.02) = 0.111
W_ferrite = 1 - 0.111 = 0.889
```

### A7: Hypoeutectoid Steel (0.52 wt% C)

**Just ABOVE eutectoid (T = 1000+ K):**
| Phase | Mass Fraction |
|-------|---------------|
| Proeutectoid α-ferrite | ~0.32 (32%) |
| γ-austenite | ~0.68 (68%) |

**Just BELOW eutectoid (T = 1000- K):**
| Phase | Mass Fraction |
|-------|---------------|
| Total α-ferrite | ~0.92 (92%) |
| Cementite | ~0.08 (8%) |
| γ-austenite | 0 (transformed) |

**α-ferrite breakdown:**
| Type | Mass Fraction |
|------|---------------|
| Proeutectoid α-ferrite | ~0.32 (formed above T_eutectoid) |
| Eutectoid α-ferrite | ~0.60 (formed from γ at T_eutectoid) |

**Explanation:**
- Proeutectoid α-ferrite forms first as large grains when cooling through α + γ region
- At eutectoid, remaining γ-austenite transforms to pearlite (fine α + Fe₃C)
- Result: Large α grains + pearlite regions

### A8: Hypereutectoid Steel

**Given:** W_eutectoid_cementite = 0.103

**Find overall carbon content:**

At eutectoid, cementite fraction in pearlite = 0.111 (from lever rule)

If eutectoid cementite = 0.103, then:
- Pearlite fraction = 0.103 / 0.111 = 0.928
- Proeutectoid cementite = 1 - 0.928 = 0.072

Using lever rule at T_eutectoid:
- C_overall = 0.072 × (6.69 - 0.76) + 0.76 = **1.19 wt% C**

**At 298 K (room temperature):**
| Phase | Mass Fraction |
|-------|---------------|
| α-ferrite | ~0.85 (85%) |
| Cementite | ~0.15 (15%) |

**Discrepancy Explanation:**
- **Observed**: α-ferrite content HIGHER than predicted
- **Reason**: Cementite (Fe₃C) is metastable
  - Slowly decomposes: Fe₃C → 3Fe + C(graphite)
  - Releases Fe, increasing α-ferrite
  - Process is slow but measurable
- **Sign**: Positive error (more α-ferrite than equilibrium)

### A9: Steel Series Analysis

| C (wt%) | Cementite (%) | Pearlite (%) | Properties |
|---------|---------------|--------------|------------|
| 0.0 | 0 | 0 | Soft, ductile |
| 0.2 | 3.0 | 26 | Low carbon steel |
| 0.4 | 6.0 | 53 | Medium carbon |
| 0.6 | 9.0 | 79 | Medium carbon |
| 0.8 | 12.0 | 100+ | High carbon |
| 1.0 | 15.0 | 96* | High carbon |

*Above eutectoid, pearlite = 100 - proeutectoid cementite

**Trends:**
- **Hardness**: Increases with C (more cementite = harder)
- **Toughness**: Decreases with C (more cementite = more brittle)

**Design Recommendation:**
- For hardness > 160 BHN AND toughness > 75 J
- **Optimal range: 0.4 - 0.6 wt% C**
- This is medium carbon steel

---

## Part B: Stainless Steel Design

### B1: Fe-12.5Cr-XC Phase Diagram

**Fixed**: Cr = 12.5 wt%
**Variable**: C = 0-5 wt%
**Temperature**: 1000-1800 K

**Phase regions along T = 1350 K:**
- Low C: BCC (ferrite)
- Intermediate C: FCC (austenite) or BCC + carbides
- High C: Multiple carbides (M₂₃C₆, M₇C₃, M₃C)
- Very high C: Cementite may appear

**Maximum C before cementite:**
- At 1350 K: ~3.0-3.5 wt% C
- At 1200 K: ~2.0-2.5 wt% C

**Carburization to 3.5 wt% C at 1525 K:**
- Surface: High C → chromium carbides
- Bulk: Low C (0.15 wt%)
- Long-term: Carbon diffuses, creates gradient
- Risk: If cementite forms, strength decreases
- Recommendation: Monitor and limit operating temperature

### B2: Ternary Fe-Cr-C at 1500 K

**Composition 1: Fe-15.0Cr-0.01C**
- Phases: BCC (ferrite)
- Composition: Nearly pure Fe-Cr solid solution with trace C

**Composition 2: Fe-15.0Cr-0.70C**
- Phases: FCC (austenite) + M₂₃C₆
- Two-phase region

**Composition 3: Fe-20.0Cr-0.20C**
- Phases: BCC + M₂₃C₆
- Higher Cr stabilizes BCC and carbides

**Composition 4: Fe-15.0Cr-3.0C**
- Phases: M₇C₃ + M₂₃C₆ + possibly cementite
- High carbon → multiple carbide phases

---

## Key Concepts Summary

### Lever Rule
For two-phase region with overall composition C₀:
```
W_right = (C₀ - C_left) / (C_right - C_left)
W_left = 1 - W_right
```

### Carbon in Cementite
Fe₃C composition:
- Fe: 93.31 wt%
- C: 6.69 wt%

### Phase Transformations
- **Eutectic**: Liquid → Two solids
- **Eutectoid**: Solid solution → Two solids
- **Pearlite**: Lamellar structure of α-ferrite + cementite

### Steel Classifications
- **Low carbon**: 0.05-0.3 wt% C (mild steel)
- **Medium carbon**: 0.3-0.6 wt% C
- **High carbon**: 1-2 wt% C
- **Cast iron**: >2 wt% C

### Stainless Steel
- **Martensitic**: 11-18% Cr, 0.1-1.2% C (Type 410)
- **Passivation**: Cr >11% forms protective oxide
- **Carburization**: Surface hardening via C enrichment

---

## Formulas and Calculations

### Weight to Mole Fraction
```
n_i = w_i / M_i
x_i = n_i / Σn_i
```

### Mole to Weight Fraction
```
m_i = x_i × M_i
w_i = m_i / Σm_i
```

### Quadratic Fit
```
T = a(wt% C)² + b(wt% C) + c
```

Use least squares regression (scipy.optimize.curve_fit)

---

## Report Writing Tips

### For Each Section:
1. **State the question** clearly
2. **Show your method** (equations, diagrams)
3. **Present calculations** with proper units
4. **Provide answers** with appropriate significant figures
5. **Include figures** with proper labels and captions
6. **Explain results** in engineering terms

### Figures:
- Phase diagrams: Label all single-phase regions
- Mark critical points (eutectic, eutectoid)
- Include axes labels with units
- Add figure captions explaining what is shown

### Calculations:
- Show all algebraic steps
- Include numerical values with units
- Use proper notation (subscripts, superscripts)
- Box or highlight final answers

### Discussion:
- Connect calculations to physical microstructure
- Explain trends in properties
- Relate to engineering applications
- Address sources of error or assumptions

---

## Common Mistakes to Avoid

1. ❌ Confusing pearlite (microstructure) with a phase
   - ✅ Pearlite is a mixture of α-ferrite + cementite

2. ❌ Forgetting to convert weight % to mole fractions
   - ✅ Use molar masses: Fe=55.845, Cr=51.996, C=12.011

3. ❌ Not showing algebraic work
   - ✅ Always show equations before plugging in numbers

4. ❌ Incorrect lever rule application
   - ✅ Remember: W_right = (C₀ - C_left) / (C_right - C_left)

5. ❌ Mixing up proeutectoid and eutectoid phases
   - ✅ Proeutectoid forms ABOVE eutectoid temperature

6. ❌ Ignoring significant figures
   - ✅ Match precision to input data

7. ❌ Not labeling phase diagram regions
   - ✅ Identify all single-phase and two-phase regions

---

## PrairieLearn Submission

Remember to submit numerical answers to PrairieLearn for:
- A3: Eutectic temperature, composition, reaction
- A4: Eutectoid temperature, composition, reaction
- A5: Quadratic fit coefficients (a, b, c)
- A6: Phase compositions and mass fractions
- A7: Mass fractions at different temperatures
- A8: Overall carbon content, pearlite fraction, ferrite at RT
- B1: Maximum carbon content values

---

## GradeScope Report

Your PDF report should include:
- All requested plots (properly labeled)
- All calculations with algebraic work
- Answers to discussion questions
- Table from A9
- Explanations and justifications

**Format:**
- Separate section for each task (A1, A2, ..., B2)
- Clear headings
- Professional presentation
- Page numbers
- Your name and course information


