import defines
import database
import requests
from bs4 import BeautifulSoup
import re

from datetime_management import convert_to_timestamp

smwc_url = "https://smwcentral.net"
blank_db = False


def scrape_hacks(page=1, total_hacks=0, moderated=True, game="SMW"):
    hack_list = []
    most_recent_hack = database.get_most_recent_hack()
    if game not in defines.Games:
        raise Exception("Invalid game specified in scrape.py")
    request_parameters = {
        "p": "section",
        "s": defines.Games[game],
        "u": 0 if moderated else 1,
        "n": 1 if page < 1 else page
    }
    smwc_page = requests.get(smwc_url, request_parameters)
    smwc_soup = BeautifulSoup(smwc_page.text, "html.parser")
    base_hack_data = smwc_soup.find_all("td", {"class": "text"})  # Get the table containing hacks
    latest_hack = database.get_most_recent_hack()
    for hack_data in base_hack_data:
        hack = defines.SMWHackInfo()
        # TODO: Add support for non-SMW titles
        basic_info = hack_data.a  # The basic info includes hack ID, title, and acceptance/upload date
        if not basic_info:
            raise Exception("Could not get basic hack information. Try again later.")
        secondary_info = hack_data.find_next_siblings("td")  # Secondary info includes everything else
        if not secondary_info:
            raise Exception("Could not get secondary hack information. Try again later.")
        hack.id = re.findall('[0-9]+', basic_info['href'])[0]
        if int(hack.id) <= latest_hack:
            break
        hack.title = basic_info.text
        print(f"Getting information for hack {hack.title}")
        if moderated:
            submission_dates, acceptance_dates = get_hack_dates(hack.id)
            hack.submissions = str(submission_dates)
            hack.earliest_submission = submission_dates[-1]
            hack.latest_submission = submission_dates[0]
            hack.acceptances = str(acceptance_dates)
            hack.earliest_acceptance = acceptance_dates[-1]
            hack.latest_acceptance = acceptance_dates[0]
        else:
            submission_timestamp = convert_to_timestamp(str(hack_data.find_next('time')['datetime']), "smwc")
            hack.submissions = str([submission_timestamp])
            hack.earliest_submission = submission_timestamp
            hack.latest_submission = submission_timestamp

            if 'moderated' in basic_info.find_parent('td').text:  # We're looking for the "being moderated by" text
                moderator_attribute = basic_info.find_next('a')
                hack.moderator = moderator_attribute.text

        hack.demo = False if secondary_info[0].text == "No" else True
        hack.hall_of_fame = False if secondary_info[1].text == "No" else True
        hack.exits = re.findall('[0-9]+', secondary_info[2].text)[0]
        hack.difficulty = secondary_info[3].text
        hack.authors = str(secondary_info[4].text.split(', '))

        hack_list.append(hack)
    return hack_list


def get_hack_dates(hack_id):
    submission_list = []
    approval_list = []
    version_url = f"https://www.smwcentral.net/?p=section&a=versionhistory&id={hack_id}"

    version_page = requests.get(version_url)
    version_soup = BeautifulSoup(version_page.text, "html.parser")
    version_data = version_soup.find_all("tr")
    version_data.pop(0)  # Since we're pulling a table, we can drop the first element. It's just headings.
    for version in version_data:
        version_id = re.findall('[0-9]+', version.a["href"])[0]
        submission_url = f"https://dl.smwcentral.net/{version_id}/*.*"
        #  For some reason, this specific cookie is required for certain hacks. I don't know why.
        submission_info = requests.head(submission_url, allow_redirects=True, headers={'Cookie': 'ageg=1'})

        try:
            submission_timestamp = convert_to_timestamp(str(submission_info.headers['last-modified']), "cloudflare")
        except KeyError:
            print("No last modified attribute for {title}. Skipping.")
            continue
        approval_timestamp = convert_to_timestamp(version.find_next("time").text, "smwc")
        submission_list.append(submission_timestamp)
        approval_list.append(approval_timestamp)

    return submission_list, approval_list

