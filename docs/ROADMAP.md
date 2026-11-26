# LỘ TRÌNH & KẾ HOẠCH THỰC THI DỰ ÁN (ROADMAP & WBS)

**Dự án:** Website đặt bàn và đặt món trước cho nhà hàng tích hợp chatbot AI (`QL09-W`)  
**Đơn vị áp dụng:** Nhà hàng Ẩm thực Vườn Phố (TP.HCM) \| **Thời gian:** `16/11/2026 – 10/01/2027` (`56 ngày` = `8 Sprint × 1 tuần`)

> Tài liệu này hợp nhất *WBS 56 ngày*, *Jira Backlog v2 (10 Epic, 54 User Story, 26 Task)*, *Bảng phân bổ tài nguyên* và *Đường cơ sở chi phí (PV/EVM)* thành nguồn theo dõi tiến độ duy nhất.  
> **Quy ước mã Jira:** Dự án trên GitHub/Jira chạy theo mã **`MC`** (`MC-xx`, khớp `CONTRIBUTING.md` & CI). Các mã `SCRUM` hoặc `QL` trong hồ sơ Word/Excel gốc được quy đổi thống nhất về `MC`.

---

## 1. Nhân sự, Component Jira, Ngân sách & Đường cơ sở EVM

### 1.1 Cơ cấu 4 thành viên & Nhà tài trợ (`640 giờ công` = `80 ngày công`)
*(Mỗi thành viên làm bán thời gian `50%`: `4 giờ/ngày`, `20 giờ/Sprint × 8 Sprint = 160 giờ/người`. Lịch làm việc `8:00–17:00`, nghỉ Tết Dương lịch `01/01/2027`, làm bù thứ Bảy `02/01/2027`.)*

| Vai trò | Họ và tên | Đơn giá (VNĐ/giờ) | Tổng giờ | Thành tiền (VNĐ) | Component Jira phụ trách |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **PM/SM** (Project Manager / Scrum Master) | **Trần Hoàng Phúc** *(MSSV: 2380601756)* | `100.000` | `160h` | `16.000.000` | `project-management`, `business-ops` |
| **PO/BA** (Product Owner / Business Analyst) | **Võ Đăng Khoa** | `87.500` | `160h` | `14.000.000` | `ba-analysis`, `ui-ux-design`, `qa-testing` |
| **Dev Fullstack** (Tech Lead FE/BE/DB/CI) | **Nguyễn Văn Tiến** | `100.000` | `160h` | `16.000.000` | `frontend`, `backend`, `database`, `deployment` |
| **AI Dev** (Kỹ sư AI Chatbot Ollama) | **Nguyễn Đoàn Trường Vũ** | `100.000` | `160h` | `16.000.000` | `ai-chatbot`, `database`, `backend`, `deployment` |
| **Nhà tài trợ (GVHD)** | **Nguyễn Hữu Trung** *(Khoa CNTT, HUTECH)* | — | — | — | Phê duyệt đề tài, Tôn chỉ, Ngân sách, CR lớn, Mốc `M1–M6` |

### 1.2 Phân bổ 10 Component Jira
| Component | Tài nguyên chính | Gói WBS liên quan | Phạm vi phụ trách |
| :--- | :--- | :--- | :--- |
| `frontend` | Dev Fullstack | `1.1.3.2`, `1.3.4`, `1.5.3–4`, `1.7.3.3`, `1.7.4.1`, `1.9.3–4`, `1.11.2.3.1`, `1.11.3`, `1.13.2.2.2`, `1.13.3` | ReactJS responsive, sơ đồ bàn kéo thả, form đặt bàn, giỏ món, ChatWidget & pre-fill URL |
| `backend` | Dev Fullstack / AI Dev | `1.1.3.2–3`, `1.3.4`, `1.5.3–4`, `1.7.3–4`, `1.9.3–5`, `1.11.3`, `1.13.3` | FastAPI REST API, Swagger, JWT/RBAC, giữ bàn chống trùng, Sandbox/Webhook, Email/SMS, `/api/v1/chat/*` |
| `database` | Dev Fullstack / AI Dev | `1.3.3.1`, `1.3.5.1`, `1.5.3.3`, `1.7.3.2`, `1.15.3.1` | ERD `>= 8` bảng, PostgreSQL, Alembic migration core & AI, ràng buộc chống trùng, seed & backup/restore |
| `ai-chatbot` | AI Dev | `1.1.4`, `1.3.5`, `1.5.5`, `1.7.5`, `1.9.5.1`, `1.11.2`, `1.13.2`, `1.15.1.2`, `1.15.3.2`, `1.15.4.2` | Ollama LLM self-host, benchmark model, RAG PostgreSQL, Parser `GMT+7`, PII Masker & Guardrails |
| `deployment` | Dev Fullstack / AI Dev | `1.1.3.1`, `1.3.3.3`, `1.9.4.2`, `1.9.5.1`, `1.15.3.1`, `1.15.3.3` | GitHub branch rules, CI GitHub Actions, Docker Compose Staging & Production `v1.0`, hardening HTTPS |
| `qa-testing` | PO/BA / AI Dev | `1.3.2.2`, `1.5.2.2`, `1.7.2.2`, `1.9.2`, `1.11.4.1`, `1.13.2.1.2`, `1.13.4.1`, `1.15.1–2` | `>= 40` test case chức năng/API, concurrent test, Guardrails & `>= 30` câu AI, nghiệm thu UAT |
| `ba-analysis` | PO/BA | `1.1.2.1–3`, `1.5.2.1`, `1.7.2.1`, `1.11.2.1.1`, `1.15.4.1` | Khảo sát nhà hàng, SRS v1.1, Product Backlog, dữ liệu mẫu ẩn danh, tri thức AI & HDSD 3 vai trò |
| `ui-ux-design` | PO/BA | `1.3.2.1` (`US-03`) | Wireframe & Prototype luồng chính trên Figma (Mobile & Desktop) |
| `project-management` | PM/SM | `1.1.1`, `1.3.1`, `1.5.1`, `1.7.1`, `1.9.1`, `1.11.1`, `1.11.4.2–3`, `1.13.1`, `1.13.4.2–3`, `1.15.5` | Quản lý 8 tuần, Tôn chỉ, RACI, Baseline `M2`, EVM, CCB, Sổ rủi ro, Feature Freeze & Tổng kết `M6` |
| `business-ops` | PM/SM | `1.7.3.4`, `1.7.4.2`, `1.9.3.3`, `1.9.4.3` | Tham số nghiệp vụ động (`US-20`), đối soát Sandbox, đăng ký tên miền & gói Email/SMS |

