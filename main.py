#!/usr/bin/env python3
"""Backward-compatible entry point for Cloudberry."""

import sys
import warnings

from cloudberry.cli import main

if __name__ == "__main__":
    warnings.warn(
        "python main.py is deprecated; use the cloudberry CLI instead",
        DeprecationWarning,
        stacklevel=1,
    )
    sys.exit(main())
