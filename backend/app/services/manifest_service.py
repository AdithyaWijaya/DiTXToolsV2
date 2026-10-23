import httpx
from sqlalchemy.orm import Session
from app.services.hubcap_service import get_hubcap_api_key
from app.config import HUBCAP_MANIFEST_API, MANIFESTHUB2_MANIFEST_API

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

async def download_manifesthub2_manifest(app_id: int):
    async with httpx.AsyncClient(timeout=60, follow_redirects=True) as client:
        response = await client.get(
            MANIFESTHUB2_MANIFEST_API.format(app_id=app_id),
            headers={
                "Accept": "application/zip, application/octet-stream, */*",
            },
        )

        return response

async def download_manifest(db: Session, app_id: int, provider: str):
    if provider == "ManifestHub2":
        return await download_manifesthub2_manifest(app_id)

    return await download_hubcap_manifest(db, app_id)
