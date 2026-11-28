# NHẬT KÝ PHIÊN LÀM VIỆC & BÀN GIAO NGỮ CẢNH (SESSION LOG)

> AI Agent và thành viên nhóm **BẮT BUỘC** đọc mục **Current Snapshot** trước khi bắt đầu phiên mới, và thêm một Entry mới lên **trên cùng** danh sách nhật ký sau khi kết thúc phiên. Không xóa các Entry cũ.

---

## Current Snapshot (Cập nhật: 28/11/2026 — `GMT+7`)

| Hạng mục | Trạng thái hiện tại |
| :--- | :--- |
| **Sprint hiện tại** | **Sprint 1** *(đang triển khai `EP-01`, hướng tới mốc `M2` ngày `29/11/2026`)* |
| **Mốc kế tiếp** | Hoàn tất kiểm chứng **`M2: Lưu Baseline MS Project (29/11/2026)`** & hoàn tất `US-06`..`US-08` |
| **Tiến độ mã nguồn** | Đã hoàn tất **`US-01` (`MC-11`)**, **`US-02` (`MC-13`)**, **`US-04` (`MC-14`)**, **`MC-70`**, **`MC-71`**, **`MC-72`** (đều đã merge `develop`) và **`US-05` (`MC-15`)**: Đăng nhập bằng Email/SĐT (`POST /api/v1/auth/login`), cấp JWT có thời hạn, điều hướng 3 vai trò (`customer`, `staff`, `manager`), khóa tạm `15 phút` sau `5` lần sai, đăng xuất hủy phiên bền vững (`POST /api/v1/auth/logout`, `GET /api/v1/auth/me`) và giao diện `LoginPage` / `AuthContext` |
| **Hồ sơ & Tài liệu** | Đã có `AGENTS.md`, `docs/SYSTEM_SPEC.md`, `docs/ERD.md`, `docs/ROADMAP.md`, `docs/SESSION_LOG.md`, `docs/MS_PROJECT_BASELINE_M2.xml`, `docs/BASELINE_M2_REPORT.md`, `docs/DOR_DOD_QUALITY.md`, `docs/RISK_REGISTER.md`, `docs/PAYMENT_EMAIL_SMS_RESEARCH.md` (`MC-69`/`MC-70`), Chat Contract (`MC-68`), `ollama/BENCHMARK_REPORT.md` & bộ ảnh Figma (`PR #10`) |
| **Quy ước đã chốt** | Jira key **`MC`** (`MC-xx`); nhóm **4 thành viên**; kiến trúc Zero File-Overlap; mật khẩu băm `bcrypt` (cost `12`), JWT `HS256` kèm thu hồi `jti`, cấu hình `.gitguardian.yaml` loại trừ thư mục test |

### Cảnh báo kỹ thuật & Blocker cần xử lý ngay
1. **Môi trường Docker / PostgreSQL trên máy local**: Khi đẩy lên GitHub/Staging hoặc chạy Docker, thực thi `alembic upgrade heads` trên PostgreSQL 16 để đồng bộ đủ 16 bảng (`core` + `ai`).
2. **Đầu việc kế tiếp trong Sprint 1**:
   - `[FS]` Mở PR `MC-15` (`US-05`) vào `develop`, sau đó triển khai tiếp `US-06` (Quên mật khẩu — link 1 lần có thời hạn), `US-07` (Phân quyền RBAC 3 vai trò & quản lý tài khoản NV) và `US-08` (CI GitHub Actions).
   - `[BA]` Hoàn tất nghiệm thu `US-03` (Prototype Figma luồng chính).

---

## Quy tắc & Template ghi nhật ký

- Ghi theo thứ tự **mới nhất lên trên (reverse chronological)** ngay dưới dòng phân cách Nhật ký bên dưới.
- Luôn ghi rõ **Ngày/Giờ (`GMT+7`)**, **Nhánh & Mã `MC-xx`**, **Đã làm**, **Quyết định chốt**, **Blocker**, và **Việc tiếp theo**.

```markdown
### [YYYY-MM-DD HH:mm GMT+7] — <Tên / AI Agent> | Nhánh: `<branch>` | Jira: `MC-<số>`
- **Mục tiêu phiên:** ...
- **Đã hoàn thành:**
  - ...
- **Quyết định chốt:** ...
- **Vấn đề / Blocker:** ...
- **Kiểm thử đã chạy:** ...
- **Bước tiếp theo:** ...
```

---

## Nhật ký các phiên làm việc

