#!/usr/bin/env python3
"""
Extract and re-export types from generated protobuf (pb2) files.
This script creates a types.py file that re-exports commonly used types from pb2 files.
"""
import os
import sys
import re
from pathlib import Path
from typing import Set, Dict, List, Tuple

ignore_files = ["types.py", "__init__.py", "common.py", "error.py"]


def throw_invalid_usage():
    print(
        "Invalid arguments. Usage: python extract_types.py <ROOT_FOLDER_PATH> <TYPES_FILE_PATH>"
    )
    sys.exit(1)


if len(sys.argv) != 3:
    throw_invalid_usage()

root_path = Path(sys.argv[1])
types_file_path = Path(sys.argv[2])


def smart_case_convert(name: str) -> str:
    """
    Convert uppercase enum/message names to PascalCase intelligently.
    Uses known mappings and intelligent word boundary detection.
    """
    # Known mappings for common patterns
    known_mappings = {
        'STATUS': 'Status',
        'COMMAND': 'Command',
        'MSG': 'Msg',
        'ERRORCMD': 'ErrorCmd',
        'ERRORTYPE': 'ErrorType',
        'DEVICEWAITINGON': 'DeviceWaitingOn',
        'DEVICEIDLESTATE': 'DeviceIdleState',
        'CMDSTATE': 'CmdState',
        'VERSION': 'Version',
        'CHUNKPAYLOAD': 'ChunkPayload',
        'CHUNKACK': 'ChunkAck',
        'SEEDGENERATIONSTATUS': 'SeedGenerationStatus',
        'COMMONERROR': 'CommonError',
        'WALLETNOTFOUND': 'WalletNotFound',
        'WALLETPARTIALSTATE': 'WalletPartialState',
        'CARDERROR': 'CardError',
        'USERREJECTION': 'UserRejection',
        'DATAFLOW': 'DataFlow',
        # Session types
        'SESSIONSTARTCMD': 'SessionStartCmd',
        'SESSIONSTARTREQUEST': 'SessionStartRequest',
        'SESSIONSTARTRESPONSE': 'SessionStartResponse',
        'SESSIONSTARTINITIATEREQUEST': 'SessionStartInitiateRequest',
        'SESSIONSTARTBEGINREQUEST': 'SessionStartBeginRequest',
        'SESSIONSTARTACKRESPONSE': 'SessionStartAckResponse',
        'SESSIONSTARTINITIATERESULTRESPONSE': 'SessionStartInitiateResultResponse',
        'SESSIONCLOSECMD': 'SessionCloseCmd',
        'SESSIONCLOSEREQUEST': 'SessionCloseRequest',
        'SESSIONCLOSERESPONSE': 'SessionCloseResponse',
        'SESSIONCLOSECLEARREQUEST': 'SessionCloseClearRequest',
        'SESSIONCLOSECLEARRESPONSE': 'SessionCloseClearResponse',
        # Version types
        'APPVERSIONCMD': 'AppVersionCmd',
        'APPVERSIONREQUEST': 'AppVersionRequest',
        'APPVERSIONRESPONSE': 'AppVersionResponse',
        'APPVERSIONINTIATEREQUEST': 'AppVersionInitiateRequest',
        'APPVERSIONRESULTRESPONSE': 'AppVersionResultResponse',
        'APPVERSIONITEM': 'AppVersionItem',
    }
    
    if name in known_mappings:
        return known_mappings[name]
    
    # Try to detect word boundaries using common prefixes and suffixes
    # Common suffixes
    suffixes = {
        'STATE': 'State',
        'TYPE': 'Type',
        'CMD': 'Cmd',
        'ERROR': 'Error',
        'REQUEST': 'Request',
        'RESPONSE': 'Response',
        'STATUS': 'Status',
        'ITEM': 'Item',
    }
    
    # Common prefixes/words
    common_words = [
        'SESSION', 'START', 'CLOSE', 'CLEAR', 'INITIATE', 'BEGIN', 'ACK', 'RESULT',
        'APP', 'VERSION', 'DEVICE', 'WALLET', 'CARD', 'USER', 'COMMON', 'CHUNK',
        'SEED', 'GENERATION', 'WAITING', 'IDLE', 'COMMAND', 'ERROR', 'PARTIAL',
        'NOT', 'FOUND', 'PAYLOAD', 'DATA', 'FLOW'
    ]
    
    # Try suffix matching first
    for suffix_key, suffix_value in suffixes.items():
        if name.endswith(suffix_key) and len(name) > len(suffix_key):
            prefix = name[:-len(suffix_key)]
            if prefix:
                # Split prefix into words
                words = []
                remaining = prefix
                while remaining:
                    found = False
                    for word in common_words:
                        if remaining.startswith(word):
                            words.append(word)
                            remaining = remaining[len(word):]
                            found = True
                            break
                    if not found:
                        # Take as one word if no match
                        words.append(remaining)
                        break
                
                if words:
                    prefix_converted = ''.join(w.capitalize() for w in words)
                    return prefix_converted + suffix_value
    
    # Fallback: try to split on common word boundaries
    words = []
    remaining = name
    while remaining:
        found = False
        for word in sorted(common_words, key=len, reverse=True):  # Try longer words first
            if remaining.startswith(word):
                words.append(word)
                remaining = remaining[len(word):]
                found = True
                break
        if not found:
            # Take remaining as one word
            if remaining:
                words.append(remaining)
            break
    
    if words:
        return ''.join(w.capitalize() for w in words)
    
    return name.capitalize()


