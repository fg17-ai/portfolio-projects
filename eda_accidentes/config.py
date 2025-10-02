from pathlib import Path

# Rutas base
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SRC_DIR = PROJECT_ROOT / "src"
VIS_DIR = PROJECT_ROOT / "visualizations"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

def get_project_root() -> Path:
    """Devuelve la ruta raíz del proyecto."""
    return str(PROJECT_ROOT)
def get_raw_data_dir() -> Path:
    """Devuelve la ruta del directorio de datos crudos."""
    return str(RAW_DATA_DIR)
def get_processed_data_dir() -> Path:
    """Devuelve la ruta del directorio de datos procesados."""
    return str(PROCESSED_DATA_DIR)
def get_src_dir() -> Path:
    """Devuelve la ruta del directorio src."""
    return str(SRC_DIR)
def get_vis_dir() -> Path:
    """Devuelve la ruta del directorio de visualizaciones."""
    return str(VIS_DIR)
def get_notebooks_dir() -> Path:
    """Devuelve la ruta del directorio de notebooks."""
    return str(NOTEBOOKS_DIR)
