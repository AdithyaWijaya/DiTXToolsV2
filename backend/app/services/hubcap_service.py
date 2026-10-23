from sqlalchemy.orm import Session
from app.services.setting_service import get_setting
from app.config import HUBCAP_APIKEY

def get_hubcap_api_key(db: Session) -> str | None:
    setting = get_setting(db, "hubcap_api_key")
    if setting and setting.value:
        return setting.value

    return HUBCAP_APIKEY