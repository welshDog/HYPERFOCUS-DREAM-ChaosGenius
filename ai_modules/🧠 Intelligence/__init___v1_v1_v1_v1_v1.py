"""
🤖💎 BROski AI Module Package 💎🤖
The legendary BROski intelligence system for ChaosGenius
"""

__version__ = "1.0.0-broski"
__author__ = "BROski Team"

# Import the core BROski components
try:
    from .broski_core import *
except ImportError:
    # Fallback to root level import
    import os
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from broski_core import *

__all__ = ["BROskiCore", "BROskiUltraEngine"]
