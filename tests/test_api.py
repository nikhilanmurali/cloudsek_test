import pytest


@pytest.mark.asyncio
async def test_health(client):
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_post_invalid_url(client):
    response = await client.post(
        "/metadata",
        json={"url": "invalid"},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_invalid_url(client):
    response = await client.get(
        "/metadata",
        params={"url": "invalid"},
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_post_success(client, monkeypatch):

    async def mock_create_metadata(url):
        return {
            "_id": "fake",
            "url": url,
            "headers": {},
            "cookies": {},
            "page_source": "html",
        }

    monkeypatch.setattr(
        "app.api.metadata.create_metadata",
        mock_create_metadata,
    )

    response = await client.post(
        "/metadata",
        json={"url": "https://example.com/"},
    )

    assert response.status_code == 201
    assert response.json()["url"] == "https://example.com/"
    assert "_id" not in response.json()


@pytest.mark.asyncio
async def test_post_fetch_failure(client, monkeypatch):

    async def mock_create_metadata(url):
        raise Exception("network failure")

    monkeypatch.setattr(
        "app.api.metadata.create_metadata",
        mock_create_metadata,
    )

    response = await client.post(
        "/metadata",
        json={"url": "https://example.com/"},
    )

    # If you changed to 502, update this to 502
    assert response.status_code in (400, 502)


@pytest.mark.asyncio
async def test_get_cache_hit(client, monkeypatch):

    async def mock_retrieve_metadata(url):
        return {
            "_id": "fake",
            "url": url,
            "headers": {},
            "cookies": {},
            "page_source": "html",
        }

    monkeypatch.setattr(
        "app.api.metadata.retrieve_metadata",
        mock_retrieve_metadata,
    )

    response = await client.get(
        "/metadata",
        params={"url": "https://example.com/"},
    )

    assert response.status_code == 200
    assert response.json()["url"] == "https://example.com/"
    assert "_id" not in response.json()


@pytest.mark.asyncio
async def test_get_cache_miss(client, monkeypatch):

    async def mock_retrieve_metadata(url):
        return None

    called = {"triggered": False}

    def mock_trigger_background(url):
        called["triggered"] = True

    monkeypatch.setattr(
        "app.api.metadata.retrieve_metadata",
        mock_retrieve_metadata,
    )

    monkeypatch.setattr(
        "app.api.metadata.trigger_background_collection",
        mock_trigger_background,
    )

    response = await client.get(
        "/metadata",
        params={"url": "https://example.com/"},
    )

    assert response.status_code == 202
    assert called["triggered"] is True
