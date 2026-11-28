"""Client bất đồng bộ giao tiếp với máy chủ Ollama self-hosted (WBS 1.3.5.2)."""

from __future__ import annotations

from dataclasses import dataclass, field
from time import perf_counter
from typing import Any

import httpx

from app.ai.config import AISettings, get_ai_settings


class OllamaError(Exception):
    """Ngoại lệ chuẩn hóa theo Chat API JSON Contract."""

    def __init__(
        self,
        code: str,
        message: str,
        *,
        status_code: int = 500,
        retryable: bool = True,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.retryable = retryable


class OllamaUnavailableError(OllamaError):
    """Lỗi máy chủ Ollama không phản hồi hoặc model chưa sẵn sàng (503)."""

    def __init__(
        self,
        message: str = "Dịch vụ AI Chatbot tạm thời không khả dụng.",
    ) -> None:
        super().__init__(
            code="MODEL_UNAVAILABLE",
            message=message,
            status_code=503,
            retryable=True,
        )


class OllamaTimeoutError(OllamaError):
    """Lỗi Ollama xử lý vượt quá thời gian cho phép (504)."""

    def __init__(
        self,
        message: str = "AI phản hồi quá lâu, vui lòng thử lại.",
    ) -> None:
        super().__init__(
            code="MODEL_TIMEOUT",
            message=message,
            status_code=504,
            retryable=True,
        )


@dataclass(slots=True)
class OllamaChatResult:
    """Kết quả một lượt gọi `/api/chat` kèm thông số hiệu năng chi tiết."""

    model: str
    content: str
    latency_ms: float
    total_duration_ms: float
    load_duration_ms: float
    prompt_eval_count: int
    prompt_eval_rate_tps: float
    eval_count: int
    eval_rate_tps: float
    done_reason: str | None = None
    used_fallback_model: bool = False


@dataclass(slots=True)
class OllamaHealthStatus:
    """Ảnh chụp trạng thái kết nối và các model sẵn sàng trên Ollama."""

    status: str
    ollama_reachable: bool
    ollama_base_url: str
    ollama_version: str | None
    configured_model: str
    fallback_model: str
    active_model: str | None
    model_ready: bool
    fallback_model_ready: bool
    is_fallback: bool
    available_models: list[str] = field(default_factory=list)
    loaded_models: list[dict[str, Any]] = field(default_factory=list)
    latency_ms: float = 0.0
    detail: str = ""


def _is_model_available(target: str, installed: list[str]) -> bool:
    """So khớp tên model linh hoạt cho trường hợp có hoặc không có tag `:latest`."""
    normalized_target = target.strip()
    if not normalized_target:
        return False
    candidates = {normalized_target}
    if ":" not in normalized_target:
        candidates.add(f"{normalized_target}:latest")
    elif normalized_target.endswith(":latest"):
        candidates.add(normalized_target.removesuffix(":latest"))
    installed_set = {name.strip() for name in installed if name}
    return any(candidate in installed_set for candidate in candidates)


def _ns_to_ms(value: Any) -> float:
    if isinstance(value, (int, float)) and value > 0:
        return round(float(value) / 1_000_000.0, 2)
    return 0.0


def _calc_tps(token_count: Any, duration_ns: Any) -> float:
    if (
        isinstance(token_count, (int, float))
        and isinstance(duration_ns, (int, float))
        and token_count > 0
        and duration_ns > 0
    ):
        return round(float(token_count) / (float(duration_ns) / 1_000_000_000.0), 2)
    return 0.0


class OllamaClient:
    """Async client cho Ollama REST API (`/api/tags`, `/api/version`, `/api/ps`, `/api/chat`)."""

    def __init__(
        self,
        settings: AISettings | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.settings = settings or get_ai_settings()
        self.base_url = self.settings.normalized_base_url
        self._transport = transport

    def _build_async_client(self, timeout_seconds: float) -> httpx.AsyncClient:
        kwargs: dict[str, Any] = {
            "base_url": self.base_url,
            "timeout": httpx.Timeout(timeout_seconds),
        }
        if self._transport is not None:
            kwargs["transport"] = self._transport
        return httpx.AsyncClient(**kwargs)

    async def get_version(self) -> str | None:
        """Lấy phiên bản Ollama (`GET /api/version`), trả về `None` nếu lỗi."""
        try:
            async with self._build_async_client(
                self.settings.ollama_health_timeout_seconds
            ) as client:
                response = await client.get("/api/version")
                response.raise_for_status()
                payload = response.json()
                version = payload.get("version")
                return str(version) if version is not None else None
        except (httpx.HTTPError, ValueError):
            return None

    async def list_models(self) -> list[dict[str, Any]]:
        """Lấy danh sách model đã tải về máy (`GET /api/tags`)."""
        try:
            async with self._build_async_client(
                self.settings.ollama_health_timeout_seconds
            ) as client:
                response = await client.get("/api/tags")
                response.raise_for_status()
                payload = response.json()
                models = payload.get("models", [])
                return models if isinstance(models, list) else []
        except httpx.TimeoutException as exc:
            raise OllamaTimeoutError(
                "Hết thời gian chờ khi kiểm tra danh sách model Ollama."
            ) from exc
        except (httpx.HTTPError, ValueError) as exc:
            raise OllamaUnavailableError(
                f"Không thể kết nối tới máy chủ Ollama tại {self.base_url}."
            ) from exc

    async def list_running_models(self) -> list[dict[str, Any]]:
        """Lấy danh sách model đang nạp trong RAM/VRAM (`GET /api/ps`)."""
        try:
            async with self._build_async_client(
                self.settings.ollama_health_timeout_seconds
            ) as client:
                response = await client.get("/api/ps")
                response.raise_for_status()
                payload = response.json()
                models = payload.get("models", [])
                if not isinstance(models, list):
                    return []
                normalized: list[dict[str, Any]] = []
                for item in models:
                    if not isinstance(item, dict):
                        continue
                    size_bytes = float(item.get("size") or 0)
                    vram_bytes = float(item.get("size_vram") or 0)
                    normalized.append(
                        {
                            "name": str(item.get("name") or item.get("model") or ""),
                            "size_mb": round(size_bytes / (1024 * 1024), 2),
                            "size_vram_mb": round(vram_bytes / (1024 * 1024), 2),
                            "processor": "GPU/CPU" if vram_bytes > 0 else "CPU",
                        }
                    )
                return normalized
        except (httpx.HTTPError, ValueError):
            return []

    async def unload_model(self, model: str) -> None:
        """Giải phóng model khỏi RAM (`keep_alive=0`) để tránh tràn bộ nhớ khi chuyển model."""
        try:
            async with self._build_async_client(
                self.settings.ollama_health_timeout_seconds
            ) as client:
                await client.post(
                    "/api/generate",
                    json={"model": model, "keep_alive": 0},
                )
        except httpx.HTTPError:
            pass

    async def check_health(self) -> OllamaHealthStatus:
        """Kiểm tra tổng thể khả năng phục vụ của Ollama và model đã cấu hình."""
        started = perf_counter()
        configured = self.settings.ollama_model
        fallback = self.settings.ollama_fallback_model

        try:
            raw_models = await self.list_models()
        except OllamaError as exc:
            latency_ms = round((perf_counter() - started) * 1000.0, 2)
            return OllamaHealthStatus(
                status="unavailable",
                ollama_reachable=False,
                ollama_base_url=self.base_url,
                ollama_version=None,
                configured_model=configured,
                fallback_model=fallback,
                active_model=None,
                model_ready=False,
                fallback_model_ready=False,
                is_fallback=True,
                available_models=[],
                loaded_models=[],
                latency_ms=latency_ms,
                detail=exc.message,
            )

        available_names = [
            str(m.get("name"))
            for m in raw_models
            if isinstance(m, dict) and m.get("name")
        ]
        version = await self.get_version()
        loaded_models = await self.list_running_models()
        latency_ms = round((perf_counter() - started) * 1000.0, 2)

        primary_ready = _is_model_available(configured, available_names)
        fallback_ready = _is_model_available(fallback, available_names)

        if primary_ready:
            active_model: str | None = configured
            status_text = "ok"
            is_fallback = False
            detail = f"Ollama sẵn sàng với model chính `{configured}`."
        elif fallback_ready:
            active_model = fallback
            status_text = "ok"
            is_fallback = False
            detail = (
                f"Model chính `{configured}` chưa có; "
                f"sẵn sàng dùng model dự phòng `{fallback}`."
            )
        else:
            active_model = None
            status_text = "degraded"
            is_fallback = True
            detail = (
                f"Ollama đã kết nối nhưng chưa tải `{configured}` "
                f"hoặc `{fallback}`. Cần chạy `ollama pull {configured}`."
            )

        return OllamaHealthStatus(
            status=status_text,
            ollama_reachable=True,
            ollama_base_url=self.base_url,
            ollama_version=version,
            configured_model=configured,
            fallback_model=fallback,
            active_model=active_model,
            model_ready=primary_ready,
            fallback_model_ready=fallback_ready,
            is_fallback=is_fallback,
            available_models=available_names,
            loaded_models=loaded_models,
            latency_ms=latency_ms,
            detail=detail,
        )

    async def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str | None = None,
        temperature: float | None = None,
        num_predict: int | None = None,
        keep_alive: str | int | None = None,
        format_json: bool = False,
        allow_fallback_model: bool = True,
        timeout_seconds: float | None = None,
    ) -> OllamaChatResult:
        """Gửi hội thoại tới `POST /api/chat` (`stream=False`) và thu thập metric phản hồi."""
        target_model = model or self.settings.ollama_model
        fallback_model = self.settings.ollama_fallback_model
        effective_timeout = (
            timeout_seconds
            if timeout_seconds is not None
            else self.settings.ollama_timeout_seconds
        )
        options: dict[str, Any] = {
            "temperature": (
                self.settings.ollama_temperature
                if temperature is None
                else temperature
            ),
            "num_predict": (
                self.settings.ollama_num_predict
                if num_predict is None
                else num_predict
            ),
        }

        return await self._send_chat_request(
            target_model=target_model,
            fallback_model=fallback_model,
            messages=messages,
            options=options,
            keep_alive=(
                self.settings.ollama_keep_alive
                if keep_alive is None
                else keep_alive
            ),
            format_json=format_json,
            allow_fallback_model=allow_fallback_model,
            timeout_seconds=effective_timeout,
            used_fallback=False,
        )

    async def _send_chat_request(
        self,
        *,
        target_model: str,
        fallback_model: str,
        messages: list[dict[str, str]],
        options: dict[str, Any],
        keep_alive: str | int,
        format_json: bool,
        allow_fallback_model: bool,
        timeout_seconds: float,
        used_fallback: bool,
    ) -> OllamaChatResult:
        payload: dict[str, Any] = {
            "model": target_model,
            "messages": messages,
            "stream": False,
            "keep_alive": keep_alive,
            "options": options,
        }
        if format_json:
            payload["format"] = "json"

        started = perf_counter()
        try:
            async with self._build_async_client(timeout_seconds) as client:
                response = await client.post("/api/chat", json=payload)

                if (
                    response.status_code == 404
                    and allow_fallback_model
                    and not used_fallback
                    and fallback_model
                    and fallback_model != target_model
                ):
                    return await self._send_chat_request(
                        target_model=fallback_model,
                        fallback_model=fallback_model,
                        messages=messages,
                        options=options,
                        keep_alive=keep_alive,
                        format_json=format_json,
                        allow_fallback_model=False,
                        timeout_seconds=timeout_seconds,
                        used_fallback=True,
                    )

                if response.status_code >= 400:
                    raise OllamaUnavailableError(
                        f"Ollama trả về mã lỗi HTTP {response.status_code} cho model `{target_model}`."
                    )

                data = response.json()
        except httpx.TimeoutException as exc:
            raise OllamaTimeoutError(
                f"Ollama quá thời gian phản hồi sau {timeout_seconds} giây."
            ) from exc
        except OllamaError:
            raise
        except (httpx.HTTPError, ValueError) as exc:
            raise OllamaUnavailableError(
                f"Không thể giao tiếp với máy chủ Ollama tại {self.base_url}."
            ) from exc

        latency_ms = round((perf_counter() - started) * 1000.0, 2)
        message_obj = data.get("message") or {}
        content = str(message_obj.get("content") or "").strip()
        prompt_eval_count = int(data.get("prompt_eval_count") or 0)
        eval_count = int(data.get("eval_count") or 0)
        prompt_eval_duration = data.get("prompt_eval_duration")
        eval_duration = data.get("eval_duration")

        return OllamaChatResult(
            model=str(data.get("model") or target_model),
            content=content,
            latency_ms=latency_ms,
            total_duration_ms=_ns_to_ms(data.get("total_duration")),
            load_duration_ms=_ns_to_ms(data.get("load_duration")),
            prompt_eval_count=prompt_eval_count,
            prompt_eval_rate_tps=_calc_tps(prompt_eval_count, prompt_eval_duration),
            eval_count=eval_count,
            eval_rate_tps=_calc_tps(eval_count, eval_duration),
            done_reason=(
                str(data.get("done_reason"))
                if data.get("done_reason") is not None
                else None
            ),
            used_fallback_model=used_fallback,
        )
