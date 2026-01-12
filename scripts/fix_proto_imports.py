#!/usr/bin/env python3
"""
Post-process generated protobuf files to fix import statements.
This script fixes absolute imports to relative imports where needed.
"""

import os
import re
import sys
from pathlib import Path


def fix_core_imports(file_path: Path) -> bool:
    """Fix imports in core package generated files."""
    content = file_path.read_text()
    original = content
    
    # Fix version_pb2 and session_pb2 imports to relative
    content = re.sub(
        r'^import version_pb2 as version__pb2',
        'from . import version_pb2 as version__pb2',
        content,
        flags=re.MULTILINE
    )
    content = re.sub(
        r'^import session_pb2 as session__pb2',
        'from . import session_pb2 as session__pb2',
        content,
        flags=re.MULTILINE
    )
    
    # Fix common_pb2 and error_pb2 imports to relative
    content = re.sub(
        r'^import common_pb2 as common__pb2',
        'from . import common_pb2 as common__pb2',
        content,
        flags=re.MULTILINE
    )
    content = re.sub(
        r'^import error_pb2 as error__pb2',
        'from . import error_pb2 as error__pb2',
        content,
        flags=re.MULTILINE
    )
    
    if content != original:
        file_path.write_text(content)
        return True
    return False


def fix_manager_imports(file_path: Path) -> bool:
    """Fix imports in manager package generated files."""
    content = file_path.read_text()
    original = content
    
    # Fix manager.* imports to relative imports
    content = re.sub(
        r'^from manager import (\w+) as (\w+)',
        r'from . import \1 as \2',
        content,
        flags=re.MULTILINE
    )
    
    # Fix common_pb2 imports to relative
    content = re.sub(
        r'^import common_pb2 as common__pb2',
        'from . import common_pb2 as common__pb2',
        content,
        flags=re.MULTILINE
    )
    
    # Fix error_pb2 imports to use core.encoders.proto.generated
    content = re.sub(
        r'^import error_pb2 as error__pb2',
        'from core.encoders.proto.generated import error_pb2 as error__pb2',
        content,
        flags=re.MULTILINE
    )
    
    if content != original:
        file_path.write_text(content)
        return True
    return False


def fix_btc_imports(file_path: Path) -> bool:
    """Fix imports in btc package generated files."""
    content = file_path.read_text()
    original = content
    
    # Fix btc.* imports to relative imports
    content = re.sub(
        r'^from btc import (\w+) as (\w+)',
        r'from . import \1 as \2',
        content,
        flags=re.MULTILINE
    )
    
    # Fix error_pb2 and common_pb2 imports to use core.encoders.proto.generated
    content = re.sub(
        r'^import error_pb2 as error__pb2',
        'from core.encoders.proto.generated import error_pb2 as error__pb2',
        content,
        flags=re.MULTILINE
    )
    content = re.sub(
        r'^import common_pb2 as common__pb2',
        'from core.encoders.proto.generated import common_pb2 as common__pb2',
        content,
        flags=re.MULTILINE
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
    
    pb2_files = list(directory.rglob("*_pb2.py"))
    
    for file_path in pb2_files:
        if package_type == "core":
            if fix_core_imports(file_path):
                print(f"Fixed imports in: {file_path}")
        elif package_type == "manager":
            if fix_manager_imports(file_path):
                print(f"Fixed imports in: {file_path}")
        elif package_type == "btc":
            if fix_btc_imports(file_path):
                print(f"Fixed imports in: {file_path}")


def main():
    if len(sys.argv) < 3:
        print("Usage: fix_proto_imports.py <directory> <package_type>")
        print("  package_type: core, manager, or btc")
        sys.exit(1)
    
    directory = Path(sys.argv[1])
    package_type = sys.argv[2]
    
    if package_type not in ["core", "manager", "btc"]:
        print(f"Error: Invalid package_type '{package_type}'. Must be 'core', 'manager', or 'btc'")
        sys.exit(1)
    
    process_directory(directory, package_type)
    print(f"Finished processing {package_type} package imports")


if __name__ == "__main__":
    main()
