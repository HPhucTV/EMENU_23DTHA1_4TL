# TÔN CHỈ DỰ ÁN (PROJECT CHARTER)

**Học phần:** Quản lý dự án Công nghệ thông tin • **Mã đề tài:** QL09-W

| Thông tin chung | Chi tiết |
| --- | --- |
| Tên dự án (Project Title): | Website đặt bàn và đặt món trước cho nhà hàng tích hợp chatbot AI (Restaurant Table Reservation and Pre-order Website with AI Chatbot) — Mã đề tài: QL09-W |
| Ngày bắt đầu (Project Start Date): | 16/11/2026 |
| Ngày kết thúc dự kiến (Projected Finish Date): | 10/01/2027 (8 tuần: Sprint 0 – Khởi động đến Sprint 7 – Phát hành, mỗi Sprint 1 tuần; nghỉ Tết Dương lịch 01/01/2027) |
| GĐ Dự án (Project Manager): | [Trần Hoàng Phúc] — MSSV: [2380601756] — ĐT: [……] — Email: [……] |

---

## 1. Thông tin về Kinh phí (Budget Information)

**Tổng kinh phí dự kiến: 69.987.500 VNĐ**, được phân bổ chi tiết theo 4 vai trò nhân sự (PM, BA, Dev Fullstack, AI Dev), dịch vụ hạ tầng và dự phòng rủi ro như sau:

- **Nhân công (62.000.000 VNĐ):** 4 thành viên × 20 ngày công (8 tuần × 2,5 ngày/tuần = 80 ngày công); đơn giá giả định theo vai trò (VNĐ/ngày):
  - **PM / Scrum Master (PM/SM):** 20 ngày × 800.000 VNĐ/ngày = 16.000.000 VNĐ (lập kế hoạch, điều phối 8 Sprint, quản lý Jira SCRUM, MS Project, Earned Value, quy trình thay đổi CCB, báo cáo tuần).
  - **Product Owner / Business Analyst (PO/BA):** 20 ngày × 700.000 VNĐ/ngày = 14.000.000 VNĐ (khảo sát nhà hàng, viết SRS và quản lý Product Backlog 54 user story, thiết kế wireframe Figma, chuẩn hóa dữ liệu mẫu ẩn danh, kiểm thử hồi quy/QA, UAT và viết hướng dẫn sử dụng).
  - **Lập trình viên Fullstack (Dev Fullstack):** 20 ngày × 800.000 VNĐ/ngày = 16.000.000 VNĐ (kiến trúc hệ thống, ERD và migration PostgreSQL, giao diện ReactJS, REST API FastAPI core, thuật toán giữ bàn chống trùng, cổng thanh toán sandbox, báo cáo, CI/CD GitHub Actions và triển khai).
  - **Kỹ sư AI (AI Dev):** 20 ngày × 800.000 VNĐ/ngày = 16.000.000 VNĐ (đánh giá và triển khai mô hình Ollama có sẵn, FastAPI AI Router, truy xuất dữ liệu thực tế RAG từ PostgreSQL, parser thời gian GMT+7, luồng đặt bàn qua chat, Guardrails/che dữ liệu cá nhân PII và bộ 30+ câu kiểm thử chatbot).
