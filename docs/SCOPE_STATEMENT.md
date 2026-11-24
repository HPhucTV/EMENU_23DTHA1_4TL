# PHÁT BIỂU PHẠM VI DỰ ÁN (SCOPE STATEMENT)

**Học phần:** Quản lý dự án Công nghệ thông tin • **Mã đề tài:** QL09-W • **Tài liệu:** D02

| Thông tin tài liệu | Nội dung chi tiết |
| --- | --- |
| Tên dự án (Project Title) | Website đặt bàn và đặt món trước cho nhà hàng tích hợp chatbot AI (Restaurant Table Reservation and Pre-order Website with AI Chatbot) — Mã đề tài: QL09-W |
| Đơn vị áp dụng thực tế | Nhà hàng Ẩm thực Vườn Phố (1 cơ sở tại TP. Hồ Chí Minh, tiền tệ VNĐ, múi giờ GMT+7) |
| Ngày lập & Phiên bản (Date) | …/11/2026 – Sprint 1 (23/11 – 29/11/2026), duyệt trước mốc M2 ngày 29/11/2026. Phiên bản 1.0, căn cứ Tôn chỉ dự án (D01) đã duyệt tại mốc M1 (22/11/2026). |
| Người viết (Prepared by) | [Họ tên thành viên BA – Product Owner / Business Analyst]; phối hợp [Họ tên thành viên PM – PM/Scrum Master], [Dev Fullstack], [AI Dev]. |

---

## 1. Lý giải về dự án (Project Justification)

Đơn vị áp dụng là Nhà hàng Ẩm thực Vườn Phố có phục vụ tại bàn, quy mô 1 cơ sở với nhiều khu vực bàn (tầng trệt, sân vườn, phòng riêng VIP) và thực đơn đa dạng. Hiện tại nhà hàng tiếp nhận đặt bàn và đặt món thủ công qua điện thoại và tin nhắn mạng xã hội nên thường xuyên phát sinh tình trạng ghi nhầm khung giờ, trùng bàn, khách đặt nhưng không đến (no-show) và chậm phản hồi thắc mắc của khách. Dự án xây dựng một nền tảng website đặt bàn và đặt món trước tập trung 24/7, tích hợp đặt cọc trực tuyến và chatbot AI trả lời tức thì.

- **Hiện trạng vận hành:** Nhà hàng tiếp nhận yêu cầu đặt bàn qua điện thoại, fanpage Facebook, Zalo cá nhân và ghi chép vào sổ tay hoặc bảng tính rời rạc; nhân viên bếp và lễ tân đối chiếu danh sách món đặt trước thủ công.
- **Vấn đề tồn tại:** Trung bình phát sinh khoảng 30 – 50 lượt đặt bàn/ngày; khoảng 10 – 15% đơn bị hủy hoặc thất thoát doanh thu do khách đặt chỗ nhưng không đến (no-show) hoặc xếp trùng khung giờ bàn; khách hàng phải chờ phản hồi tin nhắn trung bình 15 – 30 phút và ngoài giờ làm việc hoàn toàn không có người trực; khoảng 60% tin nhắn lặp lại các câu hỏi cơ bản về thực đơn, giá món, giờ mở cửa và chính sách cọc/hủy.
- **Giải pháp đề xuất:** Xây dựng website đặt bàn theo khung giờ (bước 30 phút, lượt phục vụ 90 phút, múi giờ GMT+7), giữ chỗ tạm thời 10 phút có ràng buộc cơ sở dữ liệu chống trùng bàn, cho phép đặt món trước và đặt cọc trực tuyến qua cổng thanh toán Sandbox; tích hợp chatbot AI tự vận hành qua Ollama truy xuất dữ liệu thực tế (RAG) để tư vấn món, giải đáp chính sách và dẫn dắt đặt bàn qua hội thoại.
- **Lợi ích kỳ vọng:** Nhận đặt bàn trực tuyến 24/7 (tăng tỷ lệ đơn đặt ngoài giờ làm việc); loại bỏ 100% tình trạng trùng bàn trên cùng khung giờ; giảm tỷ lệ khách đặt nhưng không đến nhờ cơ chế đặt cọc và nhắc lịch tự động trước 24 giờ và 2 giờ; rút ngắn thời gian phản hồi câu hỏi thường gặp của khách xuống dưới 5 giây; cung cấp báo cáo doanh thu cọc và công suất bàn theo thời gian thực.

