"""Integration tests for CLI"""

import os
import subprocess
import sys
import pytest


pytestmark = pytest.mark.integration


@pytest.fixture
def env_setup():
    df = os.path.dirname(__file__)
    dic = {
        "script": os.path.join(df, "..", "bin", "cli.py"),
        "xs": os.path.join(df, "data", "X.s"),
        "ys": os.path.join(df, "data", "Y.s"),
        "xf": os.path.join(df, "data", "X.f"),
        "yf": os.path.join(df, "data", "Y.f"),
        "broken": os.path.join(df, "data", "broken.f"),
        "env": {**os.environ, "TGL_GENOME_LENGTH": "7"},  # set genome length for tests
    }
    return dic


@pytest.mark.parametrize(
    "f1,f2,out",
    [
        ("xf", "yf", "Correlation between functions: 0.9452853"),
        ("yf", "xf", "Correlation between functions: 0.9452853"),
        ("ys", "xs", "Overlap coverage between segments: 3"),
        ("xs", "ys", "Overlap coverage between segments: 3"),
        ("xf", "ys", "Average function value over segments: 12.0"),
        ("ys", "xf", "Average function value over segments: 12.0"),
    ],
)
def test_cli_f1_f2(env_setup, f1, f2, out):
    """Test CLI with two functions files"""
    result = subprocess.run(
        [sys.executable, env_setup["script"], env_setup[f1], env_setup[f2]],
        capture_output=True,
        text=True,
        env=env_setup["env"],
    )
    assert result.returncode == 0, f"CLI failed with return code {result.returncode}, stderr: {result.stderr}"
    output = result.stdout.strip()
    assert out in output, f"Expected '{out}', got '{output}'"


def test_cli_broken_file(env_setup):
    """Test CLI with a broken file to check error handling"""
    result = subprocess.run(
        [sys.executable, env_setup["script"], env_setup["broken"], env_setup["yf"]],
        capture_output=True,
        text=True,
        env=env_setup["env"],
    )
    assert result.returncode != 0, "CLI should have failed with a broken file"
    assert "Error parsing file" in result.stderr, f"Expected error message in stderr, got: {result.stderr}"
