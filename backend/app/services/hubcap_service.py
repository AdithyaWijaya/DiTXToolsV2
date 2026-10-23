import httpx
from sqlalchemy.orm import Session
from app.services.setting_service import get_setting
from app.config import HUBCAP_APIKEY, HUBCAP_MANIFEST_API

def get_hubcap_api_key(db: Session) -> str | None:
    setting = get_setting(db, "hubcap_api_key")
    if setting and setting.value:
        return setting.value

    return HUBCAP_APIKEY

async def download_hubcap_manifest(db: Session, app_id: int):
    hubcap_api_key = get_hubcap_api_key(db)

    if not hubcap_api_key:
        raise ValueError("Hubcap API key is not configured.")

    async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
        response = await client.get(
            HUBCAP_MANIFEST_API.format(app_id=app_id),
            headers={
                "Authorization": f"Bearer {hubcap_api_key}",
                "Accept": "application/zip, application/octet-stream, */*",
            },
        )

        return response