import subprocess
import sys
from pathlib import Path


def test_backend_app_imports_from_backend_directory():
    repo_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "-c", "import app.main; print('ok')"],
        cwd=repo_root / "backend",
        text=True,
        capture_output=True,
        timeout=20,
    )

    assert result.returncode == 0, result.stderr
    assert "ok" in result.stdout
