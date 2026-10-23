import httpx
from sqlalchemy.orm import Session
from app.services.hubcap_service import get_hubcap_api_key
from app.config import STEAM_API, HUBCAP_API

async def search_game(
    db: Session,
    query: str,
    limit: int = 20,
    appid: bool = False,
):
    hubcap_api_key = get_hubcap_api_key(db)

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            f"{HUBCAP_API}/search",
            headers={
                "Authorization": f"Bearer {hubcap_api_key}"
            },
            params={
                "q": query,
                "limit": limit,
                "appid": appid,
            },
        )

        return response
    
async def get_steam_game_data(app_id: str) -> dict | None:
    url = STEAM_API

    async with httpx.AsyncClient(
        timeout=15.0,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        },
    ) as client:
        response = await client.get(url, params={"appids": app_id, "cc": "us", "l": "en"})
        response.raise_for_status()

    raw = response.json()
    game_data = raw.get(str(app_id), {})
    if not game_data.get("success"):
        return None

    return game_data.get("data", {})

async def get_hubcap_game_status(db: Session, app_id: int):
    hubcap_api_key = get_hubcap_api_key(db)

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(
            f"{HUBCAP_API}/status/{app_id}",
            headers={
                "Authorization": f"Bearer {hubcap_api_key}"
            }
        )

        return response