Số liệu hiện trạng trên là mức khảo sát sơ bộ ban đầu và được nhóm chuẩn hóa chính thức bằng biên bản khảo sát thực tế tại Nhà hàng Ẩm thực Vườn Phố ở Sprint 0 – Sprint 1.

---

## 2. Tính chất, yêu cầu của sản phẩm (Product Characteristics and Requirements)

### 2.1 Yêu cầu chức năng (Ưu tiên theo MoSCoW: M – Must, S – Should, C – Could)

| Mã FR | Tên yêu cầu | Mô tả và tiêu chí chấp nhận chính | Ưu tiên |
| --- | --- | --- | --- |
| FR-01 | Xác thực và phân quyền | Đăng ký, đăng nhập (email/SĐT), quên mật khẩu (liên kết dùng 1 lần); khóa tạm 15 phút khi sai quá 5 lần; phân quyền RBAC 3 vai trò: Khách hàng, Nhân viên, Quản lý. | M |
| FR-02 | Xem và tìm kiếm thực đơn | Hiển thị thực đơn đang bán theo danh mục kèm ảnh, mô tả, giá VNĐ; tìm từ khóa, lọc theo danh mục, khoảng giá, nhãn món (chay, cay, hải sản); món hết hiển thị 'Tạm hết'. | M |
| FR-03 | Quản lý thực đơn | Quản lý thêm, sửa, ẩn (xóa mềm) danh mục và món; cập nhật trạng thái Đang bán / Tạm hết / Ngừng bán; lưu lịch sử thay đổi giá; không xóa món đã phát sinh đơn. | M |
| FR-04 | Quản lý sơ đồ bàn | Khai báo khu vực, bàn, sức chứa, bàn có thể ghép; sắp xếp sơ đồ bàn trực quan bằng kéo thả lưu tọa độ; xem trạng thái từng bàn theo ngày và khung giờ. | M |
| FR-05 | Đặt bàn theo khung giờ và số khách | Chọn ngày, giờ, số khách (bước 30p, lượt 90p, đặt trước 2h–30 ngày, GMT+7); giữ chỗ tạm thời 10p trong transaction có ràng buộc CSDL chống trùng bàn. | M |
| FR-06 | Đặt món trước | Chọn món và số lượng (1–20 phần) gắn với đơn đặt bàn; lưu giá chốt (`unit_price_locked`) tại thời điểm xác nhận; khóa chỉnh sửa trước giờ hẹn 2 giờ. | M |
| FR-07 | Đặt cọc trực tuyến | Tính tiền cọc theo cấu hình (mặc định 30% giá trị món hoặc mức tối thiểu theo số khách); thanh toán qua cổng Sandbox; xử lý Callback/Webhook xác thực chữ ký HMAC, chống trùng lặp. | M |
| FR-08 | Quản lý đặt chỗ (Vận hành) | Nhân viên lọc, xem chi tiết đơn, check-in, hoàn thành, đổi bàn/giờ chống trùng, hủy đơn (ngoại lệ chỉ Quản lý kèm lý do), nhắc quá 15p chưa check-in để đánh dấu Không đến; ghi nhật ký đầy đủ. | M |
| FR-09 | Hủy đặt chỗ và hoàn cọc | Khách xem 'Đặt chỗ của tôi' và hủy đơn; tính mức hoàn cọc theo chính sách (trước ≥ 24h hoàn 100%, 2h–24h hoàn 50%, < 2h không hoàn); giải phóng bàn ngay lập tức. | M |
| FR-10 | Thông báo và nhắc lịch | Gửi email xác nhận cọc thành công và thông báo hủy đơn; tự động nhắc lịch trước 24 giờ và 2 giờ qua Email (SMS cho nhắc 2 giờ); thử lại tối đa 3 lần khi lỗi. | S |
| FR-11 | Tổng hợp món chuẩn bị cho bếp | Tổng hợp danh sách món, số lượng và ghi chú từ các đơn 'Đã xác nhận' theo ngày và khung giờ; tự cập nhật khi sửa/hủy món; hỗ trợ in hoặc xuất PDF. | S |
| FR-12 | Báo cáo thống kê | Báo cáo theo khoảng thời gian (GMT+7): số đơn theo trạng thái, tỷ lệ hủy, tỷ lệ không đến (no-show), doanh thu cọc/hoàn cọc, số đơn đặt ngoài giờ làm việc (bảng & biểu đồ). | M |
| FR-13 | Chatbot AI tư vấn món và giải đáp | Chạy mô hình mở trên Ollama (RAG từ PostgreSQL): tư vấn món theo ngân sách, số người, nhãn món kèm thẻ món 'Thêm vào đơn'; giải đáp giờ mở cửa, chính sách cọc/hủy; từ chối ngoài phạm vi/y tế. | M |
| FR-14 | Chatbot AI hỗ trợ đặt bàn qua chat | Dẫn dắt khách cung cấp ngày, giờ, số khách, khu vực; chuẩn hóa thời gian GMT+7; tra cứu bàn trống (chỉ đọc FR-05) và sinh liên kết biểu mẫu đặt bàn điền sẵn (`/booking?...`). | M |
| FR-15 | Quản trị tri thức & giám sát chatbot | Quản lý cập nhật FAQ, chính sách nhà hàng; xem lịch sử hội thoại (đã che PII, lưu tối đa 90 ngày), lọc phản hồi 'Không hữu ích' để cải thiện chất lượng AI. | S |
| FR-16 | Đặt tiệc / sự kiện (Mở rộng) | Khách gửi yêu cầu đặt tiệc nhóm đông; Quản lý duyệt, báo giá và đặt mức cọc riêng (nằm trong Backlog dự phòng). | C |
| FR-17 | Đánh giá nhà hàng (Mở rộng) | Khách chấm 1–5 sao và nhận xét sau khi đơn hoàn thành; sửa trong 7 ngày; Quản lý phản hồi hoặc kiểm duyệt (nằm trong Backlog dự phòng). | C |
| FR-18 | Chatbot tool calling (Mở rộng) | Chatbot gọi trực tiếp API tra cứu đơn, tạo giữ chỗ hoặc hủy đơn có xác nhận rõ ràng và kiểm tra quyền phía server (nằm trong Backlog dự phòng). | C |