### 1.3 Dự toán ngân sách & Đường cơ sở chi phí (PV/EVM)
- **Chi phí nhân công (80 ngày công / 640 giờ):** `62.000.000 VNĐ`
- **Chi phí dịch vụ & hạ tầng (giải ngân tại Sprint 4):** `1.625.000 VNĐ` *(Cloud/VPS 45 ngày × 25.000đ = `1.125.000đ`; Tên miền 1 năm = `300.000đ`; Email SMTP & SMS nhắc 2h = `200.000đ`; Ollama tự host & Payment Sandbox = `0đ`)*
- **Tổng chi phí cơ sở (BAC — Cost Baseline):** **`63.625.000 VNĐ`**
- **Dự phòng rủi ro (10% × BAC):** `6.362.500 VNĐ` *(chỉ giải ngân khi có CR/rủi ro được duyệt)*
- **Tổng ngân sách dự kiến trong Tôn chỉ:** **`69.987.500 VNĐ`**

| Sprint | Thời gian | Giờ công | Nhân công (VNĐ) | Chi phí cố định (VNĐ) | Tổng Sprint (VNĐ) | **PV Lũy kế (VNĐ)** |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| **Sprint 0** | `16/11 – 22/11/2026` | `80h` | `7.750.000` | `0` | `7.750.000` | **`7.750.000`** |
| **Sprint 1** | `23/11 – 29/11/2026` | `80h` | `7.750.000` | `0` | `7.750.000` | **`15.500.000`** |
| **Sprint 2** | `30/11 – 06/12/2026` | `80h` | `7.750.000` | `0` | `7.750.000` | **`23.250.000`** |
| **Sprint 3** | `07/12 – 13/12/2026` | `80h` | `7.750.000` | `0` | `7.750.000` | **`31.000.000`** |
| **Sprint 4** | `14/12 – 20/12/2026` | `80h` | `7.750.000` | `1.625.000` | `9.375.000` | **`40.375.000`** |
| **Sprint 5** | `21/12 – 27/12/2026` | `80h` | `7.750.000` | `0` | `7.750.000` | **`48.125.000`** |
| **Sprint 6** | `28/12 – 03/01/2027` | `80h` | `7.750.000` | `0` | `7.750.000` | **`55.875.000`** |
| **Sprint 7** | `04/01 – 10/01/2027` | `80h` | `7.750.000` | `0` | `7.750.000` | **`63.625.000` (BAC)** |

---

## 2. Mốc kiểm soát (`M1` – `M6`) & Lộ trình phát hành

| Mốc | WBS | Thời điểm | Git Tag | Điều kiện đạt (Exit Criteria) | Người xác nhận | Trạng thái |
| :---: | :---: | :---: | :---: | :--- | :--- | :--- |
| **M1** | `1.2` | `22/11/2026` | — | Tôn chỉ (D01), SRS v1.1, Backlog đầu được duyệt; GitHub, Jira (`MC`), MS Project đã lập & mời GV | Nhà tài trợ (GV) | **Đang hoàn tất** |
| **M2** | `1.4` | `29/11/2026` | — | Phát biểu phạm vi (D02), WBS 640h, Gantt/PERT, dự toán 69.987.500đ duyệt; lưu Baseline MS Project; CI xanh | Nhà tài trợ, PO/BA | Chưa bắt đầu |
| *Demo S2* | `1.6` | `06/12/2026` | — | Demo thực đơn, sơ đồ bàn kéo thả với dữ liệu mẫu ẩn danh; ký duyệt phương án Ollama & lõi RAG | PO/BA, Nhà hàng | Chưa bắt đầu |
| **M3** | `1.8` | `13/12/2026` | `v0.1` | RBAC 3 vai trò, thực đơn, sơ đồ bàn, đặt bàn chống trùng (Concurrent Test đạt) & giỏ món chạy ổn định | PO/BA, Nhà hàng | Chưa bắt đầu |
| *Demo S4* | `1.10` | `20/12/2026` | — | Demo đặt bàn, đặt món, cọc Sandbox, hủy/hoàn cọc & Email xác nhận trên Staging; cập nhật EVM | PO/BA, Nhà hàng | Chưa bắt đầu |
| **M4** | `1.12` | `27/12/2026` | `v0.2` | Báo cáo giữa kỳ; vận hành NV (check-in, no-show, đổi bàn) & Chatbot AI dữ liệu thật chạy trên Staging | Giảng viên, PO/BA | Chưa bắt đầu |
| **M5** | `1.14` | `03/01/2027` *(Review `31/12`)* | `v1.0-rc` | **Feature Freeze**: hoàn thiện 100% MVP (`FR-01`..`FR-14`), Guardrails AI, đặt bàn qua chat, báo cáo, bếp, nhắc lịch `24h`/`2h`; sẵn sàng UAT | PO/BA, Nhà hàng | Chưa bắt đầu |
| **M6** | `1.16` | `10/01/2027` *(Bàn giao `08/01`)* | `v1.0` | Go-live Production `v1.0`; `0` Bug Cao/Nghiêm trọng; AI đúng `>= 80%` trên `>= 30` câu; nhà hàng ký UAT; đủ HDSD, video demo & báo cáo tổng kết | Giảng viên, Nhà hàng | Chưa bắt đầu |

---

## 3. Danh mục 10 Epic & Phân bổ 252 Story Points