def extract_types_from_pb2_file(file_path: Path) -> List[str]:
    """
    Extract type names from a pb2 file by parsing _globals references.
    Returns a list of type names in correct PascalCase.
    """
    types: List[str] = []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Extract from _globals['_TYPENAME'] patterns
        # These reference the enum and message types
        pattern = r"_globals\['_([A-Z][A-Z0-9_]*)'\]"
        matches = re.findall(pattern, content)
        
        seen_uppercase = set()
        for match in matches:
            # Convert to PascalCase using smart conversion
            type_name = smart_case_convert(match)
            if type_name and type_name not in types:
                types.append(type_name)
                seen_uppercase.add(match)
        
        # Also try AST parsing for any explicit class definitions
        try:
            import ast
            tree = ast.parse(content, filename=str(file_path))
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_name = node.name
                    if not class_name.startswith("_") and class_name[0].isupper():
                        if class_name not in types:
                            types.append(class_name)
        except Exception:
            pass
    
    except Exception as e:
        print(f"Warning: Could not parse {file_path}: {e}", file=sys.stderr)
    
    return sorted(set(types))


def generate_types_file(root_path: Path, types_file_path: Path) -> None:
    """Generate a types.py file that re-exports types from pb2 files."""
    imports: List[str] = []
    all_exports: Set[str] = set()
    
    # Find all pb2 files in the root_path
    pb2_files = list(root_path.rglob("*_pb2.py"))
    
    if not pb2_files:
        print(f"Warning: No pb2 files found in {root_path}", file=sys.stderr)
        types_file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(types_file_path, "w", encoding="utf-8") as f:
            f.write("# Generated by extract_types script\n# No pb2 files found\n\n__all__ = []\n")
        return
    
    # Group imports by file
    file_exports: Dict[str, List[str]] = {}
    
    for file_path in pb2_files:
        if file_path.name in ignore_files:
            continue
        
        module_name = file_path.stem
        exports = extract_types_from_pb2_file(file_path)
        
        if exports:
            # Determine import path - relative to root_path
            rel_dir = file_path.parent.relative_to(root_path)
            if str(rel_dir) == ".":
                import_path = f".{module_name}"
            else:
                import_path = f".{str(rel_dir).replace(os.sep, '.')}.{module_name}"
            
            file_exports[import_path] = exports
            all_exports.update(exports)
    
    # Generate import statements
    for import_path, exports in sorted(file_exports.items()):
        if exports:
            imports.append(f"from {import_path} import {', '.join(exports)}")
    
    # Generate the types.py file content
    content_lines = [
        "# Generated by extract_types script",
        "# Re-exports types from generated protobuf (pb2) files",
        "",
    ]
    
    if imports:
        content_lines.extend(imports)
        content_lines.append("")
        content_lines.append(f"__all__ = {sorted(list(all_exports))}")
    else:
        content_lines.append("# No types found to export")
        content_lines.append("__all__ = []")
    
    # Write the file (overwrite if it exists, as this is auto-generated)
    types_file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(types_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content_lines))
    
    print(f"Generated types file: {types_file_path} with {len(all_exports)} exports")


def run() -> None:
    """Main entry point."""
    root_path_obj = Path(root_path)
    types_file_path_obj = Path(types_file_path)
    
    if not root_path_obj.exists():
        print(f"Error: Root path does not exist: {root_path}", file=sys.stderr)
        sys.exit(1)
    
    generate_types_file(root_path_obj, types_file_path_obj)


if __name__ == "__main__":
    run()
