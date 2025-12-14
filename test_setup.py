"""
Quick test to verify pycalphad installation and dependencies
"""

import sys

def test_imports():
    """Test that all required packages can be imported"""
    print("Testing package imports...")
    print("-" * 60)
    
    packages = [
        ('numpy', 'np'),
        ('matplotlib.pyplot', 'plt'),
        ('pandas', 'pd'),
        ('scipy', None),
        ('pycalphad', None),
    ]
    
    all_good = True
    
    for pkg_name, alias in packages:
        try:
            if alias:
                exec(f"import {pkg_name} as {alias}")
            else:
                exec(f"import {pkg_name}")
            print(f"✓ {pkg_name:25s} - OK")
        except ImportError as e:
            print(f"✗ {pkg_name:25s} - FAILED: {e}")
            all_good = False
    
    print("-" * 60)
    return all_good


def test_pycalphad():
    """Test basic pycalphad functionality"""
    print("\nTesting pycalphad functionality...")
    print("-" * 60)
    
    try:
        from pycalphad import Database, variables as v
        import numpy as np
        
        # Create a minimal test database
        tdb_str = """
        ELEMENT FE BLANK 0.0 0.0 0.0 !
        ELEMENT C  BLANK 0.0 0.0 0.0 !
        PHASE TEST % 1 1.0 !
        CONSTITUENT TEST : FE,C : !
        """
        
        db = Database(tdb_str)
        print(f"✓ Database creation works")
        print(f"  Elements: {db.elements}")
        print(f"  Phases: {list(db.phases.keys())}")
        
        print("-" * 60)
        return True
        
    except Exception as e:
        print(f"✗ pycalphad test failed: {e}")
        print("-" * 60)
        return False


def test_plotting():
    """Test matplotlib functionality"""
    print("\nTesting matplotlib...")
    print("-" * 60)
    
    try:
        import matplotlib
        matplotlib.use('Agg')  # Non-interactive backend
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Create a simple plot
        fig, ax = plt.subplots()
        x = np.linspace(0, 10, 100)
        y = np.sin(x)
        ax.plot(x, y)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Test Plot')
        
        # Save to test outputs directory
        import os
        os.makedirs('outputs', exist_ok=True)
        fig.savefig('outputs/test_plot.png', dpi=100)
        plt.close()
        
        print(f"✓ Matplotlib works")
        print(f"  Test plot saved to: outputs/test_plot.png")
        print("-" * 60)
        return True
        
    except Exception as e:
        print(f"✗ Matplotlib test failed: {e}")
        print("-" * 60)
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  PYCALPHAD SETUP VERIFICATION")
    print("="*60 + "\n")
    
    print(f"Python version: {sys.version}")
    print(f"Python path: {sys.executable}\n")
    
    # Test imports
    imports_ok = test_imports()
    
    # Test pycalphad
    pycalphad_ok = test_pycalphad()
    
    # Test plotting
    plotting_ok = test_plotting()
    
    # Summary
    print("\n" + "="*60)
    print("  SUMMARY")
    print("="*60)
    
    if imports_ok and pycalphad_ok and plotting_ok:
        print("\n✓ ALL TESTS PASSED!")
        print("\nYou're ready to run the Thermo-Calc project!")
        print("\nNext steps:")
        print("  1. Run: python3 run_all.py")
        print("  2. Select option 3 to run both parts")
        print("  3. Review outputs in outputs/ directory")
        return 0
    else:
        print("\n✗ SOME TESTS FAILED")
        print("\nPlease check the error messages above and:")
        print("  1. Make sure all dependencies are installed")
        print("  2. Activate the virtual environment if using one")
        print("  3. Try: pip install -r requirements.txt")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)