| Epic | Tên Epic | FR liên quan | Sprint mục tiêu | Story / SP MVP | Story / SP Dự phòng | Số Task |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| `EP-00` | Khởi động và quản lý dự án | `D01`, `D02`, `D03`, `D14` | Sprint 0 | `0` / `0 SP` | — | `5` |
| `EP-01` | Nền tảng kỹ thuật, Tài khoản và Phân quyền | `FR-01` | Sprint 1 | `8 US` / `28 SP` | — | `3` |
| `EP-02` | Quản lý và Hiển thị Thực đơn | `FR-02`, `FR-03` | Sprint 2 | `5 US` / `16 SP` | `1 US` / `3 SP` | `3` |
| `EP-03` | Sơ đồ bàn và Đặt bàn theo khung giờ | `FR-04`, `FR-05` | Sprint 2–4 | `7 US` / `34 SP` | — | `2` |
| `EP-04` | Đặt món trước và Đặt cọc trực tuyến | `FR-06`, `FR-07`, `FR-09` | Sprint 3–4 | `5 US` / `26 SP` | `1 US` / `8 SP` | `1` |
| `EP-05` | Vận hành đặt chỗ, Thông báo và Bếp | `FR-08`, `FR-10`, `FR-11` | Sprint 4–6 | `6 US` / `28 SP` | `1 US` / `3 SP` | `1` |
| `EP-06` | Báo cáo thống kê vận hành | `FR-12` | Sprint 6 | `1 US` / `8 SP` | `1 US` / `5 SP` | `1` |
| `EP-07` | Chatbot AI (Ollama) tư vấn & đặt bàn | `FR-13`, `FR-14`, `FR-15` | Sprint 2, 5–6 | `5 US` / `32 SP` | `1 US` / `5 SP` | `7` |
| `EP-08` | Chức năng mở rộng (Backlog dự phòng) | `FR-16`, `FR-17`, `FR-18` | Dự phòng | — | `4 US` / `26 SP` | `0` |
| `EP-09` | Staging, Kiểm thử, UAT và Phát hành v1.0 | `NFR-01`..`NFR-06` | Sprint 4, 7 | `8 US` / `30 SP` | — | `3` |
| **TỔNG** | **10 Epic (`54 US = 252 SP`, `26 Task`)** | `FR-01`..`FR-18` | **Sprint 0–7** | **`45 US` / `202 SP`** | **`9 US` / `50 SP`** | **`26`** |

---

## 4. Kế hoạch thực thi chi tiết từng Sprint (Sprint 0 → Sprint 7)

### Sprint 0 — Khởi động, Khảo sát nghiệp vụ & Thiết lập kỹ thuật
- **Thời gian:** `16/11 – 22/11/2026` \| **Khối lượng:** `80h` \| **Mốc:** `M1` \| **Trạng thái:** `Đang hoàn tất`
- **Sprint Goal:** Đề tài được duyệt, khảo sát xong đơn vị áp dụng, nhóm và bộ công cụ (GitHub, Jira `MC`, MS Project, Ollama local, Chat API Contract) sẵn sàng.
- **Sản phẩm QLDA:** `D01` SOW + Tôn chỉ dự án; `D02` Phát biểu phạm vi; `D03` Product Backlog bản đầu; `D14` Tổ chức nhóm & RACI; `D17` Kế hoạch truyền thông; `D24` Phân tích bên liên quan; SRS v1.1.

| Done | Task / Mã WBS | Assignee | Phạm vi / Vùng file | Tiêu chí Done |
| :---: | :--- | :--- | :--- | :--- |
| [x] | `[PM]` Khởi tạo Jira, MS Project, Kick-off & Bộ tài liệu D01/D14/D17 (`1.1.1.1–2`) | PM/SM | Jira, MS Project, `docs/` | Tạo xong 10 Epic, mời GV vào Jira, chốt RACI & quy ước 4 người |
| [x] | `[BA]` Khảo sát nhà hàng, hoàn thiện SRS/Backlog & gom dữ liệu thô (`1.1.2.1–3`) | PO/BA | `docs/` | Có biên bản khảo sát, chốt SRS v1.1, có menu/bàn/chính sách thô |
| [x] | `[FS]` Khởi tạo Repo GitHub, branch rules & skeleton ReactJS + FastAPI + PG (`1.1.3.1–2`) | Dev Fullstack | `frontend/`, `backend/app/core/`, `docker-compose.yml` | Đã hoàn tất repo, GitFlow, CI PR check và skeleton FE + BE + PG16 (`MC-11`) |
| [x] | `[FS]` Khảo sát cổng thanh toán Sandbox (VNPay/MoMo/PayOS) & Email/SMS (`1.1.3.3`) | Dev Fullstack | `docs/PAYMENT_EMAIL_SMS_RESEARCH.md` | Đã hoàn tất bảng so sánh & đề xuất VNPay Sandbox + Brevo + SpeedSMS (`MC-69`) |
| [ ] | `[AI]` Cài đặt Ollama local, kéo thử model VN & chốt Chat API JSON Contract (`1.1.4.1–2`) | AI Dev | `ollama/`, `docs/SYSTEM_SPEC.md` | Ollama chạy ổn định `>= 2` model; 2 Dev chốt xong JSON `/api/v1/chat/messages` |

---

### Sprint 1 — Nền tảng kỹ thuật, CSDL, Phân quyền RBAC & Benchmark AI
- **Thời gian:** `23/11 – 29/11/2026` \| **Khối lượng:** `28 SP` (`80h`) \| **Mốc:** `M2` (Baseline MS Project) \| **Trạng thái:** `Đang thực hiện`
- **Sprint Goal:** Nền tảng kỹ thuật chạy được; người dùng đăng ký, đăng nhập, phân quyền RBAC 3 vai trò; lưu Baseline MS Project (`M2`); benchmark xong mô hình Ollama.
- **Sản phẩm QLDA:** WBS chi tiết, Gantt/PERT, Resource Sheet & **Baseline MS Project (`M2`)**; Kế hoạch chất lượng & DoR/DoD; Sổ rủi ro bản đầu; chốt nhà cung cấp Sandbox/Hosting/SMS.

| Done | US | Tên User Story | Epic | FR | WBS | Prio | SP | Assignee | Tiêu chí chấp nhận cốt lõi (AC) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| [x] | `US-01` | Khung dự án và kiến trúc | `EP-01` | — | `1.3.3.2` | High | 5 | Dev Fullstack | Cấu trúc thư mục + README cài đặt; `/health` trả `200` + Swagger; BE nối PG, FE gọi API mẫu |
| [x] | `US-02` | ERD và migration CSDL | `EP-01` | — | `1.3.3.1` | High | 3 | Dev Fullstack | ERD trong repo (`docs/ERD.md`); Alembic tạo đủ 13 bảng Core trên CSDL trống; có constraint chống trùng bàn; `>= 1` review |
| [ ] | `US-03` | Thiết kế Figma luồng chính | `EP-01` | — | `1.3.2.1` | High | 5 | PO/BA | Prototype trang chủ, thực đơn, đặt bàn, đặt món, cọc, chat, quản lý; dùng tốt mobile; PO duyệt |
| [x] | `US-04` | Đăng ký tài khoản | `EP-01` | `FR-01` | `1.3.4.1` | High | 3 | Dev Fullstack | Email/SĐT không trùng; mật khẩu băm `bcrypt`; gửi email xác thực 1 lần; báo lỗi rõ từng trường (`MC-14`) |
| [ ] | `US-05` | Đăng nhập và đăng xuất | `EP-01` | `FR-01` | `1.3.4.1` | High | 3 | Dev Fullstack | Điều hướng theo vai trò; sai `> 5` lần khóa `15p`; JWT có thời hạn; đăng xuất hủy phiên |
| [ ] | `US-06` | Quên mật khẩu | `EP-01` | `FR-01` | `1.3.4.1` | Med | 2 | Dev Fullstack | Gửi link đặt lại có thời hạn, dùng `1` lần; mật khẩu mới lưu dạng băm |
| [ ] | `US-07` | Phân quyền và tài khoản nhân viên | `EP-01` | `FR-01` | `1.3.4.2` | High | 5 | Dev Fullstack | 3 vai trò (Khách, NV, QL); ngoài quyền trả `403` + log; QL tạo/khóa/mở khóa tài khoản NV |
| [ ] | `US-08` | CI bằng GitHub Actions | `EP-01` | — | `1.3.3.3` | Med | 2 | Dev Fullstack | PR kích hoạt build & test; hiển thị kết quả trên PR; lỗi build chặn merge `main` |

