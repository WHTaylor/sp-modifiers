import csv
import os.path
from datetime import datetime
from typing import List, Dict, Tuple


def main():
    inputs_with_headers = {"isis.csv": ["Modified", "Modified By"],
                           "hpl.csv": ["Modified", "Modified By"],
                           "lsf.csv": ["Modified", "Modified By"],
                           "artemis.csv": ["Modified", "Modified By"]}

    for (input_file_name, headers) in inputs_with_headers.items():
        # Modifiers is a list of tuples of the form (Date modified, modified by)
        modifiers = read_modifiers(input_file_name, headers)
        proposals_modified = count_proposals_modified_since(modifiers, datetime(2017, 1, 1))
        proposals_modified = translate_names(proposals_modified)
        modifiers_ordered_by_count = order_by_int_value(proposals_modified)
        print_formatted(input_file_name[:-4], modifiers_ordered_by_count)


def read_modifiers(input_file_name: str, header_names: List[str]) -> List[Tuple[str, str]]:
    input_file_location = os.path.join(os.curdir, "csv", input_file_name)
    date_index = -1
    modifier_index = -1
    modifiers = []

    with open(input_file_location) as input_file:
        reader = csv.reader(input_file)
        first_row = True
        for row in reader:
            if first_row:
                (date_index, modifier_index) = get_header_indexes(header_names, row)
                first_row = False
            else:
                modifiers.append((row[date_index], row[modifier_index]))
    return modifiers


def get_header_indexes(headers: List[str], row: List[str]) -> Tuple[int, ...]:
    return tuple(row.index(header) for header in headers)


def count_proposals_modified_since(modifiers: List[tuple], date_threshold: datetime) -> Dict[str, int]:
    modified_count = dict()
    for (date_string, modifier) in modifiers:
        date = datetime.strptime(date_string, "%d/%m/%Y %H:%M")
        if date > date_threshold:
            if modifier in modified_count.keys():
                modified_count[modifier] += 1
            else:
                modified_count[modifier] = 1
    return modified_count


def translate_names(proposals_modified: Dict[str, int]) -> Dict[str, int]:
    known_names = get_replacement_names()
    facility_str_prefix = "(STFC,"

    translated_names_dict = dict()
    for name, count in proposals_modified.items():
        if facility_str_prefix in name:
            translated_names_dict[name[:name.index(facility_str_prefix)]] = count
        else:
            if name in known_names:
                translated_names_dict[known_names[name]] = count
            else:
                translated_names_dict[name] = count
    return translated_names_dict


def get_replacement_names():
    try:
        name_replacements = dict()
        with open("replacement_names.csv", "r") as replacements_file:
            reader = csv.reader(replacements_file)
            for line in reader:
                name_replacements[line[0]] = line[1]
        return name_replacements

    except FileNotFoundError:
        return []


def order_by_int_value(d: Dict[str, int]) -> List[Tuple[str, int]]:
    ordered = []
    while d.items():
        most = 0
        most_key = None
        for (modifier, number_modified) in d.items():
            if number_modified > most:
                most = number_modified
                most_key = modifier
        ordered.append((most_key, most))
        del d[most_key]
    return ordered


def print_formatted(facility, modifiers):
    print(f'Facility: {facility}\n')
    print('| User | Proposals last modified |')
    print('|------|-------------------------|')
    for (name, count) in modifiers:
        if ", " in name:
            name = name[name.index(", ") + 2:] + name[:name.index(",")]
        print('|{0: <20} | {1} |'.format(name, count))
    print('')


if __name__ == "__main__":
    main()
