from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"
DOCS_DIR = PROJECT_ROOT / "docs"
SQL_DIR = PROJECT_ROOT / "sql"

RAW_DATA = DATA_DIR / "raw"
PROCESSED_DATA = DATA_DIR / "processed"

for directory in [
    RAW_DATA,
    PROCESSED_DATA,
    REPORTS_DIR,
    DASHBOARD_DIR,
    DOCS_DIR,
    SQL_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)