**Task song song Sprint 1:**
- [ ] `[PM]` Lưu Baseline MS Project (`M2`), lập DoR/DoD, Sổ rủi ro v1.0 và chốt Sandbox (`1.3.1.1–2`) — *PM/SM*
- [ ] `[AI]` Tạo `ai_models.py` (`knowledge_docs`, `chat_sessions`, `chat_messages`) & migration `alembic/*_ai_*`, không sửa `core_models.py` (`1.3.5.1`) — *AI Dev*
- [ ] `[AI]` Benchmark `>= 2` model Ollama trên `>= 10` câu tiếng Việt & dựng `OllamaClient` + `/api/v1/chat/health` (`1.3.5.2`) — *AI Dev*

---

### Sprint 2 — Quản lý Thực đơn, Sơ đồ bàn & Lõi RAG Ollama
- **Thời gian:** `30/11 – 06/12/2026` \| **Khối lượng:** `29 SP` (`80h`, tích lũy `57 SP`) \| **Mốc:** Demo Increment S2 \| **Trạng thái:** `Chưa bắt đầu`
- **Sprint Goal:** Khách xem/tìm thực đơn; Quản lý quản lý thực đơn & sơ đồ bàn kéo thả với dữ liệu mẫu ẩn danh; chốt phương án LLM (`US-15`) & dựng lõi RAG.
- **Sản phẩm QLDA:** Cost Baseline & **EVM lần 1**; quyết định Make-or-Buy LLM (`US-15`); cập nhật Sổ rủi ro.

| Done | US | Tên User Story | Epic | FR | WBS | Prio | SP | Assignee | Tiêu chí chấp nhận cốt lõi (AC) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| [ ] | `US-09` | Xem thực đơn | `EP-02` | `FR-02` | `1.5.3.1` | High | 3 | Dev Fullstack | Chỉ hiện món đang bán; món hết hiện `Tạm hết` & khóa thêm vào đơn; giá `VNĐ`; responsive |
| [ ] | `US-10` | Tìm kiếm và lọc món | `EP-02` | `FR-02` | `1.5.3.1` | Med | 3 | Dev Fullstack | Tìm từ khóa; lọc danh mục, khoảng giá, nhãn món; không có kết quả gợi ý bỏ bớt lọc |
| [ ] | `US-11` | Quản lý danh mục và món | `EP-02` | `FR-03` | `1.5.3.2` | High | 5 | Dev Fullstack | Validate tên, giá `> 0`, ảnh; xóa mềm, không xóa món đã có đơn; đồng bộ ngay cho khách |
| [ ] | `US-12` | Tình trạng món và lịch sử giá | `EP-02` | `FR-03` | `1.5.3.2` | High | 3 | Dev Fullstack | Trạng thái Đang bán/Tạm hết/Ngừng bán; lưu lịch sử giá; món hết không thêm được vào đơn |
| [ ] | `US-13` | Quản lý khu vực và bàn | `EP-03` | `FR-04` | `1.5.4.1` | High | 5 | Dev Fullstack | Tạo khu vực, bàn (mã duy nhất, chỗ `>= 1`, ghép bàn); chặn xóa/ngưng bàn có đơn tương lai |
| [ ] | `US-14` | Sơ đồ bàn trực quan | `EP-03` | `FR-04` | `1.5.4.2` | Med | 5 | Dev Fullstack | Kéo thả bàn theo khu vực & lưu tọa độ; Nhân viên chỉ xem, không sửa |
| [ ] | `US-15` | Spike: chọn phương án LLM | `EP-07` | `FR-13` | `1.5.5.1` | High | 3 | AI Dev | So sánh `>= 2` model Ollama (RAM/VRAM, latency, tiếng Việt, bảo mật) trên `>= 10` câu; PO & PM duyệt |
| [ ] | `US-16` | Dữ liệu mẫu thực tế đã ẩn danh | `EP-02` | — | `1.5.2.1` | High | 2 | PO/BA | Dữ liệu menu (`>= 30–50` món), sơ đồ bàn được đơn vị xác nhận; script nạp sạch; không có PII thật |

**Task song song Sprint 2:**
- [ ] `[PM]` Review Sprint 1, lập EVM #1, ký duyệt model Ollama `US-15` (`1.5.1.1–3`) — *PM/SM*
- [ ] `[FS]` Viết `backend/scripts/seed_core.py` nạp thực đơn, khu vực, bàn vào PostgreSQL (`1.5.3.3`) — *Dev Fullstack*
- [ ] `[AI]` Xây dựng `rag_retriever.py`, `prompts.py`, `seed_ai.py` & JSON `dish_cards[]` qua Swagger (`1.5.5.2`) — *AI Dev*

---

### Sprint 3 — Đặt bàn chống trùng, Đặt món trước & Parser GMT+7
- **Thời gian:** `07/12 – 13/12/2026` \| **Khối lượng:** `29 SP` (`80h`, tích lũy `86 SP`) \| **Mốc:** `M3` (`Tag v0.1`) \| **Trạng thái:** `Chưa bắt đầu`
- **Sprint Goal:** Khách đặt được bàn theo khung giờ không trùng bàn (`Concurrent Test` đạt) và đặt món trước với giá chốt; hoàn thiện Parser `GMT+7` & `PII Masker v1`.
- **Sản phẩm QLDA:** Cập nhật Burndown, % hoàn thành, EVM; test case đặt bàn & kiểm thử đồng thời; cập nhật Sổ rủi ro; gắn `tag v0.1`.

