"""Test imports for Streamlit app."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

print("=== TEST DES IMPORTS ===")

# Test 1: Streamlit
try:
    import streamlit as st
    print("✅ streamlit importé")
except Exception as e:
    print(f"❌ streamlit : {e}")

# Test 2: Pandas
try:
    import pandas as pd
    print("✅ pandas importé")
except Exception as e:
    print(f"❌ pandas : {e}")

# Test 3: Numpy
try:
    import numpy as np
    print("✅ numpy importé")
except Exception as e:
    print(f"❌ numpy : {e}")

# Test 4: Plotly
try:
    import plotly.graph_objects as go
    print("✅ plotly importé")
except Exception as e:
    print(f"❌ plotly : {e}")

# Test 5: Config
try:
    from utils.config import Config
    print("✅ Config importé")
    print(f"Decision classes: {Config.DECISION_CLASSES}")
except Exception as e:
    print(f"❌ Config : {e}")

# Test 6: DataLoader
try:
    from data import DataLoader
    print("✅ DataLoader importé")
except Exception as e:
    print(f"❌ DataLoader : {e}")

# Test 7: DataPreprocessor
try:
    from data import DataPreprocessor
    print("✅ DataPreprocessor importé")
except Exception as e:
    print(f"❌ DataPreprocessor : {e}")

# Test 8: HybridModel
try:
    from models import HybridModel
    print("✅ HybridModel importé")
except Exception as e:
    print(f"❌ HybridModel : {e}")

# Test 9: SHAPExplainer
try:
    from xai import SHAPExplainer
    print("✅ SHAPExplainer importé")
except Exception as e:
    print(f"❌ SHAPExplainer : {e}")

# Test 10: LIMEExplainer
try:
    from xai import LIMEExplainer
    print("✅ LIMEExplainer importé")
except Exception as e:
    print(f"❌ LIMEExplainer : {e}")

# Test 11: CounterfactualExplainer
try:
    from xai import CounterfactualExplainer
    print("✅ CounterfactualExplainer importé")
except Exception as e:
    print(f"❌ CounterfactualExplainer : {e}")

# Test 12: ArgumentBuilder
try:
    from argumentation import ArgumentBuilder
    print("✅ ArgumentBuilder importé")
except Exception as e:
    print(f"❌ ArgumentBuilder : {e}")

# Test 13: ExplanationGenerator
try:
    from argumentation import ExplanationGenerator
    print("✅ ExplanationGenerator importé")
except Exception as e:
    print(f"❌ ExplanationGenerator : {e}")

print("\n=== FIN DES TESTS ===")
