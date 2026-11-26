# EMENU_23DTHA1_4TL — Nhà hàng Ẩm thực Vườn Phố (`QL09-W`)

Hệ thống **Website đặt bàn và đặt món trước cho nhà hàng tích hợp chatbot AI** — Lớp `23DTHA1`, Nhóm `4TL`.  
Chuẩn hóa vận hành tại **TP. Hồ Chí Minh**, tiền tệ **`VNĐ` (`₫`)**, múi giờ **`GMT+7` (`Asia/Ho_Chi_Minh`)**.

---

## 1. Tech Stack & Kiến trúc

| Tầng | Công nghệ triển khai |
| :--- | :--- |
| **Front-end** | React 18 + Vite + TypeScript + Tailwind CSS + React Router v6 + TanStack Query + Axios + Vitest |
| **Back-end** | Python 3.12+ + FastAPI (Swagger `/docs`) + SQLAlchemy 2.0 + Pydantic v2 + Alembic + Pytest |
| **Cơ sở dữ liệu** | PostgreSQL 16 + tiện ích `btree_gist` (ràng buộc chống trùng bàn `FR-05`, 13 bảng Core + 3 bảng AI) |
| **Chatbot AI** | Ollama self-host (LLM mở, RAG từ PostgreSQL, PII Masking — phân vùng độc lập của `AI Dev`) |
| **Hạ tầng & CI** | Docker Compose + GitHub Actions (`.github/workflows/`) |

---

## 2. Hướng dẫn cài đặt & chạy dự án

### Cách 1: Chạy toàn bộ bằng Docker Compose (Khuyên dùng)

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Sau khi container khởi động, chạy migration tạo bảng trên PostgreSQL:
```powershell
docker compose exec backend alembic upgrade heads
```

Các địa chỉ truy cập:
- **Giao diện Web (Front-end):** http://localhost:5173
- **Tài liệu API (Swagger UI):** http://localhost:8000/docs
- **Health Check API (`200 OK`):** http://localhost:8000/health
- **API tổng quan mẫu:** http://localhost:8000/api/v1/system/overview

---

### Cách 2: Chạy trực tiếp trên máy Local

#### Bước 1: Chuẩn bị PostgreSQL 16 & Migration
```powershell
cd backend
Copy-Item .env.example .env
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Chạy Alembic tạo đủ 13 bảng Core và constraint chống trùng bàn trên CSDL trống
.\.venv\Scripts\python.exe -m alembic upgrade heads

# Khởi chạy FastAPI
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

#### Bước 2: Khởi chạy Front-end React Vite (`cổng 5173`)
```powershell
cd frontend
Copy-Item .env.example .env
npm install
npm run dev
```

---

## 3. Chạy kiểm thử tự động (Tests & Build)

```powershell
# Kiểm thử Back-end (Health, Swagger, ORM 13 bảng, Alembic Migration & Chống trùng bàn)
cd backend
.\.venv\Scripts\python.exe -m pytest -v

# Kiểm thử & Build Front-end
cd ../frontend
npm test
npm run build
```

---

## 4. Quản lý dự án & Tài liệu tham chiếu
- **Jira Board (`MC`):** [ManageProject_Check (MC)](https://tranhoangphuc98765432.atlassian.net/jira/software/c/projects/MC/boards/9/backlog)
- [CONTRIBUTING.md](./CONTRIBUTING.md) — Quy trình GitFlow, Pull Request & tự động hóa Jira `MC`
- [AGENTS.md](./AGENTS.md) — Quy tắc thực thi cho AI Agent & Dev (Zero File-Overlap, Luật nghiệp vụ)
- [docs/ERD.md](./docs/ERD.md) — Sơ đồ thực thể liên kết (ERD 16 bảng), đặc tả cột & hướng dẫn Alembic (`US-02`)
- [docs/SYSTEM_SPEC.md](./docs/SYSTEM_SPEC.md) — Đặc tả hệ thống (`18 FR`, `6 NFR`, AI 5 lớp & API Contract)
- [docs/ROADMAP.md](./docs/ROADMAP.md) — Lộ trình 8 Sprint, `54 User Story`, `26 Task`, WBS & EVM
- [docs/PAYMENT_EMAIL_SMS_RESEARCH.md](./docs/PAYMENT_EMAIL_SMS_RESEARCH.md) — Khảo sát VNPay Sandbox, Brevo Email & SpeedSMS (`MC-69`)
- [docs/SESSION_LOG.md](./docs/SESSION_LOG.md) — Nhật ký phiên làm việc & Current Snapshot