| Done | US | Tên User Story | Epic | FR | WBS | Prio | SP | Assignee | Tiêu chí chấp nhận cốt lõi (AC) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| [ ] | `US-17` | Kiểm tra bàn trống | `EP-03` | `FR-05` | `1.7.3.1` | High | 5 | Dev Fullstack | Bước `30p`, lượt `90p`, đặt trước `2h–30d` (`GMT+7`); hết bàn gợi ý giờ/khu vực gần nhất |
| [ ] | `US-18` | Giữ chỗ tạm thời, chống trùng bàn | `EP-03` | `FR-05` | `1.7.3.2` | High | 8 | Dev Fullstack | Đơn `Chờ cọc` giữ `10p`; 2 request đồng thời chỉ 1 thành công (có Concurrent Test); quá hạn chuyển `Hết hạn` |
| [ ] | `US-19` | Giao diện đặt bàn | `EP-03` | `FR-05` | `1.7.3.3` | High | 5 | Dev Fullstack | Nhập ngày/giờ/khách/khu vực/ghi chú; hiển thị khung giờ trống & đồng hồ đếm ngược; responsive |
| [ ] | `US-20` | Cấu hình tham số nghiệp vụ | `EP-03` | `FR-05,07,09` | `1.7.3.4` | High | 3 | PM/SM *(cấu hình/nghiệp vụ)* | Cấu hình lượt, giữ chỗ, mức cọc, mốc hoàn cọc, nhắc lịch, hạn sửa món; chỉ áp dụng đơn mới |
| [ ] | `US-21` | Giỏ món đặt trước | `EP-04` | `FR-06` | `1.7.4.1` | High | 5 | Dev Fullstack | Thêm/sửa/xóa SL `1–20` + ghi chú; chặn món `Tạm hết`; khóa sửa trước `2h`; cập nhật tạm tính |
| [ ] | `US-22` | Chốt món, giá chốt, tính tiền cọc | `EP-04` | `FR-06` | `1.7.4.1–2` | High | 3 | Dev Fullstack | Lưu `unit_price_locked`; tính cọc theo cấu hình; không đặt món vẫn tạo đơn cọc theo quy tắc; hiện chính sách hủy |

**Task song song Sprint 3:**
- [ ] `[PM]` Cập nhật Burndown/EVM, kiểm tra mốc `M3`, gắn tag `v0.1`, kiểm tra sẵn sàng Sandbox (`1.7.1.1–3`) — *PM/SM*
- [ ] `[BA]` Test case đặt bàn/đồng thời, chốt tham số `US-20` & soạn `15+` mẫu hội thoại AI (`1.7.2.1–2`) — *PO/BA*
- [ ] `[AI]` `datetime_parser.py` (`GMT+7`, `2h–30d`) & `booking_assistant.py` (slot-filling read-only `FR-05`, sinh `/booking?...`) (`1.7.5.1`) — *AI Dev*
- [ ] `[AI]` `pii_masker.py` v1 (che tên/SĐT/email trước Ollama) & `guardrails.py` phát hiện ngoài phạm vi/y tế (`1.7.5.2`) — *AI Dev*

---

### Sprint 4 — Đặt cọc Sandbox, Hủy/Hoàn cọc & Triển khai Staging
- **Thời gian:** `14/12 – 20/12/2026` \| **Khối lượng:** `27 SP` (`80h`, tích lũy `113 SP`) \| **Mốc:** Demo Increment S4 \| **Trạng thái:** `Chưa bắt đầu`
- **Sprint Goal:** Khách đặt cọc qua cổng Sandbox (callback HMAC idempotent), xem & hủy đặt chỗ, nhận Email xác nhận/hủy; toàn hệ thống (Web + Ollama) chạy live trên Staging.
- **Sản phẩm QLDA:** Quy trình CR/CCB; báo cáo tuần; test case thanh toán/hoàn cọc; giải ngân hạ tầng (`1.625.000đ`).

| Done | US | Tên User Story | Epic | FR | WBS | Prio | SP | Assignee | Tiêu chí chấp nhận cốt lõi (AC) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| [ ] | `US-23` | Xem trạng thái bàn theo ngày, giờ | `EP-03` | `FR-04` | `1.9.4.1` | High | 3 | Dev Fullstack | Hiện 5 trạng thái (`Trống`, `Đang giữ`, `Đã đặt`, `Đang phục vụ`, `Ngưng sử dụng`); NV & QL xem |
| [ ] | `US-24` | Đặt cọc: tạo giao dịch, chuyển cổng TT | `EP-04` | `FR-07` | `1.9.3.1` | High | 5 | Dev Fullstack | Tóm tắt đơn + đồng ý chính sách hủy; lưu mã/tiền/thời điểm/trạng thái; không lưu thẻ; chuyển Sandbox |
| [ ] | `US-25` | Xử lý kết quả thanh toán (callback) | `EP-04` | `FR-07` | `1.9.3.2` | High | 8 | Dev Fullstack | Xác thực HMAC → `Đã xác nhận` + sinh mã; idempotent; xử lý trễ (còn bàn → xác nhận, hết → hoàn cọc); lỗi → giữ `Chờ cọc` |
| [ ] | `US-26` | Đặt chỗ của tôi, hủy & yêu cầu hoàn cọc | `EP-04` | `FR-09` | `1.9.4.1` | High | 5 | Dev Fullstack | Xem DS/chi tiết đơn; hiện mức hoàn cọc (`100%/50%/0%`) trước khi hủy; chuyển `Đã hủy`, giải phóng bàn, tạo yêu cầu hoàn |
| [ ] | `US-27` | Email xác nhận và hủy đặt chỗ | `EP-05` | `FR-10` | `1.9.4.2` | High | 3 | Dev Fullstack | Gửi email khi cọc thành công & khi hủy (mã đơn, giờ, bàn, chính sách); lỗi retry tối đa `3 lần` + log |
| [ ] | `US-28` | Triển khai staging | `EP-09` | — | `1.9.4.2` | Med | 3 | Dev Fullstack | Truy cập qua URL; auto-deploy từ `develop`; có dữ liệu mẫu; GV & PO truy cập được |

**Task song song Sprint 4:**
- [ ] `[PM]` Thiết lập CR/CCB, đối soát Sandbox, thuê VPS/Domain/Email-SMS, chốt lịch UAT Tuần 8 (`1.9.1.1–3`, `1.9.3.3`, `1.9.4.3`) — *PM/SM*
- [ ] `[BA]` Test case 4 kịch bản callback & 3 mốc hoàn cọc; rà soát AI trên Staging (`1.9.2.1–2`) — *PO/BA*
- [ ] `[AI]` Đóng gói `docker-compose.ollama.yml` lên Staging & fallback `is_fallback: true` khi Ollama lỗi (`1.9.5.1`) — *AI Dev*
- [ ] `[AI]` Hoàn thiện REST API `/api/v1/chat/*` (`sessions`, `messages`, `feedback`) nối Staging (`1.9.5.2`) — *AI Dev*

