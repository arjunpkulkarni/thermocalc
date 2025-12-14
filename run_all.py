"""
Master script to run complete Thermo-Calc project
Executes both Part A (Carbon Steel) and Part B (Stainless Steel)
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_banner(text):
    """Print formatted banner"""
    print("\n" + "="*80)
    print(f"  {text}")
    print("="*80 + "\n")


def check_dependencies():
    """Check if required packages are installed"""
    print_banner("Checking Dependencies")
    
    required = ['pycalphad', 'numpy', 'matplotlib', 'scipy', 'pandas']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - NOT FOUND")
            missing.append(package)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("\nAll dependencies satisfied!")
    return True


def main():
    """
    Main execution
    """
    print_banner("THERMO-CALC PROJECT: CARBON AND STAINLESS STEEL DESIGN")
    print("Using pycalphad for computational thermodynamics")
    print("Author: Engineering Design Module 3")
    
    # Check dependencies
    if not check_dependencies():
        print("\nPlease install dependencies before continuing.")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Import after dependency check
    import part_a_carbon_steel
    import part_b_simplified as part_b_stainless_steel
    
    # Menu
    print_banner("Select Analysis")
    print("1. Part A: Carbon Steel Design (Fe-C Binary System)")
    print("2. Part B: Stainless Steel Design (Fe-Cr-C Ternary System)")
    print("3. Run Both Parts")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == '1':
        print_banner("Running Part A: Carbon Steel Design")
        part_a_carbon_steel.main()
        
    elif choice == '2':
        print_banner("Running Part B: Stainless Steel Design")
        part_b_stainless_steel.main()
        
    elif choice == '3':
        print_banner("Running Complete Project")
        
        # Part A
        part_a_carbon_steel.main()
        
        # Part B
        part_b_stainless_steel.main()
        
        print_banner("PROJECT COMPLETE")
        print("All calculations finished successfully!")
        print("\nResults Location:")
        print("  - Plots: outputs/*.png")
        print("  - Data: outputs/*.csv")
        print("  - Databases: *.tdb")
        
        print("\nNext Steps:")
        print("  1. Review plots in outputs/ directory")
        print("  2. Examine calculation results in CSV files")
        print("  3. Compile findings into your report")
        print("  4. Submit to PrairieLearn and GradeScope")
        
    elif choice == '4':
        print("Exiting...")
        sys.exit(0)
        
    else:
        print("Invalid choice. Please run again.")
        sys.exit(1)


if __name__ == "__main__":
    main()

