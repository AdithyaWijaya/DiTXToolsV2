from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from slowapi.errors import RateLimitExceeded
from app.config import BASE_DIR, ALLOWED_ORIGINS
from app.database import engine
from app.limiter import limiter
from app import models
from app.routers.admin_router import router as admin_router
from app.routers.api_router import router as api_router
from app.routers.bot_router import router as bot_router

models.Base.metadata.create_all(bind=engine)

app= FastAPI ()
app.state.limiter = limiter
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": f"Too many requests, please try again later. ({exc.detail})"},
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS or ["*"],
    allow_credentials=bool(ALLOWED_ORIGINS),
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"info": "OK"}

@app.get("/favicon.ico")
def favicon():
    return FileResponse(f"{BASE_DIR}/static/favicon.ico")

app.include_router(admin_router)

app.include_router(api_router)

app.include_router(bot_router)