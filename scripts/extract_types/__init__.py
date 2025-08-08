#!/usr/bin/env python3
import os
import sys
import re
from tsort import t_sort
from typing import Dict, List

ignore_files = ['types.py', '__init__.py']


def throw_invalid_usage():
    print('Invalid arguments. Usage: python extract_types.py <ROOT_FOLDER_PATH> <TYPES_FILE_PATH>')
    sys.exit(1)


if len(sys.argv) != 3:
    throw_invalid_usage()

root_path = sys.argv[1]
interface_file_path = sys.argv[2]


def count_chars(s, c):
    return s.count(c)


global_interface_list: Dict[str, List[str]] = {}
global_enum_list: Dict[str, List[str]] = {}


def remember_interface(interface_list: Dict[str, List[str]]) -> None:
    global global_interface_list
    global_interface_list.update(interface_list)


def remember_enum(enum_list: Dict[str, List[str]]) -> None:
    global global_enum_list
    global_enum_list.update(enum_list)


def save_interfaces(parsed_interfaces: Dict[str, Dict[str, List[str]]], tsort_edges: List[List[str]]) -> None:
    sorted_keys = t_sort(tsort_edges)[::-1]

    interface_file_data = []
    enum_file_data = []

    for key in sorted_keys:
        if key in parsed_interfaces:
            interface_file_data.append('\n'.join(parsed_interfaces[key]['data']))

    for key in global_enum_list:
        enum_file_data.append('\n'.join(global_enum_list[key]))

    file_data = '\n\n'.join(enum_file_data) + '\n\n' + ''.join(interface_file_data)

    with open(interface_file_path, 'w') as f:
        f.write(file_data)


def parse_interfaces() -> None:
    parsed_interfaces: Dict[str, Dict[str, List[str]]] = {}
    interface_names: List[str] = list(global_interface_list.keys())
    original_interface_names: List[str] = [name[1:] for name in interface_names]
    interface_block: List[str] = []
    tsort_edges: List[List[str]] = []

    for interface_name in interface_names:
        lines = global_interface_list[interface_name]
        interface_block.append(lines[0])
        dependencies = []

        for i in range(1, len(lines) - 1):
            line = lines[i]
            is_modified = False

            for idx, inner_interface_name in enumerate(original_interface_names):
                pattern = rf"(\s*\w+\s*:\s*)({inner_interface_name})(\s*(?:\[.*?\])?(?:\s*\|\s*None)?)"
                match = re.search(pattern, line)

                if match:
                    is_modified = True
                    interface_idx = original_interface_names.index(inner_interface_name)
                    dependencies.append(interface_names[interface_idx])

                    if interface_name == interface_names[interface_idx]:
                        print(f"Warning: Cyclic dependency found: {interface_name} <=> {interface_names[interface_idx]}")
                    else:
                        tsort_edges.append([interface_name, interface_names[interface_idx]])

                    new_line = f"{match.group(1)}{interface_names[interface_idx]}{match.group(3)}"
                    interface_block.append(new_line)
                    break

            if not is_modified:
                interface_block.append(line)

        interface_block.append(lines[-1])
        interface_block.append('\n')

        parsed_interfaces[interface_name] = {
            'data': interface_block,
            'dependencies': dependencies
        }

        if len(interface_block) <= 3:
            interface_block.insert(0, "# Empty interface")

        interface_block = []

    save_interfaces(parsed_interfaces, tsort_edges)


def extract_interfaces_from_file(file_data: List[str]) -> None:
    interface_list: Dict[str, List[str]] = {}
    is_interface_open = False
    interface_name = ''
    interface_block: List[str] = []
    base_indent = 0

    interface_start_regex = r"^(\s*)@dataclass\s*$"
    class_regex = r"^(\s*)class\s+(\w+)\s*\(\s*betterproto\.Message\s*\):"

    for i, line in enumerate(file_data):
        if is_interface_open:
            if line.strip() == '':
                interface_block.append(line)
            elif line.strip() and len(line) - len(line.lstrip()) <= base_indent:
                interface_list[interface_name] = interface_block
                interface_name = ''
                interface_block = []
                is_interface_open = False
                if re.match(interface_start_regex, line) and i + 1 < len(file_data):
                    next_line = file_data[i + 1]
                    class_match = re.match(class_regex, next_line)
                    if class_match:
                        is_interface_open = True
                        base_indent = len(class_match.group(1))
                        interface_name = f"I{class_match.group(2)}"
                        interface_block.append(f"{class_match.group(1)}class {interface_name}:")
            else:
                interface_block.append(line)
        else:
            if re.match(interface_start_regex, line) and i + 1 < len(file_data):
                next_line = file_data[i + 1]
                class_match = re.match(class_regex, next_line)
                if class_match:
                    is_interface_open = True
                    base_indent = len(class_match.group(1))
                    interface_name = f"I{class_match.group(2)}"
                    interface_block.append(line)
                    interface_block.append(f"{class_match.group(1)}class {interface_name}:")

    if is_interface_open and interface_name:
        interface_list[interface_name] = interface_block

    remember_interface(interface_list)


def extract_enums_from_file(file_data: List[str]) -> None:
    enum_list: Dict[str, List[str]] = {}
    is_enum_open = False
    enum_name = ''
    enum_block: List[str] = []
    base_indent = 0

    enum_start_regex = r"^(\s*)@dataclass\s*$"
    class_regex = r"^(\s*)class\s+(\w+)\s*\(\s*betterproto\.Enum\s*\):"

    for i, line in enumerate(file_data):
        if is_enum_open:
            if line.strip() == '':
                enum_block.append(line)
            elif line.strip() and len(line) - len(line.lstrip()) <= base_indent:
                enum_list[enum_name] = enum_block
                enum_name = ''
                enum_block = []
                is_enum_open = False
                if re.match(enum_start_regex, line) and i + 1 < len(file_data):
                    next_line = file_data[i + 1]
                    class_match = re.match(class_regex, next_line)
                    if class_match:
                        is_enum_open = True
                        base_indent = len(class_match.group(1))
                        enum_name = class_match.group(2)
                        enum_block.append(line)
                        enum_block.append(next_line)
            else:
                enum_block.append(line)
        else:
            if re.match(enum_start_regex, line) and i + 1 < len(file_data):
                next_line = file_data[i + 1]
                class_match = re.match(class_regex, next_line)
                if class_match:
                    is_enum_open = True
                    base_indent = len(class_match.group(1))
                    enum_name = class_match.group(2)
                    enum_block.append(line)
                    enum_block.append(next_line)

    if is_enum_open and enum_name:
        enum_list[enum_name] = enum_block

    remember_enum(enum_list)


def extract_types_from_file(file_path: str) -> None:
    with open(file_path, 'r') as f:
        file_data = f.read().split('\n')

    extract_interfaces_from_file(file_data)
    extract_enums_from_file(file_data)


def extract_types(root_path: str) -> None:
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file in ignore_files:
                continue

            file_path = os.path.join(root, file)

            if not os.path.isfile(file_path) or not file_path.endswith('.py'):
                continue

            extract_types_from_file(file_path)


def run() -> None:
    extract_types(root_path)
    parse_interfaces()


if __name__ == "__main__":
    run()