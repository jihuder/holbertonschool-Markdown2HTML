#!/usr/bin/python3
"""Markdown python file"""
import hashlib
import os
import re
import sys

if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>",
              file=sys.stderr)
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    # Aquí iría el código para convertir el archivo Markdown en HTML

    sys.exit(0)
