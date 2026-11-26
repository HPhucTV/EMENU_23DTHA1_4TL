# NHẬT KÝ PHIÊN LÀM VIỆC & BÀN GIAO NGỮ CẢNH (SESSION LOG)

> AI Agent và thành viên nhóm **BẮT BUỘC** đọc mục **Current Snapshot** trước khi bắt đầu phiên mới, và thêm một Entry mới lên **trên cùng** danh sách nhật ký sau khi kết thúc phiên. Không xóa các Entry cũ.

---

## Current Snapshot (Cập nhật: 26/11/2026 — `GMT+7`)

| Hạng mục | Trạng thái hiện tại |
| :--- | :--- |
| **Sprint hiện tại** | **Sprint 1** *(đang triển khai `EP-01`, hướng tới mốc `M2` ngày `29/11/2026`)* |
| **Mốc kế tiếp** | **M2: Lưu Baseline MS Project (`29/11/2026`)** + hoàn tất `US-02`..`US-08` |
| **Tiến độ mã nguồn** | Đã hoàn tất **`US-01` (`MC-11`)**: dựng xong `frontend/` (React 18 + Vite + TS + Tailwind), `backend/` (FastAPI + SQLAlchemy 2.0 + Pydantic v2 + `/health` + Swagger `/docs`), `docker-compose.yml` (PostgreSQL 16 + `btree_gist` + `GMT+7`), `.gitignore` & cập nhật `README.md` |
| **Hồ sơ & Tài liệu** | Bộ 4 file chuẩn hóa (`AGENTS.md`, `docs/SYSTEM_SPEC.md`, `docs/ROADMAP.md`, `docs/SESSION_LOG.md`) + 5 file hồ sơ BA (`MC-66` đã merge) |
| **Quy ước đã chốt** | Jira key **`MC`** (`MC-xx`); nhóm **4 thành viên** (`PM/SM`, `PO/BA`, `Dev Fullstack`, `AI Dev`); kiến trúc Zero File-Overlap; thư mục thiết kế `figma/` giữ ở local (`.gitignore`) để tham chiếu giao diện |

### Cảnh báo kỹ thuật & Blocker cần xử lý ngay
1. **Môi trường Docker / PostgreSQL trên máy Dev Fullstack**: Máy Windows hiện có sẵn `Node v24.17.0` và `Python 3.14` (`py`), nhưng **chưa cài Docker Desktop hoặc PostgreSQL 16**. Cần cài Docker Desktop (khuyên dùng, chạy `docker compose up --build`) hoặc PostgreSQL 16 để chạy migration thật ở `US-02`.
2. **Đầu việc kế tiếp trong Sprint 1**:
   - `[FS]` Mở PR `MC-11` (`US-01`) vào `develop`, sau đó triển khai `US-02` (13 bảng `core_models.py` + Alembic migration + constraint `btree_gist`), `US-04..07` (Auth & RBAC) và `US-08` (CI test workflow); gửi bảng so sánh Sandbox cho PM.
   - `[AI]` Dựng `ai_models.py` + migration `*_ai_*`, cài Ollama local & benchmark `>= 2` model tiếng Việt.

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
