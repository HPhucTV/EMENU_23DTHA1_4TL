"""Script benchmark thực tế >= 2 model Ollama trên >= 10 câu tiếng Việt (WBS 1.3.5.2).

Cách chạy từ thư mục gốc repo:
    backend\\.venv\\Scripts\\python.exe ollama\\run_benchmark.py
"""

from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone, timedelta
import json
from pathlib import Path
import platform
import re
import sys
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND_DIR = REPO_ROOT / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.ai.config import AISettings  # noqa: E402
from app.ai.ollama_client import OllamaClient, OllamaError  # noqa: E402

CJK_PATTERN = re.compile(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]")
VN_TZ = timezone(timedelta(hours=7), name="Asia/Ho_Chi_Minh")


def _evaluate_reply(reply: str, case: dict[str, Any]) -> dict[str, Any]:
    normalized = " ".join(reply.lower().split())
    has_cjk = bool(CJK_PATTERN.search(reply))
    is_empty = len(normalized) == 0

    must_any = [kw.lower() for kw in case.get("must_contain_any", [])]
    must_not_any = [kw.lower() for kw in case.get("must_not_contain_any", [])]

    matched_required = [kw for kw in must_any if kw in normalized]
    hit_forbidden = [kw for kw in must_not_any if kw in normalized]

    reasons: list[str] = []
    if is_empty:
        reasons.append("empty_reply")
    if case.get("forbidden_cjk", True) and has_cjk:
        reasons.append("contains_cjk")
    if must_any and not matched_required:
        reasons.append("missing_expected_intent_keywords")
    if hit_forbidden:
        reasons.append(f"forbidden_phrases:{','.join(hit_forbidden)}")

    return {
        "passed": len(reasons) == 0,
        "has_cjk": has_cjk,
        "matched_required": matched_required,
        "hit_forbidden": hit_forbidden,
        "reasons": reasons,
    }


def _percentile_95(values: list[float]) -> float:
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    idx = min(len(sorted_vals) - 1, max(0, int(round(0.95 * (len(sorted_vals) - 1)))))
    return round(sorted_vals[idx], 2)


async def benchmark_model(
    client: OllamaClient,
    model_name: str,
    system_prompt: str,
    cases: list[dict[str, Any]],
    disk_size_mb: float,
    num_predict: int,
) -> dict[str, Any]:
    print(f"\n=== Đang đo model: {model_name} (disk={disk_size_mb:.1f} MB) ===", flush=True)

    # 1. Warm-up để nạp model vào RAM và đo thông số bộ nhớ thực tế qua /api/ps
    warmup_res = await client.chat(
        [
            {"role": "system", "content": "Trả lời bằng một từ tiếng Việt."},
            {"role": "user", "content": "Xin chào"},
        ],
        model=model_name,
        num_predict=16,
        temperature=0.0,
        keep_alive="10m",
        allow_fallback_model=False,
        timeout_seconds=120.0,
    )
    running = await client.list_running_models()
    ram_loaded_mb = 0.0
    vram_loaded_mb = 0.0
    processor = "CPU"
    for item in running:
        if item.get("name", "").startswith(model_name.split(":")[0]):
            ram_loaded_mb = float(item.get("size_mb", 0.0))
            vram_loaded_mb = float(item.get("size_vram_mb", 0.0))
            processor = str(item.get("processor", "CPU"))
            break

    print(
        f"  Warm-up xong: cold_load={warmup_res.load_duration_ms} ms, "
        f"RAM={ram_loaded_mb:.1f} MB, processor={processor}",
        flush=True,
    )

    # 2. Chạy độc lập từng câu hỏi trong bộ benchmark
    case_results: list[dict[str, Any]] = []
    for case in cases:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": case["prompt"]},
        ]
        try:
            res = await client.chat(
                messages,
                model=model_name,
                num_predict=num_predict,
                temperature=0.2,
                keep_alive="10m",
                allow_fallback_model=False,
                timeout_seconds=90.0,
            )
            evaluation = _evaluate_reply(res.content, case)
            item = {
                "id": case["id"],
                "category": case["category"],
                "prompt": case["prompt"],
                "reply": res.content,
                "latency_ms": res.latency_ms,
                "total_duration_ms": res.total_duration_ms,
                "prompt_eval_count": res.prompt_eval_count,
                "prompt_eval_rate_tps": res.prompt_eval_rate_tps,
                "eval_count": res.eval_count,
                "eval_rate_tps": res.eval_rate_tps,
                "passed": evaluation["passed"],
                "has_cjk": evaluation["has_cjk"],
                "reasons": evaluation["reasons"],
            }
            status_tag = "PASS" if evaluation["passed"] else f"FAIL({','.join(evaluation['reasons'])})"
            print(
                f"  [{case['id']}] {status_tag} | {res.latency_ms:.0f} ms | "
                f"{res.eval_rate_tps:.2f} tok/s | tokens={res.eval_count}",
                flush=True,
            )
        except OllamaError as exc:
            item = {
                "id": case["id"],
                "category": case["category"],
                "prompt": case["prompt"],
                "reply": "",
                "latency_ms": 0.0,
                "total_duration_ms": 0.0,
                "prompt_eval_count": 0,
                "prompt_eval_rate_tps": 0.0,
                "eval_count": 0,
                "eval_rate_tps": 0.0,
                "passed": False,
                "has_cjk": False,
                "reasons": [f"error:{exc.code}"],
            }
            print(f"  [{case['id']}] ERROR: {exc.code} - {exc.message}", flush=True)
        case_results.append(item)

    # 3. Giải phóng model khỏi RAM trước khi đo model kế tiếp
    await client.unload_model(model_name)

    latencies = [c["latency_ms"] for c in case_results if c["latency_ms"] > 0]
    eval_rates = [c["eval_rate_tps"] for c in case_results if c["eval_rate_tps"] > 0]
    passed_count = sum(1 for c in case_results if c["passed"])
    cjk_count = sum(1 for c in case_results if c["has_cjk"])
    total_cases = len(case_results)

    summary = {
        "model": model_name,
        "disk_size_mb": round(disk_size_mb, 2),
        "ram_loaded_mb": round(ram_loaded_mb, 2),
        "vram_loaded_mb": round(vram_loaded_mb, 2),
        "processor": processor,
        "cold_load_ms": warmup_res.load_duration_ms,
        "warmup_latency_ms": warmup_res.latency_ms,
        "total_cases": total_cases,
        "passed_cases": passed_count,
        "pass_rate_percent": round((passed_count / total_cases) * 100.0, 2) if total_cases else 0.0,
        "cjk_leak_cases": cjk_count,
        "vietnamese_purity_percent": round(((total_cases - cjk_count) / total_cases) * 100.0, 2) if total_cases else 0.0,
        "avg_latency_ms": round(sum(latencies) / len(latencies), 2) if latencies else 0.0,
        "p95_latency_ms": _percentile_95(latencies),
        "avg_eval_rate_tps": round(sum(eval_rates) / len(eval_rates), 2) if eval_rates else 0.0,
        "avg_eval_tokens": round(
            sum(c["eval_count"] for c in case_results) / total_cases, 2
        )
        if total_cases
        else 0.0,
    }
    return {"summary": summary, "cases": case_results}


