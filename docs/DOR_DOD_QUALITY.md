# KẾ HOẠCH CHẤT LƯỢNG, TIÊU CHÍ SẴN SÀNG (DoR) & HOÀN THÀNH (DoD) — v1.0

**Dự án:** Website đặt bàn và đặt món trước cho nhà hàng tích hợp chatbot AI (`QL09-W`)  
**Task Jira:** `MC-70` | **Mã WBS:** `1.3.1.1`, `1.3.1.2` | **Phiên bản:** `v1.0` (`26/11/2026`)  
**Người lập & Điều phối:** **Trần Hoàng Phúc** (`PM/SM`) | **Phối hợp duyệt:** **Võ Đăng Khoa** (`PO/BA`), **Nguyễn Văn Tiến** (`Dev Fullstack`), **Nguyễn Đoàn Trường Vũ** (`AI Dev`)

---

## 1. Quy chuẩn Vận hành Jira `MC`, GitFlow & Phân vùng Không xung đột

### 1.1 Luồng trạng thái trên Board Jira `MC`
- **5 cột chuẩn:** `To Do` → `In Progress` → `In Review` → `In Testing` → `Done`.
- **Ánh xạ ưu tiên MoSCoW:** `Must = High` | `Should = Medium` | `Could = Low`.
- **Ước lượng Story Points (Fibonacci):** `1, 2, 3, 5, 8, 13` *(Story `>= 13 SP` phải tách nhỏ trước khi đưa vào Sprint)*.

### 1.2 Quy ước GitHub ↔ Jira & Tự động hóa CI
- **Tạo nhánh từ `develop`:** `[<feature|fix|hotfix|docs|chore|refactor|test>/]MC-<số>-<mô-tả>` *(hỗ trợ cả nhánh tạo trực tiếp từ nút Create branch trên Jira)*.
- **Commit message:** `MC-<số> [<PM|BA|FS|AI|US-xx>] <Mô tả>` kèm trailer `Co-Authored-By` nếu có AI hỗ trợ.
- **Pull Request:** Tiêu đề bắt buộc có `[MC-<số>]` hướng về `develop` (`main` chỉ nhận từ `develop`, `release/*`, `hotfix/*`).
- **Tự động hóa GitHub Actions** ([pr-check.yml](../.github/workflows/pr-check.yml), [pr-rejected-jira.yml](../.github/workflows/pr-rejected-jira.yml)):
  - Push nhánh → Jira tự chuyển `In Progress`.
  - Mở PR → Jira tự chuyển `In Review`.
  - Reviewer bấm **Request changes** hoặc đóng PR chưa merge → Trả `Task` về `In Progress` + tự tạo `Bug` liên kết `blocks`.
  - Đạt `>= 1` Approve + CI xanh + Merge PR → Jira tự chuyển `Done`.

### 1.3 Ranh giới Phân vùng Zero File-Overlap (`AGENTS.md`)
| Vai trò | Vùng sở hữu độc quyền | Ranh giới giao tiếp |
| :--- | :--- | :--- |
| **Dev Fullstack** | `frontend/`, `backend/app/core/`, `backend/app/api/` *(trừ `chat_router.py`)*, `backend/app/services/`, `backend/app/models/core_models.py`, `backend/scripts/seed_core.py`, `docker-compose.yml` | Xuất `availability_service` (`FR-05`), giữ nguyên nhánh Alembic `core` |
| **AI Dev** | `backend/app/ai/`, `backend/app/api/v1/chat_router.py`, `backend/app/models/ai_models.py`, `backend/alembic/versions/*_ai_*`, `backend/scripts/seed_ai.py`, `ollama/`, `docker-compose.ollama.yml` | Chỉ gọi read-only `availability_service`; giao tiếp FE qua `/api/v1/chat/*`; giữ nhánh Alembic `ai` |
| **PO/BA & PM/SM** | `docs/`, `figma/`, Jira `MC`, MS Project | Không sửa mã nguồn nếu chưa thống nhất qua PR |

---

## 2. Tiêu chí Sẵn sàng — Definition of Ready (`DoR` v1.0)

Một **User Story** trên Jira `MC` chỉ được đưa vào **Sprint Backlog** trong buổi **Sprint Planning** khi đáp ứng đủ **7 điều kiện** sau:

