#!/usr/bin/env python3
"""Prints LICENSE_OK ... or LICENSE_PROBLEM: <plain message> (exit 1). Used by the health check and the router skill."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); import license as L
try: p = L.require(); s = L.status(); print("LICENSE_OK " + s["message"])
except L.LicenseError as e: print("LICENSE_PROBLEM: " + str(e)); sys.exit(1)
