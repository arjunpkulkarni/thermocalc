"""
Utility functions for thermodynamic calculations and phase diagram analysis
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from typing import Tuple, Dict, List


def find_eutectic_point(temp_grid, comp_grid, phases_present):
    """
    Find eutectic point in a phase diagram
    
    Parameters:
    -----------
    temp_grid : array-like
        Temperature grid
    comp_grid : array-like
        Composition grid
    phases_present : array-like
        3D array of phase presence
        
    Returns:
    --------
    tuple : (temperature, composition)
    """
    # Look for point where liquid + two solid phases meet
    # This is a simplified approach - actual implementation depends on data structure
    pass


def find_eutectoid_point(temp_grid, comp_grid, phases_present):
    """
    Find eutectoid point in a phase diagram
    Similar to eutectic but solid -> solid transformation
    """
    pass


def lever_rule(overall_comp: float, left_comp: float, right_comp: float) -> Tuple[float, float]:
    """
    Apply the lever rule to calculate phase fractions
    
    Parameters:
    -----------
    overall_comp : float
        Overall composition (wt%)
    left_comp : float
        Composition of left phase (wt%)
    right_comp : float
        Composition of right phase (wt%)
        
    Returns:
    --------
    tuple : (fraction_left, fraction_right)
    """
    if right_comp == left_comp:
        return 0.0, 0.0
    
    fraction_right = (overall_comp - left_comp) / (right_comp - left_comp)
    fraction_left = 1.0 - fraction_right
    
    return fraction_left, fraction_right


def quadratic_fit(x_data: np.ndarray, y_data: np.ndarray) -> Tuple[float, float, float]:
    """
    Perform quadratic least-squares fit: y = a*x^2 + b*x + c
    
    Parameters:
    -----------
    x_data : array
        Independent variable data
    y_data : array
        Dependent variable data
        
    Returns:
    --------
    tuple : (a, b, c) coefficients
    """
    def quadratic(x, a, b, c):
        return a * x**2 + b * x + c
    
    popt, _ = curve_fit(quadratic, x_data, y_data)
    return tuple(popt)


def wt_to_mole_fraction(wt_fractions: Dict[str, float], molar_masses: Dict[str, float]) -> Dict[str, float]:
    """
    Convert weight fractions to mole fractions
    
    Parameters:
    -----------
    wt_fractions : dict
        Weight fractions of each element
    molar_masses : dict
        Molar masses of each element
        
    Returns:
    --------
    dict : Mole fractions
    """
    moles = {elem: wt / molar_masses[elem] for elem, wt in wt_fractions.items()}
    total_moles = sum(moles.values())
    return {elem: mol / total_moles for elem, mol in moles.items()}


def mole_to_wt_fraction(mole_fractions: Dict[str, float], molar_masses: Dict[str, float]) -> Dict[str, float]:
    """
    Convert mole fractions to weight fractions
    
    Parameters:
    -----------
    mole_fractions : dict
        Mole fractions of each element
    molar_masses : dict
        Molar masses of each element
        
    Returns:
    --------
    dict : Weight fractions
    """
    weights = {elem: mole * molar_masses[elem] for elem, mole in mole_fractions.items()}
    total_weight = sum(weights.values())
    return {elem: wt / total_weight for elem, wt in weights.items()}


def calculate_cementite_content(carbon_wt: float) -> float:
    """
    Calculate cementite (Fe3C) content from carbon weight percentage
    
    Cementite composition: Fe3C = 3*55.845 + 12.011 = 179.546 g/mol
    Carbon content in cementite: 12.011/179.546 = 6.69 wt%
    
    Parameters:
    -----------
    carbon_wt : float
        Carbon weight percentage in the steel
        
    Returns:
    --------
    float : Cementite weight percentage
    """
    carbon_in_cementite = 6.69  # wt% C in Fe3C
    return (carbon_wt / carbon_in_cementite) * 100


def format_composition(composition: Dict[str, float]) -> str:
    """
    Format composition dictionary as Fe-XXCr-YYC string
    
    Parameters:
    -----------
    composition : dict
        Composition dictionary with element keys
        
    Returns:
    --------
    str : Formatted composition string
    """
    fe = composition.get('FE', 0) * 100
    cr = composition.get('CR', 0) * 100
    c = composition.get('C', 0) * 100
    
    if cr > 0.01 and c > 0.001:
        return f"Fe-{cr:.2f}Cr-{c:.2f}C"
    elif c > 0.001:
        return f"Fe-{c:.2f}C"
    else:
        return f"Fe-{fe:.2f}"


def save_plot(fig, filename: str, dpi: int = 300):
    """
    Save matplotlib figure to outputs directory
    
    Parameters:
    -----------
    fig : matplotlib.figure.Figure
        Figure to save
    filename : str
        Output filename
    dpi : int
        Resolution in dots per inch
    """
    import os
    os.makedirs('outputs', exist_ok=True)
    filepath = os.path.join('outputs', filename)
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
    print(f"Saved: {filepath}")


def print_section_header(title: str):
    """Print formatted section header"""
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


