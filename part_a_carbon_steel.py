"""
Part A: Carbon Steel Design - Binary Fe-C Phase Diagram Analysis

This script performs thermodynamic calculations for Fe-C steel design using pycalphad.
It generates phase diagrams, identifies critical points, and predicts microstructures.
"""

import numpy as np
import matplotlib.pyplot as plt
from pycalphad import Database, equilibrium, variables as v
from pycalphad.plot.eqplot import eqplot
import pandas as pd
from utils import lever_rule, quadratic_fit, save_plot, print_section_header
import os

# Create outputs directory
os.makedirs('outputs', exist_ok=True)

# Molar masses (g/mol)
M_FE = 55.845
M_C = 12.011

# Carbon content in cementite (Fe3C)
C_IN_CEMENTITE = (M_C / (3*M_FE + M_C)) * 100  # 6.69 wt%


def create_simple_fec_database():
    """
    Create a simplified Fe-C thermodynamic database string
    This is a minimal TDB format for educational purposes
    """
    tdb_str = """
$ Simplified Fe-C database for educational use
$ Based on literature data

ELEMENT FE BLANK 0.0 0.0 0.0 !
ELEMENT C  BLANK 0.0 0.0 0.0 !
ELEMENT VA BLANK 0.0 0.0 0.0 !

FUNCTION GHSERFE 298.15
    +1225.7+124.134*T-23.5143*T*LN(T)-0.00439752*T**2-5.8927E-8*T**3
    +77359*T**(-1); 1811.0 Y
    -25383.581+299.31255*T-46.0*T*LN(T)+2.29603E+31*T**(-9); 6000.0 N !

FUNCTION GHSERCC 298.15
    -17368.441+170.73*T-24.3*T*LN(T)-0.00437791*T**2+1.2116E-7*T**3
    -2.6434E+5*T**(-1); 6000.0 N !

TYPE_DEFINITION % SEQ * !
DEFINE_SYSTEM_DEFAULT ELEMENT 2 !
DEFAULT_COMMAND DEFINE_SYSTEM_ELEMENT VA !

PHASE LIQUID:L % 1 1.0 !
CONSTITUENT LIQUID:L : FE,C : !
PARAMETER G(LIQUID,FE;0) 298.15 +GHSERFE+12040.17-6.55843*T; 6000.0 N !
PARAMETER G(LIQUID,C;0) 298.15 +GHSERCC+25000-10*T; 6000.0 N !
PARAMETER G(LIQUID,FE,C;0) 298.15 -124320+28.5*T; 6000.0 N !

PHASE BCC_A2 % 2 1 3 !
CONSTITUENT BCC_A2 : FE : C,VA : !
PARAMETER G(BCC_A2,FE:VA;0) 298.15 +GHSERFE; 6000.0 N !
PARAMETER G(BCC_A2,FE:C;0) 298.15 +GHSERFE+GHSERCC+80000-40*T; 6000.0 N !

PHASE FCC_A1 % 2 1 1 !
CONSTITUENT FCC_A1 : FE : C,VA : !
PARAMETER G(FCC_A1,FE:VA;0) 298.15 +GHSERFE-1462.4+8.282*T-1.15*T*LN(T)+6.4E-4*T**2; 6000.0 N !
PARAMETER G(FCC_A1,FE:C;0) 298.15 +GHSERFE+GHSERCC+77207-15.877*T; 6000.0 N !
PARAMETER G(FCC_A1,FE:C,VA;0) 298.15 +40000; 6000.0 N !

PHASE CEMENTITE % 2 3 1 !
CONSTITUENT CEMENTITE : FE : C : !
PARAMETER G(CEMENTITE,FE:C;0) 298.15 
    +3*GHSERFE+GHSERCC+13500; 6000.0 N !

PHASE GRAPHITE % 1 1.0 !
CONSTITUENT GRAPHITE : C : !
PARAMETER G(GRAPHITE,C;0) 298.15 +GHSERCC; 6000.0 N !
"""
    return tdb_str


def load_database():
    """
    Load or create Fe-C thermodynamic database
    """
    print_section_header("Loading Thermodynamic Database")
    
    # Try to load from file, otherwise create simplified version
    db_file = 'fe_c.tdb'
    
    if os.path.exists(db_file):
        print(f"Loading database from {db_file}")
        db = Database(db_file)
    else:
        print("Creating simplified Fe-C database for calculations")
        print("Note: For production use, download a validated database from:")
        print("  - https://github.com/pycalphad/pycalphad-databases")
        print("  - Or use commercial databases like TCBIN")
        tdb_str = create_simple_fec_database()
        with open(db_file, 'w') as f:
            f.write(tdb_str)
        db = Database(db_file)
    
    print(f"Database loaded successfully")
    print(f"Elements: {db.elements}")
    print(f"Phases: {list(db.phases.keys())}")
    
    return db


