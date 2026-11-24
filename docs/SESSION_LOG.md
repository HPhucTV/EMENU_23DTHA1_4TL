# NHẬT KÝ PHIÊN LÀM VIỆC & BÀN GIAO NGỮ CẢNH (SESSION LOG)

> AI Agent và thành viên nhóm **BẮT BUỘC** đọc mục **Current Snapshot** trước khi bắt đầu phiên mới, và thêm một Entry mới lên **trên cùng** danh sách nhật ký sau khi kết thúc phiên. Không xóa các Entry cũ.

---

## Current Snapshot (Cập nhật: 24/11/2026 — `GMT+7`)

| Hạng mục | Trạng thái hiện tại |
| :--- | :--- |
| **Sprint hiện tại** | **Sprint 0** *(đang hoàn tất M1 → chuẩn bị mở Sprint 1)* |
| **Mốc kế tiếp** | Hoàn tất `M1` (Sprint 0) → **M2: Lưu Baseline MS Project (`29/11/2026`)** |
| **Tiến độ mã nguồn** | Đã có GitFlow, PR template, CI convention check; **chưa khởi tạo code `frontend/`, `backend/`** |
| **Hồ sơ & Tài liệu** | Đã chuẩn hóa thành 4 file tự chứa: `AGENTS.md`, `docs/SYSTEM_SPEC.md`, `docs/ROADMAP.md`, `docs/SESSION_LOG.md` |
| **Quy ước đã chốt** | Jira key **`MC`** (`MC-xx`); nhóm **4 thành viên** (`PM/SM`, `PO/BA`, `Dev Fullstack`, `AI Dev`); kiến trúc Zero File-Overlap; đề xuất stack S1 (Vite+TS+Tailwind, FastAPI+SQLAlchemy2+Pydantic v2, PG16+`btree_gist`) |

### Cảnh báo kỹ thuật & Blocker cần xử lý ngay
1. **Đã xử lý regex CI cho nhánh tạo từ Jira**: Workflow `.github/workflows/pr-check.yml` đã được nới lỏng để hỗ trợ cả nhánh tạo trực tiếp từ Jira (`MC-<số>-<mô-tả-có-dấu>`) bên cạnh chuẩn `<type>/MC-<số>-<mô-tả>`. Sau khi đưa thay đổi `pr-check.yml` lên nhánh mặc định/PR (`develop`), bấm **Re-run jobs** trên PR #3 để CI báo xanh.
2. **Đầu việc kỹ thuật cuối của Sprint 0 cần chốt trước khi vào Sprint 1**:
   - `[FS]` Dựng skeleton `frontend/` + `backend/` + `docker-compose.yml` (PostgreSQL) & hoàn tất khảo sát Payment Sandbox (VNPay/MoMo/PayOS).
   - `[AI]` Cài Ollama local, kéo thử `>= 2` model tiếng Việt & xác nhận Chat API JSON Contract `/api/v1/chat/messages`.

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
