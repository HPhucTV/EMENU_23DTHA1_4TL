# BÁO CÁO ĐƯỜNG CƠ SỞ DỰ ÁN — BASELINE M2 (v1.0)

**Dự án:** Website đặt bàn và đặt món trước cho nhà hàng tích hợp chatbot AI (`QL09-W`)  
**Đơn vị áp dụng:** Nhà hàng Ẩm thực Vườn Phố *(TP. Hồ Chí Minh — tiền tệ `VNĐ`, múi giờ `GMT+7`)*  
**Task Jira:** `MC-70` | **Mã WBS:** `1.3.1.1` (`Mốc M2: 1.4`) | **Ngày chốt:** `26/11/2026` *(trước hạn mốc `M2` ngày `29/11/2026`)*  
**Người lập:** **Trần Hoàng Phúc** (`PM/SM` — MSSV: `2380601756`)  
**Tệp nguồn MS Project XML (đã lưu sẵn `Baseline 0`):** [MS_PROJECT_BASELINE_M2.xml](./MS_PROJECT_BASELINE_M2.xml)

---

## 1. Mục tiêu và Phạm vi Đường cơ sở (Scope Baseline)

Tài liệu này khóa 3 đường cơ sở gốc của dự án (**Phạm vi — Tiến độ — Chi phí**) tại cột mốc **`M2`** để làm chuẩn đối soát sai lệch (`Variance`), đo lường giá trị đạt được (**EVM**: `SPI`, `CPI`) từ Sprint 2 đến Sprint 7 và kiểm soát thay đổi qua quy trình **CR/CCB**.