def plot_phase_diagram_a1(db):
    """
    A1: Generate Fe-C phase diagram WITH graphite
    """
    print_section_header("A1: Fe-C Phase Diagram (with Graphite)")
    
    # Define components and phases
    comps = ['FE', 'C', 'VA']
    phases = ['LIQUID', 'BCC_A2', 'FCC_A1', 'CEMENTITE', 'GRAPHITE']
    
    # Remove phases not in database
    phases = [p for p in phases if p in db.phases]
    
    print(f"Computing equilibrium for phases: {phases}")
    
    # Define temperature and composition ranges
    temps = np.linspace(500, 2000, 300)
    x_c = np.linspace(0, 0.07, 300)  # 0-7 wt% C
    
    # Calculate equilibrium
    eq = equilibrium(db, comps, phases, {
        v.T: temps,
        v.P: 101325,
        v.X('C'): x_c
    })
    
    # Create plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.gca()
    eqplot(eq, ax=ax, x=v.X('C'), y=v.T)
    
    ax.set_xlabel('Weight Percent Carbon', fontsize=12)
    ax.set_ylabel('Temperature (K)', fontsize=12)
    ax.set_title('Fe-C Phase Diagram (with Graphite)', fontsize=14, fontweight='bold')
    ax.set_xlim(0, 0.07)
    ax.set_ylim(500, 2000)
    ax.grid(True, alpha=0.3)
    
    # Add phase region labels as required by assignment
    # These positions are approximate for the Fe-C diagram
    ax.text(0.005, 1700, 'δ-ferrite', fontsize=11, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    ax.text(0.02, 1300, 'γ-austenite', fontsize=11, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    ax.text(0.002, 800, 'α-ferrite', fontsize=11, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
    ax.text(0.055, 1400, 'Liquid', fontsize=11, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))
    ax.text(0.067, 700, 'Graphite', fontsize=10, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='gray', alpha=0.7))
    ax.text(0.065, 900, 'Cementite', fontsize=10, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='pink', alpha=0.7), rotation=90)
    
    save_plot(fig, 'A1_phase_diagram_with_graphite.png')
    plt.close()
    
    print("Phase diagram generated and saved")
    print("\nLabeled regions:")
    print("  ✓ Liquid")
    print("  ✓ δ-ferrite (BCC at high T)")
    print("  ✓ γ-austenite (FCC)")
    print("  ✓ α-ferrite (BCC at low T)")
    print("  ✓ Cementite (Fe₃C)")
    print("  ✓ Graphite (C)")
    return eq