### [2026-11-28 19:38 GMT+7] — Antigravity AI + Dev Fullstack (Nguyễn Văn Tiến) | Nhánh: `MC-15-us-05-dang-nhập-va-dang-xuất` | Jira: `MC-15`
- **Mục tiêu phiên:** Đồng bộ nhánh `MC-15` lên `origin/develop` (`a6c2b2d`) và triển khai trọn vẹn **`[US-05]` Đăng nhập và đăng xuất** (`FR-01`: đăng nhập Email/SĐT, điều hướng 3 vai trò, khóa tạm `15 phút` sau `5` lần sai mật khẩu, JWT có thời hạn, đăng xuất hủy phiên).
- **Đã hoàn thành:**
  - Bổ sung [.gitguardian.yaml](../.gitguardian.yaml) ở thư mục gốc và chuẩn hóa dữ liệu giả lập kiểm thử để không phát sinh cảnh báo nhầm của GitGuardian trên PR.
  - Mở rộng [security.py](../backend/app/core/security.py) và tạo [deps.py](../backend/app/core/deps.py): phát hành & xác thực JWT `HS256` (`PyJWT`, đảm bảo khóa ký `>= 32 bytes` chuẩn RFC 7518), gắn `exp` (`60 phút` mặc định hoặc `7 ngày` khi chọn `Ghi nhớ đăng nhập`) và thu hồi `jti` bền vững qua `reservation_audit_logs` khi đăng xuất.
  - Mở rộng [auth_schemas.py](../backend/app/schemas/auth_schemas.py), [auth_service.py](../backend/app/services/auth_service.py), [auth_router.py](../backend/app/api/v1/auth_router.py): cung cấp `POST /api/v1/auth/login` (nhận Email hoặc SĐT Việt Nam, trả `redirect_path` theo vai trò `customer -> /`, `staff -> /ops/reservations`, `manager -> /ops`; đếm lần sai và khóa `423 ACCOUNT_LOCKED` trong `15 phút` khi chạm `5` lần sai, tự mở khóa & reset bộ đếm sau `15 phút`), `GET /api/v1/auth/me` và `POST /api/v1/auth/logout`.
  - Xây dựng [AuthContext.tsx](../frontend/src/context/AuthContext.tsx), cập nhật [http.ts](../frontend/src/lib/http.ts), [CustomerLayout.tsx](../frontend/src/layouts/CustomerLayout.tsx), [OperationsLayout.tsx](../frontend/src/layouts/OperationsLayout.tsx) và màn hình [LoginPage.tsx](../frontend/src/pages/LoginPage.tsx) bám sát Figma (`10_dang_nhap.png` & `12_dang_nhap_dien_thoai.png`).
  - Viết bộ kiểm thử tự động [test_auth_login.py](../backend/tests/core/test_auth_login.py) & [LoginPage.test.tsx](../frontend/src/test/LoginPage.test.tsx); cập nhật [ROADMAP.md](ROADMAP.md).
- **Quyết định chốt:**
  - Hủy phiên đăng xuất ở cả 2 lớp: xóa session + Bearer token phía trình duyệt và thu hồi `jti` phía server (bộ nhớ đệm + bản ghi `auth_logout` trong `reservation_audit_logs`) để token cũ không thể tái sử dụng kể cả khi server khởi động lại.
- **Vấn đề / Blocker:**
  - Không có blocker.
- **Kiểm thử đã chạy:**
  - Back-end `pytest -v`: **`28/28 passed`** (`16` test Core gồm `US-01`, `US-02`, `US-04`, `US-05` + `12` test AI).
  - Front-end `npm test` (`vitest run`): **`8/8 passed`** (`HomePage`, `RegisterPage`, `LoginPage`); `npm run build` (`tsc -b && vite build`): **thành công (`0` lỗi)**.
- **Bước tiếp theo:**
  1. Commit, push nhánh `MC-15-us-05-dang-nhập-va-dang-xuất` và mở PR `[MC-15] [US-05] Đăng nhập Email/SĐT, điều hướng vai trò, khóa 15p và đăng xuất hủy phiên` vào `develop`.
  2. Triển khai tiếp `US-06` (Quên mật khẩu), `US-07` (Phân quyền RBAC & tài khoản nhân viên) và `US-08` (CI GitHub Actions).

