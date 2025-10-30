import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "login_url": os.getenv("LOGIN_URL"),
    "tle_objects_extraction_url": os.getenv("TLE_OBJECTS_EXTRACTION_URL"),
    "space_track_output_file_name": os.getenv("SPACE_TRACK_OUTPUT_FILE_NAME"),
    "new_space_output_folder_path": os.getenv("NEW_SPACE_OUTPUT_FOLDER_PATH"),
    "credentials": {
        "identity": os.getenv("EMAIL"),
        "password": os.getenv("PASSWORD")
    },
    "sleeping_time_in_seconds": os.getenv("SLEEPING_TIME_IN_SECONDS")
}