---

### Sprint 5 — Vận hành Nhân viên & Chatbot AI Tư vấn Dữ liệu thật
- **Thời gian:** `21/12 – 27/12/2026` \| **Khối lượng:** `31 SP` (`80h`, tích lũy `144 SP`) \| **Mốc:** `M4` (`Tag v0.2`) \| **Trạng thái:** `Chưa bắt đầu`
- **Sprint Goal:** Nhân viên xử lý trọn vẹn đơn đặt chỗ (check-in, no-show, đổi bàn/giờ có log); Chatbot AI tư vấn món & chính sách trên dữ liệu thật kèm thẻ món `Thêm vào đơn`.
- **Sản phẩm QLDA:** Báo cáo giữa kỳ (`M4`), cập nhật EVM #2, báo cáo Bug & CR, gắn `tag v0.2`.

| Done | US | Tên User Story | Epic | FR | WBS | Prio | SP | Assignee | Tiêu chí chấp nhận cốt lõi (AC) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| [ ] | `US-29` | Tích hợp LLM và khung chat | `EP-07` | `FR-13` | `1.11.2.2–3` | High | 8 | AI Dev | ChatWidget trên các trang chính, nêu rõ là trợ lý AI; gọi Ollama (`US-15`), lưu hội thoại; lỗi/timeout fallback sang menu & form |
| [ ] | `US-30` | Chatbot tư vấn món và chính sách | `EP-07` | `FR-13` | `1.11.2.2.2` | High | 8 | AI Dev | Trả lời realtime theo DB; gợi ý theo ngân sách/số người/nhãn kèm `dish_cards[]` (`Thêm vào đơn`); thiếu dữ liệu hướng dẫn liên hệ NV |
| [ ] | `US-31` | Danh sách, lọc và chi tiết đơn đặt chỗ | `EP-05` | `FR-08` | `1.11.3.1` | High | 5 | Dev Fullstack | Lọc ngày, trạng thái, khu vực, mã đơn, SĐT; chi tiết khách/bàn/món/cọc/lịch sử; chỉ NV & QL truy cập |
| [ ] | `US-32` | Check-in, hoàn thành, đánh dấu không đến | `EP-05` | `FR-08` | `1.11.3.2` | High | 5 | Dev Fullstack | Check-in → `Đã đến`, xong → `Hoàn thành`; nhắc quá `15p` chưa check-in; đánh dấu `Không đến`; chặn sửa trạng thái cuối |
| [ ] | `US-33` | Đổi bàn/giờ, hủy bởi nhân viên, nhật ký | `EP-05` | `FR-08` | `1.11.3.3` | High | 5 | Dev Fullstack | Chặn đổi sang bàn/giờ trùng; hủy ngoại lệ chỉ QL + lý do; ghi nhật ký (ai, lúc nào, cũ/mới) & báo khách |

**Task song song Sprint 5:**
- [ ] `[PM]` Cập nhật EVM #2, kiểm tra `M4`, gắn tag `v0.2` & chốt phạm vi S6 (giữ/lùi `US-37`, `US-38` theo velocity) (`1.11.1.1–3`, `1.11.4.2–3`) — *PM/SM*
- [ ] `[BA]` Duyệt tri thức Chatbot, test nghiệp vụ NV & soạn nháp bộ `30+` câu test AI (`US-40`) (`1.11.2.1.1`, `1.11.4.1`) — *PO/BA*
- [ ] `[FS]` Hoàn thiện ReactJS `ChatWidget` (thẻ món `Thêm vào đơn`, feedback, fallback UI) (`1.11.2.3.1`) — *Dev Fullstack*

---

### Sprint 6 — Guardrails AI, Đặt bàn qua Chat, Báo cáo & Nhắc lịch (Feature Freeze)
- **Thời gian:** `28/12/2026 – 03/01/2027` *(Nghỉ Tết DL `01/01`, Review sớm `31/12/2026`, làm bù `02/01/2027`)* \| **Khối lượng:** `31 SP` (`80h`, tích lũy `175 SP`) \| **Mốc:** `M5` (`Tag v1.0-rc`) \| **Trạng thái:** `Chưa bắt đầu`
- **Sprint Goal:** Chatbot an toàn (Guardrails + PII Masking) & đặt bàn qua chat `GMT+7`; hoàn tất báo cáo thống kê, tổng hợp món cho bếp & nhắc lịch `24h`/`2h`; **Đóng băng tính năng (`Feature Freeze`)**.
- **Sản phẩm QLDA:** Cập nhật EVM & dự báo hoàn thành; rà soát rủi ro trước phát hành; kịch bản UAT gửi nhà hàng; gắn `tag v1.0-rc`.

| Done | US | Tên User Story | Epic | FR | WBS | Prio | SP | Assignee | Tiêu chí chấp nhận cốt lõi (AC) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| [ ] | `US-34` | Guardrails: chống bịa tin, bảo vệ dữ liệu | `EP-07` | `FR-13` | `1.13.2.1.1–2` | High | 5 | AI Dev | Che họ tên/SĐT/email trước Ollama; từ chối ngoài phạm vi/y tế/dị ứng; rate limit & độ dài; QA test `>= 20` câu không bịa |
| [ ] | `US-35` | Đặt bàn qua chat | `EP-07` | `FR-14` | `1.13.2.2.1–2` | High | 8 | AI Dev | Hỏi ngày/giờ/khách `GMT+7`, tra bàn trống (read-only) → sinh link `/booking?...`; giữ info qua Login; không tự báo đã đặt |
| [ ] | `US-36` | Báo cáo đơn, tỷ lệ hủy/no-show, doanh thu cọc | `EP-06` | `FR-12` | `1.13.3.1` | High | 8 | Dev Fullstack | Đơn theo trạng thái, tỷ lệ hủy, tỷ lệ no-show, doanh thu cọc/hoàn, đơn ngoài giờ; bảng & biểu đồ; chỉ QL truy cập |
| [ ] | `US-37` | Tổng hợp món chuẩn bị cho bếp | `EP-05` | `FR-11` | `1.13.3.2` | Med | 5 | Dev Fullstack | Tổng hợp món/SL/ghi chú từ đơn `Đã xác nhận`; tự cập nhật khi sửa/hủy; hỗ trợ in hoặc xuất PDF |
| [ ] | `US-38` | Nhắc lịch trước 24 giờ và 2 giờ | `EP-05` | `FR-10` | `1.13.3.3` | Med | 5 | Dev Fullstack | Nhắc `24h` (Email) & `2h` (Email/SMS nếu bật); bỏ qua đơn hủy; ghi trạng thái & retry tối đa `3 lần` |