### 2.2 Phạm vi Chatbot AI – Năm lớp quyết định

| Lớp quyết định | Quyết định kỹ thuật và nghiệp vụ đã chốt |
| --- | --- |
| 1. Kết quả (Outcome) | Trả lời câu hỏi thường gặp của khách về thực đơn, giá món, giờ mở cửa, chính sách đặt cọc/hủy và dẫn dắt đặt bàn tức thì (≤ 5 giây) 24/7, kể cả ngoài giờ làm việc; giảm tải tin nhắn lặp lại cho nhân viên. |
| 2. Dữ liệu (Data & RAG) | Chỉ truy xuất từ cơ sở dữ liệu PostgreSQL đã được nhà hàng duyệt (thực đơn đang bán, giá hiện hành, trạng thái còn/hết, bàn trống, chính sách, FAQ). Toàn bộ thông tin cá nhân (họ tên, SĐT, email) được loại bỏ/che (PII Masking) trước khi gửi sang LLM. |
| 3. Mô hình (Model) | Sử dụng mô hình ngôn ngữ lớn mã nguồn mở có sẵn chạy tự chủ qua Ollama (chốt model tối ưu tiếng Việt tại Sprint 2, không huấn luyện mô hình); trả lời đúng ≥ 80% trên bộ ≥ 30 câu hỏi kiểm thử chuẩn & dẫn dụ; phản hồi ≤ 5 giây với 95% truy vấn. |
| 4. Tích hợp (Integration) | Nhúng khung ChatWidget ReactJS trên các trang chính của website; giao tiếp qua REST API `/api/v1/chat/*`; kết nối dịch vụ kiểm tra bàn trống FR-05 ở chế độ chỉ đọc để tạo liên kết đặt bàn điền sẵn thông tin; hướng dẫn liên hệ nhân viên khi thiếu dữ liệu hoặc gặp khiếu nại/dị ứng. |
| 5. Quản trị (Governance) | Áp dụng Guardrails chống bịa thông tin (hallucination); từ chối lịch sự câu hỏi ngoài phạm vi nhà hàng; không cam kết về y tế/dị ứng; không báo 'đã đặt thành công' khi hệ thống chưa xác nhận; giới hạn tần suất (rate limit) và độ dài tin nhắn; lưu log hội thoại tối đa 90 ngày. |