- **Dịch vụ và hạ tầng (1.625.000 VNĐ):** Máy chủ Cloud/VPS chạy Web App (ReactJS, FastAPI, PostgreSQL) & Ollama LLM (Staging + Production) 1.125.000 VNĐ (45 ngày từ Sprint 4 đến Sprint 7 × 25.000 VNĐ/ngày; chatbot dùng mô hình mở tự host trên Ollama nên chi phí gọi API LLM bên ngoài = 0 VNĐ); Tên miền 300.000 VNĐ (1 năm); Dịch vụ Email SMTP & SMS nhắc lịch 200.000 VNĐ (SMS dùng cho nhắc lịch trước 2 giờ theo hạn mức thử nghiệm); Cổng thanh toán trực tuyến 0 VNĐ (môi trường Sandbox).
- **Công cụ phát triển và quản lý (0 VNĐ):** GitHub (repo private và GitHub Actions gói miễn phí), Jira Software (gói Free, khóa SCRUM), Figma (gói giáo dục), Microsoft Project (bản quyền của trường), Ollama và các mô hình LLM mã nguồn mở có sẵn.
- **Dự phòng rủi ro (6.362.500 VNĐ):** 10% × 63.625.000 VNĐ (tổng chi phí nhân công, dịch vụ và hạ tầng).
- **Kiểm soát ngân sách:** Nhà tài trợ phê duyệt ngân sách; nếu chi phí thực tế vượt quá 10% kế hoạch hoặc chỉ số hiệu quả chi phí CPI < 0,9 thì PM báo cáo nhà tài trợ trong tuần. Số liệu chi tiết trình bày trong báo cáo dự án và khớp với Resource Sheet / Baseline trên tệp Microsoft Project.

| Hạng mục chi phí | Diễn giải tính toán | Thành tiền (VNĐ) |
| --- | --- | --- |
| 1. Chi phí nhân công | 4 thành viên × 20 ngày công (80 ngày công) | 62.000.000 |
| • PM / Scrum Master (PM/SM) | 20 ngày × 800.000 VNĐ/ngày | 16.000.000 |
| • Product Owner / Business Analyst (PO/BA) | 20 ngày × 700.000 VNĐ/ngày | 14.000.000 |
| • Lập trình viên Fullstack (Dev Fullstack) | 20 ngày × 800.000 VNĐ/ngày | 16.000.000 |
| • Kỹ sư AI (AI Dev) | 20 ngày × 800.000 VNĐ/ngày | 16.000.000 |
| 2. Dịch vụ và hạ tầng | Phục vụ môi trường Staging, Production & kiểm thử | 1.625.000 |
| • Cloud/VPS (Web App + Ollama LLM) | 45 ngày × 25.000 VNĐ/ngày (Ollama tự host, API LLM = 0 VNĐ) | 1.125.000 |
| • Tên miền (Domain) & Email/SMS thông báo | Domain 1 năm (300.000) + Email/SMS nhắc lịch (200.000) | 500.000 |
| • Cổng thanh toán trực tuyến (Sandbox) | Môi trường thử nghiệm giao dịch đặt cọc | 0 |
| 3. Công cụ quản lý & phát triển | GitHub, Jira (SCRUM), Figma, MS Project, Ollama | 0 |
| **Tổng chi phí cơ sở (1 + 2 + 3)** | | **63.625.000** |
| 4. Dự phòng rủi ro (10%) | 10% × 63.625.000 VNĐ | 6.362.500 |
| **TỔNG KINH PHÍ DỰ KIẾN** | **Đã bao gồm 10% dự phòng rủi ro** | **69.987.500** |

---

## 2. Mục tiêu dự án (Project Objectives)

