from pathlib import Path

PATH_GOOGLE = Path("./configuration/google_api.conf")
PATH_DB = Path("./configuration/db.conf")

if not PATH_GOOGLE.exists():
    PATH_GOOGLE = Path("./configuration/example_google_api.conf")
if not PATH_DB.exists():
    PATH_DB = Path("./configuration/example_db.conf")