### 2.3 Yêu cầu phi chức năng và kỹ thuật

| Mã NFR | Nhóm yêu cầu | Chỉ tiêu kỹ thuật và tiêu chí chấp nhận |
| --- | --- | --- |
| NFR-01 | Hiệu năng & Chịu tải | Trang web tải ≤ 3 giây trên mạng 4G/tiêu chuẩn; API nghiệp vụ phản hồi ≤ 2 giây; Chatbot AI phản hồi ≤ 5 giây (95% câu hỏi); đáp ứng 50 người dùng đồng thời trong kiểm thử tải và xử lý 100% chính xác đặt bàn đồng thời. |
| NFR-02 | Bảo mật & Dữ liệu cá nhân | Truyền tải qua HTTPS; mật khẩu băm một chiều (bcrypt/Argon2); khóa đăng nhập 15 phút sau 5 lần sai; phân quyền RBAC 3 vai trò ở tầng API; không lưu số thẻ thanh toán; che PII trước khi gửi lên LLM. |
| NFR-03 | Giao diện & Tương thích | Thiết kế Responsive hiển thị tốt trên điện thoại và máy tính; tương thích Chrome, Edge, Safari bản mới; giao diện tiếng Việt, tiền tệ VNĐ, múi giờ chuẩn GMT+7. |
| NFR-04 | Kiến trúc & Toàn vẹn dữ liệu | Kiến trúc Client–Server: Front-end ReactJS – REST API Python FastAPI (tài liệu Swagger) – Cơ sở dữ liệu PostgreSQL (ERD ≥ 8 bảng, Alembic migration); Front-end không truy cập trực tiếp CSDL; ràng buộc DB chống trùng bàn. |
| NFR-05 | Vận hành & Sao lưu | Đóng gói Docker triển khai trên Cloud/VPS (tách biệt Staging và Production); hoạt động liên tục 24/7; sao lưu CSDL hằng ngày và kiểm thử khôi phục; có cơ chế fallback an toàn khi dịch vụ Ollama gián đoạn. |
| NFR-06 | Bảo trì & Kiểm thử | Quản lý mã nguồn GitHub (nhánh main/develop/feature, Pull Request có review); CI tự động build & test bằng GitHub Actions; đạt ≥ 40 test case chức năng/API và ≥ 30 câu test Chatbot; 0 Bug Nghiêm trọng/Cao khi phát hành. |

### 2.4 Ngoài phạm vi (Out of Scope)

- Ứng dụng di động cài đặt riêng trên hệ điều hành iOS/Android (chỉ phát triển website responsive dùng tốt trên trình duyệt điện thoại).
- Thanh toán toàn bộ hóa đơn ăn uống tại bàn (phần mềm POS) và xuất hóa đơn giá trị gia tăng (VAT).
- Quản lý kho, định lượng nguyên vật liệu, quản lý nhân sự và chấm công nhân viên.
- Chức năng đặt món giao hàng tận nơi (delivery) và mua mang đi (take-away).
- Giao dịch thanh toán bằng tiền thật (chỉ tích hợp môi trường thử nghiệm Sandbox).
- Xây dựng, huấn luyện hoặc tinh chỉnh (fine-tune) mô hình học máy/LLM; chatbot tự ý hoàn tiền, đổi đơn hoặc cấp mã giảm giá qua hội thoại khi chưa có xác nhận và kiểm tra phía server.

### 2.5 Giả định và ràng buộc