- **Mục tiêu nghiệp vụ cốt lõi (Product Goal):** Xây dựng website đặt bàn và đặt món trước cho nhà hàng tích hợp chatbot AI (QL09-W), cho phép khách hàng đặt bàn theo khung giờ (bước 30 phút, lượt phục vụ 90 phút, đặt trước từ 2 giờ đến 30 ngày theo múi giờ GMT+7), đặt món trước và đặt cọc trực tuyến 24/7; giúp nhà hàng sắp xếp sơ đồ bàn, chuẩn bị bếp chính xác và giảm tỷ lệ khách đặt nhưng không đến (no-show).
- **Tích hợp Chatbot AI (Ollama):** Tích hợp trợ lý hội thoại AI sử dụng mô hình ngôn ngữ lớn mở có sẵn chạy trên Ollama (không huấn luyện hay tinh chỉnh mô hình), truy xuất dữ liệu thực tế (RAG) từ PostgreSQL để tư vấn món ăn (kèm thẻ món thêm vào đơn), giải đáp giờ mở cửa, chính sách đặt cọc/hủy và hỗ trợ đặt bàn qua hội thoại; trang bị Guardrails chống bịa thông tin (ảo giác), che dữ liệu cá nhân (PII) trước khi gửi lên LLM và ghi nhật ký hội thoại; trả lời đúng ≥ 80% trên bộ ≥ 30 câu hỏi kiểm thử chuẩn và dẫn dụ, phản hồi trong vài giây.
- **Hoàn thành phạm vi chức năng MVP trước khi đóng băng tính năng (hết Sprint 6):** Hoàn tất 45 user story (202 Story Points) thuộc các yêu cầu chức năng MVP trong SRS (FR-01 đến FR-14 và lõi FR-15) trên bản triển khai thật:
  1. Xác thực và phân quyền 3 vai trò: Khách hàng, Nhân viên, Quản lý (FR-01).
  2. Xem, tìm kiếm, lọc và quản lý thực đơn, tình trạng còn/hết, lưu lịch sử đổi giá (FR-02, FR-03).
  3. Quản lý khu vực, sơ đồ bàn trực quan kéo thả và trạng thái bàn theo ngày/giờ (FR-04).
  4. Đặt bàn theo khung giờ và số khách, giữ chỗ tạm thời 10 phút kèm ràng buộc cơ sở dữ liệu chống trùng bàn (FR-05).
  5. Đặt món trước với giá chốt, đặt cọc trực tuyến qua cổng thanh toán sandbox (xử lý callback/webhook an toàn), hủy đặt chỗ và hoàn cọc theo chính sách (FR-06, FR-07, FR-09).
  6. Vận hành đặt chỗ cho nhân viên (check-in, đổi bàn/giờ, đánh dấu không đến), gửi email/SMS nhắc lịch trước 24 giờ và 2 giờ, tổng hợp danh sách món chuẩn bị cho bếp (FR-08, FR-10, FR-11).
  7. Báo cáo thống kê số đơn, tỷ lệ hủy/không đến, doanh thu cọc và đơn đặt ngoài giờ làm việc (FR-12).
  8. Chatbot AI tư vấn món, giải đáp chính sách và hỗ trợ đặt bàn qua hội thoại chuẩn hóa GMT+7 (FR-13, FR-14).
- **Đáp ứng yêu cầu kỹ thuật và an toàn dữ liệu:** Kiến trúc client–server gồm front-end ReactJS (responsive trên điện thoại và máy tính), back-end Python FastAPI (REST API có tài liệu Swagger), cơ sở dữ liệu PostgreSQL (quản lý migration bằng Alembic, có ràng buộc chống trùng bàn), dịch vụ Ollama cho AI; truyền tải qua HTTPS, mật khẩu lưu dạng băm, không lưu số thẻ thanh toán; tự động hóa kiểm thử/build qua GitHub Actions.
- **Áp dụng thực tế và kiểm thử nghiệm thu (UAT) tại đơn vị nhà hàng:** Sử dụng bộ dữ liệu thực đơn, sơ đồ bàn, chính sách thực tế đã ẩn danh từ đơn vị áp dụng; thực hiện kiểm thử hệ thống, hồi quy và UAT theo kịch bản với đơn vị áp dụng trong Sprint 7 (không còn lỗi mức Cao hoặc Nghiêm trọng); đạt giá trị đo lường nhận đặt bàn 24/7 (tăng đơn đặt ngoài giờ làm việc) và giảm tỷ lệ khách không đến nhờ cơ chế đặt cọc và nhắc lịch.
- **Quản lý dự án:** Bàn giao sản phẩm phiên bản v1.0 đúng hạn ngày 08/01/2027, trong ngân sách 69.987.500 VNĐ; duy trì chỉ số tiến độ SPI ≥ 0,9 và chi phí CPI ≥ 0,9 qua các Sprint; 100% user story hoàn thành (Done) đáp ứng Definition of Done; hoàn thiện đầy đủ hồ sơ quản lý dự án theo yêu cầu học phần.
- **Ngoài phạm vi (Out of Scope):** Thanh toán toàn bộ hóa đơn tại bàn (POS) và xuất hóa đơn VAT; quản lý kho, nguyên liệu, nhân sự và chấm công; chức năng giao hàng và mang đi; ứng dụng di động riêng biệt (website được thiết kế responsive cho điện thoại); huấn luyện hoặc tinh chỉnh (fine-tune) mô hình AI. (Các tính năng mở rộng FR-15 đến FR-18 gồm quản trị tri thức AI nâng cao, đặt tiệc/sự kiện, đánh giá nhà hàng và chatbot tool calling nằm trong danh mục dự phòng 50 SP, chỉ kéo vào Sprint nếu velocity vượt kế hoạch trước thời điểm đóng băng tính năng hết Sprint 6).

