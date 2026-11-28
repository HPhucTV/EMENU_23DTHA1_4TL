"""Kiểm thử tự động cho OllamaClient, `/api/v1/chat/health` và kết quả benchmark (WBS 1.3.5.2)."""

import asyncio
import json
from pathlib import Path
from typing import Any

from fastapi.testclient import TestClient
import httpx
import pytest

from app.ai.config import AISettings
from app.ai.ollama_client import (
    OllamaClient,
    OllamaTimeoutError,
    OllamaUnavailableError,
)
from app.api.v1.chat_router import get_ollama_client
from app.main import app

BACKEND_DIR = Path(__file__).resolve().parents[2]
REPO_ROOT = BACKEND_DIR.parent


def _make_mock_client(
    handler: Any,
    *,
    primary_model: str = "gemma3:4b",
    fallback_model: str = "llama3.1:8b",
) -> OllamaClient:
    settings = AISettings(
        ollama_base_url="http://localhost:11434",
        ollama_model=primary_model,
        ollama_fallback_model=fallback_model,
        ollama_timeout_seconds=5.0,
        ollama_health_timeout_seconds=2.0,
    )
    return OllamaClient(
        settings=settings,
        transport=httpx.MockTransport(handler),
    )


def test_chat_health_route_registered_in_openapi() -> None:
    client = TestClient(app)
    openapi = client.get("/openapi.json")
    assert openapi.status_code == 200
    paths = openapi.json()["paths"]
    assert "/api/v1/chat/health" in paths


def test_chat_health_returns_200_ok_when_ollama_ready() -> None:
    def _handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/tags":
            return httpx.Response(
                200,
                json={"models": [{"name": "gemma3:4b"}, {"name": "llama3.1:8b"}]},
            )
        if request.url.path == "/api/version":
            return httpx.Response(200, json={"version": "0.40.18"})
        if request.url.path == "/api/ps":
            return httpx.Response(
                200,
                json={
                    "models": [
                        {
                            "name": "gemma3:4b",
                            "size": 3_100_000_000,
                            "size_vram": 0,
                        }
                    ]
                },
            )
        return httpx.Response(404)

    app.dependency_overrides[get_ollama_client] = lambda: _make_mock_client(_handler)
    try:
        res = TestClient(app).get("/api/v1/chat/health")
        assert res.status_code == 200
        body = res.json()
        assert body["status"] == "ok"
        assert body["ollama_reachable"] is True
        assert body["ollama_version"] == "0.40.18"
        assert body["model_ready"] is True
        assert body["fallback_model_ready"] is True
        assert body["active_model"] == "gemma3:4b"
        assert body["is_fallback"] is False
        assert body["loaded_models"][0]["processor"] == "CPU"
        assert body["loaded_models"][0]["size_mb"] > 2900
    finally:
        app.dependency_overrides.clear()


def test_chat_health_returns_200_with_fallback_model_when_primary_missing() -> None:
    def _handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/tags":
            return httpx.Response(200, json={"models": [{"name": "llama3.1:8b"}]})
        if request.url.path == "/api/version":
            return httpx.Response(200, json={"version": "0.40.18"})
        if request.url.path == "/api/ps":
            return httpx.Response(200, json={"models": []})
        return httpx.Response(404)

    app.dependency_overrides[get_ollama_client] = lambda: _make_mock_client(_handler)
    try:
        res = TestClient(app).get("/api/v1/chat/health")
        assert res.status_code == 200
        body = res.json()
        assert body["status"] == "ok"
        assert body["model_ready"] is False
        assert body["fallback_model_ready"] is True
        assert body["active_model"] == "llama3.1:8b"
        assert body["is_fallback"] is False
    finally:
        app.dependency_overrides.clear()


