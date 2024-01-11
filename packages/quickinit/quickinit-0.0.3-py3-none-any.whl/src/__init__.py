"""
quickinit - Quick scaffolding for coding projects
Usage: 
    import quickinit
    quickinit.main()

Requirements:
    inquirer
"""

import sys
import importlib

required = {"inquirer"}
missing = [] 
for package in required:
    try: 
        importlib.import_module(package) 
    except ImportError:  
        missing.append(package)
        
if missing:
   print(f"Missing required dependencies: {missing}")
   sys.exit(1)
   
__version__ = "0.0.2" 