### 1.1 Tổng hợp Phạm vi đã khóa tại Baseline `M2`
| Hạng mục phạm vi | Chỉ số Baseline `M2` | Nguồn đối chiếu chuẩn |
| :--- | :---: | :--- |
| **Tổng cấu trúc WBS** | **`164` dòng** (`37` gói công việc `A`–`AK`, `105` công việc lá, `51` dòng tổng hợp, `8` mốc) | [WBS 56 ngày](./references/WBS_QL09-W_Website_Dat_Ban_Nha_Hang_Chatbot_AI_56Ngay.xlsx) & [MS_PROJECT_BASELINE_M2.xml](./MS_PROJECT_BASELINE_M2.xml) |
| **Yêu cầu chức năng MVP** | **`FR-01` – `FR-14`** *(+ lõi `FR-15`)* | [SYSTEM_SPEC.md](./SYSTEM_SPEC.md) |
| **Yêu cầu phi chức năng** | **`NFR-01` – `NFR-06`** | [SYSTEM_SPEC.md](./SYSTEM_SPEC.md) |
| **User Story & Story Points MVP** | **`45 US` / `202 SP`** *(thuộc `10 Epic`)* | [ROADMAP.md](./ROADMAP.md) |
| **Task quản lý & kỹ thuật song song** | **`26 Task`** *(Sprint 0–7)* | [ROADMAP.md](./ROADMAP.md) |
| **Backlog dự phòng (không tính vào cam kết MVP)** | **`9 US` / `50 SP`** (`US-46` – `US-54`, chỉ kéo trước Feature Freeze `M5` nếu velocity vượt chuẩn) | [ROADMAP.md](./ROADMAP.md#L267-L281) |
| **Ngoài phạm vi (Out-of-Scope)** | Cấm làm: POS/VAT, kho/nguyên liệu, nhân sự/chấm công, delivery/take-away, app iOS/Android riêng, thanh toán tiền thật, fine-tune LLM | [SCOPE_STATEMENT.md](./SCOPE_STATEMENT.md#L73-L80) |

> **Quy tắc kiểm soát phạm vi sau `M2` (`29/11/2026`):** Mọi thay đổi tính năng, ngày mốc hoặc chi phí so với Baseline `M2` bắt buộc tạo **Change Request (`CR`)** trên Jira `MC`, đánh giá tác động bởi `PM/SM` + `PO/BA` và thông qua **Hội đồng CCB** trước khi thực hiện (chi tiết tại [DOR_DOD_QUALITY.md](./DOR_DOD_QUALITY.md)).

---

## 2. Đường cơ sở Tiến độ (Schedule Baseline)

### 2.1 Tham số Lịch làm việc & Thời lượng gốc
- **Thời gian dự án:** `16/11/2026 08:00` → `10/01/2027 17:00` (**`56 ngày lịch`** = **`8 Sprint × 7 ngày`**).
- **Lịch làm việc trong MS Project (`Standard - QL09-W 7 Ngay`):** `8 giờ/ngày` (`08:00–12:00` và `13:00–17:00`), chế độ `7 ngày/tuần` theo đúng quy ước bảng WBS, mỗi thành viên làm bán thời gian **`50%` Max Units** (`4 giờ/ngày` = `20 giờ/Sprint`).
- **Nghỉ lễ & làm bù:** Nghỉ Tết Dương lịch thứ Sáu **`01/01/2027`**; làm bù thứ Bảy **`02/01/2027`**; buổi **Sprint Review Sprint 6** tổ chức sớm vào **`31/12/2026`**.

### 2.2 Chuỗi phụ thuộc Găng & 8 Mốc kiểm soát (`M1` – `M6`)

```mermaid
flowchart LR
    S0["Sprint 0 (16/11-22/11 · 80h)"] --> M1["M1: Duyệt Tôn chỉ & Công cụ (22/11)"]
    M1 --> S1["Sprint 1 (23/11-29/11 · 28 SP)"]
    S1 --> M2["M2: Baseline MS Project (29/11)"]
    M2 --> S2["Sprint 2 (30/11-06/12 · 29 SP)"]
    S2 --> D2["Demo S2: Menu, Bàn & Chốt Ollama (06/12)"]
    D2 --> S3["Sprint 3 (07/12-13/12 · 29 SP)"]
    S3 --> M3["M3: Tag v0.1 Đặt bàn & Món (13/12)"]
    M3 --> S4["Sprint 4 (14/12-20/12 · 27 SP)"]
    S4 --> D4["Demo S4: Cọc Sandbox & Staging (20/12)"]
    D4 --> S5["Sprint 5 (21/12-27/12 · 31 SP)"]
    S5 --> M4["M4: Tag v0.2 NV & AI RAG (27/12)"]
    M4 --> S6["Sprint 6 (28/12-03/01 · 31 SP)"]
    S6 --> M5["M5: Feature Freeze v1.0-rc (03/01)"]
    M5 --> S7["Sprint 7 (04/01-10/01 · 27 SP)"]
    S7 --> M6["M6: UAT & Go-live v1.0 (10/01)"]
```

| WBS | UID XML | Mốc kiểm soát | Ngày Baseline | Điều kiện đạt (Exit Criteria) | Người xác nhận |
| :---: | :---: | :--- | :---: | :--- | :--- |
| `1.2` | `17` | **M1:** Hoàn thành Sprint 0 | `22/11/2026` | Tôn chỉ `D01`, SRS `v1.1`, Backlog đầu duyệt; GitHub, Jira `MC`, MS Project lập xong & mời GV | Nhà tài trợ (GV) |
| `1.4` | `36` | **M2:** Lưu Baseline MS Project | `29/11/2026` | Scope `D02`, WBS `640h`, Gantt/PERT, dự toán `69.987.500 VNĐ` duyệt; lưu Baseline MS Project; CI xanh | Nhà tài trợ, PO/BA |
| `1.6` | `56` | *Demo S2:* Thực đơn, Bàn & Ollama | `06/12/2026` | Demo thực đơn, sơ đồ bàn kéo thả dữ liệu ẩn danh; ký duyệt phương án Ollama (`US-15`) & lõi RAG | PO/BA, Nhà hàng |
| `1.8` | `77` | **M3:** Demo `v0.1` | `13/12/2026` | RBAC 3 vai trò, thực đơn, sơ đồ bàn, đặt bàn chống trùng (Concurrent Test đạt) & giỏ món; tag `v0.1` | PO/BA, Nhà hàng |
| `1.10` | `98` | *Demo S4:* Cọc Sandbox & Staging | `20/12/2026` | Demo đặt bàn, đặt món, cọc VNPay Sandbox, hủy/hoàn cọc & Email trên Staging; cập nhật EVM | PO/BA, Nhà hàng |
| `1.12` | `122` | **M4:** Báo cáo giữa kỳ (`v0.2`) | `27/12/2026` | Báo cáo giữa kỳ; vận hành NV (check-in, no-show, đổi bàn) & Chatbot AI dữ liệu thật trên Staging; tag `v0.2` | Giảng viên, PO/BA |
| `1.14` | `144` | **M5:** Feature Freeze (`v1.0-rc`) | `03/01/2027` | Hoàn thiện 100% MVP (`FR-01`..`FR-14`), Guardrails AI, đặt bàn qua chat, báo cáo, bếp, nhắc `24h`/`2h` *(Review sớm `31/12`)* | PO/BA, Nhà hàng |
| `1.16` | `164` | **M6:** Bảo vệ & Go-live (`v1.0`) | `10/01/2027` | Release `v1.0` *(bàn giao `08/01`)*; `0` Bug Cao/Nghiêm trọng; AI đúng `>= 80%` trên `>= 30` câu; ký UAT nhà hàng; đủ HDSD & video | Giảng viên, Nhà hàng |

---

## 3. Đường cơ sở Nguồn lực & Chi phí (`Resource & Cost Baseline`)

### 3.1 Bảng Tài nguyên (Resource Sheet) — Tổng `640 giờ` (`62.000.000 VNĐ`)
| UID XML | Tài nguyên | Viết tắt | Max Units | Đơn giá (VNĐ/giờ) | Giờ công Baseline | Thành tiền (VNĐ) |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| `1` | **Trần Hoàng Phúc** *(PM/SM)* | `PM/SM` | `50%` | `100.000` | `160h` | `16.000.000` |
| `2` | **Võ Đăng Khoa** *(PO/BA)* | `PO/BA` | `50%` | `87.500` | `160h` | `14.000.000` |
| `3` | **Nguyễn Văn Tiến** *(Dev Fullstack)* | `FS` | `50%` | `100.000` | `160h` | `16.000.000` |
| `4` | **Nguyễn Đoàn Trường Vũ** *(AI Dev)* | `AI` | `50%` | `100.000` | `160h` | `16.000.000` |
| **Tổng** | **4 thành viên (`105` công việc lá)** | — | **`50%`/người** | — | **`640h`** | **`62.000.000`** |

### 3.2 Chi phí cố định Hạ tầng & Dịch vụ (`1.625.000 VNĐ` — WBS `1.9.4`, UID `91`)
| Hạng mục | Thời điểm giải ngân | Đơn giá & Định mức | Chi phí Baseline (VNĐ) |
| :--- | :---: | :--- | :---: |
| Cloud / VPS chạy Web App + Ollama | Sprint 4 (`14/12 – 20/12`) | `45 ngày × 25.000 VNĐ/ngày` (Sprint 4–7) | `1.125.000` |
| Tên miền (`Domain`) | Sprint 4 (`14/12 – 20/12`) | `1 năm` | `300.000` |
| Dịch vụ Email & SMS nhắc lịch `2h` | Sprint 4 (`14/12 – 20/12`) | Brevo Free (`0đ`) + SpeedSMS/eSMS gói trả trước | `200.000` |
| Cổng thanh toán **VNPay Sandbox** & Ollama | Sprint 0–7 | Miễn phí môi trường Sandbox & tự host LLM | `0` |
| **Tổng chi phí cố định (`FixedCost`)** | **Sprint 4 (`UID 91`)** | — | **`1.625.000`** |

### 3.3 Đường cơ sở Chi phí (`BAC`) & Kế hoạch Giá trị Dự kiến (`PV` cho EVM)
- **Tổng Chi phí Cơ sở (`BAC` — Budget at Completion):** `62.000.000 + 1.625.000 =` **`63.625.000 VNĐ`** *(khớp 100% `UID 1` trong [MS_PROJECT_BASELINE_M2.xml](./MS_PROJECT_BASELINE_M2.xml))*.
- **Quỹ Dự phòng Rủi ro (`10% × BAC` — Management Reserve):** **`6.362.500 VNĐ`** *(nằm ngoài `BAC`, chỉ giải ngân khi có CR hoặc rủi ro được phê duyệt)*.
- **Tổng Ngân sách trong Tôn chỉ dự án (`D01`):** **`69.987.500 VNĐ`**.

| Sprint | WBS | Thời gian | SP MVP | Giờ công | Nhân công (VNĐ) | Chi phí cố định (VNĐ) | Tổng Sprint (VNĐ) | **PV Lũy kế (VNĐ)** |
| :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sprint 0** | `1.1` | `16/11 – 22/11/2026` | — | `80h` | `7.750.000` | `0` | `7.750.000` | **`7.750.000`** |
| **Sprint 1** | `1.3` | `23/11 – 29/11/2026` | `28` | `80h` | `7.750.000` | `0` | `7.750.000` | **`15.500.000`** |
| **Sprint 2** | `1.5` | `30/11 – 06/12/2026` | `29` | `80h` | `7.750.000` | `0` | `7.750.000` | **`23.250.000`** |
| **Sprint 3** | `1.7` | `07/12 – 13/12/2026` | `29` | `80h` | `7.750.000` | `0` | `7.750.000` | **`31.000.000`** |
| **Sprint 4** | `1.9` | `14/12 – 20/12/2026` | `27` | `80h` | `7.750.000` | `1.625.000` | `9.375.000` | **`40.375.000`** |
| **Sprint 5** | `1.11` | `21/12 – 27/12/2026` | `31` | `80h` | `7.750.000` | `0` | `7.750.000` | **`48.125.000`** |
| **Sprint 6** | `1.13` | `28/12/2026 – 03/01/2027` | `31` | `80h` | `7.750.000` | `0` | `7.750.000` | **`55.875.000`** |
| **Sprint 7** | `1.15` | `04/01 – 10/01/2027` | `27` | `80h` | `7.750.000` | `0` | `7.750.000` | **`63.625.000` (`BAC`)** |

**Ngưỡng kiểm soát Earned Value (EVM) áp dụng từ Sprint 2:**
- `SPI = EV / PV` *(mục tiêu **`>= 0,90`**)*; `CPI = EV / AC` *(mục tiêu **`>= 0,90`**)*.
- Nếu `SPI < 0,90` hoặc `CPI < 0,90` hoặc chi phí vượt `> 10%` kế hoạch: PM lập báo cáo nguyên nhân & phương án khắc phục gửi **Nhà tài trợ (GVHD)** ngay trong tuần.

---

## 4. Hướng dẫn Mở và Chốt File `.mpp` trên Microsoft Project

Tệp [MS_PROJECT_BASELINE_M2.xml](./MS_PROJECT_BASELINE_M2.xml) đã được dựng theo chuẩn **MSPDI (`http://schemas.microsoft.com/project`)** với đầy đủ `164` dòng WBS, `4` tài nguyên, `105` phân công (`Assignment`), lịch làm việc và dữ liệu **`Baseline 0`** lưu sẵn cho từng công việc:

1. **Mở tệp XML trong Microsoft Project:**
   - Mở **Microsoft Project** → **File → Open → Browse** → ở góc dưới bên phải đổi bộ lọc từ `Projects (*.mpp)` sang **`XML Format (*.xml)`** (hoặc `All Files (*.*)`).
   - Chọn tệp `docs/MS_PROJECT_BASELINE_M2.xml` → ở hộp thoại Import Wizard chọn **`As a new project`** → bấm **Finish**.
2. **Kiểm tra dữ liệu Baseline M2 đã lưu sẵn:**
   - Vào tab **View → Tables → Variance** (kiểm tra `Baseline Start` = `16/11/2026`, `Baseline Finish` = `10/01/2027`, `Variance = 0 days`).
   - Vào tab **View → Tables → Cost** (kiểm tra `Baseline Cost` = **`63.625.000 VNĐ`**).
   - Vào tab **View → Resource Sheet** (kiểm tra đủ `4` thành viên với `Max. Units = 50%`, không quá tải đỏ).
   - *(Lưu ý nếu MS Project tự động dời lịch Sprint 6 thêm 1 ngày do ngày nghỉ `01/01/2027` — hãy kiểm tra ở `Tracking Gantt`: phần thanh xám `Baseline` vẫn giữ nguyên cố định `16/11/2026 – 10/01/2027`, hoặc tắt `Project → Change Working Time` cho ngày `01/01/2027` nếu muốn giữ tròn `56` ngày làm việc theo Excel).*
3. **Lưu thành tệp `.mpp` & Chụp minh chứng nộp `M2`:**
   - Bấm **File → Save As** → lưu dưới định dạng **`Project (*.mpp)`** (ví dụ `QL09-W_Baseline_M2.mpp`) để theo dõi `% Complete` hàng tuần.
   - Chụp ảnh màn hình **Tracking Gantt** (thấy thanh Baseline xám) và **Resource Sheet** đính kèm lên issue Jira **`MC-70`** để nghiệm thu mốc **`M2`**.
