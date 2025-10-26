import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "login_url": os.getenv("LOGIN_URL"),
    "tle_objects_extraction_url": os.getenv("TLE_OBJECTS_EXTRACTION_URL"),
    "ny2o_output_file_name": os.getenv("NY2O_OUTPUT_FILE_NAME"),
    "new_space_output_folder_path": os.getenv("NEW_SPACE_OUTPUT_FOLDER_PATH"),
    "credentials": {
        "identity": os.getenv("EMAIL"),
        "password": os.getenv("PASSWORD")
    },
    "mongo_db_uri": os.getenv("MONGO_DB_URI"),
    "sleeping_time_in_seconds": os.getenv("SLEEPING_TIME_IN_SECONDS")
}