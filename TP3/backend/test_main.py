import asyncio
import base64
import json

import pytest
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)
PNG = b"\x89PNG\r\n\x1a\n" + b"0" * 32
OK = {"furniture": [{"type": "sofa", "x": .5, "y": .6, "width": .3, "depth": .12, "rotation_deg": 0, "confidence": .8}], "warnings": ["oclusión parcial"]}


def post(data=PNG, mime="image/png", **form):
    return client.post("/api/analyze-room", files={"image": ("r.png", data, mime)}, data=form)


def provider(payload=None, exc=None):
    async def fake(image, mime):
        if exc: raise exc
        return payload
    return fake


def test_ok_uncalibrated(monkeypatch):
    monkeypatch.setattr(main, "analyze_with_provider", provider(OK))
    r = post(); assert r.status_code == 200
    j = r.json()
    assert j["calibration"] == {"status": "uncalibrated", "width_m": None}
    assert j["furniture"][0]["type"] == "sofa" and j["warnings"] == ["oclusión parcial"]


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


def test_provider_failure(monkeypatch):
    monkeypatch.setattr(main, "analyze_with_provider", provider(exc=main.ProviderError("x")))
    r = post(); assert r.status_code == 502 and r.json()["error"]["code"] == "provider_failure"


@pytest.mark.parametrize("bad", [{"furniture": [{**OK["furniture"][0], "type": "lampara"}]},
                                 {"furniture": [{**OK["furniture"][0], "x": 1.7}]}, {"nope": 1}])
def test_provider_invalid_output(monkeypatch, bad):
    monkeypatch.setattr(main, "analyze_with_provider", provider(bad))
    r = post(); assert r.status_code == 502 and r.json()["error"]["code"] == "provider_failure"
