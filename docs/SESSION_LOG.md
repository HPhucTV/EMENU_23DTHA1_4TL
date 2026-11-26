# NHẬT KÝ PHIÊN LÀM VIỆC & BÀN GIAO NGỮ CẢNH (SESSION LOG)

> AI Agent và thành viên nhóm **BẮT BUỘC** đọc mục **Current Snapshot** trước khi bắt đầu phiên mới, và thêm một Entry mới lên **trên cùng** danh sách nhật ký sau khi kết thúc phiên. Không xóa các Entry cũ.

---

## Current Snapshot (Cập nhật: 26/11/2026 — `GMT+7`)

| Hạng mục | Trạng thái hiện tại |
| :--- | :--- |
| **Sprint hiện tại** | **Sprint 1** *(đang triển khai `EP-01`, hướng tới mốc `M2` ngày `29/11/2026`)* |
| **Mốc kế tiếp** | **M2: Lưu Baseline MS Project (`29/11/2026`)** + hoàn tất `US-05`..`US-08` |
| **Tiến độ mã nguồn** | Đã hoàn tất **`US-01` (`MC-11` — merged)**, **`US-02` (`MC-13` — merged)** và **`US-04` (`MC-14`)**: Đăng ký tài khoản khách hàng (`POST /api/v1/auth/register`, `/verify-email`, `/resend-verification`), băm mật khẩu `bcrypt`, chống trùng Email/SĐT chuẩn hóa VN, gửi email xác thực một lần và giao diện `RegisterPage` / `VerifyEmailPage` khớp Figma |
| **Hồ sơ & Tài liệu** | Đã có `AGENTS.md`, `docs/SYSTEM_SPEC.md`, `docs/ERD.md`, `docs/ROADMAP.md`, `docs/SESSION_LOG.md`, `docs/PAYMENT_EMAIL_SMS_RESEARCH.md` (`MC-69`), Chat Contract (`MC-68`) & bộ ảnh Figma (`PR #10`) |
| **Quy ước đã chốt** | Jira key **`MC`** (`MC-xx`); nhóm **4 thành viên**; kiến trúc Zero File-Overlap; mật khẩu băm `bcrypt` (cost `12`), token xác thực một lần lưu băm `SHA-256` trong `password_reset_tokens` |

### Cảnh báo kỹ thuật & Blocker cần xử lý ngay
1. **Môi trường Docker / PostgreSQL trên máy Dev Fullstack**: Máy Windows hiện có sẵn `Node v24.17.0` và `Python 3.14` (`py`), nhưng **chưa cài Docker Desktop hoặc PostgreSQL 16**. Nên cài Docker Desktop để chạy PostgreSQL 16 + Mailpit local khi kiểm thử tích hợp thực tế.
2. **Đầu việc kế tiếp trong Sprint 1**:
   - `[FS]` Mở PR `MC-14` (`US-04`) vào `develop`, sau đó triển khai tiếp `US-05` (Đăng nhập/Đăng xuất bằng Email hoặc SĐT, cấp JWT, điều hướng 3 vai trò, khóa tạm 15 phút sau 5 lần sai), `US-06` (Quên mật khẩu), `US-07` (Phân quyền RBAC & quản lý tài khoản NV) và `US-08` (CI GitHub Actions).
   - `[AI]` Dựng `ai_models.py` + migration nhánh `ai` (`--branch-label ai --head 20261126_0001_core`), benchmark model Ollama.

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
