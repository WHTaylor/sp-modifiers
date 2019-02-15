import os.path
import json
from datetime import datetime
from main import order_by_int_value, get_replacement_names


def modifications_per_list():
    cache_folder = os.path.join(os.curdir, "data", "cache")
    for filename in os.listdir(cache_folder):
        list_modifications = dict()
        with open(os.path.join(cache_folder, filename), "r") as input_file:
            data = json.load(input_file)
            for entry in data:
                date = datetime.strptime(entry["Modified"], "%Y-%m-%dT%H:%M:%S")
                if date > datetime(2017, 1, 1):
                    if entry["ModifiedById"] in list_modifications:
                        list_modifications[entry["ModifiedById"]] += 1
                    else:
                        list_modifications[entry["ModifiedById"]] = 1
        ordered = order_by_int_value(list_modifications)
        translated_names = translate_names(ordered)
        print_formatted(translated_names, filename)
        print("\n")


def combine_cached_data():
    combined = dict()
    cache_folder = os.path.join(os.curdir, "data", "cache")
    for filename in os.listdir(cache_folder):
        with open(os.path.join(cache_folder, filename), "r") as input_file:
            data = json.load(input_file)
            for entry in data:
                date = datetime.strptime(entry["Modified"], "%Y-%m-%dT%H:%M:%S")
                if date > datetime(2017, 1, 1):
                    if entry["ModifiedById"] in combined:
                        combined[entry["ModifiedById"]] += 1
                    else:
                        combined[entry["ModifiedById"]] = 1
    ordered = order_by_int_value(combined)
    translated_names = translate_names(ordered)
    for name, count in translated_names:
        print(name, count)


def translate_names(modifier_counts):
    named_modifiers = replace_ids_with_names(modifier_counts)
    known_names = get_replacement_names()
    translated = []
    for name, count in named_modifiers:
        replacement_name = name
        if name in known_names:
            replacement_name = known_names[name]

        replacement_name = replacement_name.replace("(STFC,RAL,ISIS)", "")
        replacement_name = replacement_name.replace("(STFC,RAL,CLF)", "")
        translated.append((replacement_name, count))

    return translated


def replace_ids_with_names(modifier_counts):
    ids = [id for (id, _) in modifier_counts]
    names = dict()
    with open(os.path.join(os.curdir, "data", "sp_users.json")) as input_file:
        data = json.load(input_file)
        for entry in data:
            if entry["Id"] in ids:
                names[entry["Id"]] = entry["Name"]
    return [(names[id], count) for (id, count) in modifier_counts]


def print_formatted(translated_names, filename):
    print(filename[:-5])
    print("\n| User | modifications")
    print("|--------|-------------|")
    for name, count in translated_names:
        print(f'| {name} | {count} |')


if __name__ == "__main__":
    # combine_cached_data()
    modifications_per_list()