**Task song song Sprint 6:**
- [ ] `[PM]` Cập nhật EVM, kiểm tra tiêu chí Feature Freeze (`M5`), sao lưu DB trước UAT, gắn `v1.0-rc` (`1.13.1.1–3`, `1.13.4.2–3`) — *PM/SM*
- [ ] `[BA]` Lập kịch bản UAT (`US-41`), test `>= 20` câu adversarial Guardrails (`US-34`) & đối soát báo cáo/bếp (`1.13.2.1.2`, `1.13.4.1`) — *PO/BA*
- [ ] `[FS]` Hỗ trợ pre-fill URL params `/booking?date=...` & giữ state qua Login (`1.13.2.2.2`) — *Dev Fullstack*

---

### Sprint 7 — Kiểm thử Hồi quy, UAT, Hardening & Phát hành `v1.0`
- **Thời gian:** `04/01 – 10/01/2027` *(Bàn giao `v1.0` ngày `08/01/2027`, Bảo vệ & Go-live `10/01/2027`)* \| **Khối lượng:** `27 SP` (`80h`, tích lũy `202 SP`) \| **Mốc:** `M6` (`Tag v1.0`) \| **Trạng thái:** `Chưa bắt đầu`
- **Sprint Goal:** Không nhận tính năng mới; hoàn tất kiểm thử hồi quy, bộ `>= 30` câu test Chatbot, UAT tại Nhà hàng Ẩm thực Vườn Phố, hardening bảo mật/hiệu năng, phát hành `v1.0` và đóng dự án.
- **Sản phẩm QLDA:** Biên bản UAT có chữ ký nhà hàng; HDSD 3 vai trò & Chatbot; Slide & Video demo `5–7 phút`; Báo cáo tổng kết, bài học kinh nghiệm, đóng sổ rủi ro, chốt EVM cuối kỳ.

| Done | US | Tên User Story | Epic | FR | WBS | Prio | SP | Assignee | Tiêu chí chấp nhận cốt lõi (AC) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| [ ] | `US-39` | Kiểm thử hệ thống và hồi quy | `EP-09` | — | `1.15.1.1` | High | 5 | PO/BA | Chạy đủ `>= 40` test case MVP + API Postman trên Staging; hồi quy sau mỗi lần sửa; `0` Bug Cao/Nghiêm trọng |
| [ ] | `US-40` | Bộ câu hỏi kiểm thử chatbot | `EP-09` | `FR-13,14` | `1.15.1.2` | High | 3 | AI Dev | Bộ `>= 30` câu (món, giá, chính sách, đặt bàn, ngoài phạm vi, dẫn dụ); đạt đúng `>= 80%`; câu sai log Bug; PO duyệt |
| [ ] | `US-41` | UAT với đơn vị áp dụng | `EP-09` | — | `1.15.2.1` | High | 5 | PO/BA | Nhà hàng Ẩm thực Vườn Phố chạy đủ kịch bản UAT; log lỗi Jira; có báo cáo & biên bản UAT |
| [ ] | `US-42` | Sửa lỗi UAT và hardening | `EP-09` | — | `1.15.3.1–2` | High | 5 | Dev Fullstack | Sửa hết Bug Cao/Nghiêm trọng; rà soát HTTPS, RBAC, không lưu thẻ; test backup & restore DB |
| [ ] | `US-43` | Hướng dẫn sử dụng | `EP-09` | — | `1.15.4.1` | High | 3 | PO/BA | HDSD riêng cho Khách, Nhân viên, Quản lý & Chatbot kèm ảnh minh họa; nhà hàng xác nhận dễ dùng |
| [ ] | `US-44` | Phát hành `v1.0` | `EP-09` | — | `1.15.3.3` | High | 3 | Dev Fullstack | Deploy Production sau backup; tag & release `v1.0` trên GitHub + release notes; README đủ hướng dẫn; CI xanh |
| [ ] | `US-45` | Demo và kết thúc dự án | `EP-09` | — | `1.15.4.2`, `1.15.5.5` | High | 3 | PM/SM | Slide & video demo `5–7 phút`; báo cáo tổng kết, bài học kinh nghiệm; đóng sổ rủi ro; chốt MS Project & EVM |

**Task song song Sprint 7:**
- [ ] `[AI]` Sửa Bug UAT phần Chatbot, tối ưu latency Ollama Production (`keep_alive`) & log rotation `90 ngày` (`1.15.3.2`) — *AI Dev*
- [ ] `[PM]` Điều phối Scrum cuối, chốt EVM tổng kết, đóng sổ rủi ro & hồ sơ nghiệm thu `M6` (`1.15.5.1–4`) — *PM/SM*

### Phụ thuộc cốt lõi liên Sprint
1. `US-18` phụ thuộc `US-13` (bàn) và `US-17` (kiểm tra bàn trống).
2. `US-24`, `US-25` phụ thuộc tài khoản Sandbox chốt từ Sprint 1.
3. `US-29`..`US-35` phụ thuộc quyết định model Ollama ở `US-15` (S2), dữ liệu mẫu `US-16` và tham số `US-20`.
4. `US-35` phụ thuộc `US-17`, `US-19` (truy vấn bàn trống & form `/booking?...`).
5. `US-37`, `US-38` phụ thuộc đơn ở trạng thái `Đã xác nhận` (`US-25`).
6. **Feature Freeze hết Sprint 6 (`M5`)**: Từ Sprint 7 chỉ sửa lỗi, kiểm thử, tài liệu và phát hành.

---

## 5. Backlog dự phòng (`9 User Story = 50 SP`: `US-46` – `US-54`)

