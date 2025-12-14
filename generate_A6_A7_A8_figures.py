"""
Generate enhanced figures for A6, A7, and A8 analyses
This script creates comprehensive visualizations for the report
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from utils import lever_rule, save_plot

# Constants
T_eutectoid = 1000  # K
C_eutectoid = 0.76  # wt%
C_ferrite = 0.02   # wt% C in α-ferrite
C_cementite = 6.69  # wt% C in cementite

def create_A7_hypoeutectoid_figure():
    """
    A7: Comprehensive hypoeutectoid steel analysis with cooling path
    """
    print("Generating A7: Hypoeutectoid Steel Analysis...")
    
    C_overall = 0.52  # wt% C
    
    # Calculate mass fractions
    # Above eutectoid
    W_proeutectoid_ferrite, W_austenite = lever_rule(C_overall, C_ferrite, C_eutectoid)
    
    # Below eutectoid
    W_total_ferrite, W_cementite = lever_rule(C_overall, C_ferrite, C_cementite)
    W_eutectoid_ferrite = W_total_ferrite - W_proeutectoid_ferrite
    
    # Create figure with 4 panels
    fig = plt.figure(figsize=(18, 10))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.2, 1], width_ratios=[1.5, 1, 1])
    
    # Panel 1: Phase diagram with cooling path
    ax1 = fig.add_subplot(gs[0, :])
    
    # Draw phase boundaries
    C_range = np.linspace(0, 1.5, 100)
    T_alpha_gamma = T_eutectoid + 200 - 180 * (C_range - 0.02)**2
    T_gamma_cem = T_eutectoid + 200 - 150 * (C_range - C_eutectoid)**2
    
    ax1.plot(C_range, T_alpha_gamma, 'b-', linewidth=2, label='α + γ boundary')
    ax1.plot(C_range, T_gamma_cem, 'r-', linewidth=2, label='γ + Fe₃C boundary')
    ax1.axhline(y=T_eutectoid, color='green', linestyle='--', linewidth=2, label=f'Eutectoid T = {T_eutectoid} K')
    
    # Cooling path with labeled points
    cooling_T = np.array([1075, T_eutectoid + 5, T_eutectoid - 5, 950])
    cooling_C = np.ones_like(cooling_T) * C_overall
    
    ax1.plot(cooling_C, cooling_T, 'k-', linewidth=4, zorder=5)
    ax1.plot(cooling_C[0], cooling_T[0], 'go', markersize=18, zorder=6, 
            markeredgecolor='darkgreen', markeredgewidth=2)
    ax1.plot(cooling_C[1], cooling_T[1], 'yo', markersize=18, zorder=6,
            markeredgecolor='orange', markeredgewidth=2)
    ax1.plot(cooling_C[2], cooling_T[2], 'ro', markersize=18, zorder=6,
            markeredgecolor='darkred', markeredgewidth=2)
    ax1.plot(cooling_C[3], cooling_T[3], 'mo', markersize=18, zorder=6,
            markeredgecolor='purple', markeredgewidth=2)
    
    # Labels for points
    ax1.text(C_overall + 0.08, cooling_T[0], 'd: Start\n1075 K\nγ-austenite', 
            fontsize=10, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    ax1.text(C_overall + 0.08, cooling_T[1], f'e: T={T_eutectoid}+ K\nα + γ', 
            fontsize=10, bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    ax1.text(C_overall + 0.08, cooling_T[2], f'f: T={T_eutectoid}- K\nα + Fe₃C', 
            fontsize=10, bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
    ax1.text(C_overall + 0.08, cooling_T[3], 'Final\n950 K\nα + Fe₃C', 
            fontsize=10, bbox=dict(boxstyle='round', facecolor='plum', alpha=0.8))
    
    # Phase region labels
    ax1.text(0.3, 1050, 'α + γ', fontsize=12, ha='center',
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
    ax1.text(1.0, 1050, 'γ + Fe₃C', fontsize=12, ha='center',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.6))
    ax1.text(C_eutectoid, 1150, 'γ-austenite', fontsize=12, ha='center',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.6))
    ax1.text(C_overall, 920, 'α + Fe₃C\n(Pearlite + Proeutectoid α)', fontsize=11, ha='center',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))
    
    ax1.set_xlabel('Weight % Carbon', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Temperature (K)', fontsize=13, fontweight='bold')
    ax1.set_title(f'A7: Hypoeutectoid Steel ({C_overall} wt% C) - Cooling Path',
                 fontsize=14, fontweight='bold')
    ax1.set_xlim(0, 1.5)
    ax1.set_ylim(900, 1200)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper right', fontsize=10)
    
    # Panel 2: Point d, e, f explanations
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.axis('off')
    
    explanation = f'''MICROSTRUCTURE EVOLUTION:

Point d (1075 K):
• Single phase: γ-austenite (FCC)
• All carbon dissolved in austenite
• Homogeneous microstructure

Point e (T = {T_eutectoid}+ K):
• Two phases: α-ferrite + γ-austenite
• Proeutectoid α-ferrite: {W_proeutectoid_ferrite*100:.1f}%
• γ-austenite: {W_austenite*100:.1f}%
• Large α grains nucleate and grow

Point f (T = {T_eutectoid}- K):
• Two phases: α-ferrite + cementite
• Total α-ferrite: {W_total_ferrite*100:.1f}%
• Cementite: {W_cementite*100:.1f}%
• γ transformed to pearlite (α + Fe₃C)

DIFFERENCE:
• Proeutectoid α: Forms ABOVE T_eutectoid
  → Large, blocky grains at grain boundaries
• Eutectoid α: Forms FROM γ at T_eutectoid
  → Fine lamellar structure in pearlite
'''
    
    ax2.text(0.05, 0.95, explanation, fontsize=10, ha='left', va='top',
            transform=ax2.transAxes, family='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Panel 3: Mass fractions above eutectoid
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.axis('off')
    ax3.set_title('Above Eutectoid\n(Point e)', fontsize=11, fontweight='bold')
    
    phases_above = ['Proeutectoid\nα-ferrite', 'γ-austenite']
    fractions_above = [W_proeutectoid_ferrite, W_austenite]
    colors_above = ['lightblue', 'lightgreen']
    
    pie1 = ax3.pie(fractions_above, labels=phases_above, colors=colors_above,
                   autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})
    
    # Panel 4: Mass fractions below eutectoid
    ax4 = fig.add_subplot(gs[1, 2])
    ax4.axis('off')
    ax4.set_title('Below Eutectoid\n(Point f)', fontsize=11, fontweight='bold')
    
    text_below = f'''Total α-ferrite: {W_total_ferrite*100:.1f}%
  • Proeutectoid: {W_proeutectoid_ferrite*100:.1f}%
  • Eutectoid: {W_eutectoid_ferrite*100:.1f}%

Cementite: {W_cementite*100:.1f}%
'''
    
    ax4.text(0.5, 0.5, text_below, fontsize=10, ha='center', va='center',
            transform=ax4.transAxes, family='monospace',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    
    plt.tight_layout()
    save_plot(fig, 'A7_hypoeutectoid_steel.png')
    plt.close()
    
    print("✓ A7 figure saved: A7_hypoeutectoid_steel.png")


def create_A8_hypereutectoid_figure():
    """
    A8: Comprehensive hypereutectoid steel analysis
    """
    print("\nGenerating A8: Hypereutectoid Steel Analysis...")
    
    # Given data
    W_eutectoid_cementite_given = 0.103
    
    # Calculate eutectoid cementite fraction in pearlite
    _, W_cem_in_pearlite = lever_rule(C_eutectoid, C_ferrite, C_cementite)
    
    # Calculate pearlite fraction
    W_pearlite = W_eutectoid_cementite_given / W_cem_in_pearlite
    W_proeutectoid_cementite = 1 - W_pearlite
    
    # Calculate overall carbon content
    C_overall = W_proeutectoid_cementite * (C_cementite - C_eutectoid) + C_eutectoid
    
    # At room temperature
    W_ferrite_RT, W_cementite_RT = lever_rule(C_overall, C_ferrite, C_cementite)
    
    # Create figure
    fig = plt.figure(figsize=(18, 10))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.2, 1])
    
    # Panel 1: Phase diagram with cooling path
    ax1 = fig.add_subplot(gs[0, :])
    
    C_range = np.linspace(0.5, 2.5, 100)
    T_alpha_gamma = T_eutectoid + 200 - 180 * (C_range - 0.02)**2
    T_gamma_cem = T_eutectoid + 200 - 150 * (C_range - C_eutectoid)**2
    
    ax1.plot(C_range, T_alpha_gamma, 'b-', linewidth=2, label='α + γ boundary')
    ax1.plot(C_range, T_gamma_cem, 'r-', linewidth=2, label='γ + Fe₃C boundary')
    ax1.axhline(y=T_eutectoid, color='green', linestyle='--', linewidth=2, label='Eutectoid T')
    ax1.axhline(y=298, color='blue', linestyle=':', linewidth=2, label='Room T (298 K)')
    
    # Cooling path
    cooling_T = np.array([1500, T_eutectoid + 5, T_eutectoid - 5, 298])
    cooling_C = np.ones_like(cooling_T) * C_overall
    
    ax1.plot(cooling_C, cooling_T, 'k-', linewidth=4, zorder=5)
    ax1.plot(cooling_C[0], cooling_T[0], 'go', markersize=16, zorder=6)
    ax1.plot(cooling_C[1], cooling_T[1], 'yo', markersize=16, zorder=6)
    ax1.plot(cooling_C[2], cooling_T[2], 'ro', markersize=16, zorder=6)
    ax1.plot(cooling_C[3], cooling_T[3], 'bo', markersize=16, zorder=6)
    
    ax1.text(C_overall + 0.15, 1500, f'Start\n{C_overall:.2f} wt% C', 
            fontsize=10, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    ax1.text(C_overall + 0.15, T_eutectoid + 50, 'Above eutectoid\nγ + Fe₃C', 
            fontsize=10, bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))
    ax1.text(C_overall + 0.15, 950, 'Below eutectoid\nα + Fe₃C', 
            fontsize=10, bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
    ax1.text(C_overall + 0.15, 550, 'Room temp\n298 K', 
            fontsize=10, bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
    
    ax1.set_xlabel('Weight % Carbon', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Temperature (K)', fontsize=13, fontweight='bold')
    ax1.set_title(f'A8: Hypereutectoid Steel ({C_overall:.3f} wt% C) - Cooling Path',
                 fontsize=14, fontweight='bold')
    ax1.set_xlim(0.5, 2.5)
    ax1.set_ylim(200, 1600)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper right', fontsize=10)
    
    # Panel 2: Calculation of overall carbon content
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.axis('off')
    ax2.set_title('Carbon Content Calculation', fontsize=12, fontweight='bold')
    
    calc_text = f'''GIVEN:
Eutectoid cementite = {W_eutectoid_cementite_given}

CALCULATION:
Cementite in pearlite:
  W_cem = {W_cem_in_pearlite:.4f}

Pearlite fraction:
  W_pearlite = {W_eutectoid_cementite_given}/{W_cem_in_pearlite:.4f}
  W_pearlite = {W_pearlite:.4f}

Proeutectoid cementite:
  W_pro_cem = 1 - {W_pearlite:.4f}
  W_pro_cem = {W_proeutectoid_cementite:.4f}

Overall carbon (lever rule):
  C = {W_proeutectoid_cementite:.4f}×({C_cementite}-{C_eutectoid})
      + {C_eutectoid}
  C = {C_overall:.4f} wt%
'''
    
    ax2.text(0.05, 0.95, calc_text, fontsize=9, ha='left', va='top',
            transform=ax2.transAxes, family='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # Panel 3: Pearlite fraction
    ax3 = fig.add_subplot(gs[1, 1])
    ax3.axis('off')
    ax3.set_title('Microstructure Fractions', fontsize=12, fontweight='bold')
    
    phases = ['Pearlite\n(eutectoid)', 'Proeutectoid\nCementite']
    fractions = [W_pearlite, W_proeutectoid_cementite]
    colors = ['lightyellow', 'pink']
    
    ax3.pie(fractions, labels=phases, colors=colors, autopct='%1.1f%%',
           startangle=90, textprops={'fontsize': 10})
    
    ax3.text(0.5, -0.15, f'Pearlite fraction DOES NOT change\nupon further cooling below eutectoid',
            ha='center', va='top', transform=ax3.transAxes, fontsize=9, style='italic',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    
    # Panel 4: Room temperature + discrepancy
    ax4 = fig.add_subplot(gs[1, 2])
    ax4.axis('off')
    ax4.set_title('Room Temperature Analysis', fontsize=12, fontweight='bold')
    
    rt_text = f'''AT 298 K (Equilibrium):
α-ferrite: {W_ferrite_RT*100:.2f}%
Cementite: {W_cementite_RT*100:.2f}%

EXPERIMENTAL DISCREPANCY:
Measured α > Predicted α

EXPLANATION:
• Fe₃C is METASTABLE
• Graphite is thermodynamically
  favored at room temperature
• Slow decomposition:
  Fe₃C → 3Fe + C(graphite)
• Releases Fe atoms
• Increases α-ferrite content
• Sign: POSITIVE ERROR
  (more α than predicted)
'''
    
    ax4.text(0.05, 0.95, rt_text, fontsize=9, ha='left', va='top',
            transform=ax4.transAxes, family='monospace',
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.8))
    
    plt.tight_layout()
    save_plot(fig, 'A8_hypereutectoid_steel.png')
    plt.close()
    
    print("✓ A8 figure saved: A8_hypereutectoid_steel.png")
    
    # Save summary data
    summary_data = f"""A8 HYPEREUTECTOID STEEL SUMMARY

