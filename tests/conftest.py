import sys
import os

# Add the parent directory to the Python path so tests can import from the root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))