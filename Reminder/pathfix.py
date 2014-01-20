import os
import sys

base_path = os.path.abspath(os.path.dirname(__file__))
print(base_path)
sys.path.append(os.path.join(base_path))