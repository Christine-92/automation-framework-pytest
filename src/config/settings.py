
# reads .env file which is in .gitignore
import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# repo root: .../PythonProject
ROOT = Path(__file__).resolve().parents[2]
ENV = ROOT / ".env"

loaded = False
if ENV.exists():
    load_dotenv(ENV, override=True)     # load by absolute path
    loaded = True
else:
    # fallback: search upwards from CWD
    found = find_dotenv(usecwd=True)
    if found:
        load_dotenv(found, override=True)
        loaded = True


BASE_URL   = os.getenv("BASE_URL", "").strip()
USERNAME   = os.getenv("USERNAME", "").strip()
PASSWORD   = os.getenv("PASSWORD", "").strip()
ACCOUNT_ID = os.getenv("ACCOUNT_ID", "").strip()

if not (BASE_URL and USERNAME and PASSWORD and ACCOUNT_ID):
    raise RuntimeError("Missing envs. Ensure .env has BASE_URL/USERNAME/PASSWORD/ACCOUNT_ID.")

# minimal normalize
if not BASE_URL.startswith(("http://", "https://")):
    BASE_URL = "https://" + BASE_URL
BASE_URL = BASE_URL.rstrip("/")
ACCOUNT_ID = int(ACCOUNT_ID)

