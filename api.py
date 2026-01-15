import defines
import database
import requests
import json
import time
from datetime_management import convert_to_timestamp

API_URL = "https://www.smwcentral.net/ajax.php"


def get_section_list(page=1, moderated=True, game="SMW"):
    if game not in defines.Games:
        raise Exception("Invalid game specified for the API request.")

    hack_list = []
    request_parameters = {
        "a": "getsectionlist",
        "s": defines.Games[game],
        "u": 0 if moderated else 1,
        "n": 1 if page < 1 else page
    }
    section_response = make_request(request_parameters)
    section_data = json.loads(section_response.text)

    for hack_data in section_data['data']:
        hack = defines.SMWHackInfo()

        hack.id = hack_data['id']
        hack.title = hack_data['name']
        hack.authors = str([author['name'] for author in hack_data['authors']])
        hack.exits = hack_data['raw_fields']['length']
        hack.difficulty = hack_data['fields']['difficulty']
        hack.type = str(hack_data['raw_fields']['type'])
        hack.hall_of_fame = hack_data['raw_fields']['hof']
        hack.demo = hack_data['raw_fields']['demo']
        hack.sa_1 = hack_data['raw_fields']['sa1']
        hack.collab = hack_data['raw_fields']['collab']
        submission_dates, acceptance_dates = get_hack_dates(hack.id)
        hack.submissions = str(submission_dates)
        hack.earliest_submission = submission_dates[-1]
        hack.latest_submission = submission_dates[0]
        hack.acceptances = str(acceptance_dates)
        if hack_data['moderated']:
            hack.earliest_acceptance = acceptance_dates[-1]
            hack.latest_acceptance = acceptance_dates[0]
        hack_list.append(hack)

    return hack_list


def get_file(file_id):
    request_parameters = {
        "a": "getfile",
        "v": 2,
        "id": file_id
    }
    file_response = make_request(request_parameters)

    return file_response


def make_request(parameters):
    response = requests.get(API_URL, parameters)

    while response.status_code != 200:
        if response.status_code == 429:
            # ("Rate limit exceeded. Waiting...")
            time.sleep(int(response.headers["Retry-After"]) + 1)
            response = requests.get(API_URL, parameters)
        else:
            print(f'Got unknown response code {response.status_code}. Exiting.')
            quit(1)

    return response


def get_hack_dates(hack_id):
    submission_list = []
    approval_list = []
    file_response = get_file(hack_id)
    file_data = json.loads(file_response.text)

    for version in file_data['versions']:
        version_id = version['id']
        queried_file_data = file_data

        if version_id != queried_file_data['id']:
            queried_file_data = json.loads(get_file(file_data['id']).text)

        if queried_file_data['moderated']:
            approval_list.append(queried_file_data['time'])

            submission_url = f"https://dl.smwcentral.net/{queried_file_data['id']}/*.*"
            submission_info = requests.head(submission_url, allow_redirects=True, headers={'Cookie': 'ageg=1'})

            try:
                submission_timestamp = convert_to_timestamp(str(submission_info.headers['last-modified']), "cloudflare")
            except KeyError:
                print(f"No last modified attribute for {queried_file_data['id']}. Skipping.")
                continue

            submission_list.append(submission_timestamp)
        else:
            submission_list.append(queried_file_data['time'])

    return submission_list, approval_list


def update_database():
    page = 1
    moderated_done = False
    unmoderated_done = False

    while not moderated_done or not unmoderated_done:
        if not moderated_done:
            hacks = get_section_list(page=page)
        else:
            hacks = get_section_list(page=page, moderated=False)
        hacks_to_insert = []

        for hack in hacks:
            hack_search = database.search_hack({'txt-id': str(hack.id)})

            if hack_search:
                if moderated_done:
                    unmoderated_done = True
                else:
                    moderated_done = True
                    page = 0
                break
            else:
                hacks_to_insert.append(hack)

        if hacks_to_insert:
            database.insert_smw_hacks(hacks_to_insert)

        page += 1

    return
