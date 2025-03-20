"""
run_tests.py

A simple test runner that discovers and runs all tests in the 'tests' folder using pytest.
"""

import pytest
import sys

if __name__ == '__main__':
    sys.exit(pytest.main(["tests"]))
