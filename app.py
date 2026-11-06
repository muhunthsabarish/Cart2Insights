import sys
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STREAMLIT_DIR = ROOT / "streamlit"

sys.path.insert(0, str(STREAMLIT_DIR))

runpy.run_path(
    str(STREAMLIT_DIR / "app.py"),
    run_name="__main__"
)
