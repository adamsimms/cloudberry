#!/usr/bin/env python3
"""Backward-compatible entry point for Cloudberry."""

import sys

from cloudberry.cli import main

if __name__ == "__main__":
    sys.exit(main())