async def main_async(
    base_url: str,
    requested_models: list[str] | None,
    prompts_path: Path,
    output_path: Path,
    num_predict: int,
) -> dict[str, Any]:
    spec = json.loads(prompts_path.read_text(encoding="utf-8"))
    system_prompt: str = spec["system_prompt"]
    cases: list[dict[str, Any]] = spec["cases"]

    settings = AISettings(ollama_base_url=base_url)
    client = OllamaClient(settings=settings)
    version = await client.get_version()
    installed = await client.list_models()
    installed_sizes = {
        str(m.get("name")): round(float(m.get("size") or 0) / (1024 * 1024), 2)
        for m in installed
        if isinstance(m, dict) and m.get("name")
    }

    default_order = ["gemma3:4b", "llama3.1:8b", "qwen2.5:7b"]
    targets = requested_models or [m for m in default_order if m in installed_sizes]
    if len(targets) < 2:
        raise RuntimeError(
            f"Cần ít nhất 2 model trên Ollama để benchmark; hiện thấy: {list(installed_sizes)}"
        )

    results: list[dict[str, Any]] = []
    for model_name in targets:
        results.append(
            await benchmark_model(
                client=client,
                model_name=model_name,
                system_prompt=system_prompt,
                cases=cases,
                disk_size_mb=installed_sizes.get(model_name, 0.0),
                num_predict=num_predict,
            )
        )

    report = {
        "generated_at": datetime.now(VN_TZ).isoformat(),
        "environment": {
            "os": platform.platform(),
            "python": platform.python_version(),
            "ollama_base_url": base_url,
            "ollama_version": version,
            "num_predict": num_predict,
            "total_questions": len(cases),
        },
        "models": results,
    }
    output_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nĐã lưu kết quả benchmark tại: {output_path}", flush=True)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Benchmark các model Ollama trên bộ câu hỏi tiếng Việt Nhà hàng Vườn Phố."
    )
    parser.add_argument("--base-url", default="http://127.0.0.1:11434")
    parser.add_argument("--models", nargs="*", default=None)
    parser.add_argument(
        "--prompts",
        type=Path,
        default=REPO_ROOT / "ollama" / "benchmark_prompts.json",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "ollama" / "benchmark_results.json",
    )
    parser.add_argument("--num-predict", type=int, default=140)
    args = parser.parse_args()

    asyncio.run(
        main_async(
            base_url=args.base_url,
            requested_models=args.models,
            prompts_path=args.prompts,
            output_path=args.output,
            num_predict=args.num_predict,
        )
    )


if __name__ == "__main__":
    main()
