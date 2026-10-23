import httpx
from typing import Literal
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse, Response
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services.steam_service import search_game, get_steam_game_data, get_hubcap_game_status
from app.services.manifest_service import download_manifest

router = APIRouter(prefix="/api",tags=["API"])

@router.get("/search")
async def search(
    q: str = Query(..., min_length=3),
    limit: int = Query(20, ge=1, le=100),
    appid: bool = False,
    db: Session = Depends(get_db),
):

    response = await search_game(db, q, limit, appid)

    if response.status_code == 200:
        return response.json()

    raise HTTPException(
        response.status_code,
        "Search failed."
    )

@router.get("/status/{app_id}")
async def manifest_status(
    app_id: int,
    db: Session = Depends(get_db),
):

    response = await get_hubcap_game_status(db, app_id)

    if response.status_code == 200:
        return response.json()

    if response.status_code == 404:
        raise HTTPException(
            404,
            "Game not found."
        )

    raise HTTPException(
        response.status_code,
        "Failed to fetch manifest status."
    )

@router.get("/steam/{app_id}")
async def get_steam_details(app_id: str):
    try:
        game_data = await get_steam_game_data(app_id)
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Steam API error: {e.response.text}",
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Failed to reach Steam: {str(e)}",
        )

    if game_data is None:
        raise HTTPException(status_code=404, detail="Game not found on Steam")

    return JSONResponse(content={
        "name":        game_data.get("name"),
        "headerImage": game_data.get("header_image"),
        "releaseDate": game_data.get("release_date", {}).get("date"),
        "genres":      [g["description"] for g in game_data.get("genres", [])],
        "description": game_data.get("short_description"),
        "developers":  game_data.get("developers", []),
        "publishers":  game_data.get("publishers", []),
    })

#GET
#/api/manifest/{app_id}?provider=hubcap|ManifestHub2
#Download a game manifest ZIP file. Counts toward your daily usage (hubcap only).
@router.get("/manifest/{app_id}")
async def download_manifest_endpoint(
    app_id: int,
    provider: Literal["hubcap", "ManifestHub2"] = Query("hubcap"),
    db: Session = Depends(get_db),
):
    try:
        response = await download_manifest(db, app_id, provider)
    except ValueError:
        raise HTTPException(
            401,
            "Hubcap API key is not configured."
        )
    except httpx.RequestError:
        raise HTTPException(
            502,
            f"Failed to reach {provider} manifest provider."
        )

    if response.status_code == 404:
        raise HTTPException(
            404,
            f"Manifest not found on {provider}."
        )

    if provider == "hubcap" and response.status_code in (401, 403):
        raise HTTPException(
            response.status_code,
            "Invalid Hubcap API key."
        )

    if response.status_code != 200:
        raise HTTPException(
            response.status_code,
            f"Failed to download manifest from {provider}."
        )

    return Response(
        content=response.content,
        media_type=response.headers.get("content-type", "application/zip"),
        headers={
            "Content-Disposition": f'attachment; filename="{app_id}.zip"',
        },
    )