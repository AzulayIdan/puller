import os
import re
import logging
import requests
import html2text
from config import config
from datetime import datetime, time
from dbOperations import getNorads, getRelevantNorads

logging.basicConfig(level=logging.INFO)

norad_ids = getNorads()
relevant_norad_ids = getRelevantNorads()

def create_session():
    session = requests.Session()
    return session

def login(session: requests.Session):
    try:
        response = session.post(config["login_url"], data=config["credentials"])
        response.raise_for_status()

        if response.status_code == 200:
            logging.info("Login successful!")
            return True
        logging.error(f'Login failed. Status code: {response.status_code}')
        return False
    
    except requests.exceptions.ConnectionError:
        logging.error("A connection error occurred.")
    except requests.exceptions.Timeout:
        logging.error("The request timed out.")
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.TooManyRedirects:
        logging.error("Too many redirects.")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"An error occurred: {req_err}")
    
    return False


def find_satellite_name(text_content: str):
    satellite_name = ""
    whole_text_lines = text_content.split("\n")
    for whole_text_line in whole_text_lines:
        if whole_text_line.startswith("# "):
            satellite_name = whole_text_line.split("# ")[1]

    return satellite_name if satellite_name != "" else "unknown"

def write_tle_sets_into_text_file(tle_sets: list):
    folder_path = config["new_space_output_folder_path"]
    full_ny2o_file_path = os.path.join(folder_path, config["ny2o_output_file_name"] + ".TLE")

    with open(full_ny2o_file_path, "w") as f:
        f.write("[")
        tle_sets = [tle_set for tle_set in tle_sets if (len(str(tle_set[0][3]).strip()) > 0 and len(str(tle_set[0][4]).strip()) > 0)]
        for i in range(0, len(tle_sets)):
            tle_set = tle_sets[i]
            satellite = str(tle_set[2])
            first_tle_line = str(tle_set[0][3]).strip()
            second_tle_line = str(tle_set[0][4]).strip()
            f.write("{")
            f.write(f'"satellite": "{satellite}","line1":"{first_tle_line}","line2":"{second_tle_line}"')
            f.write("}")
            if i < len(tle_sets) - 1:
                f.write(",")
        f.write("]")

    f.close()
    logging.info(f'TLE objects written successfully into {full_ny2o_file_path}')

def extract_tle_sets_from_ny2o(session: requests.Session):
    pattern_for_finding_tle_start_text = r'Two Line Element Set(?:\s*\([^)]*\))*:\s*(.*)'
    pattern_for_finding_tle_start_text = re.compile(pattern_for_finding_tle_start_text, re.DOTALL)
    tle_sets = []
    for norad in norad_ids:
        data_response = session.get(f'{config["tle_objects_extraction_url"]}?s={norad}')
        logging.info(f"Parsing html page content for satellite with norad id {norad}...")
        html_content = data_response.text
        text_content = html2text.html2text(html_content)

        satellite_name = find_satellite_name(text_content=text_content)

        tle_data_matches = re.search(pattern_for_finding_tle_start_text, text_content)

        if tle_data_matches and norad in relevant_norad_ids:
            content_after_tle_set_line = tle_data_matches.group(1).strip()
            cleaned_text = re.sub(r'\n{2,}', '\n', content_after_tle_set_line)
            lines = cleaned_text.split('\n')
            tle_sets.append([lines, norad, satellite_name])
            logging.info(f"The lines are: ")
            logging.info(lines[3])
            logging.info(lines[4])
        else:
            logging.info("Phrase 'Two Line Element Set' not found in the text.")
    
    write_tle_sets_into_text_file(tle_sets=tle_sets)

def main():
    session = create_session()
    is_login_successful = login(session=session)
    if is_login_successful:
        extract_tle_sets_from_ny2o(session=session)

main()