1. **Đúng cấu trúc & rõ giá trị:** Ghi rõ vai trò (*Với tư cách... tôi muốn... để...*), gắn đúng `Epic` (`EP-01`..`EP-09`), `FR/NFR` và `Component` (`frontend`, `backend`, `database`, `ai-chatbot`, `qa-testing`...).
2. **Tiêu chí chấp nhận (Acceptance Criteria — AC) kiểm thử được:** Có danh sách AC cụ thể, đo được *(giá trị ngưỡng, mã HTTP `403`/`409`, thông báo lỗi, quy tắc `GMT+7`/`VNĐ`)*.
3. **Đã ước lượng kích thước:** Có điểm **Story Points** thống nhất bởi `PO/BA`, `Dev Fullstack` và `AI Dev` (`<= 8 SP`; nếu `13 SP` phải tách nhỏ).
4. **Rõ phụ thuộc kỹ thuật & nghiệp vụ:** Xác định xong các US/Task tiên quyết *(VD: `US-18` cần `US-13`, `US-17`; `US-24/25` cần chốt Sandbox ở `MC-70`)*.
5. **Sẵn sàng thiết kế giao diện (nếu có UI):** Đã có wireframe/màn hình tương ứng trong `figma/` (cả Desktop & Mobile) và đã được PO thống nhất.
6. **Rõ ranh giới phân vùng file & Contract:** Biết rõ thành phần nào thuộc `Core` (`Dev Fullstack`) hay `AI` (`AI Dev`) để không xung đột file.
7. **Được PO/BA nghiệm thu đầu vào:** `Võ Đăng Khoa` xác nhận Story đạt DoR trong buổi **Backlog Refinement** trước khi Sprint mới bắt đầu.

---

## 3. Tiêu chí Hoàn thành — Definition of Done (`DoD` v1.0)

### 3.1 DoD Cấp User Story / Task (`MC-xx`)
Một hạng mục chỉ được kéo sang cột **`Done`** khi thỏa mãn đồng thời **5 điều kiện nền tảng** và **Checklist Luật thép** tương ứng:

1. **Quy trình Git & CI sạch:**
   - Nhánh và commit gắn đúng mã `MC-<số>`, đúng phạm vi Zero File-Overlap.
   - Pull Request đã có ít nhất **`1` thành viên review & Approve**, check GitHub Actions CI báo xanh, đã merge sạch vào `develop` (hoặc `main` theo luồng release).
2. **Kiểm thử đạt chuẩn:**
   - Toàn bộ Unit Test / Integration Test và Test Case của Story chạy đạt trên môi trường local/Staging; không phát sinh Bug mức **Cao** hoặc **Nghiêm trọng** mới.
3. **Nghiệm thu vận hành thực tế:**
   - Chức năng chạy ổn định trên bản triển khai thực tế (`Staging` từ Sprint 4) và được **`PO/BA`** nghiệm thu chấp nhận tại **Sprint Review**.
4. **Đồng bộ tài liệu:**
   - Tài liệu kỹ thuật liên quan (Swagger `/docs`, [ERD.md](./ERD.md), [ROADMAP.md](./ROADMAP.md), [SESSION_LOG.md](./SESSION_LOG.md), hướng dẫn sử dụng) được cập nhật đồng bộ.
5. **Trách nhiệm giải trình khi dùng AI hỗ trợ:**
   - Thành viên phụ trách nắm rõ và giải thích được cơ chế code/tài liệu, đã tự kiểm chứng tính đúng đắn và chịu trách nhiệm hoàn toàn trước nhóm & giảng viên.

**Checklist Luật thép kỹ thuật & nghiệp vụ (bắt buộc rà soát khi code & review PR):**
- [ ] **Thời gian & Tiền tệ:** Dùng `GMT+7` (`Asia/Ho_Chi_Minh`) và tiền nguyên `VNĐ` trên API, DB và giao diện.
- [ ] **Chống trùng bàn (`FR-05`):** Bước `30p`, lượt `90p`, đặt trước `2h–30 ngày`; giữ chỗ `10p` trong cùng DB transaction + constraint `btree_gist`.
- [ ] **Đặt món & Xóa mềm (`FR-03`, `FR-06`):** Lưu `unit_price_locked` khi chốt món; chỉ dùng xóa mềm; chặn xóa món/bàn đã có đơn.
- [ ] **Bảo mật & Thanh toán (`NFR-02`, `FR-07`):** Ép RBAC 3 vai trò (`customer`, `staff`, `manager`) ở API (`403` + audit log); mật khẩu `bcrypt`; khóa `15p` sau `5` lần sai; không lưu số thẻ; webhook thanh toán kiểm tra `HMAC` và xử lý idempotent.
- [ ] **Chatbot AI Guardrails (`FR-13`, `FR-14`):** RAG chỉ lấy dữ liệu PostgreSQL thật; chạy **PII Masking** trước khi gửi Ollama; từ chối ngoài phạm vi/y tế/dị ứng; không tự báo "đã đặt thành công"; lỗi/timeout trả `is_fallback: true`; lưu log tối đa `90 ngày`.

### 3.2 DoD Cấp Sprint (Kết thúc mỗi tuần)
- Hoàn thành mục tiêu Sprint Goal hoặc ghi nhận rõ lý do chuyển backlog sang Sprint kế tiếp.
- `PM/SM` cập nhật đầy đủ `% hoàn thành` trên MS Project, biểu đồ **Burndown**, **Velocity**, chỉ số **EVM** (`SPI`, `CPI` từ Sprint 2), rà soát **Sổ rủi ro** và gửi báo cáo tuần cho GVHD.
- Cập nhật tick `[x]` trong [ROADMAP.md](./ROADMAP.md) và ghi entry mới tại [SESSION_LOG.md](./SESSION_LOG.md).

