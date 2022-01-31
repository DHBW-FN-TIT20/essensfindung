import shutil
from pathlib import Path

PATH_GOOGLE = Path("./configuration/google_api.conf")
PATH_DB = Path("./configuration/db.conf")

if not PATH_GOOGLE.exists():
    shutil.copy("./configuration/example_google_api.conf", str(PATH_GOOGLE))
if not PATH_DB.exists():
    shutil.copy("./configuration/example_db.conf", str(PATH_DB))
