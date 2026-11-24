# AGENTS.md — EMENU_23DTHA1_4TL (`QL09-W`)

Dự án **Website đặt bàn và đặt món trước cho nhà hàng tích hợp chatbot AI** — Nhà hàng Ẩm thực Vườn Phố (TP.HCM, tiền tệ `VNĐ`, múi giờ `GMT+7`).

## Bản đồ tài liệu
| Tài liệu | Mục đích |
| :--- | :--- |
| [docs/SYSTEM_SPEC.md](docs/SYSTEM_SPEC.md) | Đặc tả hệ thống, 18 FR, 6 NFR, AI 5 lớp, ERD & Chat API Contract |
| [docs/ROADMAP.md](docs/ROADMAP.md) | Lộ trình 8 Sprint, 54 User Story, 26 Task, WBS, Ngân sách & EVM |
| [docs/SESSION_LOG.md](docs/SESSION_LOG.md) | Trạng thái hiện tại (Current Snapshot), Blocker & nhật ký phiên |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Quy trình GitFlow, Pull Request & tự động hóa Jira `MC` |

## Tech Stack
| Thành phần | `[SRS Chốt]` | `[Đề xuất kỹ thuật S1]` |
| :--- | :--- | :--- |
| Front-end | ReactJS (Responsive Web) | React 18 + Vite + TypeScript + Tailwind CSS + TanStack Query + Vitest |
| Back-end | Python FastAPI (Swagger, JWT, RBAC) | Python 3.12 + SQLAlchemy 2.0 + Pydantic v2 + Pytest + APScheduler |
| Database | PostgreSQL + Alembic (ERD >= 8 bảng) | PostgreSQL 16 + `btree_gist` (constraint chống trùng bàn) |
| Chatbot AI | Ollama self-host (không fine-tune), RAG | Benchmark chốt model tối ưu tiếng Việt tại `US-15` |
| Infra & CI | Docker, Cloud/VPS, Sandbox, Email/SMS | GitHub Actions CI (`.github/workflows/pr-check.yml`) |

## Phân vùng Zero File-Overlap
- **Dev Fullstack**: `frontend/`, `backend/app/core/`, `backend/app/api/` (trừ `chat_router.py`), `backend/app/services/`, `backend/app/models/core_models.py`, `backend/scripts/seed_core.py`, `docker-compose.yml`.
- **AI Dev**: `backend/app/ai/`, `backend/app/api/v1/chat_router.py`, `backend/app/models/ai_models.py`, `alembic/versions/*_ai_*`, `backend/scripts/seed_ai.py`, `ollama/`, `docker-compose.ollama.yml`.
- **Ranh giới tích hợp**: AI chỉ gọi read-only `availability_service` (`FR-05`) và giao tiếp FE qua `/api/v1/chat/*`. Không sửa file ngoài phân vùng khi chưa thống nhất qua PR.

## Luật thép kỹ thuật & nghiệp vụ
- **Thời gian & Tiền tệ**: Chuẩn hóa `GMT+7` và `VNĐ` trên toàn bộ API, DB và UI.
- **Chống trùng bàn**: Kiểm tra & giữ chỗ tạm `10 phút` (bước `30p`, lượt `90p`, đặt trước `2h–30 ngày`) trong cùng DB transaction + constraint PostgreSQL.
- **Đặt món & Xóa mềm**: Lưu giá chốt `unit_price_locked` khi xác nhận món; chỉ dùng `soft delete` cho món/bàn; chặn xóa món/bàn đã có đơn liên quan.
- **Bảo mật & Thanh toán**: RBAC 3 vai trò (`customer`, `staff`, `manager`) ép ở tầng API (`403` + audit log); băm mật khẩu `bcrypt/Argon2`; khóa `15p` sau `5` lần sai; không lưu số thẻ; webhook thanh toán bắt buộc xác thực HMAC và xử lý idempotent.
- **AI Guardrails**: RAG chỉ truy xuất PostgreSQL thực tế; **PII Masking** (họ tên, SĐT, email) TRƯỚC khi gửi Ollama; từ chối ngoài phạm vi/y tế/dị ứng; không báo "đã đặt thành công" khi server chưa xác nhận; lỗi/timeout trả `is_fallback: true`; lưu log chat tối đa `90 ngày`.
- **Cấm Out-of-Scope**: Không làm POS/VAT, quản lý kho/nguyên liệu, nhân sự/chấm công, delivery/take-away, native app iOS/Android, thanh toán tiền thật hay fine-tune LLM.

## Quy ước GitFlow & Jira (`MC`)
- Nhánh tách từ `develop`: `[<feature|fix|hotfix|docs|chore|refactor|test>/]MC-<số>-<mô-tả>` (hỗ trợ cả nhánh tự sinh từ Jira có dấu tiếng Việt).
- Commit: `MC-<số> [<PM|BA|FS|AI|US-xx>] <Mô tả>` (VD: `MC-65 [PM] Khởi tạo Jira (SCRUM), MS Project, Kick-off và Bộ tài liệu D01/D14/D17`). PR title: `[MC-<số>] <Mô tả>` → đích `develop` (`main` chỉ nhận từ `develop`, `release/*`, `hotfix/*`).
- Lưu ý: Tài liệu gốc từng ghi `SCRUM`/`QL`, nhưng repo và CI chạy thống nhất theo mã **`MC`**.

## Quy trình bắt buộc cho AI Agent
1. Đọc `docs/SESSION_LOG.md` (mục *Current Snapshot*) và `docs/ROADMAP.md` trước khi thực thi.
2. Đối chiếu FR/NFR/schema tại `docs/SYSTEM_SPEC.md`; không tự phát sinh tính năng ngoài scope.
3. Chạy kiểm thử liên quan trước khi kết thúc; cập nhật `docs/SESSION_LOG.md` và tick `[x]` trong `docs/ROADMAP.md` sau mỗi phiên.

## Commit Attribution
AI commits MUST include:
```text
Co-Authored-By: Antigravity AI <noreply@example.com>
```
