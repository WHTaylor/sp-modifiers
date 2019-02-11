import os.path
import csv
from typing import List, Tuple


def get_distinct_headers():
    filenames = ["isis.csv", "hpl.csv", "lsf.csv", "artemis.csv"]
    distinct_headers = set()

    for filename in filenames:
        distinct_headers.update([header for (header, facility) in headers(filename) if not to_ignore(header, facility)])

    print_formatted(sorted(distinct_headers))
    print(len(distinct_headers))


def headers(input_file_name: str,) -> List[Tuple[str, str]]:
    input_file_location = os.path.join(os.curdir, "csv", input_file_name)
    with open(input_file_location) as input_file:
        reader = csv.reader(input_file)
        row = reader.__next__()
        # We use the facility for looking up where headers come from (manually)
        return [(header, input_file_name[:-3]) for header in row]


def to_ignore(header, facility):
    u_case = header.upper()
    ignored_headers = ["PRINCIPAL INVESTIGATOR",  # All names and emails are to be removed
                       "EXPERIMENT_CONTACT",      # in favour of getting from UOWS with UN
                       "LOCAL_CONTACT",
                       "FACILITYAPP",             # In favour of including facility separately
                       "RBNO",                    # In favour of RB
                       "RATING_NO",               # In favour of RATING
                       "USER_NUMBER",             # In favour of UN
                       "TARGET_AREA_ALLOCATED",   # Artemis only, just says artemis with different capitalization

                       "PATH",                     # Think these are meta data? Can't see on actual lists
                       "ITEM TYPE",

                       "ID"
                       ]
    prefixes_to_ignore = ["APPNO",      # In favour of App (also removing AppNo to App... yeah that exists)
                          "EMAIL_"      # See explanation for PRINCIPAL INVESTIGATOR etc.
                          ]
    if u_case == "":    # For checking where specific headers come from
        print(facility)

    if u_case in ignored_headers:
        return True
    else:
        for prefix in prefixes_to_ignore:
            if u_case.startswith(prefix):
                return True
    return False


def print_formatted(headers):
    s = ""
    row_len = 12

    for i in range(len(headers)):
        s += headers[i]
        if i % row_len == row_len - 1:
            s += "\n"
        else:
            s += " - "
    print(s[:-3])


if __name__ == "__main__":
    get_distinct_headers()