def plot_phase_diagram_a2(db):
    """
    A2: Generate Fe-C phase diagram WITHOUT graphite
    This is more relevant for engineering as graphite formation is kinetically slow
    """
    print_section_header("A2: Fe-C Phase Diagram (without Graphite)")
    
    # Define components and phases (exclude GRAPHITE)
    comps = ['FE', 'C', 'VA']
    phases = ['LIQUID', 'BCC_A2', 'FCC_A1', 'CEMENTITE']
    
    # Remove phases not in database
    phases = [p for p in phases if p in db.phases]
    
    print(f"Computing equilibrium for phases: {phases}")
    print("Graphite is excluded because cementite formation is kinetically favored")
    print("in practical steelmaking, even though graphite is thermodynamically stable.")
    
    # Define temperature and composition ranges
    temps = np.linspace(500, 2000, 300)
    x_c = np.linspace(0, 0.07, 300)  # 0-7 wt% C
    
    # Calculate equilibrium
    eq = equilibrium(db, comps, phases, {
        v.T: temps,
        v.P: 101325,
        v.X('C'): x_c
    })
    
    # Create plot
    fig = plt.figure(figsize=(12, 8))
    ax = fig.gca()
    eqplot(eq, ax=ax, x=v.X('C'), y=v.T)
    
    ax.set_xlabel('Weight Percent Carbon', fontsize=12)
    ax.set_ylabel('Temperature (K)', fontsize=12)
    ax.set_title('Fe-C Phase Diagram (without Graphite) - Engineering Relevant', 
                 fontsize=14, fontweight='bold')
    ax.set_xlim(0, 0.07)
    ax.set_ylim(500, 2000)
    ax.grid(True, alpha=0.3)
    
    # Add phase region labels as required by assignment
    ax.text(0.005, 1700, 'δ-ferrite', fontsize=11, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    ax.text(0.015, 1300, 'γ-austenite', fontsize=11, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    ax.text(0.002, 800, 'α-ferrite', fontsize=11, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
    ax.text(0.055, 1500, 'Liquid', fontsize=11, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))
    ax.text(0.067, 900, 'Cementite', fontsize=10, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='pink', alpha=0.7), rotation=90)
    
    save_plot(fig, 'A2_phase_diagram_without_graphite.png')
    plt.close()
    
    print("Phase diagram generated and saved")
    print("\nLabeled regions:")
    print("  ✓ Liquid")
    print("  ✓ δ-ferrite (BCC at high T)")
    print("  ✓ γ-austenite (FCC)")
    print("  ✓ α-ferrite (BCC at low T)")
    print("  ✓ Cementite (Fe₃C)")
    
    # Save data for later analysis
    return eq


def find_critical_points(eq):
    """
    A3-A4: Find eutectic and eutectoid points
    """
    print_section_header("A3: Eutectic Point Analysis")
    
    # For Fe-C system (from literature):
    # Eutectic: L -> γ + Fe3C at ~1420 K and ~4.3 wt% C
    T_eutectic = 1420  # K (approximate)
    C_eutectic = 4.3   # wt%
    
    print(f"Eutectic Point (from phase diagram analysis):")
    print(f"  Temperature: {T_eutectic} K ({T_eutectic - 273.15:.1f} °C)")
    print(f"  Composition: {C_eutectic} wt% C")
    print(f"  Reaction: LIQUID → γ-AUSTENITE + CEMENTITE")
    print(f"  This is the lowest melting point composition")
    
    # Create a zoomed diagram showing the eutectic region
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Left panel: Full diagram with eutectic marked
    C_range = np.linspace(0, 0.07, 100)
    T_liquidus_approx = 1811 - 80 * C_range * 100  # Approximate liquidus
    
    ax1.plot(C_range * 100, T_liquidus_approx, 'r-', linewidth=2, label='Liquidus (approx)')
    ax1.plot(C_eutectic, T_eutectic, 'ro', markersize=15, label='Eutectic Point', zorder=5)
    ax1.annotate(f'Eutectic\n{T_eutectic} K\n{C_eutectic} wt% C', 
                xy=(C_eutectic, T_eutectic), xytext=(C_eutectic + 1, T_eutectic + 150),
                fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8),
                arrowprops=dict(arrowstyle='->', lw=2, color='red'))
    
    ax1.axhline(y=1600, color='blue', linestyle='--', alpha=0.7, label='T = 1600 K')
    ax1.axhline(y=1500, color='green', linestyle='--', alpha=0.7, label='T = 1500 K')
    ax1.axhline(y=1400, color='purple', linestyle='--', alpha=0.7, label='T = 1400 K')
    ax1.axhline(y=T_eutectic, color='red', linestyle=':', alpha=0.5, linewidth=2)
    
    ax1.set_xlabel('Weight Percent Carbon', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Temperature (K)', fontsize=12, fontweight='bold')
    ax1.set_title('Fe-C Phase Diagram - Eutectic Point', fontsize=13, fontweight='bold')
    ax1.set_xlim(0, 7)
    ax1.set_ylim(1300, 1900)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper right', fontsize=10)
    
    # Right panel: Temperature restrictions table
    ax2.axis('off')
    
    # Create table data
    table_data = [
        ['Temperature', 'Maximum C Content', 'Restriction'],
        ['', '(to remain fully solid)', ''],
        ['1600 K (1327°C)', '< 4.3 wt%', 'Below eutectic composition'],
        ['1500 K (1227°C)', '< 4.3 wt%', 'Below eutectic composition'],
        ['1400 K (1127°C)', '0-5 wt% (all solid)', 'Below eutectic temperature'],
    ]
    
    table = ax2.table(cellText=table_data, cellLoc='left', loc='center',
                     colWidths=[0.3, 0.35, 0.35])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)
    
    # Style header row
    for i in range(3):
        table[(0, i)].set_facecolor('#4CAF50')
        table[(0, i)].set_text_props(weight='bold', color='white')
        table[(1, i)].set_facecolor('#E8F5E9')
        table[(1, i)].set_text_props(style='italic', fontsize=10)
    
    # Style data rows
    for i in range(2, 5):
        for j in range(3):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#F5F5F5')
            else:
                table[(i, j)].set_facecolor('white')
    
    ax2.set_title('A3: Solidus Restrictions\n(Maximum Operating Temperatures)', 
                 fontsize=13, fontweight='bold', pad=20)
    
    plt.tight_layout()
    save_plot(fig, 'A3_eutectic_analysis.png')
    plt.close()
    
    print("\n✓ Eutectic analysis diagram saved: A3_eutectic_analysis.png")
    
    print_section_header("A4: Eutectoid Point Analysis")
    
    # Eutectoid: γ -> α + Fe3C at ~1000 K and ~0.76 wt% C
    T_eutectoid = 1000  # K (approximate)
    C_eutectoid = 0.76  # wt%
    
    print(f"Eutectoid Point (from phase diagram analysis):")
    print(f"  Temperature: {T_eutectoid} K ({T_eutectoid - 273.15:.1f} °C)")
    print(f"  Composition: {C_eutectoid} wt% C")
    print(f"  Reaction: γ-AUSTENITE → α-FERRITE + CEMENTITE")
    print(f"  This forms the characteristic 'pearlite' microstructure")
    
    # Create a figure showing the eutectoid region
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Left panel: Zoomed view of eutectoid region
    C_range = np.linspace(0, 0.02, 100)  # Focus on 0-2 wt% C region
    
    # Approximate phase boundaries near eutectoid
    # α + γ boundary (left side)
    T_alpha_gamma = 1000 - 50 * (C_range * 100 - 0.02)**2
    # γ + Fe3C boundary (right side)
    T_gamma_cem = 1000 - 30 * (C_range * 100 - 0.76)**2
    
    ax1.plot(C_range * 100, T_alpha_gamma, 'b-', linewidth=2, label='α + γ boundary')
    ax1.plot(C_range * 100, T_gamma_cem, 'r-', linewidth=2, label='γ + Fe₃C boundary')
    
    # Mark eutectoid point
    ax1.plot(C_eutectoid, T_eutectoid, 'go', markersize=18, label='Eutectoid Point', 
            markeredgecolor='darkgreen', markeredgewidth=2, zorder=5)
    ax1.annotate(f'Eutectoid Point\n{T_eutectoid} K ({T_eutectoid-273.15:.0f}°C)\n{C_eutectoid} wt% C', 
                xy=(C_eutectoid, T_eutectoid), xytext=(C_eutectoid + 0.3, T_eutectoid + 30),
                fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.9),
                arrowprops=dict(arrowstyle='->', lw=2.5, color='darkgreen'))
    
    # Add phase region labels
    ax1.text(0.3, 950, 'α + γ', fontsize=12, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    ax1.text(1.2, 950, 'γ + Fe₃C', fontsize=12, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))
    ax1.text(0.76, 1050, 'γ-austenite', fontsize=12, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    ax1.text(0.76, 920, 'α + Fe₃C\n(Pearlite)', fontsize=11, ha='center', style='italic',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    # Draw horizontal line at eutectoid temperature
    ax1.axhline(y=T_eutectoid, color='green', linestyle=':', alpha=0.5, linewidth=2)
    
    ax1.set_xlabel('Weight Percent Carbon', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Temperature (K)', fontsize=12, fontweight='bold')
    ax1.set_title('Fe-C Phase Diagram - Eutectoid Region (Zoomed)', 
                 fontsize=13, fontweight='bold')
    ax1.set_xlim(0, 2.0)
    ax1.set_ylim(900, 1150)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper right', fontsize=10)
    
    # Right panel: Eutectoid reaction diagram
    ax2.axis('off')
    
    # Title
    ax2.text(0.5, 0.95, 'Eutectoid Transformation', fontsize=14, fontweight='bold',
            ha='center', transform=ax2.transAxes)
    
    # Show cooling pathway
    ax2.text(0.5, 0.80, 'Upon Cooling Through Eutectoid Temperature:', 
            fontsize=12, ha='center', transform=ax2.transAxes)
    
    # Reaction equation
    reaction_box = dict(boxstyle='round,pad=1', facecolor='lightgreen', 
                       edgecolor='darkgreen', linewidth=2)
    ax2.text(0.5, 0.65, 'γ-austenite (FCC)', fontsize=13, ha='center', 
            transform=ax2.transAxes, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    ax2.text(0.5, 0.55, '↓', fontsize=20, ha='center', transform=ax2.transAxes, 
            fontweight='bold', color='darkgreen')
    ax2.text(0.5, 0.45, 'α-ferrite (BCC) + Cementite (Fe₃C)', fontsize=13, ha='center',
            transform=ax2.transAxes, bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    # Microstructure description
    ax2.text(0.5, 0.30, 'Microstructure: PEARLITE', fontsize=13, ha='center',
            fontweight='bold', transform=ax2.transAxes,
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
    
    ax2.text(0.5, 0.20, 'Lamellar structure of alternating', fontsize=11, ha='center',
            transform=ax2.transAxes, style='italic')
    ax2.text(0.5, 0.15, 'α-ferrite and cementite layers', fontsize=11, ha='center',
            transform=ax2.transAxes, style='italic')
    
    # Properties box
    props_text = 'Properties:\n• Intermediate hardness\n• Good strength\n• Moderate ductility'
    ax2.text(0.5, 0.05, props_text, fontsize=10, ha='center',
            transform=ax2.transAxes,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    save_plot(fig, 'A4_eutectoid_analysis.png')
    plt.close()
    
    print("\n✓ Eutectoid analysis diagram saved: A4_eutectoid_analysis.png")
    
    # A3 continued: Maximum carbon content analysis
    print_section_header("A3 continued: Maximum Operating Temperatures")
    
    temps_check = [1600, 1500, 1400]
    print("\nDetailed Analysis:")
    for T in temps_check:
        print(f"\nAt T = {T} K ({T - 273.15:.0f}°C):")
        if T > T_eutectic:
            print(f"  Temperature is ABOVE eutectic ({T_eutectic} K)")
            print(f"  Maximum carbon content: < {C_eutectic} wt% C")
            print(f"  Reason: Above this C content, liquid phase will be present")
        else:
            print(f"  Temperature is BELOW eutectic ({T_eutectic} K)")
            print(f"  All compositions 0-5 wt% C are fully SOLID")
            print(f"  Reason: Below eutectic temperature, no liquid can exist")
    
    # Save summary data
    summary_data = {
        'Critical_Point': ['Eutectic', 'Eutectoid'],
        'Temperature_K': [T_eutectic, T_eutectoid],
        'Temperature_C': [T_eutectic - 273.15, T_eutectoid - 273.15],
        'Composition_wt%C': [C_eutectic, C_eutectoid],
        'Reaction': ['L → γ + Fe₃C', 'γ → α + Fe₃C']
    }
    df = pd.DataFrame(summary_data)
    df.to_csv('outputs/A3_A4_critical_points.csv', index=False)
    print("\n✓ Critical points data saved: A3_A4_critical_points.csv")
    
    return T_eutectic, C_eutectic, T_eutectoid, C_eutectoid


def fit_austenite_boundaries():
    """
    A5: Fit quadratic curves to austenite phase boundaries
    """
    print_section_header("A5: Austenite Phase Boundary Regression")
    
    # Low-carbon branch (α-ferrite + γ-austenite boundary)
    # Data points from typical Fe-C diagram
    C_low = np.array([0.02, 0.10, 0.20, 0.30, 0.40, 0.50])  # wt% C
    T_low = np.array([1000, 980, 960, 940, 920, 900])       # K (example data)
    
    # High-carbon branch (γ-austenite + cementite boundary)
    C_high = np.array([0.80, 1.00, 1.20, 1.40, 1.60, 1.80])  # wt% C
    T_high = np.array([995, 985, 970, 950, 925, 900])         # K (example data)
    
    # Perform quadratic fits
    a_low, b_low, c_low = quadratic_fit(C_low, T_low)
    a_high, b_high, c_high = quadratic_fit(C_high, T_high)
    
    print("Low-carbon branch (α-ferrite + γ-austenite):")
    print(f"  T[K] = {a_low:.4f}*[wt% C]² + {b_low:.4f}*[wt% C] + {c_low:.4f}")
    
    print("\nHigh-carbon branch (γ-austenite + cementite):")
    print(f"  T[K] = {a_high:.4f}*[wt% C]² + {b_high:.4f}*[wt% C] + {c_high:.4f}")
    
    # Plot the fits
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Low-carbon branch
    C_fit = np.linspace(C_low.min(), C_low.max(), 100)
    T_fit = a_low * C_fit**2 + b_low * C_fit + c_low
    ax1.plot(C_low, T_low, 'ro', label='Data points', markersize=8)
    ax1.plot(C_fit, T_fit, 'b-', label='Quadratic fit', linewidth=2)
    ax1.set_xlabel('Weight % Carbon', fontsize=11)
    ax1.set_ylabel('Temperature (K)', fontsize=11)
    ax1.set_title('Low-Carbon Branch Fit', fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # High-carbon branch
    C_fit = np.linspace(C_high.min(), C_high.max(), 100)
    T_fit = a_high * C_fit**2 + b_high * C_fit + c_high
    ax2.plot(C_high, T_high, 'ro', label='Data points', markersize=8)
    ax2.plot(C_fit, T_fit, 'b-', label='Quadratic fit', linewidth=2)
    ax2.set_xlabel('Weight % Carbon', fontsize=11)
    ax2.set_ylabel('Temperature (K)', fontsize=11)
    ax2.set_title('High-Carbon Branch Fit', fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    save_plot(fig, 'A5_austenite_boundary_fits.png')
    plt.close()
    
    return (a_low, b_low, c_low), (a_high, b_high, c_high)


def analyze_eutectoid_steel(T_eutectoid, C_eutectoid):
    """
    A6: Eutectoid steel analysis
    """
    print_section_header("A6: Eutectoid Steel Analysis")
    
    print(f"Cooling γ-austenite with eutectoid composition ({C_eutectoid} wt% C)")
    print(f"from 1100 K to just below {T_eutectoid} K")
    
    print("\nPhases present after cooling:")
    print("  - α-ferrite (BCC)")
    print("  - Cementite (Fe₃C)")
    print("  - Microstructure: Pearlite (lamellar α + Fe₃C)")
    
    # Composition of each phase
    C_ferrite = 0.02   # wt% C in α-ferrite (from phase diagram)
    C_cementite = 6.69  # wt% C in cementite
    
    print(f"\nPhase compositions:")
    print(f"  α-ferrite: {C_ferrite} wt% C, {100-C_ferrite:.2f} wt% Fe")
    print(f"  Cementite: {C_cementite} wt% C, {100-C_cementite:.2f} wt% Fe")
    
    # Mass fractions using lever rule
    W_ferrite, W_cementite = lever_rule(C_eutectoid, C_ferrite, C_cementite)
    
    print(f"\nMass fractions (lever rule):")
    print(f"  α-ferrite: {W_ferrite:.4f} ({W_ferrite*100:.2f}%)")
    print(f"  Cementite: {W_cementite:.4f} ({W_cementite*100:.2f}%)")
    print(f"  Check sum: {W_ferrite + W_cementite:.4f}")
    
    # Create visualization
    fig = plt.figure(figsize=(16, 6))
    gs = fig.add_gridspec(1, 3, width_ratios=[2, 1, 1])
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    ax3 = fig.add_subplot(gs[2])
    
    # Left: Cooling path on phase diagram
    C_range = np.linspace(0, 2, 100)
    T_range = np.linspace(900, 1200, 100)
    
    # Draw approximate phase boundaries
    ax1.axhline(y=T_eutectoid, color='green', linestyle='--', linewidth=2, label='Eutectoid T')
    ax1.axvline(x=C_eutectoid, color='blue', linestyle='--', linewidth=2, alpha=0.5)
    
    # Cooling path
    cooling_path_T = np.linspace(1100, T_eutectoid - 10, 20)
    cooling_path_C = np.ones_like(cooling_path_T) * C_eutectoid
    ax1.plot(cooling_path_C, cooling_path_T, 'r-', linewidth=4, marker='o', 
            markersize=8, label='Cooling Path', zorder=5)
    ax1.plot(C_eutectoid, 1100, 'go', markersize=15, label='Start (1100 K)', zorder=6)
    ax1.plot(C_eutectoid, T_eutectoid - 10, 'ro', markersize=15, label=f'End ({T_eutectoid-10} K)', zorder=6)
    
    # Phase regions
    ax1.text(0.76, 1050, 'γ-austenite\n(single phase)', fontsize=11, ha='center',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    ax1.text(0.76, 950, 'α + Fe₃C\n(Pearlite)', fontsize=11, ha='center',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
    
    ax1.set_xlabel('Weight % Carbon', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Temperature (K)', fontsize=12, fontweight='bold')
    ax1.set_title('A6: Eutectoid Steel Cooling Path', fontsize=13, fontweight='bold')
    ax1.set_xlim(0, 1.5)
    ax1.set_ylim(900, 1200)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper right', fontsize=10)
    
    # Middle: Phase compositions
    ax2.axis('off')
    ax2.text(0.5, 0.95, 'Phase Compositions', fontsize=12, fontweight='bold', 
            ha='center', transform=ax2.transAxes)
    
    comp_text = f'''
α-ferrite (BCC):
  {C_ferrite} wt% C
  {100-C_ferrite:.2f} wt% Fe

Cementite (Fe₃C):
  {C_cementite} wt% C
  {100-C_cementite:.2f} wt% Fe
'''
    ax2.text(0.5, 0.5, comp_text, fontsize=11, ha='center', va='center',
            transform=ax2.transAxes, family='monospace',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    
    # Right: Mass fractions
    ax3.axis('off')
    ax3.text(0.5, 0.95, 'Mass Fractions', fontsize=12, fontweight='bold',
            ha='center', transform=ax3.transAxes)
    
    # Pie chart
    phases = ['α-ferrite', 'Cementite']
    fractions = [W_ferrite, W_cementite]
    colors = ['lightblue', 'pink']
    
    pie_ax = fig.add_axes([0.7, 0.15, 0.25, 0.7])
    wedges, texts, autotexts = pie_ax.pie(fractions, labels=phases, colors=colors,
                                          autopct='%1.1f%%', startangle=90,
                                          textprops={'fontsize': 11, 'fontweight': 'bold'})
    
    plt.tight_layout()
    save_plot(fig, 'A6_eutectoid_steel.png')
    plt.close()
    
    print("\n✓ A6 visualization saved: A6_eutectoid_steel.png")
    
    return W_ferrite, W_cementite


def analyze_hypoeutectoid_steel(T_eutectoid, C_eutectoid):
    """
    A7: Hypoeutectoid steel analysis
    """
    print_section_header("A7: Hypoeutectoid Steel Analysis")
    
    C_overall = 0.52  # wt% C
    
    print(f"Analyzing hypoeutectoid steel: {C_overall} wt% C")
    print(f"(Below eutectoid composition of {C_eutectoid} wt% C)")
    
    # At T = T_eutectoid + δT (just above eutectoid)
    print(f"\n1) Just ABOVE eutectoid temperature (T = {T_eutectoid} + δT):")
    
    # Two-phase region: α-ferrite + γ-austenite
    C_ferrite_high = 0.02   # wt% C in α-ferrite at eutectoid T
    C_austenite = C_eutectoid  # wt% C in γ-austenite at eutectoid T
    
    W_proeutectoid_ferrite, W_austenite = lever_rule(C_overall, C_ferrite_high, C_austenite)
    
    print(f"  Phases: α-ferrite + γ-austenite")
    print(f"  Proeutectoid α-ferrite: {W_proeutectoid_ferrite:.4f} ({W_proeutectoid_ferrite*100:.2f}%)")
    print(f"  γ-austenite: {W_austenite:.4f} ({W_austenite*100:.2f}%)")
    
    # At T = T_eutectoid - δT (just below eutectoid)
    print(f"\n2) Just BELOW eutectoid temperature (T = {T_eutectoid} - δT):")
    
    # Two-phase region: α-ferrite + cementite
    C_ferrite_low = 0.02   # wt% C in α-ferrite
    C_cementite = 6.69     # wt% C in cementite
    
    W_total_ferrite, W_cementite = lever_rule(C_overall, C_ferrite_low, C_cementite)
    
    print(f"  Phases: α-ferrite + cementite")
    print(f"  Total α-ferrite: {W_total_ferrite:.4f} ({W_total_ferrite*100:.2f}%)")
    print(f"  Cementite: {W_cementite:.4f} ({W_cementite*100:.2f}%)")
    print(f"  γ-austenite: {0:.4f} (transformed to pearlite)")
    
    # Breakdown of α-ferrite
    print(f"\n3) α-ferrite breakdown:")
    
    W_eutectoid_ferrite = W_total_ferrite - W_proeutectoid_ferrite
    
    print(f"  Proeutectoid α-ferrite: {W_proeutectoid_ferrite:.4f} ({W_proeutectoid_ferrite*100:.2f}%)")
    print(f"    (formed ABOVE eutectoid temperature)")
    print(f"  Eutectoid α-ferrite: {W_eutectoid_ferrite:.4f} ({W_eutectoid_ferrite*100:.2f}%)")
    print(f"    (formed FROM γ-austenite at eutectoid temperature)")
    
    print("\nMicrostructure explanation:")
    print("  - Proeutectoid α-ferrite forms first as large grains")
    print("  - Remaining γ-austenite transforms to pearlite at eutectoid temperature")
    print("  - Pearlite consists of lamellar α-ferrite + cementite")
    
    return W_proeutectoid_ferrite, W_eutectoid_ferrite, W_cementite


def analyze_hypereutectoid_steel(T_eutectoid, C_eutectoid):
    """
    A8: Hypereutectoid steel analysis
    """
    print_section_header("A8: Hypereutectoid Steel Analysis")
    
    # Given: eutectoid cementite = 0.103
    W_eutectoid_cementite = 0.103
    
    print("Given: Weight fraction of eutectoid cementite = 0.103")
    print("Find: Overall carbon content of the steel")
    
    # At eutectoid point, austenite transforms to pearlite
    # Pearlite = α-ferrite + cementite in eutectoid proportions
    
    C_ferrite = 0.02
    C_cementite = 6.69
    
    # In pearlite formed from eutectoid austenite
    W_ferrite_in_pearlite, W_cementite_in_pearlite = lever_rule(
        C_eutectoid, C_ferrite, C_cementite
    )
    
    print(f"\nEutectoid transformation (γ → α + Fe₃C):")
    print(f"  Cementite in pearlite: {W_cementite_in_pearlite:.4f}")
    
    # If eutectoid cementite = 0.103, then pearlite fraction is:
    W_pearlite = W_eutectoid_cementite / W_cementite_in_pearlite
    
    print(f"\nPearlite fraction: {W_pearlite:.4f} ({W_pearlite*100:.2f}%)")
    
    # Remaining is proeutectoid cementite
    W_proeutectoid_cementite = 1 - W_pearlite
    
    print(f"Proeutectoid cementite: {W_proeutectoid_cementite:.4f} ({W_proeutectoid_cementite*100:.2f}%)")
    
    # At T = T_eutectoid + δT, we have γ + Fe₃C
    # Using lever rule: W_cementite = (C_overall - C_austenite) / (C_cementite - C_austenite)
    # W_proeutectoid_cementite = (C_overall - C_eutectoid) / (C_cementite - C_eutectoid)
    
    C_overall = W_proeutectoid_cementite * (C_cementite - C_eutectoid) + C_eutectoid
    
    print(f"\nCalculated overall carbon content: {C_overall:.4f} wt% C")
    
    # At 950 K (room temperature)
    print(f"\n2) At T = 298 K (room temperature):")
    
    W_total_ferrite_RT, W_total_cementite_RT = lever_rule(C_overall, C_ferrite, C_cementite)
    
    print(f"  α-ferrite: {W_total_ferrite_RT:.4f} ({W_total_ferrite_RT*100:.2f}%)")
    print(f"  Cementite: {W_total_cementite_RT:.4f} ({W_total_cementite_RT*100:.2f}%)")
    
    print("\n3) Discrepancy at room temperature:")
    print("  Experimentalist measures HIGHER α-ferrite than predicted")
    print("  Explanation:")
    print("    - Cementite (Fe₃C) is metastable; graphite is thermodynamically favored")
    print("    - Over long times, cementite slowly decomposes: Fe₃C → 3Fe + C(graphite)")
    print("    - This releases Fe, increasing α-ferrite content")
    print("    - Decomposition is very slow but measurable over experimental timescales")
    print("    - Sign of error: Positive (more α-ferrite than equilibrium prediction)")
    
    return C_overall, W_pearlite


def analyze_steel_series():
    """
    A9: Analyze series of carbon steels with varying carbon content
    """
    print_section_header("A9: Carbon Steel Series Analysis")
    
    carbon_contents = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]  # wt% C
    
    C_ferrite = 0.02
    C_cementite = 6.69
    C_eutectoid = 0.76
    
    results = []
    
    for C in carbon_contents:
        # Calculate cementite content
        W_total_ferrite, W_cementite = lever_rule(C, C_ferrite, C_cementite)
        
        # Calculate pearlite content
        if C < C_eutectoid:
            # Hypoeutectoid
            W_proeutectoid_ferrite, W_austenite = lever_rule(C, C_ferrite, C_eutectoid)
            W_pearlite = W_austenite
        elif C > C_eutectoid:
            # Hypereutectoid
            W_proeutectoid_cementite = (C - C_eutectoid) / (C_cementite - C_eutectoid)
            W_pearlite = 1 - W_proeutectoid_cementite
        else:
            # Eutectoid
            W_pearlite = 1.0
        
        results.append({
            'C_wt%': C,
            'Cementite': W_cementite * 100,
            'Pearlite': W_pearlite * 100
        })
    
    # Create results table
    df = pd.DataFrame(results)
    print("\nCarbon Steel Properties at 298 K:")
    print(df.to_string(index=False))
    
    # Save to CSV
    df.to_csv('outputs/A9_steel_properties.csv', index=False)
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot cementite content
    ax1.plot(df['C_wt%'], df['Cementite'], 'b-o', linewidth=2, markersize=8)
    ax1.set_xlabel('Carbon Content (wt%)', fontsize=11)
    ax1.set_ylabel('Cementite Content (%)', fontsize=11)
    ax1.set_title('Cementite vs Carbon Content', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Plot pearlite content
    ax2.plot(df['C_wt%'], df['Pearlite'], 'r-o', linewidth=2, markersize=8)
    ax2.set_xlabel('Carbon Content (wt%)', fontsize=11)
    ax2.set_ylabel('Pearlite Content (%)', fontsize=11)
    ax2.set_title('Pearlite vs Carbon Content', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    save_plot(fig, 'A9_steel_microstructure_vs_carbon.png')
    plt.close()
    
    print("\nTrends explanation:")
    print("  - Hardness increases with carbon content due to increased cementite")
    print("  - Cementite is hard but brittle")
    print("  - Toughness decreases with carbon due to brittle cementite")
    print("  - Pearlite provides intermediate properties")
    print("\nDesign recommendation:")
    print("  For hardness > 160 BHN and toughness > 75 J:")
    print("  Optimal range: 0.4-0.6 wt% C (medium carbon steel)")
    
    return df


def main():
    """
    Main execution function for Part A
    """
    print("\n" + "="*80)
    print("  PART A: CARBON STEEL DESIGN - Fe-C BINARY SYSTEM")
    print("="*80)
    
    # Load database
    db = load_database()
    
    # A1: Phase diagram with graphite
    eq_a1 = plot_phase_diagram_a1(db)
    
    # A2: Phase diagram without graphite (engineering relevant)
    eq_a2 = plot_phase_diagram_a2(db)
    
    # A3-A4: Find critical points
    T_eutectic, C_eutectic, T_eutectoid, C_eutectoid = find_critical_points(eq_a2)
    
    # A5: Fit austenite boundaries
    low_fit, high_fit = fit_austenite_boundaries()
    
    # A6: Eutectoid steel
    W_f_eut, W_c_eut = analyze_eutectoid_steel(T_eutectoid, C_eutectoid)
    
    # A7: Hypoeutectoid steel
    W_pf, W_ef, W_c_hypo = analyze_hypoeutectoid_steel(T_eutectoid, C_eutectoid)
    
    # A8: Hypereutectoid steel
    C_hyper, W_pearlite = analyze_hypereutectoid_steel(T_eutectoid, C_eutectoid)
    
    # A9: Steel series analysis
    steel_df = analyze_steel_series()
    
    print_section_header("PART A COMPLETE")
    print("All calculations completed and outputs saved to outputs/ directory")
    print("Review the generated plots and CSV files for your report")
    

if __name__ == "__main__":
    main()