### [2026-11-27 21:42 GMT+7] — Antigravity AI + AI Dev (Nguyễn Đoàn Trường Vũ) | WBS: `1.3.5.2`
- **Mục tiêu phiên:** Benchmark `>= 2` model Ollama trên `>= 10` câu tiếng Việt, xây dựng `OllamaClient` bất đồng bộ và mở endpoint `GET /api/v1/chat/health` theo phân vùng Zero File-Overlap.
- **Đã hoàn thành:**
  - Xây dựng module `backend/app/ai/`: [config.py](../backend/app/ai/config.py) (`AISettings`), [schemas.py](../backend/app/ai/schemas.py) (`ChatHealthResponse`, `LoadedModelMemory`), [ollama_client.py](../backend/app/ai/ollama_client.py) (`OllamaClient`, fallback model tự động khi HTTP 404, chuẩn hóa `OllamaTimeoutError`/`OllamaUnavailableError`), và [__init__.py](../backend/app/ai/__init__.py).
  - Xây dựng [chat_router.py](../backend/app/api/v1/chat_router.py) mở `GET /api/v1/chat/health` (tự động gắn vào `/api/v1` qua `router.py` không cần sửa file Core), trả `200 OK` khi Ollama sẵn sàng hoặc `503` kèm `is_fallback: true` khi gián đoạn/thiếu model.
  - Thiết lập bộ `12` câu tiếng Việt 7 nhóm tại [benchmark_prompts.json](../ollama/benchmark_prompts.json), viết script đo tự động [run_benchmark.py](../ollama/run_benchmark.py), chạy đo thực tế trên `Ollama 0.40.18` (100% CPU, 16 GB RAM) cho 3 model và tổng hợp kết quả tại [benchmark_results.json](../ollama/benchmark_results.json) & [BENCHMARK_REPORT.md](../ollama/BENCHMARK_REPORT.md):
    - `gemma3:4b`: `2754.96 MB` RAM, `13.54 tok/s`, trung bình `12.40 s`, thuần tiếng Việt `100%`, đạt `10/12` (`83.33%`; lộ prompt injection ở `Q11` nếu chưa có lớp Guardrails backend).
    - `llama3.1:8b`: `5325.81 MB` RAM, `7.09 tok/s`, trung bình `9.06 s`, thuần tiếng Việt `100%`, đạt `11/12` (`91.67%`).
    - `qwen2.5:7b`: `4835.05 MB` RAM, `8.01 tok/s`, trung bình `8.62 s`, thuần tiếng Việt `100%` (không lẫn CJK khi có system prompt chặt), đạt `12/12` (`100%`).
  - Viết bộ kiểm thử [test_ollama_client_and_health.py](../backend/tests/ai/test_ollama_client_and_health.py) và tick `[x]` task `1.3.5.2` trong [ROADMAP.md](ROADMAP.md).
- **Quyết định chốt:**
  - Giữ mặc định `OLLAMA_MODEL=gemma3:4b` (nhẹ `2.69 GiB` RAM, tốc độ sinh token cao nhất) + `OLLAMA_FALLBACK_MODEL=llama3.1:8b`, đồng thời cung cấp đầy đủ số liệu cả `qwen2.5:7b` để PO/PM duyệt chốt chính thức tại Spike `US-15` (Sprint 2).
  - Bắt buộc tách lớp `guardrails.py` ở Sprint 3 để chặn prompt injection/dị ứng/ngoài phạm vi bằng rule trước khi gọi LLM nhỏ.
- **Vấn đề / Blocker:**
  - Không có blocker; chạy thực tế trên CPU không có GPU rời nên lượt đầu chưa cache KV mất `15–26s`, cần giữ `keep_alive` và rút gọn system prompt khi vào Sprint 2–5 để đạt KPI `<= 5s`.
- **Kiểm thử đã chạy:**
  - Kiểm chứng trực tiếp `GET /api/v1/chat/health` với `ollama.exe serve` thật đang chạy → HTTP `200 OK` (`status="ok"`, `active_model="gemma3:4b"`, `is_fallback=false`).
  - Back-end `pytest -v` (`tests/core/` + `tests/ai/`): đạt 100%.
- **Bước tiếp theo:**
  1. AI Dev tạo nhánh từ `develop` gắn mã Jira `MC-<số>`, commit và push lên GitHub để mở PR vào `develop`.
  2. Sang Sprint 2: trình bày [BENCHMARK_REPORT.md](../ollama/BENCHMARK_REPORT.md) để PO & PM chốt model (`US-15`), sau đó dựng `rag_retriever.py`, `prompts.py` và `seed_ai.py`.

### [2026-11-27 17:45 GMT+7] — Antigravity AI + AI Dev (Nguyễn Đoàn Trường Vũ) | WBS: `1.3.5.1`
- **Mục tiêu phiên:** Tạo `backend/app/models/ai_models.py` (`knowledge_docs`, `chat_sessions`, `chat_messages`) và Alembic migration nhánh `ai`, tuân thủ tuyệt đối Zero File-Overlap (không sửa `core_models.py` hay `alembic/env.py`).
- **Đã hoàn thành:**
  - Thiết lập môi trường ảo `backend/.venv` và cài đặt đầy đủ phụ thuộc từ [requirements.txt](../backend/requirements.txt).
  - Tạo [ai_models.py](../backend/app/models/ai_models.py) định nghĩa 3 bảng ORM SQLAlchemy 2.0: `KnowledgeDoc` (`knowledge_docs`), `ChatSession` (`chat_sessions` dùng `Uuid(as_uuid=True)`, hạn mặc định `90 ngày` theo `GMT+7`) và `ChatMessage` (`chat_messages` với `masked_content`, `response_meta_json`, `feedback`, `is_fallback`, `latency_ms`), dùng quan hệ một chiều tới `User` để không chạm vào `core_models.py`.
  - Tạo [20261127_0001_ai_initial_tables.py](../backend/alembic/versions/20261127_0001_ai_initial_tables.py) (`branch_labels = ("ai",)`, `down_revision = None`, `depends_on = ("20261126_0001_core",)`) tách nhánh `ai` độc lập khỏi nhánh `core` nhưng đảm bảo thứ tự tạo/xóa phụ thuộc `users.id`.
  - Tạo bộ kiểm thử [test_ai_models_and_migration.py](../backend/tests/ai/test_ai_models_and_migration.py) kiểm chứng `alembic upgrade heads` / `downgrade base` đủ 16 bảng, DDL PostgreSQL (`UUID`, `TIMESTAMPTZ`, `ON DELETE SET NULL`/`CASCADE`, `CheckConstraint`), CRUD & toàn vẹn dữ liệu, và Zero File-Overlap.
  - Cập nhật trạng thái hoàn thành WBS `1.3.5.1` trong [ROADMAP.md](ROADMAP.md) và ghi nhật ký tại [SESSION_LOG.md](SESSION_LOG.md).