def test_chat_health_returns_503_when_models_missing_or_ollama_down() -> None:
    def _empty_models_handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/api/tags":
            return httpx.Response(200, json={"models": []})
        if request.url.path == "/api/version":
            return httpx.Response(200, json={"version": "0.40.18"})
        if request.url.path == "/api/ps":
            return httpx.Response(200, json={"models": []})
        return httpx.Response(404)

    app.dependency_overrides[get_ollama_client] = lambda: _make_mock_client(
        _empty_models_handler
    )
    try:
        degraded_res = TestClient(app).get("/api/v1/chat/health")
        assert degraded_res.status_code == 503
        degraded_body = degraded_res.json()
        assert degraded_body["status"] == "degraded"
        assert degraded_body["ollama_reachable"] is True
        assert degraded_body["is_fallback"] is True
    finally:
        app.dependency_overrides.clear()

    def _unreachable_handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("Connection refused", request=request)

    app.dependency_overrides[get_ollama_client] = lambda: _make_mock_client(
        _unreachable_handler
    )
    try:
        down_res = TestClient(app).get("/api/v1/chat/health")
        assert down_res.status_code == 503
        down_body = down_res.json()
        assert down_body["status"] == "unavailable"
        assert down_body["ollama_reachable"] is False
        assert down_body["is_fallback"] is True
    finally:
        app.dependency_overrides.clear()


def test_ollama_client_chat_success_and_fallback_retry() -> None:
    seen_models: list[str] = []

    def _handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content.decode("utf-8"))
        seen_models.append(body["model"])
        if body["model"] == "gemma3:4b":
            return httpx.Response(404, json={"error": "model not found"})
        return httpx.Response(
            200,
            json={
                "model": body["model"],
                "message": {
                    "role": "assistant",
                    "content": "Dạ, nhà hàng mở cửa từ 10:00 đến 22:00 ạ.",
                },
                "done_reason": "stop",
                "total_duration": 1_500_000_000,
                "load_duration": 100_000_000,
                "prompt_eval_count": 24,
                "prompt_eval_duration": 400_000_000,
                "eval_count": 18,
                "eval_duration": 1_000_000_000,
            },
        )

    client = _make_mock_client(_handler)
    result = asyncio.run(
        client.chat([{"role": "user", "content": "Nhà hàng mở cửa mấy giờ?"}])
    )

    assert seen_models == ["gemma3:4b", "llama3.1:8b"]
    assert result.used_fallback_model is True
    assert result.model == "llama3.1:8b"
    assert "10:00" in result.content
    assert result.eval_count == 18
    assert result.eval_rate_tps == 18.0
    assert result.prompt_eval_rate_tps == 60.0
    assert result.total_duration_ms == 1500.0
    assert result.load_duration_ms == 100.0


def test_ollama_client_maps_timeout_and_connection_errors() -> None:
    def _timeout_handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("Timed out", request=request)

    timeout_client = _make_mock_client(_timeout_handler)
    with pytest.raises(OllamaTimeoutError) as timeout_exc:
        asyncio.run(
            timeout_client.chat([{"role": "user", "content": "Xin chào"}])
        )
    assert timeout_exc.value.code == "MODEL_TIMEOUT"
    assert timeout_exc.value.status_code == 504

    def _error_handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"error": "internal server error"})

    error_client = _make_mock_client(_error_handler)
    with pytest.raises(OllamaUnavailableError) as conn_exc:
        asyncio.run(error_client.chat([{"role": "user", "content": "Xin chào"}]))
    assert conn_exc.value.code == "MODEL_UNAVAILABLE"
    assert conn_exc.value.status_code == 503


def test_benchmark_results_and_report_meet_acceptance_criteria() -> None:
    prompts_path = REPO_ROOT / "ollama" / "benchmark_prompts.json"
    results_path = REPO_ROOT / "ollama" / "benchmark_results.json"
    report_path = REPO_ROOT / "ollama" / "BENCHMARK_REPORT.md"

    assert prompts_path.is_file()
    assert results_path.is_file()
    assert report_path.is_file()

    prompts_data = json.loads(prompts_path.read_text(encoding="utf-8"))
    results_data = json.loads(results_path.read_text(encoding="utf-8"))
    report_text = report_path.read_text(encoding="utf-8")

    assert len(prompts_data["cases"]) >= 10
    models = results_data["models"]
    assert len(models) >= 2

    for entry in models:
        summary = entry["summary"]
        assert summary["total_cases"] >= 10
        assert summary["ram_loaded_mb"] > 0
        assert summary["avg_latency_ms"] > 0
        assert summary["avg_eval_rate_tps"] > 0
        assert 0 <= summary["pass_rate_percent"] <= 100
        assert len(entry["cases"]) == summary["total_cases"]
        assert summary["model"] in report_text
