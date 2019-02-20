import json
import os.path


def entries_unique_to_one_list(field, lists):
    cache_folder = os.path.join(os.curdir, "data", "cache")
    filenames = [list_name + ".json" for list_name in lists]
    seen_at = dict()

    for filename in filenames:
        with open(os.path.join(cache_folder, filename), "r") as input_file:
            data = json.load(input_file)
            for entry in data:
                v = entry[field]
                if v in seen_at:
                    seen_at[v].append(filename)
                else:
                    seen_at[v] = [filename]

    return [(v, l[0][:-5]) for v, l in seen_at.items() if len(l) == 1]


if __name__ == "__main__":
    uniques = entries_unique_to_one_list("RB", ["ExperimentTeam", "ProposalInvestigators"])
    counts = dict()
    for (_, l) in uniques:
        if l in counts:
            counts[l] += 1
        else:
            counts[l] = 1
    print(counts)