- **Giả định:** Nhà hàng Ẩm thực Vườn Phố cung cấp dữ liệu thực tế đã ẩn danh (≥ 30–50 món ăn, sơ đồ khu vực/bàn, giờ mở cửa, chính sách đặt cọc/hủy, FAQ); cử đại diện tham dự Sprint Review và chạy kiểm thử nghiệm thu UAT ở Sprint 7.
- **Ràng buộc:** Thời gian thực hiện 8 Sprint × 1 tuần (16/11/2026 – 10/01/2027, tổng 56 ngày lịch; nghỉ Tết Dương lịch 01/01/2027, làm bù thứ Bảy 02/01/2027); tổng ngân sách phê duyệt 69.987.500 VNĐ (trong đó Chi phí cơ sở WBS/BAC = 63.625.000 VNĐ và dự phòng 10% = 6.362.500 VNĐ); nhóm gồm 4 thành viên chuyên trách (PM/SM, PO/BA, Dev Fullstack, AI Dev), mỗi người 20 giờ công/Sprint (160 giờ/người, tổng 640 giờ công = 80 ngày công); bắt buộc quản lý bằng GitHub, Jira (SCRUM) và Microsoft Project; mọi thay đổi phạm vi sau mốc M2 (29/11/2026) phải thông qua Hội đồng kiểm soát thay đổi (CCB).

---

## 3. Sản phẩm bàn giao – Quản lý dự án (Project Management-Related Deliverables)

| STT | Sản phẩm bàn giao quản lý dự án | Thời điểm | Chịu trách nhiệm | Công cụ, định dạng |
| --- | --- | --- | --- | --- |
| 1 | Tôn chỉ dự án (Project Charter – D01) & SOW | Sprint 0 (M1) | PM/SM, PO/BA | Word (.docx), có chữ ký |
| 2 | Phát biểu phạm vi dự án (Scope Statement – D02 – tài liệu này) | Sprint 1 (trước M2) | PO/BA | Word (.docx) |
| 3 | WBS, Từ điển WBS & Product Backlog (D03) | Sprint 0–1; cập nhật mỗi Sprint | PM/SM, PO/BA | Excel (.xlsx), MS Project, Jira (SCRUM) |
| 4 | Lịch trình dự án: Gantt, PERT, đường găng, lưu Baseline | Sprint 1 (M2 – 29/11/2026) | PM/SM | Microsoft Project (.mpp) |
| 5 | Đường cơ sở chi phí (Cost Baseline) & Báo cáo Earned Value (EVM) | Sprint 1–2; EVM cuối mỗi Sprint | PM/SM | MS Project, Excel (.xlsx) |
| 6 | Kế hoạch chất lượng, Definition of Ready (DoR) & Definition of Done (DoD) | Sprint 1 | PO/BA, PM/SM | Word, Jira |
| 7 | Kế hoạch nhân sự, phân bổ nguồn lực & Ma trận RACI (D14) | Sprint 0–1 | PM/SM | Excel, MS Project |
| 8 | Kế hoạch truyền thông (D17) & Báo cáo tiến độ hằng tuần | Sprint 0; định kỳ hằng tuần | PM/SM | Word, Google Drive |
| 9 | Sổ đăng ký rủi ro (Risk Register – bao gồm rủi ro ảo giác AI, trùng bàn) | Sprint 1; rà soát mỗi Sprint | PM/SM, PO/BA | Excel, Jira |
| 10 | Phân tích Tự làm hay Mua/Thuê (Ollama LLM, VPS, Sandbox, Email/SMS) | Sprint 0–2 (US-15) | AI Dev, Dev Fullstack | Word / Excel |
| 11 | Yêu cầu thay đổi (CR) & Biên bản Hội đồng kiểm soát thay đổi (CCB) | Khi phát sinh sau M2 | PM/SM, PO/BA | Jira (Issue CR) |
| 12 | Biên bản họp Sprint Planning, Sprint Review & Retrospective | Mỗi Sprint (S0 – S7) | PM/SM, PO/BA | Word, Jira |
| 13 | Báo cáo tổng kết dự án, bài học kinh nghiệm & hồ sơ đóng dự án | Sprint 7 (M6 – 10/01/2027) | PM/SM và cả nhóm | Word, PDF, MS Project |

---

## 4. Sản phẩm bàn giao – Sản phẩm (Product-Related Deliverables)

