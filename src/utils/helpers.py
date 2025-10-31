from pathlib import Path
from typing import Optional


def ensure_directory(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_filename(filename: str) -> str:
    # Remove path separators and dangerous characters
    keepcharacters = (' ', '.', '_', '-')
    return "".join(
        c for c in filename 
        if c.isalnum() or c in keepcharacters
    ).strip()


def calculate_percentage(value: float, total: float) -> float:
    if total == 0:
        return 0.0
    return round((value / total) * 100, 2)