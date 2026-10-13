import asyncio
import base64
import json

import pytest
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)
PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 32
OK = {"furniture": [{"type": "sofa", "x": .5, "y": .6, "width": .3, "depth": .12, "rotation_deg": 0, "confidence": .8}], "warnings": ["oclusión parcial"]}
<<<<<<< HEAD
CATALOG = [{"id": "coffee-table", "name": "Mesa ratona", "category": "furniture", "tags": ["living-room", "table"]}]
CATALOG_RESULT = {"furniture": [{"asset_id": "coffee-table", "x": .5, "y": .6, "width": .3, "depth": .12, "rotation_deg": 0, "confidence": .8}], "warnings": []}


def post(data=PNG, mime="image/png", catalog=None, **form):
    if catalog is not None:
        form["catalog_json"] = json.dumps(catalog)
=======


def post(data=PNG, mime="image/png", **form):
>>>>>>> 718d31a2a94a0e4bc7c0a2070706df2b3a09ac24
    return client.post("/api/analyze-room", files={"image": ("r.png", data, mime)}, data=form)


def provider(payload=None, exc=None):
<<<<<<< HEAD
    async def fake(image, mime, catalog=None):
=======
    async def fake(image, mime):
>>>>>>> 718d31a2a94a0e4bc7c0a2070706df2b3a09ac24
        if exc: raise exc
        return payload
    return fake


def test_ok_uncalibrated(monkeypatch):
    monkeypatch.setattr(main, "analyze_with_provider", provider(OK))
    r = post(); assert r.status_code == 200
    j = r.json()
    assert j["calibration"] == {"status": "uncalibrated", "width_m": None}
    assert j["furniture"][0]["type"] == "sofa" and j["warnings"] == ["oclusión parcial"]
<<<<<<< HEAD
    assert "asset_id" not in j["furniture"][0]
=======
>>>>>>> 718d31a2a94a0e4bc7c0a2070706df2b3a09ac24


def test_ok_calibrated(monkeypatch):
    monkeypatch.setattr(main, "analyze_with_provider", provider(OK))
    assert post(known_width_m="4.5").json()["calibration"] == {"status": "user_provided", "width_m": 4.5}


@pytest.mark.parametrize("w", ["0", "-2", "500"])
def test_bad_calibration(w):
    r = post(known_width_m=w); assert r.status_code == 422 and r.json()["error"]["code"] == "invalid_calibration"


def test_bad_mime():
    r = post(mime="application/pdf"); assert r.status_code == 400 and r.json()["error"]["code"] == "invalid_file_type"


def test_too_large(monkeypatch):
    monkeypatch.setenv("MAX_IMAGE_BYTES", "10")
    r = post(); assert r.status_code == 413 and r.json()["error"]["code"] == "file_too_large"


def test_unreadable():
    r = post(data=b"no soy png"); assert r.status_code == 422 and r.json()["error"]["code"] == "image_unreadable"