---

## 3. Cách tiếp cận (Approach)

- **Quy trình Scrum:** Áp dụng khung làm việc Scrum (Scrum Guide 2020) gồm 8 tuần (Sprint 0 khởi động + 7 Sprint phát triển và phát hành, mỗi Sprint 1 tuần; velocity kế hoạch 27–31 SP/Sprint). Mỗi Sprint có Sprint Planning đầu tuần (≤ 2 giờ), Daily Scrum hằng ngày (≤ 15 phút), Backlog Refinement giữa tuần (≤ 1 giờ), Sprint Review cuối tuần (≤ 1 giờ) và Sprint Retrospective (≤ 45 phút).
- **Lộ trình thực hiện 8 tuần (Sprint 0 đến Sprint 7):** Chi tiết mục tiêu, hạng mục công việc, khối lượng Story Points và mốc nghiệm thu từng Sprint:

| Sprint / Thời gian | Nội dung trọng tâm & Sản phẩm bàn giao | SP | Mốc & Tag |
| --- | --- | --- | --- |
| Sprint 0 – Khởi động<br>(16/11 – 22/11/2026) | Khảo sát nghiệp vụ nhà hàng; lập SOW, Tôn chỉ dự án (D01), Phát biểu phạm vi (D02), Product Backlog bản đầu (D03), RACI (D14), Kế hoạch truyền thông (D17), Phân tích bên liên quan (D24); thiết lập GitHub, Jira (SCRUM), MS Project và mời GV; cài Ollama local & chốt Chat API Contract. | — | M1<br>(Duyệt đề tài & Tôn chỉ) |
| Sprint 1<br>(23/11 – 29/11/2026) | Dựng khung ReactJS + FastAPI + PostgreSQL, thiết kế ERD & Alembic migration (ràng buộc chống trùng bàn), wireframe Figma; đăng ký, đăng nhập, quên mật khẩu, phân quyền 3 vai trò (FR-01); CI GitHub Actions; benchmark mô hình Ollama; lập WBS, lịch, Resource Sheet & lưu Baseline MS Project. | 28 SP | M2<br>(Baseline MS Project) |
| Sprint 2<br>(30/11 – 06/12/2026) | Xem, tìm kiếm, lọc và quản lý thực đơn, tình trạng món, lịch sử đổi giá (FR-02, FR-03); quản lý khu vực, bàn và sơ đồ bàn kéo thả (FR-04); chuẩn hóa & nạp dữ liệu mẫu ẩn danh; nghiệm thu Spike chốt mô hình Ollama (US-15) & dựng lõi RAG từ PostgreSQL; lập EVM lần đầu. | 29 SP | — |
| Sprint 3<br>(7/12 – 13/12/2026) | Kiểm tra bàn trống và giữ chỗ tạm thời 10 phút chống trùng bàn có test đồng thời (FR-05); giao diện đặt bàn kèm countdown; cấu hình tham số nghiệp vụ; giỏ món đặt trước, lưu giá chốt và tính tiền cọc (FR-06); parser thời gian GMT+7, luồng đặt bàn chat & PII Masker v1. | 29 SP | M3<br>Tag v0.1 |
| Sprint 4<br>(14/12 – 20/12/2026) | Xem trạng thái bàn theo ngày/giờ; thanh toán đặt cọc qua cổng Sandbox và xử lý callback/webhook xác thực chữ ký, chống trùng lặp (FR-07); trang "Đặt chỗ của tôi", hủy đơn & yêu cầu hoàn cọc (FR-09); email xác nhận/hủy (FR-10); triển khai tự động Staging (gồm Ollama & khung chat); quy trình CR/CCB. | 27 SP | — |
| Sprint 5<br>(21/12 – 27/12/2026) | Vận hành đặt chỗ cho nhân viên: danh sách, bộ lọc, chi tiết đơn, check-in, hoàn thành, nhắc quá 15p, đánh dấu không đến, đổi bàn/giờ có nhật ký (FR-08); tích hợp chính thức Chatbot AI trên dữ liệu thật kèm thẻ món "Thêm vào đơn" (FR-13); cập nhật Earned Value. | 31 SP | M4<br>Tag v0.2 |
| Sprint 6<br>(28/12 – 3/01/2027) | Guardrails chatbot (che PII, chống bịa tin, từ chối ngoài phạm vi/y tế, rate limit) và đặt bàn qua chat GMT+7 (FR-13, FR-14); báo cáo thống kê đơn, tỷ lệ hủy/no-show, doanh thu cọc, đặt ngoài giờ (FR-12); tổng hợp món cho bếp (FR-11) & nhắc lịch 24h/2h (FR-10). (Sprint Review ngày 31/12 do nghỉ Tết Dương lịch 01/01). | 31 SP | M5 (Feature Freeze)<br>Tag v1.0-rc |
| Sprint 7 – Phát hành<br>(04/01 – 10/01/2027) | Kiểm thử toàn bộ hệ thống, hồi quy (Postman & test case), chạy bộ ≥ 30 câu test Chatbot (US-40); chạy UAT với đơn vị nhà hàng (US-41); sửa lỗi UAT, hardening bảo mật/hiệu năng & test backup/restore (US-42); viết hướng dẫn sử dụng 3 vai trò (US-43); triển khai Production, báo cáo tổng kết & video demo. | 27 SP | M6<br>Tag v1.0 (Bàn giao) |