| STT | Sản phẩm bàn giao kỹ thuật & nghiệp vụ | Thời điểm | Chịu trách nhiệm | Tiêu chí chấp nhận |
| --- | --- | --- | --- | --- |
| 1 | Báo cáo khảo sát nghiệp vụ tại Nhà hàng Ẩm thực Vườn Phố | Sprint 0 | PO/BA | Có biên bản khảo sát và số liệu hiện trạng quy trình đặt bàn |
| 2 | Đặc tả yêu cầu phần mềm SRS v1.1 & Product Backlog | Sprint 0–1 | PO/BA | Đủ 18 FR, 6 NFR và 54 User Story (45 MVP = 202 SP) được duyệt |
| 3 | Tài liệu thiết kế: kiến trúc hệ thống, ERD CSDL & Prototype Figma | Sprint 1 | Dev Fullstack, PO/BA | ERD ≥ 8 bảng (core + AI), Alembic migration sạch; đủ màn hình MVP |
| 4 | Tài liệu REST API (OpenAPI / Swagger) | Sprint 1–6 | Dev Fullstack, AI Dev | Đầy đủ endpoint cho FR-01..FR-14 và `/api/v1/chat/*` |
| 5 | Mã nguồn trên GitHub & các bản phát hành (tag v0.1, v0.2, v1.0-rc, v1.0) | Sprint 3, 5, 6, 7 | Dev Fullstack, AI Dev | Cả 4 thành viên commit đúng nhánh; PR có review; CI xanh |
| 6 | Cơ sở dữ liệu PostgreSQL, script khởi tạo & dữ liệu mẫu ẩn danh | Sprint 2 | PO/BA, Dev Fullstack | ≥ 30–50 món ăn, sơ đồ bàn, chính sách thực tế đã ẩn danh PII |
| 7 | Chatbot AI (Ollama): cấu hình model, tri thức RAG & bộ ≥ 30 câu test | Sprint 2, 5–7 | AI Dev, PO/BA | Trả lời đúng ≥ 80% trên ≥ 30 câu test; phản hồi ≤ 5 giây; che PII |
| 8 | Kế hoạch kiểm thử, bộ test case & báo cáo kiểm thử hồi quy | Sprint 1–7 | PO/BA | ≥ 40 test case chức năng/API (Postman); 0 Bug Cao/Nghiêm trọng |
| 9 | Kết quả kiểm thử nghiệm thu UAT & phiếu xác nhận của nhà hàng | Sprint 7 (M6) | PO/BA, PM/SM | Đơn vị nhà hàng chạy thử đủ kịch bản và ký xác nhận đạt |
| 10 | Bản triển khai chính thức trên Cloud/VPS (Staging & Production v1.0) | Sprint 4, 7 | Dev Fullstack, AI Dev | Chạy liên tục 24/7 trên Docker (Web App + Ollama), HTTPS, backup |
| 11 | Tài liệu hướng dẫn sử dụng (Khách hàng, Nhân viên, Quản lý & Chatbot) | Sprint 7 | PO/BA | Có ảnh chụp màn hình minh họa chi tiết; nhà hàng xác nhận dễ dùng |
| 12 | Video demo sản phẩm (5 – 7 phút) & Slide bảo vệ đồ án | Sprint 7 | AI Dev, cả nhóm | Thể hiện trọn vẹn luồng đặt bàn chống trùng, đặt cọc và Chatbot AI |

**Lưu ý về phần cứng:** Không mua sắm mới; sử dụng máy tính cá nhân và điện thoại thông minh sẵn có của 4 thành viên nhóm và đơn vị nhà hàng áp dụng.

---

## 5. Tiêu chí thành công của dự án (Project Success Criteria)

Dự án được đánh giá là thành công khi đáp ứng đồng thời toàn bộ 6 nhóm tiêu chí dưới đây, được kiểm chứng qua các buổi Sprint Review, nghiệm thu UAT tại Nhà hàng Ẩm thực Vườn Phố và buổi bảo vệ đồ án ngày 10/01/2027:

