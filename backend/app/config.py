import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=dotenv_path)

ALLOWED_ORIGINS = [origin.strip()for origin in os.getenv("ALLOWED_ORIGINS", "").split(",")if origin.strip()]
DATABASE_URL: str = os.getenv("DATABASE_URL")
ADMIN_API_KEY = os.getenv("ADMIN_API_KEY")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

STEAM_API = "https://store.steampowered.com/api/appdetails"

HUBCAP_API = "https://hubcapmanifest.com/api/v1"
HUBCAP_APIKEY: str = os.getenv("HUBCAP_APIKEY")
HUBCAP_MANIFEST_API = "https://hubcapmanifest.com/api/v1/manifest/{app_id}"
MANIFESTHUB2_MANIFEST_API = "https://codeload.github.com/SSMGAlt/ManifestHub2/zip/refs/heads/{app_id}"