### 3.3 DoD Cấp Phát hành (`v0.1`, `v0.2`, `v1.0-rc`, `v1.0`)
| Mốc phát hành | Yêu cầu chất lượng bổ sung (Release Gate) |
| :--- | :--- |
| **`v0.1` (`M3` — Sprint 3)** | RBAC 3 vai trò, thực đơn, sơ đồ bàn, đặt bàn giữ chỗ `10p` vượt qua **Concurrent Test** (`0%` trùng bàn) & giỏ món `unit_price_locked`. |
| **`v0.2` (`M4` — Sprint 5)** | Cọc VNPay Sandbox (HMAC idempotent), vận hành NV (check-in, no-show, đổi bàn có log) & Chatbot AI RAG dữ liệu thật chạy trên Staging. |
| **`v1.0-rc` (`M5` — Sprint 6)** | **Feature Freeze**: `100%` MVP (`FR-01`..`FR-14`), Guardrails + `>= 20` câu test adversarial, đặt bàn qua chat `GMT+7`, báo cáo, bếp, nhắc `24h`/`2h`; backup DB trước UAT. |
| **`v1.0` (`M6` — Sprint 7)** | `>= 40` test case chức năng/API (Postman) đạt; bộ `>= 30` câu test AI đạt đúng `>= 80%`, `<= 5s` (`95%`); **`0` Bug Cao/Nghiêm trọng**; **Nhà hàng Ẩm thực Vườn Phố ký biên bản UAT (`>= 4/5`)**; đủ HDSD 3 vai trò & video demo `5–7 phút`. |

---

## 4. Điều phối Sự kiện Scrum & Kiểm soát Thay đổi (`CR / CCB`)

### 4.1 Lịch Sự kiện Scrum hằng tuần (`WBS 1.3.1.2` — Sprint 1 tuần)
| Sự kiện | Thời điểm | Time-box | Chủ trì & Tham gia | Đầu ra bắt buộc |
| :--- | :--- | :---: | :--- | :--- |
| **Sprint Planning** | Sáng Thứ Hai | `<= 2 giờ` | `PM/SM` điều phối; `PO/BA` trình bày; `2 Dev` ước lượng | Sprint Goal, Sprint Backlog trên Jira `MC` |
| **Daily Scrum** | Hằng ngày (`08:30` hoặc cuối ngày) | `<= 15 phút` | Luân phiên `FS`, `AI`, `PO/BA`, `PM/SM` | Cập nhật tiến độ, blocker & kéo cột Jira `MC` |
| **Backlog Refinement** | Thứ Tư / Thứ Năm | `<= 1 giờ` | `PO/BA` + `2 Dev` | Story Sprint sau đạt chuẩn **`DoR v1.0`** |
| **Sprint Review** | Chiều Chủ Nhật *(S6: `31/12`)* | `<= 1 giờ` | `PO/BA` nghiệm thu; `2 Dev` demo *(mời GV/Nhà hàng)* | Increment demo, Burndown, Velocity, chốt mốc `M1–M6` |
| **Sprint Retrospective** | Ngay sau Review | `<= 45 phút` | `PM/SM` điều phối; cả nhóm rút kinh nghiệm | Danh sách hành động cải tiến cho Sprint kế tiếp |

### 4.2 Quy trình Kiểm soát Thay đổi (`CR` & Hội đồng `CCB` — áp dụng sau `M2`)
Sau khi lưu **Baseline MS Project (`M2 – 29/11/2026`)**, mọi yêu cầu thêm/bớt tính năng, đổi luồng nghiệp vụ hoặc dời mốc thời gian đều phải đi qua quy trình 4 bước:
1. **Đề xuất (`CR`):** Tạo issue loại **Change Request (`CR`)** trên Jira `MC`, mô tả rõ lý do và phạm vi thay đổi.
2. **Đánh giá tác động:** `PO/BA` đánh giá giá trị nghiệp vụ; `PM/SM` + `2 Dev` đánh giá tác động đến **Story Points**, **đường găng MS Project**, **EVM / chi phí** và **Sổ rủi ro**.
3. **Phê duyệt bởi Hội đồng `CCB`:**
   - Thay đổi nhỏ trong giới hạn SP/thời gian Sprint: **CCB nội bộ nhóm** (`PM/SM`, `PO/BA`, `Dev Fullstack`, `AI Dev`) bỏ phiếu phê duyệt.
   - Thay đổi lớn (đổi phạm vi MVP `FR-01`..`FR-14`, dùng quỹ dự phòng `6.362.500 VNĐ`, hoặc dời mốc `M3–M6`): Bắt buộc xin phê duyệt **Nhà tài trợ (GVHD Nguyễn Hữu Trung)** và đại diện Nhà hàng nếu liên quan nghiệp vụ.
4. **Cập nhật & Thực thi:** Chỉ kéo vào Sprint tiếp theo *(và tuyệt đối không nhận thêm tính năng mới sau mốc **Feature Freeze `M5` ngày `03/01/2027`**)*.
