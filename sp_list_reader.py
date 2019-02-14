import requests
import os.path
import json
import xml.etree.ElementTree
from requests_ntlm import HttpNtlmAuth


def download_modified_data():
    headers = ["Modified", "ModifiedById"]
    for (list_name, facility) in get_all_list_names():
        list_done = False
        parsed_entries = []
        url = build_url(f"http://www.facilities.rl.ac.uk/{facility}/programme/_vti_bin/ListData.svc/{list_name}", headers)
        while not list_done:
            print(f'Requesting {url}')
            response = get_xml_list_selected_fields(url)
            parsed_response, next_page = parse(response)
            parsed_entries.extend(parsed_response)
            if next_page:
                url = next_page
            else:
                list_done = True
        write_to_file(parsed_entries, list_name)


def get_all_list_names():
    list_names = []
    with open(os.path.join(os.curdir, "data", "isis_list_names.txt"), "r") as isis_file:
        for line in isis_file:
            list_names.append((line.strip('\n'), "isis"))

    with open(os.path.join(os.curdir, "data", "clf_list_names.txt"), "r") as clf_file:
        for line in clf_file:
            list_names.append((line.strip('\n'), "clf"))

    return list_names


def build_url(base_url, parameters):
    if parameters:
        if "$skiptoken=" in base_url:
            base_url += "&"

        base_url += "?$select=" + ",".join(parameters)
    return base_url


def get_xml_list_selected_fields(url):
    response = request_session().get(url)
    return response.text


def request_session():
    session = requests.Session()
    session.auth = build_auth()
    return session


def build_auth():
    with open(os.path.join(os.curdir, "data", "auth.json")) as auth_file:
        auth_data = json.load(auth_file)
        return HttpNtlmAuth(auth_data['user'], auth_data['password'])


def parse(xml_string):
    next_page = None
    parsed_entries = []
    tree = xml.etree.ElementTree.fromstring(xml_string)
    for child in tree:
        if child.tag.endswith("entry"):
            parsed_entry = dict()
            for entry in child:
                if entry.tag.endswith("content"):
                    for content in entry:
                        for properties in content:
                            if not properties.tag.endswith("Title"):
                                s = properties.tag
                                parsed_entry[s[s.index("}") + 1:]] = properties.text
            parsed_entries.append(parsed_entry)
        elif child.tag.endswith("link"):
            if child.attrib["rel"] == "next":
                next_page = child.attrib["href"]

    return parsed_entries, next_page


def write_to_file(to_write, list_name):
    with open(os.path.join(os.curdir, "data", "cache", f"{list_name}.json"), 'w+') as out_file:
        json.dump(to_write, out_file)


if __name__ == "__main__":
    download_modified_data()
    # parsed_response = get_xml_list_selected_fields(f"http://www.facilities.rl.ac.uk/isis/programme/_vti_bin/ListData.svc/ProposalList",
    #                                                ["Modified", "ModifiedById"])
    # for entry in parsed_response:
    #     print(type(entry), entry)
    # exit()
    # list_names = get_all_list_names()
    # print(list_names)
    # for list_name in ["ConsumableCases", "ConsumableInvoices", "ProposalList", "ExperimentTeam", "FAPInstruments", "ProposalInvestigators"]:#list_names:
    #     parsed_response = get_xml_list_selected_fields(f"http://www.facilities.rl.ac.uk/isis/programme/_vti_bin/ListData.svc/{list_name}", ["Modified", "ModifiedById"])
    #     counter = 0
    #     for entry in parsed_response:
    #         counter += 1
    #     print(f'Received {counter} responses for {list_name}')