- **Kiến trúc làm việc song song không xung đột (Zero File-Overlap):** Phân vùng sở hữu thư mục cứng giữa Dev Fullstack (`frontend/`, `backend/app/core|api|services/`, `core_models.py`) và AI Dev (`backend/app/ai/`, `chat_router.py`, `ai_models.py`, `ollama/`), giao tiếp qua Chat API Contract chốt từ Sprint 0 và hàm kiểm tra bàn trống chỉ đọc `availability_service` để loại bỏ xung đột mã nguồn.
- **Công cụ quản lý:** Jira Software (dự án Scrum, khóa SCRUM, quản lý 10 Epic, 54 User Story, Bug, CR, Burndown, Velocity); GitHub (repo private, nhánh `main`/`develop`/`feature/SCRUM-xx`, pull request bắt buộc review, GitHub Actions CI/CD, tag phát hành); Microsoft Project (WBS, Gantt, đường găng, Baseline, Earned Value); Figma; Zalo và Google Meet.
- **Công nghệ:** Front-end ReactJS; Back-end Python FastAPI (REST API + Swagger); Cơ sở dữ liệu PostgreSQL (Alembic migration); Chatbot AI dùng mô hình ngôn ngữ mở chạy sẵn trên Ollama; Cổng thanh toán Sandbox; Dịch vụ Email/SMS; Triển khai Docker trên Cloud/VPS.
- **Kiểm soát dự án:** Thay đổi phạm vi xử lý qua quy trình CR và Hội đồng kiểm soát thay đổi (CCB gồm PO/BA, PM, Dev Fullstack, AI Dev và xin duyệt giảng viên với thay đổi lớn); cập nhật tiến độ và Earned Value cuối mỗi Sprint; rà soát Sổ rủi ro hằng tuần (bao gồm rủi ro ảo giác AI, lộ PII, trùng bàn, khách không đến); gửi báo cáo tuần cho giảng viên.

---

## 4. Vai trò và Trách nhiệm (Roles and Responsibilities)

