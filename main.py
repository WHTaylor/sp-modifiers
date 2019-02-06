import csv
import os.path
from datetime import datetime


def main():
    # The artemis list does not contain 'modified' information, and has <200 entries (?)
    inputs_with_headers = {"isis.csv": ["Modified", "Modified By"],
                           "hpl.csv": ["Modified", "Modified By"],
                           "lsf.csv": ["Modified", "Modified By"]}

    for (input_file_name, headers) in inputs_with_headers.items():
        # Modifiers is a list of tuples of the form (Date modified, modified by)
        modifiers = read_modifiers(input_file_name, headers)
        proposals_modified = count_proposals_modified_since(modifiers, datetime(2016, 1, 1))
        modifiers_ordered_by_count = order_by_int_value(proposals_modified)
        print('Facility: {}\nModifiers: {}'.format(input_file_name[:-4], modifiers_ordered_by_count))


def read_modifiers(input_file_name, header_names):
    input_file_location = os.path.join(os.curdir, "csv", input_file_name)
    date_index = -1
    modifier_index = -1
    modifiers = []

    with open(input_file_location) as input_file:
        reader = csv.reader(input_file)
        first_row = True
        for row in reader:
            if first_row:
                [date_index, modifier_index] = get_header_indexes(header_names, row)
                first_row = False
            else:
                modifiers.append((row[date_index], row[modifier_index]))
    return modifiers


def get_header_indexes(headers, row):
    return [row.index(header) for header in headers]


def count_proposals_modified_since(modifiers, date_threshold):
    modified_count = dict()
    for (date_string, modifier) in modifiers:
        date = datetime.strptime(date_string, "%d/%m/%Y %H:%M")
        if date > date_threshold:
            if modifier in modified_count.keys():
                modified_count[modifier] += 1
            else:
                modified_count[modifier] = 1
    return modified_count


def order_by_int_value(d):
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


if __name__ == "__main__":
    main()