*(Chỉ kéo vào Sprint khi velocity thực tế vượt kế hoạch `27–31 SP/Sprint` và **trước Feature Freeze hết Sprint 6**. Ưu tiên #1 là `US-46`.)*

| Done | US | Tên User Story | Epic | FR | Prio | SP | Assignee | Tiêu chí chấp nhận cốt lõi (AC) |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :--- | :--- |
| [ ] | `US-46` | Quản trị tri thức và giám sát chatbot *(Ưu tiên #1)* | `EP-07` | `FR-15` | Med | 5 | AI Dev | Thêm/sửa FAQ, chính sách dùng ngay; xem hội thoại lọc `Không hữu ích`, đánh dấu sai; che PII, lưu `<= 90 ngày` |
| [ ] | `US-47` | Báo cáo mở rộng và xuất tệp | `EP-06` | `FR-12` | Med | 5 | Dev Fullstack | Món đặt nhiều nhất, công suất bàn, thống kê chatbot; xuất Excel/PDF; `> 1 năm` yêu cầu thu hẹp |
| [ ] | `US-48` | Hoàn cọc tự động và xử lý lỗi hoàn | `EP-04` | `FR-09` | Med | 8 | Dev Fullstack | Gọi API hoàn cọc Sandbox theo chính sách; lỗi chuyển `Chờ xử lý thủ công`; thông báo khách |
| [ ] | `US-49` | Cảnh báo đơn bị ảnh hưởng khi món hết | `EP-02` | `FR-03` | Med | 3 | Dev Fullstack | Đánh dấu đơn `Đã xác nhận` có món hết/ngừng bán; hiện cảnh báo cho NV; ghi log đổi món |
| [ ] | `US-50` | Tạo đơn thay khách (đặt qua điện thoại) | `EP-05` | `FR-08` | Med | 3 | Dev Fullstack | NV tạo đơn theo luồng đặt bàn, nhập info khách, gửi link cọc, ghi nguồn `phone` |
| [ ] | `US-51` | Đánh giá nhà hàng | `EP-08` | `FR-17` | Low | 5 | Dev Fullstack | `1–5` sao + nhận xét cho đơn `Hoàn thành` (1 lần/đơn, sửa `7 ngày`); QL phản hồi/ẩn vi phạm |
| [ ] | `US-52` | Chatbot tool calling: tra cứu | `EP-08` | `FR-18` | Low | 8 | AI Dev | Gọi tool read-only whitelist (đơn của chính khách, bàn trống, chính sách hoàn); BE check quyền; ghi log |
| [ ] | `US-53` | Chatbot tool calling: thao tác có xác nhận | `EP-08` | `FR-18` | Low | 5 | AI Dev | Tóm tắt & chờ khách xác nhận trước khi giữ chỗ/hủy; cọc vẫn qua link cổng TT; rate limit & log |
| [ ] | `US-54` | Đặt tiệc / sự kiện | `EP-08` | `FR-16` | Low | 8 | Dev Fullstack | Form sự kiện nhóm đông; QL duyệt, báo giá, đặt cọc riêng; dùng chung giữ bàn `FR-05`; báo giá tự hết hạn |

---

## 6. Quản trị Scrum, Jira `MC`, CR/CCB & Sổ rủi ro

### 6.1 Sự kiện Scrum (Time-box cho Sprint 1 tuần)
| Sự kiện | Thời điểm | Time-box | Chủ trì & Điều phối | Đầu ra |
| :--- | :--- | :---: | :--- | :--- |
| **Sprint Planning** | Đầu tuần | `<= 2 giờ` | PM/SM điều phối; PO/BA trình bày; 2 Dev ước lượng | Sprint Goal, Sprint Backlog |
| **Daily Scrum** | Hằng ngày | `<= 15 phút` | Luân phiên Dev Fullstack, AI Dev, PO/BA | Cập nhật Board Jira `MC` |
| **Backlog Refinement** | Giữa tuần | `<= 1 giờ` | PO/BA + 2 Dev | Story đạt DoR cho Sprint sau |
| **Sprint Review** | Cuối tuần | `<= 1 giờ` | PO/BA nghiệm thu; 2 Dev demo (+ GV/Nhà hàng khi cần) | Increment demo; Burndown, Velocity |
| **Sprint Retrospective** | Sau Review | `<= 45 phút` | PM/SM điều phối; cả nhóm rút kinh nghiệm | Hành động cải tiến trên Jira |

### 6.2 Quy trình Jira `MC`, DoR, DoD & Kiểm soát thay đổi (CR/CCB)
- **Board Jira `MC`**: 5 cột `To Do → In Progress → In Review → In Testing → Done`. Ánh xạ ưu tiên: `Must = High`, `Should = Medium`, `Could = Low`.
- **Tự động hóa GitHub ↔ Jira**: Tạo nhánh `<type>/MC-xx-...` → `In Progress`; mở PR vào `develop` → `In Review`; Merge PR → `Done`.
- **Definition of Ready (DoR)**: Story đủ câu User Story + Acceptance Criteria kiểm thử được; đã ước lượng SP (`1, 2, 3, 5, 8, 13`); xác định phụ thuộc; có Figma (nếu có UI); được PO duyệt.
- **Definition of Done (DoD)**: Đủ 5 điều kiện tại mục 8.3 của [SYSTEM_SPEC.md](SYSTEM_SPEC.md).
- **Quy trình CR & CCB (sau mốc Baseline `M2 – 29/11/2026`)**: Mọi thay đổi phạm vi phải lập issue CR → PO/BA & PM/SM đánh giá tác động (phạm vi, tiến độ, chi phí) → Hội đồng CCB (PM/SM, PO/BA, Dev Fullstack, AI Dev; xin duyệt GVHD nếu thay đổi lớn) phê duyệt trước khi đưa vào Sprint kế tiếp.

### 6.3 Sổ rủi ro cốt lõi (Rà soát hằng tuần)
| Mã | Rủi ro | Kiểm soát & Ứng phó |
| :--- | :--- | :--- |
| `R1` | Khách đặt nhưng không đến (`No-show`) | Bắt buộc cọc `30%`, nhắc lịch `24h`/`2h`, hoàn cọc theo mốc, theo dõi báo cáo `FR-12` |
| `R2` | Trùng bàn khi đặt đồng thời (`Double Booking`) | Transaction + `EXCLUDE USING GIST` trong PostgreSQL + giữ chỗ `10p` + Concurrent Test |
| `R3` | Thực đơn đổi giá/hết món sau khi đặt | Lưu `unit_price_locked`; cảnh báo đơn bị ảnh hưởng khi món hết/ngừng bán |
| `R4` | Chatbot bịa tin hoặc rò rỉ PII | RAG thuần DB thật; PII Masker trước Ollama; từ chối ngoài phạm vi/y tế; log giám sát |
| `R5` | Ollama quá tải hoặc gián đoạn | Chốt model gọn nhẹ ở Sprint 2 (`US-15`); timeout + fallback `is_fallback: true` |
| `R6` | Chậm dữ liệu nhà hàng hoặc trễ cổng Sandbox | Dùng dữ liệu mẫu ẩn danh chuẩn hóa sớm từ S0–S2; chốt Sandbox ngay Sprint 1 |