- **Quyết định chốt:**
  - Dùng `down_revision = None` + `depends_on = ("20261126_0001_core",)` kèm `branch_labels = ("ai",)` để `core@head` và `ai@head` hoàn toàn độc lập khi `Dev Fullstack` và `AI Dev` tạo migration song song, đồng thời `alembic upgrade heads` vẫn chạy đúng thứ tự `core` trước `ai`.
- **Vấn đề / Blocker:**
  - Không có blocker; Docker daemon chưa bật trên máy local nên kiểm thử SQLite online + xuất DDL PostgreSQL offline (`alembic upgrade heads --sql`).
- **Kiểm thử đã chạy:**
  - Back-end `pytest -v`: toàn bộ test `tests/core/` và `tests/ai/` đạt.
  - `alembic heads` hiển thị 2 head độc lập (`20261126_0001_core (core)` và `20261127_0001_ai (ai)`).
- **Bước tiếp theo:**
  1. AI Dev tự tạo nhánh theo quy ước Jira `MC-<số>` từ `develop`, commit và push lên GitHub để mở PR vào `develop`.
  2. Triển khai tiếp task `1.3.5.2`: Benchmark `>= 2` model Ollama trên `>= 10` câu tiếng Việt & dựng `OllamaClient` + `/api/v1/chat/health`.

### [2026-11-26 18:25 GMT+7] — Antigravity AI + PM/SM (Trần Hoàng Phúc) | Nhánh: `MC-70-pm-lưu-baseline-ms-project-m-2-lập-do-r-do-d-sổ-rủi-ro-va-chốt-sandbox` | Jira: `MC-70`
- **Mục tiêu phiên:** Giải thích nhiệm vụ `MC-70` cho PM/SM và hoàn tất toàn bộ 4 đầu ra của `MC-70` (Baseline MS Project `M2`, bộ tiêu chí `DoR/DoD v1.0`, `Sổ rủi ro v1.0`, phê duyệt chốt cổng thanh toán Sandbox + Email/SMS theo đề xuất của Dev Fullstack ở `MC-69`).
- **Đã hoàn thành:**
  - Trích xuất 100% bảng WBS (`164` dòng, `640` giờ công, `BAC = 63.625.000 VNĐ`), `4` tài nguyên (`50%` Max Units) và `105` phân công từ [WBS 56 ngày](references/WBS_QL09-W_Website_Dat_Ban_Nha_Hang_Chatbot_AI_56Ngay.xlsx) sang tệp chuẩn Microsoft Project XML [MS_PROJECT_BASELINE_M2.xml](MS_PROJECT_BASELINE_M2.xml) đã nhúng sẵn `<Baseline><Number>0</Number>...</Baseline>` trên mọi Task, Resource và Assignment.
  - Tạo [BASELINE_M2_REPORT.md](BASELINE_M2_REPORT.md) tổng hợp 3 đường cơ sở Phạm vi – Tiến độ – Chi phí (`BAC = 63.625.000 VNĐ`, Dự phòng `6.362.500 VNĐ`, tổng `69.987.500 VNĐ`), bảng `PV` lũy kế EVM Sprint 0–7 và hướng dẫn mở `.xml` lưu `.mpp` trong MS Project.
  - Ban hành [DOR_DOD_QUALITY.md](DOR_DOD_QUALITY.md) (`DoR/DoD v1.0` ở 3 cấp Story/Sprint/Release, checklist Luật thép kỹ thuật, lịch Scrum `WBS 1.3.1.2` và quy trình `CR/CCB` sau mốc `M2`).
  - Lập [RISK_REGISTER.md](RISK_REGISTER.md) (`v1.0`) với ma trận đánh giá `5 × 5` và `12` rủi ro chi tiết (`R01`–`R12`), gắn người phụ trách và phương án ứng phó.
  - Cập nhật [PAYMENT_EMAIL_SMS_RESEARCH.md](PAYMENT_EMAIL_SMS_RESEARCH.md) ghi nhận quyết định phê duyệt chính thức ngày `26/11/2026` của PM/SM (`MC-70`) đối với đề xuất của Dev Fullstack (`VNPay Sandbox` chính, `MoMo Sandbox` dự phòng, `Brevo + Mailpit` Email, `SpeedSMS/eSMS <= 200.000 VNĐ` bật qua `SMS_ENABLED`).
  - Cập nhật đồng bộ trạng thái mốc `M2` và tick `[x]` task `MC-70` trong [ROADMAP.md](ROADMAP.md).
