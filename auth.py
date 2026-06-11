from fastapi import APIRouter, HTTPException

from backend.auth.security import create_access_token
from backend.models.schemas import LoginRequest, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest) -> TokenResponse:
    # Demo auth for the B.Tech project scaffold. Replace with a user repository.
    if not payload.username or not payload.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(payload.username))