| Nhóm tiêu chí | Chỉ số mục tiêu đạt được | Phương pháp kiểm chứng |
| --- | --- | --- |
| Phạm vi (Scope) | Hoàn thành 100% phạm vi chức năng MVP (FR-01 đến FR-14, 45 User Story = 202 SP) đạt tiêu chí chấp nhận; đại diện Nhà hàng Ẩm thực Vườn Phố ký xác nhận biên bản UAT. | Sprint Review, Jira Board (SCRUM), Biên bản UAT |
| Thời gian (Schedule) | Bàn giao phiên bản chính thức v1.0 đúng hạn ngày 10/01/2027; duy trì chỉ số hiệu quả tiến độ SPI ≥ 0,9 qua các Sprint. | Microsoft Project, Báo cáo tiến độ tuần |
| Chi phí (Cost) | Tổng chi phí thực tế nằm trong ngân sách 69.987.500 VNĐ (Chi phí cơ sở BAC = 63.625.000 VNĐ); duy trì chỉ số hiệu quả chi phí CPI ≥ 0,9. | Bảng theo dõi Earned Value (EVM) trên MS Project & Excel |
| Chất lượng (Quality) | 100% User Story ở trạng thái Done đáp ứng Definition of Done; không còn lỗi (Bug) mức Nghiêm trọng hoặc Cao khi phát hành; Chatbot AI trả lời đúng ≥ 80% bộ ≥ 30 câu test, phản hồi ≤ 5 giây. | Báo cáo kiểm thử, Postman, Kết quả test AI (US-40) |
| Giá trị nghiệp vụ (Business Value) | Hệ thống nhận đặt bàn trực tuyến 24/7; 0% đơn trùng bàn trên cùng khung giờ; giảm tỷ lệ khách không đến (no-show) nhờ đặt cọc và nhắc lịch; mức độ hài lòng UAT ≥ 4/5. | Dữ liệu báo cáo thống kê (FR-12), Phiếu khảo sát UAT |
| Học tập (Academic) | Hoàn thiện đầy đủ hồ sơ quản lý dự án theo quy định học phần, báo cáo tổng kết cuối kỳ; demo sản phẩm trực tiếp và bảo vệ thành công. | Hội đồng đánh giá học phần |

---

## 6. Tiêu chí hoàn thành (Definition of Done – DoD)

Một User Story / hạng mục công việc trên Jira (khóa SCRUM) chỉ được công nhận là hoàn thành (`Done`) khi thỏa mãn đồng thời 5 điều kiện sau:

1. Mã nguồn đã được kiểm tra chéo (Pull Request có ít nhất 1 thành viên review), vượt qua kiểm tra tự động CI (GitHub Actions) và merge sạch vào nhánh `develop`/`main`; tên nhánh và commit gắn đúng mã issue Jira (`SCRUM-xx`).
2. Toàn bộ test case của User Story đã chạy đạt trên môi trường Staging; không tồn tại hoặc làm phát sinh lỗi (Bug) mức Cao hoặc Nghiêm trọng mới.
3. Chức năng chạy ổn định trên bản triển khai thực tế và được Product Owner (PO/BA) nghiệm thu chấp nhận tại buổi Sprint Review.
4. Tài liệu kỹ thuật liên quan (tài liệu REST API Swagger, sơ đồ ERD, tài liệu hướng dẫn sử dụng) đã được cập nhật đồng bộ.
5. Đối với các phần công việc có sử dụng công cụ AI hỗ trợ lập trình/soạn thảo: thành viên phụ trách giải thích rõ cơ chế hoạt động, đã kiểm chứng độ chính xác và chịu trách nhiệm hoàn toàn về sản phẩm.

---

## 7. Ký duyệt phạm vi dự án (Sign-off & Comments)

| Vai trò | Họ và tên | Ngày duyệt | Chữ ký xác nhận |
| --- | --- | --- | --- |
| Người lập – Product Owner / Business Analyst (PO/BA) | [Võ Đăng Khoa BA] | …/11/2026 | Khoa |
| Giám đốc dự án / Scrum Master (PM/SM) | [Trần Hoàng Phúc PM] | …/11/2026 | Phúc |
| Đại diện kỹ thuật – Dev Fullstack & AI Dev | [Nguyễn Văn Tiến / Nguyễn Đoàn Trường Vũ Dev Fullstack / AI Dev] | …/11/2026 | Tiến - Vũ |
| Đại diện đơn vị nhà hàng áp dụng (Customer) | [Nhà hàng Ẩm thực Vườn Phố] | …/11/2026 | |
| Nhà tài trợ dự án (Giảng viên hướng dẫn) | [Nguyễn Hữu Trung (GVHD)] | …/11/2026 | |

**Chú thích (Comments):** (Nhận xét viết tay hoặc đánh máy của Nhà tài trợ, Đại diện Nhà hàng Ẩm thực Vườn Phố hoặc các bên liên quan, nếu có.)
