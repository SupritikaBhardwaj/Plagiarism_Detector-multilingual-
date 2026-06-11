import pytest
from httpx import ASGITransport, AsyncClient

from backend.api.main import app


@pytest.mark.asyncio
async def test_health() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_compare_api() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/analysis/compare",
            json={
                "left": {"name": "a.py", "language": "python", "content": "def add(a,b):\n return a+b\n"},
                "right": {"name": "b.py", "language": "python", "content": "def sum(x,y):\n return x+y\n"},
                "enable_ai": True,
            },
        )
    assert response.status_code == 200
    assert response.json()["overall_similarity"] > 0.4


@pytest.mark.asyncio
async def test_compare_rejects_language_mismatch() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post(
            "/api/analysis/compare",
            json={
                "left": {"name": "a.cpp", "language": "python", "content": "#include <iostream>\nint main() { return 0; }\n"},
                "right": {"name": "b.cpp", "language": "python", "content": "#include <iostream>\nint main() { return 0; }\n"},
                "enable_ai": True,
            },
        )
    assert response.status_code == 422
    assert "language is set to python" in response.json()["detail"]