| Vai trò | Họ Tên | Tổ chức / Vị trí (Organization/Position) | Liên hệ (Contact information) |
| --- | --- | --- | --- |
| Nhà tài trợ (Project Sponsor) | Nguyễn Hữu Trung (GVHD) | Khoa CNTT – HUTECH — Giảng viên hướng dẫn học phần; phê duyệt đề tài, tôn chỉ, ngân sách, các thay đổi lớn; đánh giá các mốc M1–M6 và nghiệm thu cuối. | [ĐT] / [Email] |
| Đại diện khách hàng (Customer) | [Họ tên đại diện nhà hàng] | Nhà hàng [Tên đơn vị áp dụng] — [Chức vụ]; cung cấp thực đơn, sơ đồ bàn, chính sách và dữ liệu mẫu; góp ý tại Sprint Review; tham gia UAT và xác nhận nghiệm thu. | [ĐT] / [Email] |
| Quản lý dự án / Scrum Master (PM / SM) | Trần Hoàng Phúc | Nhóm [..] — Lập kế hoạch, quản lý tiến độ, chi phí, Earned Value (MS Project); điều phối các sự kiện Scrum; quản lý Jira (SCRUM), sổ rủi ro, quy trình CR/CCB; lập báo cáo tuần. | [ĐT] / [Email] |
| Chủ sản phẩm / Phân tích nghiệp vụ (PO / BA) | Võ Đăng Khoa | Nhóm [..] — Khảo sát nhà hàng, viết SRS và quản lý Product Backlog (54 user story) trên Jira; thiết kế wireframe Figma; chuẩn hóa dữ liệu mẫu ẩn danh; xây dựng test case, điều phối kiểm thử hồi quy, UAT và viết hướng dẫn sử dụng. | [ĐT] / [Email] |
| Lập trình viên Fullstack (Dev Fullstack) | Nguyễn Văn Tiến | Nhóm [..] — Thiết kế kiến trúc hệ thống, ERD và migration PostgreSQL; phát triển giao diện ReactJS (bao gồm khung chat), REST API FastAPI core, dịch vụ kiểm tra/giữ bàn chống trùng, cổng thanh toán sandbox, báo cáo, CI/CD GitHub Actions và triển khai Staging/Production. | [ĐT] / [Email] |
| Kỹ sư AI (AI Dev) | Nguyễn Đoàn Trường Vũ | Nhóm [..] — Đánh giá, lựa chọn và đóng gói mô hình Ollama có sẵn; xây dựng FastAPI AI Router, tầng truy xuất dữ liệu thực tế (RAG) từ PostgreSQL, parser thời gian GMT+7, luồng đặt bàn qua hội thoại, Guardrails chống bịa tin/che dữ liệu cá nhân (PII) và bộ 30+ câu kiểm thử chatbot. | [ĐT] / [Email] |

---

## 5. Phê duyệt và Ký tên (Sign-off & Comments)

**Ký tên (Sign-off):** (Chữ ký xác nhận của các bên liên quan và toàn bộ thành viên nhóm dự án.) — **Ngày duyệt:** …/11/2026 – Mốc M1, Sprint 0.

| | | |
| --- | --- | --- |
| **Nhà tài trợ (Project Sponsor)**<br>(Ký và ghi rõ họ tên) | **Đại diện khách hàng (Customer)**<br>(Ký và ghi rõ họ tên) | **Quản lý dự án (PM / SM)**<br>(Ký và ghi rõ họ tên)<br>Trần Hoàng Phúc |
| **Chủ sản phẩm (PO / BA)**<br>(Ký và ghi rõ họ tên)<br>Võ Đang Khoa | **Lập trình viên Fullstack (Dev Fullstack)**<br>(Ký và ghi rõ họ tên)<br>Nguyễn Văn Tiến | **Kỹ sư AI (AI Dev)**<br>(Ký và ghi rõ họ tên)<br>Nguyễn Đoàn Trường Vũ |

**Chú thích (Comments):** (Nhận xét viết tay hoặc đánh máy của Nhà tài trợ, Đại diện nhà hàng hoặc các bên liên quan, nếu có.)