Given: Eutectoid cementite fraction = {W_eutectoid_cementite_given}

Calculated Results:
- Overall carbon content: {C_overall:.4f} wt% C
- Pearlite fraction: {W_pearlite:.4f} ({W_pearlite*100:.2f}%)
- Proeutectoid cementite: {W_proeutectoid_cementite:.4f} ({W_proeutectoid_cementite*100:.2f}%)
- α-ferrite at 298 K: {W_ferrite_RT:.4f} ({W_ferrite_RT*100:.2f}%)
- Cementite at 298 K: {W_cementite_RT:.4f} ({W_cementite_RT*100:.2f}%)

Pearlite fraction upon further cooling: NO CHANGE
(Pearlite forms at eutectoid temperature and remains constant below)

Experimental discrepancy:
- Predicted α-ferrite: {W_ferrite_RT*100:.2f}%
- Measured α-ferrite: HIGHER (slight but statistically significant)
- Reason: Cementite decomposition (Fe₃C → 3Fe + C_graphite)
- Sign: Positive error (more α than equilibrium prediction)
"""
    
    with open('outputs/A8_hypereutectoid_summary.txt', 'w') as f:
        f.write(summary_data)
    
    print("✓ A8 summary saved: A8_hypereutectoid_summary.txt")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  GENERATING A7 AND A8 FIGURES")
    print("="*60)
    
    import os
    os.makedirs('outputs', exist_ok=True)
    
    create_A7_hypoeutectoid_figure()
    create_A8_hypereutectoid_figure()
    
    print("\n" + "="*60)
    print("  ALL FIGURES GENERATED SUCCESSFULLY!")
    print("="*60)
    print("\nGenerated files:")
    print("  - outputs/A7_hypoeutectoid_steel.png")
    print("  - outputs/A8_hypereutectoid_steel.png")
    print("  - outputs/A8_hypereutectoid_summary.txt")


