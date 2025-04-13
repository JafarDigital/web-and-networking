from httpx import AsyncClient
from app.main import app
import pytest

@pytest.mark.asyncio
async def test_hello():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/graphql", json={"query": "{ hello }"})
    assert response.status_code == 200
    assert response.json()["data"]["hello"] == "Hello, GraphQL + FastAPI!"