- **Quyết định chốt:**
  - Chốt **VNPay Sandbox** (chính) + **MoMo Sandbox** (dự phòng); **Brevo Free + Mailpit** (Email); **SpeedSMS/eSMS gói `<= 200.000 VNĐ`** (`SMS_ENABLED`) cho nhắc lịch `2h`.
  - Khóa Baseline `M2` (`56 ngày`, `640h`, `45 US MVP = 202 SP`, `BAC = 63.625.000 VNĐ`); mọi thay đổi sau `29/11/2026` đi qua quy trình `CR/CCB`.
- **Vấn đề / Blocker:**
  - Máy hiện tại chưa cài đặt `Microsoft Project` (`WINPROJ.EXE`), vì vậy đã xuất sẵn định dạng chuẩn `.xml` MSPDI kèm Baseline `0` để PM mở bằng Microsoft Project trên máy cá nhân/trường và `Save As .mpp` đính kèm ảnh chụp lên Jira `MC-70`.
- **Kiểm thử đã chạy:**
  - Kiểm tra tự động parse XML `MS_PROJECT_BASELINE_M2.xml` (`164` Task, `640h`, `BAC = 63.625.000 VNĐ`, `4` Resource, `105` Assignment có đủ `Baseline 0`), kiểm tra liên kết Markdown nội bộ, quy chuẩn nhánh PR `MC` và `git status` chỉ trong `docs/`.
- **Bước tiếp theo:**
  1. PM push nhánh `MC-70-...` lên GitHub và mở Pull Request `[MC-70] [PM] Lưu Baseline MS Project (M2), lập DoR/DoD, Sổ rủi ro và chốt Sandbox` vào `develop`.
  2. Mở [MS_PROJECT_BASELINE_M2.xml](MS_PROJECT_BASELINE_M2.xml) bằng Microsoft Project → `Save As .mpp` và chụp ảnh Tracking Gantt / Resource Sheet đính kèm vào Jira `MC-70`.
  3. Theo dõi `Dev Fullstack` (`US-05`..`US-08`), `PO/BA` (`US-03`) và `AI Dev` (`ai_models.py`, benchmark Ollama) hoàn thành Sprint 1 trước mốc `M2 (29/11/2026)`.

