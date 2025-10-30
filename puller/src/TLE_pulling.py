import os
import re
import logging
import requests
from datetime import datetime

from config import config

logging.basicConfig(level=logging.INFO)

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

def create_replaced_text(text: str):
    text = text.replace("TLE_LINE1", "line1")
    text = text.replace("TLE_LINE2", "line2")
    text = text.replace("OBJECT_NAME", "satellite")

    return text

def extract_tle_objects_from_space_track(session: requests.Session):
    data_response = session.get(config["tle_objects_extraction_url"])
    logging.info(len(str(data_response)))
    text = create_replaced_text(str(data_response.text[1:-1]))
    logging.info(len(str(text)))
    pattern = r'\{[^}]*\}'
    matches = re.findall(pattern, text)

    line_counter = 0

    folder_path = config["new_space_output_folder_path"]
    full_space_track_file_path = os.path.join(folder_path, config["space_track_output_file_name"] + ".TLE")

    with open(full_space_track_file_path, "w") as f:
        f.write("[")
        for i in range(0, len(matches)):
            fixed_match = str(matches[i])[1:-1].split(',')
            f.write("{")
            text_to_write = str(fixed_match)[1:-1]
            text_to_write = text_to_write.replace("'", "")
            f.write(text_to_write)
            f.write("}")
            if i < len(matches) - 1:
                f.write(",")
            line_counter += 1
        f.write("]")
    f.close()
    logging.info(f'TLE objects written successfully into {full_space_track_file_path}')
    logging.info(f'{full_space_track_file_path} contains {line_counter} lines.')

def main():
    session = create_session()
    is_login_successful = login(session=session)
    if is_login_successful:
        extract_tle_objects_from_space_track(session=session)

main()