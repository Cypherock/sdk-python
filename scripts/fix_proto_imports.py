#!/usr/bin/env python3
"""
Post-process generated protobuf files to fix import statements.
This script fixes absolute imports to relative imports where needed.
"""

import os
import re
import sys
from pathlib import Path


def fix_top_level_imports(file_path: Path) -> bool:
    """Fix imports in top level generated files."""
    content = file_path.read_text()
    original = content

    content = re.sub(
        r"^import (\w+)_pb2 as (\w+)__pb2",
        r"from . import \1_pb2 as \2__pb2",
        content,
        flags=re.MULTILINE,
    )

    if content != original:
        file_path.write_text(content)
        return True
    return False


def fix_package_level_imports(file_path: Path, package_name: str) -> bool:
    """Fix imports in package generated files."""
    content = file_path.read_text()
    original = content

    # Fix package_name.* imports to relative imports
    content = re.sub(
        f"^from {package_name} import (\w+) as (\w+)",
        r"from . import \1 as \2",
        content,
        flags=re.MULTILINE,
    )

    # Fix all other imports(importted from top-level files) to relative imports
    content = re.sub(
        r"^import (\w+)_pb2 as (\w+)__pb2",
        r"from .. import \1_pb2 as \2__pb2",
        content,
        flags=re.MULTILINE,
    )

    if content != original:
        file_path.write_text(content)
        return True
    return False


def process_directory(directory: Path, package_type: str):
    """Process all _pb2.py files in a directory."""
    if not directory.exists():
        print(f"Warning: Directory {directory} does not exist")
        return

    # first get the top level *_pb2.py files
    top_level_pb2_files = list(directory.glob("*_pb2.py"))
    for file_path in top_level_pb2_files:
        if fix_top_level_imports(file_path):
            print(f"Fixed imports in: {file_path}")

    # now get the package level *_pb2.py files
    package_level_pb2_files = list(directory.glob(f"{package_type}/*_pb2.py"))
    for file_path in package_level_pb2_files:
        if fix_package_level_imports(file_path, package_type):
            print(f"Fixed imports in: {file_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: fix_proto_imports.py <directory> <package_type>")
        print("  package_type: core, manager, or btc")
        sys.exit(1)

    directory = Path(sys.argv[1])
    package_type = sys.argv[2]

    process_directory(directory, package_type)
    print(f"Finished processing {package_type} package imports")


if __name__ == "__main__":
    main()