### [2026-11-26 16:11 GMT+7] — Antigravity AI + Dev Fullstack (Nguyễn Văn Tiến) | Nhánh: `MC-14-us-04-dang-ky-tai-khoản` | Jira: `MC-14`
- **Mục tiêu phiên:** Đồng bộ nhánh `MC-14` lên `origin/develop` (sau PR #13) và triển khai trọn vẹn **`[US-04]` Đăng ký tài khoản** (`FR-01`: chống trùng Email/SĐT, băm mật khẩu `bcrypt`, gửi & xác thực email một lần, báo lỗi rõ theo từng trường nhập).
- **Đã hoàn thành:**
  - Xây dựng [security.py](../backend/app/core/security.py): băm mật khẩu một chiều bằng `bcrypt` (`rounds=12`) và sinh/băm token một lần bằng `SHA-256`.
  - Xây dựng [email_service.py](../backend/app/services/email_service.py): hỗ trợ 3 chế độ gửi mail (`console` cho local/test, `smtp`/Mailpit và `brevo` REST API) kèm tự động retry tối đa `3 lần` theo `MC-69`.
  - Xây dựng [auth_schemas.py](../backend/app/schemas/auth_schemas.py), [auth_service.py](../backend/app/services/auth_service.py), [auth_router.py](../backend/app/api/v1/auth_router.py) và bộ chuẩn hóa lỗi tiếng Việt trong [main.py](../backend/app/main.py): mở `POST /api/v1/auth/register` (`201`/`409`/`422`), `POST /api/v1/auth/verify-email` và `POST /api/v1/auth/resend-verification`; tự động chuẩn hóa SĐT Việt Nam (`+84...` → `0...`) và email thường để ngăn đăng ký trùng.
  - Xây dựng giao diện [RegisterPage.tsx](../frontend/src/pages/RegisterPage.tsx) và [VerifyEmailPage.tsx](../frontend/src/pages/VerifyEmailPage.tsx) bám sát Figma (`11_dang_ky.png` Desktop & `13_dang_ky_dien_thoai.png` Mobile): nút `Hiện/Ẩn` mật khẩu, validate tức thì trên trình duyệt kết hợp tô đỏ đúng trường lỗi trả về từ API (`field_errors`), gợi ý chuyển sang Đăng nhập khi trùng email.
  - Viết bộ kiểm thử tự động [test_auth_register.py](../backend/tests/core/test_auth_register.py) & [RegisterPage.test.tsx](../frontend/src/test/RegisterPage.test.tsx); cập nhật [ROADMAP.md](ROADMAP.md).
- **Quyết định chốt:**
  - Dùng thư viện `bcrypt` trực tiếp (thay `passlib` không còn tương thích Python 3.13+) và chỉ lưu `SHA-256(token)` vào `password_reset_tokens` (`purpose='email_verify'`, hạn `24h`).
- **Vấn đề / Blocker:**
  - Không có blocker.
- **Kiểm thử đã chạy:**
  - Back-end `pytest -v`: **`13 passed`** (`4` test `US-01` + `5` test `US-02` + `4` test `US-04`).
  - Front-end `npm test` (`vitest run`): **`5 passed`** (`2` test `US-01` + `3` test `US-04`); `npm run build` (`tsc -b && vite build`): **thành công (`0` lỗi)**.
- **Bước tiếp theo:**
  1. Commit, push nhánh `MC-14-us-04-dang-ky-tai-khoản` và mở PR `[MC-14] [US-04] Triển khai đăng ký tài khoản khách hàng và xác thực email` vào `develop`.
  2. Triển khai tiếp `US-05` (Đăng nhập & đăng xuất bằng Email/SĐT, JWT có hạn, điều hướng 3 vai trò, khóa tạm 15 phút sau 5 lần sai).

### [2026-11-26 15:45 GMT+7] — Antigravity AI + Dev Fullstack (Nguyễn Văn Tiến) | Nhánh: `MC-13-us-02-erd-va-migration-csdl` | Jira: `MC-13`
- **Mục tiêu phiên:** Đồng bộ nhánh `MC-13` với `origin/develop` và triển khai trọn vẹn **`[US-02]` ERD và migration CSDL** (ERD lưu trong repo, Alembic tạo đủ bảng trên CSDL trống, ràng buộc CSDL chống trùng bàn), đồng thời xử lý cảnh báo GitGuardian cho biến môi trường mẫu.
- **Đã hoàn thành:**
  - Đồng bộ fast-forward `MC-13` lên `origin/develop` (`1fdf3dd`) và khôi phục [README.md](../README.md) bị rỗng sau merge trước đó.
  - Tạo [docs/ERD.md](ERD.md) lưu sơ đồ Mermaid ERD 16 bảng (13 Core + 3 AI), từ điển ràng buộc toàn vẹn, cơ chế `btree_gist` chống trùng bàn và hướng dẫn vận hành Alembic đa nhánh.
  - Xây dựng đầy đủ **13 bảng ORM Core** tại [core_models.py](../backend/app/models/core_models.py) (`users`, `password_reset_tokens`, `categories`, `dishes`, `dish_price_history`, `areas`, `tables`, `reservations`, `reservation_items`, `deposit_transactions`, `reservation_audit_logs`, `notifications`, `business_configs`) với `TIMESTAMPTZ`, tiền nguyên `VNĐ`, `ON DELETE RESTRICT` chống xóa món/bàn đã có đơn, `unit_price_locked` và `provider_txn_id` unique chống trùng webhook.
  - Thiết lập [alembic.ini](../backend/alembic.ini), [alembic/env.py](../backend/alembic/env.py) (tự động nạp `ai_models.py` không cần sửa file Core) và tạo migration khởi tạo [20261126_0001_core_initial_schema.py](../backend/alembic/versions/20261126_0001_core_initial_schema.py) gắn `branch_labels = ("core",)` kèm `CREATE EXTENSION IF NOT EXISTS btree_gist` và `EXCLUDE USING gist` `ex_reservations_no_overlapping_table_slot`.
  - Thay chuỗi mẫu `emenu_secret` bằng placeholder chuẩn `changeme` trong `.env.example`, `backend/.env.example`, `docker-compose.yml` và loại bỏ mật khẩu mặc định trong `config.py` để không kích hoạt cảnh báo GitGuardian.
  - Viết bộ kiểm thử [test_migrations_and_models.py](../backend/tests/core/test_migrations_and_models.py) và cập nhật [ROADMAP.md](ROADMAP.md).
- **Quyết định chốt:**
  - Dùng `branch_labels = ("core",)` cho chuỗi migration của Dev Fullstack và `alembic upgrade heads` để AI Dev có thể tạo nhánh migration `ai` độc lập 100% (Zero File-Overlap).
  - Bổ sung trạng thái `need_refund` và `refunded` vào `deposit_transactions.status` khớp báo cáo khảo sát VNPay Sandbox (`MC-69`).
- **Vấn đề / Blocker:**
  - Không có blocker về code/test; cần ít nhất `1` thành viên trong nhóm review PR `MC-13` trên GitHub để hoàn tất điều kiện DoD cuối cùng của `US-02`.
- **Kiểm thử đã chạy:**
  - Back-end `pytest -v`: **`9 passed`** (`4` test `US-01` + `5` test `US-02`: kiểm tra `docs/ERD.md`, `alembic upgrade heads` & `downgrade base` trên CSDL trống, xuất DDL PostgreSQL kiểm chứng `btree_gist` & `EXCLUDE USING gist`, kiểm chứng chặn trùng khung giờ & giải phóng khi `expired`, kiểm chứng `ON DELETE RESTRICT` & `provider_txn_id` idempotent).
- **Bước tiếp theo:**
  1. Commit, push nhánh `MC-13-us-02-erd-va-migration-csdl` và mở PR `[MC-13] [US-02] Thiết kế ERD và khởi tạo Alembic migration 13 bảng Core` vào `develop` (nhờ `>= 1` thành viên review).
  2. Triển khai tiếp `US-04` (Đăng ký tài khoản) và `US-05` (Đăng nhập/Đăng xuất + JWT + khóa 15p).

### [2026-11-26 14:55 GMT+7] — Antigravity AI + Dev Fullstack (Nguyễn Văn Tiến) | Nhánh: `MC-11-us-01-khung-dự-an-va-kiến-truc` | Jira: `MC-11`
- **Mục tiêu phiên:** Rà soát bộ 13 màn hình thiết kế Figma mới, tổng hợp lộ trình công việc của Dev Fullstack và triển khai trọn vẹn **`[US-01]` Khung dự án và kiến trúc** (`MC-11`, kiêm hoàn tất skeleton Sprint 0 `1.1.3.2`).
- **Đã hoàn thành:**
  - Cấu hình [.gitignore](../.gitignore) bỏ qua thư mục `figma/` (chỉ lưu local để xem khi code), `.env`, `.venv/`, `node_modules/`, `dist/`.
  - Thiết lập [docker-compose.yml](../docker-compose.yml), [.env.example](../.env.example) và [01_init_extensions.sql](../docker/postgres/init/01_init_extensions.sql) cho PostgreSQL 16 (tự động bật `btree_gist` và múi giờ `Asia/Ho_Chi_Minh`).
  - Khởi tạo `backend/` (FastAPI + SQLAlchemy 2.0 + Pydantic v2 + `psycopg[binary]`): chuẩn hóa `GMT+7` & `VNĐ`, kết nối DB qua `SELECT 1` (đồng bộ session timezone PostgreSQL), mở `GET /health` (`200 OK`), Swagger `/docs`, `GET /api/v1/system/overview`, `GET /api/v1/system/db-check`, và cơ chế tự động gắn `chat_router.py` của AI Dev đảm bảo Zero File-Overlap.
  - Khởi tạo `frontend/` (React 18 + Vite + TypeScript + Tailwind CSS + React Router v6 + TanStack Query + Axios + Vitest): cấu hình Design Tokens Vườn Phố (`#1E4332`, `#F8F7F3`, font Serif/Sans), dựng `CustomerLayout`, `OperationsLayout` và `HomePage` gọi trực tiếp `/health` & `/api/v1/system/overview`.
  - Cập nhật [README.md](../README.md) hướng dẫn đầy đủ cách chạy bằng Docker Compose và chạy trực tiếp trên máy local; tick hoàn thành `US-01` & task skeleton trong [ROADMAP.md](ROADMAP.md).
- **Quyết định chốt:**
  - Giữ thư mục `figma/` (13 file PNG) ở máy local trong `.gitignore` theo yêu cầu của Dev Fullstack.
  - Dùng driver `psycopg[binary]` v3 để tương thích đồng thời Python 3.12 (Docker/CI) và Python 3.14 trên Windows local mà không cần trình biên dịch C.
- **Vấn đề / Blocker:**
  - Máy Windows local hiện chưa cài Docker Desktop / PostgreSQL 16; cần cài Docker Desktop trước khi chạy migration thực tế ở `US-02`.
- **Kiểm thử đã chạy:**
  - Back-end: `pytest -v` → **`4 passed`** (`/health` 200, Swagger `/docs` & `/openapi.json`, `/api/v1/system/overview`, `/api/v1/system/db-check` 200/503).
  - Front-end: `npm test` (`vitest run`) → **`2 passed`**; `npm run build` (`tsc -b && vite build`) → **thành công (`0` lỗi TypeScript)**.
- **Bước tiếp theo:**
  1. Commit thay đổi trên nhánh `MC-11-us-01-khung-dự-an-va-kiến-truc`, push và mở PR `[MC-11] [US-01] Khởi tạo khung dự án và kiến trúc FE/BE/PostgreSQL` vào `develop`.
  2. Cài Docker Desktop (hoặc PostgreSQL 16) để chuẩn bị cho `US-02` (ERD 13 bảng Core + Alembic migration + constraint `btree_gist`).
  3. Triển khai tiếp chuỗi xác thực & phân quyền `US-04` → `US-07` và CI `US-08` trong Sprint 1.

### [2026-11-24 20:15 GMT+7] — Antigravity AI + PM | Nhánh: `MC-65-pm-khởi-tạo-...` | Jira: `MC-65`
- **Mục tiêu phiên:** Đọc toàn bộ 7 tài liệu Word/Excel hiện có và thiết lập bộ 4 tài liệu Markdown chuẩn hóa phục vụ AI Agent, Dev Fullstack, AI Dev và truy vết QLDA.
- **Đã hoàn thành:**
  - Đọc đầy đủ 7 tài liệu gốc (`PHAT_BIEU_BAI_TOAN`, `TON_CHI_DU_AN`, `PHAT_BIEU_PHAM_VI`, `SRS v1.1`, `Product Backlog`, `Tong_Hop_Jira_Backlog_v2.xlsx`, `WBS_56Ngay.xlsx`) và cấu hình repo (`README.md`, `CONTRIBUTING.md`, `.github/`).
  - Di chuyển 7 file `.docx`/`.xlsx` gốc vào `docs/references/` để lưu tạm trước khi PM loại bỏ.
  - Xóa file rỗng `sqlite_mcp_server.db` (`0 bytes`).
  - Tạo [AGENTS.md](../AGENTS.md) ở thư mục gốc (`<= 100` dòng) quy định Tech Stack, Zero File-Overlap, luật thép nghiệp vụ/bảo mật, GitFlow/Jira `MC` và quy trình cập nhật docs.
  - Tạo [docs/SYSTEM_SPEC.md](SYSTEM_SPEC.md) tự chứa 100%: bài toán, KPI, In/Out-of-Scope, Make-or-Buy, kiến trúc + Mermaid, Chatbot AI 5 lớp, phân quyền, vòng đời 7 trạng thái, đủ `18 FR` (`FR-01`–`FR-18`), `6 NFR` (`NFR-01`–`NFR-06`), `[Đề xuất kỹ thuật]` ERD 16 bảng + constraint `btree_gist` + Chat API Contract, ma trận truy vết & DoD.
  - Tạo [docs/ROADMAP.md](ROADMAP.md) tự chứa 100%: nhân sự 4 thành viên (`640h`), 10 Component Jira, ngân sách `69.987.500 VNĐ` + PV/EVM, 8 mốc `M1–M6`, 10 Epic, trọn bộ `45 US MVP` (`202 SP`) + `26 Task` chia theo Sprint 0–7, `9 US dự phòng` (`50 SP`), Scrum/DoR/DoD/CR-CCB & Sổ rủi ro.
  - Khởi tạo `docs/SESSION_LOG.md` và cập nhật mục liên kết tài liệu trong [README.md](../README.md).
- **Quyết định chốt:**
  - Chuẩn hóa mã Jira toàn repo theo **`MC`** (thay `SCRUM`/`QL` trong tài liệu gốc).
  - Chuẩn hóa nhân sự **4 thành viên** (`PM/SM`, `PO/BA`, `Dev Fullstack`, `AI Dev` — bỏ bản nháp 5 thành viên `TV1–TV5`).
  - Gắn nhãn rõ `[Đề xuất kỹ thuật]` cho các phần thiết kế chi tiết chưa có trong SRS (Vite/TS/Tailwind, SQLAlchemy 2.0, ERD 16 bảng, Chat Contract).
- **Vấn đề / Blocker:**
  - Nhánh Git hiện tại không khớp regex CI `.github/workflows/pr-check.yml` (cần tạo nhánh `docs/MC-65-init-project-docs` trước khi mở PR).
- **Kiểm thử đã chạy:**
  - Kiểm tra cấu trúc thư mục, độ dài `AGENTS.md` (`<= 100` dòng), quét đủ `18 FR`, `6 NFR`, `10 Epic`, `54 US` và kiểm tra không còn placeholder (`TBD`/`TODO`).
- **Bước tiếp theo:**
  1. Rà soát 4 file Markdown mới; sau khi hài lòng có thể xóa thư mục `docs/references/`.
  2. Chuyển sang nhánh chuẩn `docs/MC-65-init-project-docs`, commit và mở PR vào `develop`.
  3. Hoàn tất 3 task kỹ thuật còn lại của Sprint 0 (skeleton FE/BE/PG, khảo sát Sandbox, cài Ollama local + chốt Chat Contract) để bắt đầu **Sprint 1 (`US-01`..`US-08`)**.