def test_provider_not_configured(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    r = post(); assert r.status_code == 503 and r.json()["error"]["code"] == "provider_not_configured"


def test_gemini_request_and_response(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    captured = {}

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"candidates": [{"content": {"parts": [{"text": json.dumps(OK)}]}}]}

    class FakeClient:
        def __init__(self, timeout):
            assert timeout == 45

        async def __aenter__(self):
            return self

        async def __aexit__(self, *_):
            pass

        async def post(self, url, json, headers):
            captured.update(url=url, body=json, headers=headers)
            return FakeResponse()

    monkeypatch.setattr(main.httpx, "AsyncClient", FakeClient)
    result = asyncio.run(main.analyze_with_provider(PNG, "image/png"))

    assert result == OK
    assert captured["url"].endswith("/models/gemini-3.8-flash:generateContent")
    assert captured["headers"] == {"x-goog-api-key": "test-key"}
    parts = captured["body"]["contents"][0]["parts"]
    assert parts[1]["inlineData"] == {"mimeType": "image/png", "data": base64.b64encode(PNG).decode()}
    assert captured["body"]["generationConfig"]["responseMimeType"] == "application/json"
<<<<<<< HEAD
    response_schema = captured["body"]["generationConfig"]["responseSchema"]
    furniture_schema = response_schema["properties"]["furniture"]["items"]
    assert furniture_schema["properties"]["type"]["enum"] == [
        "sofa", "mesa", "silla", "estante", "cama", "planta", "tv"
    ]
    assert furniture_schema["required"] == [
        "type", "x", "y", "width", "depth", "rotation_deg", "confidence"
    ]
    assert response_schema["required"] == ["furniture", "warnings"]


def test_catalog_request_returns_only_catalog_asset_ids(monkeypatch):
    received = {}

    async def fake(image, mime, catalog=None):
        received["catalog"] = [option.model_dump() for option in catalog]
        return CATALOG_RESULT

    monkeypatch.setattr(main, "analyze_with_provider", fake)
    response = post(catalog=CATALOG)

    assert response.status_code == 200
    assert response.json()["furniture"][0]["asset_id"] == "coffee-table"
    assert "type" not in response.json()["furniture"][0]
    assert received["catalog"] == CATALOG


@pytest.mark.parametrize("catalog_json", ["{invalid", "[]", json.dumps([*CATALOG, *CATALOG])])
def test_invalid_catalog_is_rejected(catalog_json):
    response = client.post(
        "/api/analyze-room",
        files={"image": ("r.png", PNG, "image/png")},
        data={"catalog_json": catalog_json},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_catalog"


@pytest.mark.parametrize(
    "catalog_json",
    [
        json.dumps([{"id": f"item-{index}", "name": "Mueble", "category": "furniture"} for index in range(101)]),
        " " * (main.MAX_CATALOG_BYTES + 1),
        json.dumps([{**CATALOG[0], "tags": [f"tag-{index}" for index in range(11)]}]),
    ],
    ids=["too-many-options", "too-large", "too-many-tags"],
)
def test_catalog_limits_are_enforced(catalog_json):
    response = client.post(
        "/api/analyze-room",
        files={"image": ("r.png", PNG, "image/png")},
        data={"catalog_json": catalog_json},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_catalog"


def test_catalog_with_model_url_is_rejected():
    catalog = [{**CATALOG[0], "src": "https://example.invalid/model.glb"}]

    response = post(catalog=catalog)

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_catalog"


def test_provider_asset_id_outside_request_catalog_is_rejected(monkeypatch):
    result = {**CATALOG_RESULT, "furniture": [{**CATALOG_RESULT["furniture"][0], "asset_id": "invented-item"}]}
    monkeypatch.setattr(main, "analyze_with_provider", provider(result))

    response = post(catalog=CATALOG)

    assert response.status_code == 502
    assert response.json()["error"]["code"] == "provider_failure"


def test_provider_cannot_mix_legacy_type_with_catalog_asset_id(monkeypatch):
    result = {
        **CATALOG_RESULT,
        "furniture": [{**CATALOG_RESULT["furniture"][0], "type": "sofa"}],
    }
    monkeypatch.setattr(main, "analyze_with_provider", provider(result))

    response = post(catalog=CATALOG)

    assert response.status_code == 502
    assert response.json()["error"]["code"] == "provider_failure"


def test_gemini_catalog_schema_is_dynamic(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    captured = {}

    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"candidates": [{"content": {"parts": [{"text": json.dumps(CATALOG_RESULT)}]}}]}

    class FakeClient:
        def __init__(self, timeout):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *_):
            pass

        async def post(self, url, json, headers):
            captured.update(body=json)
            return FakeResponse()

    monkeypatch.setattr(main.httpx, "AsyncClient", FakeClient)
    catalog = main.parse_catalog(json.dumps(CATALOG))
    asyncio.run(main.analyze_with_provider(PNG, "image/png", catalog))

    schema = captured["body"]["generationConfig"]["responseSchema"]
    furniture_schema = schema["properties"]["furniture"]["items"]
    assert furniture_schema["properties"]["asset_id"]["enum"] == ["coffee-table"]
    assert "type" not in furniture_schema["properties"]
    assert furniture_schema["required"][0] == "asset_id"
    prompt = captured["body"]["contents"][0]["parts"][0]["text"]
    assert "[[CATALOG_START]]" in prompt and "[[CATALOG_END]]" in prompt
    assert "Mesa ratona" in prompt and "living-room" in prompt
=======
>>>>>>> 718d31a2a94a0e4bc7c0a2070706df2b3a09ac24


def test_provider_failure(monkeypatch):
    monkeypatch.setattr(main, "analyze_with_provider", provider(exc=main.ProviderError("x")))
    r = post(); assert r.status_code == 502 and r.json()["error"]["code"] == "provider_failure"


@pytest.mark.parametrize("bad", [{"furniture": [{**OK["furniture"][0], "type": "lampara"}]},
                                 {"furniture": [{**OK["furniture"][0], "x": 1.7}]}, {"nope": 1}])
def test_provider_invalid_output(monkeypatch, bad):
    monkeypatch.setattr(main, "analyze_with_provider", provider(bad))
    r = post(); assert r.status_code == 502 and r.json()["error"]["code"] == "provider_failure"
