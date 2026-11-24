# TÀI LIỆU ĐẶC TẢ YÊU CẦU PHẦN MỀM
## SOFTWARE REQUIREMENTS SPECIFICATION (SRS)

**Website đặt bàn và đặt món trước cho nhà hàng tích hợp chatbot AI (Mã đề tài: QL09-W)**

| Thông tin tài liệu | Nội dung chi tiết |
| --- | --- |
| Tên dự án | Website đặt bàn và đặt món trước cho nhà hàng tích hợp chatbot AI (Restaurant Table Reservation and Pre-order Website with AI Chatbot) |
| Mã đề tài / Mã Jira | QL09-W \| Khóa dự án Jira: SCRUM |
| Lĩnh vực & Nền tảng | Nhà hàng, quán ăn phục vụ tại bàn \| Ứng dụng Web (Front-end ReactJS + Back-end Python FastAPI + PostgreSQL + Ollama AI) |
| Phiên bản & Trạng thái | 1.1 – Hoàn thiện đầy đủ phạm vi chức năng, kiến trúc AI 5 lớp, NFR định lượng, ma trận truy vết & tiêu chí nghiệm thu |
| Người lập (Prepared by) | [Võ Đăng Khoa BA – PO/BA]; phối hợp [Trần Hoàng Phúc - PM/SM], [Nguyễn Văn Tiến - Dev Fullstack], [Nguyễn Đoàn Trường Vũ - AI Dev] |
| Căn cứ & Mốc duyệt | Căn cứ Tôn chỉ dự án (M1), Phát biểu phạm vi & Khảo sát thực tế đơn vị áp dụng; duyệt trước mốc M2 (Baseline) |

---

## 1. Giới thiệu hệ thống

### 1.1 Mục đích tài liệu

Tài liệu Đặc tả yêu cầu phần mềm (SRS) này mô tả đầy đủ các yêu cầu chức năng, yêu cầu phi chức năng, kiến trúc chatbot AI, ràng buộc kỹ thuật và tiêu chí nghiệm thu của hệ thống Website đặt bàn và đặt món trước cho nhà hàng tích hợp chatbot AI. Tài liệu là cơ sở pháp lý và kỹ thuật thống nhất giữa Product Owner/Business Analyst, Project Manager/Scrum Master, nhóm phát triển (Dev Fullstack, AI Dev) và đơn vị nhà hàng áp dụng về những gì hệ thống phải thực hiện.

Từ tài liệu này, nhóm xây dựng Product Backlog (10 Epic, 54 User Story, tiêu chí chấp nhận), thiết kế kiến trúc – giao diện Figma – cơ sở dữ liệu (ERD ≥ 8 bảng), bộ test case kiểm thử chức năng/hồi quy (≥ 40 test case), bộ câu hỏi kiểm thử chatbot AI (≥ 30 câu) và kịch bản nghiệm thu thực tế (UAT).

Tài liệu gồm ba phần chính: Phần 1 giới thiệu tổng quan, bối cảnh định lượng, kiến trúc công nghệ – AI 5 lớp và yêu cầu phi chức năng; Phần 2 đặc tả chi tiết 18 yêu cầu chức năng (FR-01 đến FR-18); Phần 3 quy định sản phẩm bàn giao kỹ thuật, tiêu chí nghiệm thu, Definition of Done, ma trận truy vết và ký duyệt.

### 1.2 Phạm vi hệ thống (System Scope)

Hệ thống là ứng dụng web (front-end và back-end API) dành cho nhà hàng, quán ăn có phục vụ tại bàn. Khách hàng đặt bàn theo khung giờ, đặt món và đặt cọc trước 24/7, đồng thời được chatbot AI hỗ trợ tư vấn món và đặt bàn qua hội thoại. Nhân viên và quản lý dùng hệ thống để sắp xếp sơ đồ bàn, chuẩn bị bếp, xử lý đơn đặt chỗ và theo dõi báo cáo hoạt động.

#### Trong phạm vi (In Scope):

- Xem, tìm kiếm, lọc và quản lý thực đơn, tình trạng món (đang bán, tạm hết, ngừng bán) và lịch sử thay đổi giá (FR-02, FR-03).
- Quản lý khu vực, sơ đồ bàn trực quan kéo thả và theo dõi trạng thái bàn theo ngày/giờ (FR-04).
- Đặt bàn theo khung giờ (bước 30 phút, lượt 90 phút, múi giờ GMT+7) và số khách; giữ chỗ tạm thời 10 phút có ràng buộc cơ sở dữ liệu chống trùng bàn (FR-05).
- Đặt món trước với giá chốt (`unit_price_locked`) và đặt cọc trực tuyến qua cổng thanh toán Sandbox (xử lý callback/webhook an toàn); hủy đặt chỗ và hoàn cọc theo chính sách cấu hình (FR-06, FR-07, FR-09).
- Vận hành đặt chỗ cho nhân viên (check-in, hoàn thành, đổi bàn/giờ, đánh dấu không đến có nhật ký), thông báo Email và nhắc lịch tự động trước 24 giờ và 2 giờ (Email/SMS), tổng hợp danh sách món chuẩn bị cho bếp (FR-08, FR-10, FR-11).
- Báo cáo thống kê số đơn, tỷ lệ hủy và không đến (no-show), doanh thu cọc/hoàn cọc và số đơn đặt ngoài giờ làm việc (FR-12).
- Chatbot AI chạy mô hình mở trên Ollama tư vấn món (kèm thẻ món thêm vào đơn), giải đáp chính sách dựa trên dữ liệu thực tế (RAG), hỗ trợ đặt bàn qua hội thoại GMT+7 và quản trị tri thức/giám sát hội thoại (FR-13, FR-14, FR-15).
- Mở rộng (đưa vào Backlog dự phòng 50 SP, triển khai nếu velocity vượt kế hoạch trước thời điểm đóng băng tính năng hết Sprint 6): Đặt tiệc/sự kiện cho nhóm đông (FR-16), đánh giá nhà hàng 1–5 sao (FR-17), chatbot thực hiện thao tác nghiệp vụ qua API có xác nhận – tool calling (FR-18).

#### Ngoài phạm vi (Out of Scope):

- Thanh toán toàn bộ hóa đơn tại bàn (POS) và xuất hóa đơn giá trị gia tăng (VAT).
- Quản lý kho, định lượng nguyên liệu, quản lý nhân sự và chấm công.
- Chức năng đặt hàng giao tận nơi (delivery) và mang đi (take-away).
- Ứng dụng di động cài đặt riêng trên iOS/Android (website được thiết kế responsive tối ưu hiển thị trên trình duyệt điện thoại).
- Xây dựng, huấn luyện hoặc tinh chỉnh (fine-tune) mô hình học máy/LLM; hệ thống chỉ sử dụng mô hình ngôn ngữ mở có sẵn chạy qua Ollama và không tự ý hoàn tiền, đổi đơn hoặc cấp mã giảm giá qua chat khi chưa có xác nhận và kiểm tra phía server.

### 1.3 Đối tượng đọc tài liệu

- **Product Owner / Business Analyst (PO/BA):** Lập backlog, thiết kế wireframe, chuẩn hóa dữ liệu mẫu ẩn danh, điều phối kiểm thử và UAT.
- **Project Manager / Scrum Master (PM/SM):** Nắm phạm vi chức năng/phi chức năng để lập kế hoạch 8 Sprint, theo dõi tiến độ, chi phí (EVM) và quản lý thay đổi (CCB).
- **Lập trình viên Fullstack (Dev Fullstack):** Thiết kế kiến trúc hệ thống, cơ sở dữ liệu PostgreSQL, REST API FastAPI, giao diện ReactJS và tích hợp cổng thanh toán/thông báo.
- **Kỹ sư AI (AI Dev):** Triển khai mô hình Ollama, xây dựng tầng truy xuất dữ liệu thực tế (RAG), parser thời gian GMT+7, Guardrails/che dữ liệu cá nhân (PII) và bộ kiểm thử chất lượng AI.
- **Giảng viên hướng dẫn (Nhà tài trợ) và Đơn vị nhà hàng áp dụng:** Đánh giá mốc nghiệm thu M1–M6, xác nhận yêu cầu nghiệp vụ thực tế và ký biên bản UAT.

### 1.4 Định nghĩa, thuật ngữ và từ viết tắt

| Thuật ngữ / Viết tắt | Giải thích chi tiết |
| --- | --- |
| SRS | Software Requirements Specification – Tài liệu đặc tả yêu cầu phần mềm. |
| MVP | Minimum Viable Product – Tập chức năng tối thiểu bắt buộc của sản phẩm để vận hành thực tế. |
| FR / NFR | Functional Requirement (Yêu cầu chức năng, mã FR-xx) / Non-Functional Requirement (Yêu cầu phi chức năng, mã NFR-xx). |
| Đơn đặt chỗ | Bản ghi gồm thông tin khách, bàn, khung giờ, số khách, món đặt trước (nếu có) và giao dịch tiền cọc. |
| Khung giờ | Khoảng thời gian khách dự kiến dùng bàn, chia theo bước cố định 30 phút (lượt phục vụ mặc định 90 phút). |
| Tiền cọc | Khoản thanh toán trực tuyến trước để giữ chỗ, được trừ trực tiếp vào hóa đơn khi khách dùng bữa. |
| Giữ chỗ tạm thời | Cơ chế khóa giữ bàn trong thời gian ngắn (mặc định 10 phút) trong lúc khách hoàn tất thanh toán cọc. |
| Không đến (No-show) | Khách đã đặt chỗ và đặt cọc nhưng không đến dùng bữa và không hủy theo quy định. |
| Chatbot AI / Ollama | Trợ lý hội thoại sử dụng mô hình ngôn ngữ lớn (LLM) mã nguồn mở tự vận hành cục bộ/VPS qua Ollama. |
| RAG | Retrieval-Augmented Generation – Kỹ thuật truy xuất dữ liệu thực tế từ CSDL trước khi sinh câu trả lời để chống bịa tin. |
| Ảo giác (Hallucination) | Hiện tượng mô hình AI sinh ra thông tin sai lệch hoặc không có căn cứ trong dữ liệu nhà hàng. |
| PII Masking | Kỹ thuật loại bỏ hoặc che giấu dữ liệu định danh cá nhân (họ tên, SĐT, email) trước khi gửi ngữ cảnh cho LLM. |
| Tool calling | Cơ chế để mô hình AI yêu cầu hệ thống gọi các API nghiệp vụ nằm trong danh sách cho phép (whitelist). |
| UAT | User Acceptance Test – Kiểm thử nghiệm thu thực tế bởi đơn vị nhà hàng áp dụng. |

### 1.5 Bối cảnh, lý giải dự án và chỉ tiêu định lượng

Đơn vị áp dụng là nhà hàng/quán ăn có phục vụ tại bàn. Khách hàng có nhu cầu đặt bàn theo khung giờ cụ thể, đặt món và đặt cọc trước; nhà hàng cần sắp xếp bàn hợp lý và chuẩn bị nguyên liệu bếp từ trước.

- **Hiện trạng vận hành:** Nhà hàng hiện tiếp nhận đặt bàn thủ công qua điện thoại, tin nhắn mạng xã hội và ghi chép sổ/bảng tính riêng lẻ.
- **Vấn đề tồn tại (số liệu khảo sát nền):** Trung bình phát sinh khoảng 30 – 50 lượt đặt bàn/ngày; khoảng 10 – 15% đơn bị hủy hoặc thất thoát doanh thu do khách đặt nhưng không đến (no-show) hoặc ghi nhầm/trùng khung giờ bàn; khách hàng phải chờ nhân viên phản hồi tin nhắn trung bình 15 – 30 phút và ngoài giờ làm việc hoàn toàn không có người trực; khoảng 60% tin nhắn của khách lặp lại các câu hỏi cơ bản về thực đơn, giá món, giờ mở cửa và chính sách cọc/hủy.
- **Giải pháp đề xuất:** Xây dựng website đặt bàn và đặt món trước tập trung 24/7, tích hợp cơ chế giữ chỗ chống trùng bàn ở tầng cơ sở dữ liệu, đặt cọc trực tuyến, nhắc lịch tự động và chatbot AI trả lời tức thì dựa trên dữ liệu thực tế.

Số liệu hiện trạng trên là mức cơ sở ban đầu từ khảo sát sơ bộ và được nhóm chuẩn hóa chính thức bằng biên bản khảo sát thực tế tại đơn vị áp dụng trong Sprint 0 – Sprint 1.

| Vấn đề hiện tại | Chỉ tiêu mục tiêu (KPI) sau triển khai | Cách thức đo lường & kiểm chứng |
| --- | --- | --- |
| Chỉ nhận đặt bàn thủ công trong giờ làm việc | Nhận đặt bàn trực tuyến 24/7; ghi nhận đơn đặt ngoài giờ làm việc rõ ràng | Báo cáo thống kê hệ thống (FR-12): chỉ số số đơn đặt ngoài giờ làm việc |
| Dễ trùng bàn, sai khung giờ khi ghi chép thủ công | 0% đơn trùng bàn trên cùng khung giờ; giữ chỗ tạm thời 10 phút chính xác | Kiểm thử đồng thời (Concurrent Test) trên API/DB (FR-05) & dữ liệu UAT |
| 10 – 15% khách đặt nhưng không đến (no-show) | Giảm rõ rệt tỷ lệ no-show nhờ đặt cọc trực tuyến và nhắc lịch trước 24h & 2h | Báo cáo thống kê (FR-12): tỷ lệ đơn không đến / tổng đơn đã xác nhận |
| Chờ trả lời tin nhắn 15 – 30 phút; 60% câu hỏi lặp lại | Chatbot AI phản hồi ≤ 5 giây với 95% câu hỏi; trả lời đúng ≥ 80% bộ ≥ 30 câu test | Log thời gian phản hồi AI, kết quả bộ 30+ câu kiểm thử (US-40) & phiếu UAT |
| Thực đơn/giá thay đổi gây sai lệch thông tin | 100% đơn đặt trước lưu giá chốt; món hết khóa đặt ngay; cảnh báo đơn ảnh hưởng | Kiểm thử nghiệp vụ FR-03, FR-06 và đối soát danh sách chuẩn bị bếp (FR-11) |

### 1.6 Tổng quan hệ thống và Kiến trúc

#### 1.6.1 Mục tiêu hệ thống

- Cho phép khách đặt bàn theo khung giờ và số khách mọi lúc (24/7), không phụ thuộc giờ làm việc của nhân viên.
- Cho phép đặt món và đặt cọc trực tuyến trước để nhà hàng chuẩn bị nguyên liệu bếp và giảm tình trạng khách đặt nhưng không đến.
- Giúp quản lý và nhân viên sắp xếp sơ đồ bàn, xử lý check-in/đổi bàn chính xác, loại bỏ hoàn toàn tình trạng trùng bàn.
- Hỗ trợ khách hàng bằng chatbot AI tư vấn món ăn, giải đáp chính sách và dẫn dắt đặt bàn qua hội thoại dựa trên dữ liệu thực tế của nhà hàng.
- Cung cấp báo cáo thống kê trực quan (bảng và biểu đồ) để quản lý theo dõi doanh thu cọc, công suất bàn và hiệu quả vận hành.

#### 1.6.2 Tác nhân và người dùng

| Tác nhân | Mô tả | Vai trò và quyền hạn chính |
| --- | --- | --- |
| Khách vãng lai | Người truy cập website nhưng chưa đăng nhập. | Xem thực đơn, tìm kiếm/lọc món, trò chuyện tư vấn với chatbot AI, đăng ký và đăng nhập tài khoản. |
| Khách hàng | Người dùng đã đăng ký và đăng nhập. | Đặt bàn theo khung giờ, đặt món trước, thanh toán cọc trực tuyến, xem/hủy đặt chỗ, đặt bàn qua chatbot, (mở rộng: đặt tiệc, đánh giá). |
| Nhân viên | Lễ tân, phục vụ, nhân viên bếp. | Xem sơ đồ bàn theo giờ, cập nhật trạng thái món còn/hết, xử lý đơn đặt chỗ (check-in, đổi bàn/giờ, đánh dấu không đến), xem/in danh sách món chuẩn bị cho bếp. |
| Quản lý | Chủ hoặc quản lý nhà hàng. | Toàn quyền quản lý thực đơn, sơ đồ bàn, tham số nghiệp vụ (cọc/hủy/nhắc lịch), tài khoản nhân viên, báo cáo thống kê và quản trị tri thức/giám sát chatbot. |
| Chatbot AI | Thành phần trợ lý hội thoại thông minh. | Truy xuất thực đơn/chính sách (RAG), tư vấn món kèm thẻ món, tra cứu bàn trống (chỉ đọc) và tạo liên kết đặt bàn điền sẵn. |
| Hệ thống ngoài | Cổng thanh toán Sandbox, máy chủ Ollama, dịch vụ Email/SMS. | Xử lý giao dịch đặt cọc qua webhook/callback, sinh câu trả lời ngôn ngữ tự nhiên cho chatbot, gửi email/SMS xác nhận và nhắc lịch. |

#### 1.6.3 Kiến trúc tổng quan và công nghệ chuẩn hóa

Hệ thống được xây dựng theo kiến trúc Client–Server phân tách rõ ràng: Front-end giao tiếp với Back-end qua REST API chuẩn JSON; Back-end truy xuất cơ sở dữ liệu quan hệ, tích hợp cổng thanh toán trực tuyến, dịch vụ gửi thông báo và máy chủ mô hình ngôn ngữ lớn Ollama.

| Thành phần | Công nghệ / Giải pháp chốt | Vai trò và ghi chú kỹ thuật |
| --- | --- | --- |
| Front-end | ReactJS (Responsive Web) | Giao diện tối ưu cho cả điện thoại và máy tính; tích hợp khung chat Widget và sơ đồ bàn trực quan. |
| Back-end | Python FastAPI | Cung cấp REST API hiệu năng cao, tự động sinh tài liệu OpenAPI/Swagger, xác thực JWT và phân quyền RBAC. |
| Cơ sở dữ liệu | PostgreSQL + Alembic | Lưu trữ người dùng, thực đơn, sơ đồ bàn, đơn đặt chỗ, giao dịch cọc và lịch sử chat; có ràng buộc DB chống trùng bàn. |
| Chatbot AI | Ollama (Mô hình mở có sẵn) | Tự vận hành trên hạ tầng dự án (không huấn luyện mô hình); kết hợp RAG từ PostgreSQL, parser GMT+7 và PII Masker. |
| Thanh toán | Cổng thanh toán Sandbox (VNPay/MoMo/PayOS) | Thu tiền cọc trực tuyến qua môi trường thử nghiệm; xác thực chữ ký HMAC trên callback/webhook. |
| Thông báo | Dịch vụ Email (SMTP) & SMS | Gửi email xác nhận/hủy đơn và nhắc lịch tự động trước 24 giờ và 2 giờ (SMS dùng cho nhắc lịch trước 2 giờ). |
| Triển khai & CI/CD | Docker, Cloud/VPS, GitHub Actions | Đóng gói container tách biệt Web App và Ollama; tự động chạy kiểm thử và deploy Staging/Production. |

#### 1.6.4 Kiến trúc Chatbot AI – Năm lớp quyết định

Để kiểm soát chặt chẽ phạm vi, độ chính xác và tính an toàn của trợ lý ảo trong nghiệp vụ nhà hàng, Chatbot AI được thiết kế theo mô hình 5 lớp quyết định sau:

| Lớp quyết định | Quy định thiết kế và tiêu chí kiểm soát đã chốt |
| --- | --- |
| 1. Lớp Kết quả (Outcome) | Trả lời câu hỏi thường gặp của khách hàng tức thì (≤ 5 giây) 24/7 kể cả ngoài giờ làm việc; hỗ trợ dẫn dắt đặt bàn qua hội thoại; giảm tải tin nhắn lặp lại cho nhân viên lễ tân. |
| 2. Lớp Dữ liệu (Data & RAG) | Chỉ truy xuất từ nguồn dữ liệu thực tế đã được nhà hàng duyệt trong PostgreSQL (thực đơn đang bán, giá hiện hành, tình trạng còn/hết, bàn trống, giờ mở cửa, chính sách đặt cọc/hủy, FAQ). Mọi thông tin định danh cá nhân (họ tên, SĐT, email) được loại bỏ hoặc che (PII Masking) trước khi gửi sang LLM. |
| 3. Lớp Mô hình (Model) | Sử dụng mô hình ngôn ngữ mở có sẵn chạy trên Ollama (đánh giá và chốt phiên bản model tối ưu tiếng Việt ở Sprint 2, không huấn luyện mô hình). Đạt độ chính xác ≥ 80% trên bộ ≥ 30 câu hỏi kiểm thử chuẩn và dẫn dụ; thời gian phản hồi ≤ 5 giây với 95% truy vấn. |
| 4. Lớp Tích hợp (Integration) | Nhúng khung Chat Widget trên giao diện website; giao tiếp qua REST API `/api/v1/chat/*`; kết nối dịch vụ kiểm tra bàn trống của FR-05 ở chế độ chỉ đọc để sinh liên kết đặt bàn điền sẵn thông tin (mở rộng FR-18 hỗ trợ tool calling có xác nhận). Khi gặp câu hỏi ngoài phạm vi hoặc khiếu nại/dị ứng, chatbot hướng dẫn chuyển sang nhân viên. |
| 5. Lớp Quản trị (Governance & Guardrails) | Áp dụng Guardrails chống bịa thông tin (hallucination); từ chối lịch sự các câu hỏi ngoài phạm vi nhà hàng; không cam kết về y tế/dị ứng; không tự ý chốt đơn, hoàn tiền hay cấp mã giảm giá; giới hạn tần suất (rate limit) và độ dài tin nhắn; lưu nhật ký hội thoại tối đa 90 ngày (che PII khi hiển thị); Quản lý có thể cập nhật tri thức và giám sát hội thoại ngay trên hệ thống. |

### 1.7 Dịch vụ bên ngoài và Phân tích Tự làm hay Mua/Thuê (Make-or-Buy)

Hệ thống tích hợp một số dịch vụ hạ tầng và bên thứ ba. Nhóm thực hiện đánh giá phương án tự triển khai hay thuê dịch vụ để tối ưu chi phí và bảo mật dữ liệu:

| Dịch vụ / Thành phần | Vai trò trong hệ thống | Quyết định Tự làm / Mua-Thuê & Lý do |
| --- | --- | --- |
| Mô hình LLM cho Chatbot (FR-13, FR-14, FR-18) | Hiểu ngôn ngữ tự nhiên tiếng Việt và sinh câu trả lời tư vấn, đặt bàn. | Tự triển khai (Self-host) mô hình mở qua Ollama trên VPS: chi phí gọi API = 0 VNĐ, kiểm soát hoàn toàn dữ liệu không gửi ra bên thứ ba; chốt model tối ưu tại Sprint 2 (US-15). |
| Cổng thanh toán trực tuyến (FR-07, FR-09) | Thu tiền cọc giữ chỗ và đối soát giao dịch hoàn cọc. | Thuê dịch vụ cổng thanh toán (môi trường Sandbox miễn phí): đảm bảo chuẩn bảo mật thanh toán, không lưu số thẻ trên hệ thống nhà hàng. |
| Hạ tầng Cloud / VPS (Staging & Production) | Vận hành Front-end ReactJS, Back-end FastAPI, PostgreSQL và Ollama. | Thuê máy chủ Cloud/VPS cấu hình phù hợp trong thời gian phát triển và UAT; triển khai bằng Docker để dễ sao lưu và di chuyển. |
| Dịch vụ Email & SMS (FR-10) | Gửi email xác nhận/hủy đơn và tin nhắn nhắc lịch trước 24 giờ, 2 giờ. | Dùng dịch vụ SMTP Email miễn phí/cơ bản kết hợp gói SMS thử nghiệm cho mốc nhắc lịch quan trọng (trước 2 giờ) nhằm kiểm soát chi phí. |

### 1.8 Ràng buộc, giả định và phụ thuộc

#### Ràng buộc dự án:

- Sản phẩm là ứng dụng web (responsive), tuân thủ bộ công nghệ chuẩn hóa ở mục 1.6.3 (ReactJS, Python FastAPI, PostgreSQL, Ollama).
- Chatbot sử dụng mô hình ngôn ngữ mở có sẵn, không huấn luyện mô hình; tuyệt đối không gửi dữ liệu định danh cá nhân (PII) của khách lên dịch vụ AI.
- Dự án thực hiện theo quy trình Scrum gồm 8 Sprint (mỗi Sprint 1 tuần), quản lý backlog trên Jira (khóa SCRUM), mã nguồn trên GitHub và tiến độ/chi phí trên Microsoft Project.
- Nhóm thực hiện gồm 4 thành viên chuyên trách: Project Manager / Scrum Master (PM/SM), Product Owner / Business Analyst (PO/BA), Lập trình viên Fullstack (Dev Fullstack) và Kỹ sư AI (AI Dev).
- Mọi thay đổi về phạm vi yêu cầu sau mốc Baseline (M2) phải thông qua quy trình Yêu cầu thay đổi (CR) và được Hội đồng kiểm soát thay đổi (CCB) phê duyệt.

#### Giả định:

- Nhà hàng vận hành một cơ sở; đơn vị tiền tệ là Việt Nam Đồng (VNĐ); múi giờ chuẩn là Việt Nam (GMT+7); giao diện hiển thị tiếng Việt.
- Khách hàng, nhân viên và quản lý truy cập hệ thống bằng trình duyệt web hiện đại trên điện thoại thông minh hoặc máy tính.
- Các tham số nghiệp vụ nêu ở Phần 2 (lượt ăn 90 phút, bước khung giờ 30 phút, giữ chỗ 10 phút, mức cọc 30%, mốc hoàn cọc 24h/2h, mốc nhắc lịch 24h/2h) là giá trị mặc định có thể cấu hình động bởi Quản lý và được đơn vị áp dụng xác nhận.
- Dữ liệu thử nghiệm (≥ 30–50 món ăn, sơ đồ khu vực/bàn, chính sách, FAQ) được lấy từ dữ liệu thực tế của đơn vị nhà hàng áp dụng và đã ẩn danh toàn bộ thông tin cá nhân.

#### Phụ thuộc:

- Môi trường cổng thanh toán Sandbox, máy chủ Cloud/VPS, mô hình Ollama và dịch vụ gửi Email/SMS sẵn sàng trong suốt thời gian phát triển và kiểm thử.
- Đơn vị nhà hàng áp dụng cung cấp dữ liệu thực đơn, sơ đồ bàn, giờ mở cửa, chính sách cọc/hủy đúng hạn ở giai đoạn đầu và cử đại diện tham gia Sprint Review, chạy UAT ở Sprint cuối.

### 1.9 Yêu cầu phi chức năng và kỹ thuật (Non-Functional Requirements)

| Mã NFR | Nhóm yêu cầu | Chỉ tiêu kỹ thuật và tiêu chí chấp nhận cụ thể |
| --- | --- | --- |
| NFR-01 | Hiệu năng & Chịu tải (Performance) | • Thời gian tải trang ban đầu ≤ 3 giây trên kết nối mạng 4G/tiêu chuẩn.<br>• Các API nghiệp vụ thường dùng (xem thực đơn, kiểm tra bàn trống) phản hồi ≤ 2 giây.<br>• Chatbot AI phản hồi ≤ 5 giây cho 95% câu hỏi trong điều kiện bình thường.<br>• Hệ thống đáp ứng tối thiểu 50 người dùng đồng thời trong kiểm thử tải và xử lý chính xác 100% các yêu cầu đặt cùng một bàn tại cùng thời điểm. |
| NFR-02 | Bảo mật & Dữ liệu cá nhân (Security & Privacy) | • Toàn bộ truyền tải sử dụng giao thức mã hóa HTTPS.<br>• Mật khẩu người dùng lưu dưới dạng băm một chiều an toàn (bcrypt/Argon2); khóa đăng nhập 15 phút khi nhập sai quá 5 lần.<br>• Phân quyền chặt chẽ theo 3 vai trò (Khách hàng, Nhân viên, Quản lý) ở tầng API; truy cập trái phép trả về mã 403 và ghi nhật ký.<br>• Không lưu số thẻ hay thông tin thanh toán nhạy cảm; loại bỏ/che dữ liệu cá nhân (PII) trước khi gửi sang LLM; tuân thủ quy định bảo vệ dữ liệu cá nhân. |
| NFR-03 | Giao diện & Khả năng tương thích (Usability & Compatibility) | • Thiết kế Responsive hiển thị tốt trên cả màn hình điện thoại di động và máy tính.<br>• Hoạt động ổn định trên các trình duyệt Chrome, Microsoft Edge, Safari phiên bản mới.<br>• Giao diện tiếng Việt thống nhất, định dạng tiền tệ VNĐ, chuẩn hóa ngày giờ theo múi giờ GMT+7. |
| NFR-04 | Kiến trúc & Toàn vẹn dữ liệu (Architecture & Data) | • Tuân thủ kiến trúc Client–Server: Front-end ReactJS chỉ giao tiếp qua REST API FastAPI (có tài liệu Swagger), không truy cập trực tiếp PostgreSQL.<br>• Thiết kế cơ sở dữ liệu chuẩn hóa (ERD ≥ 8 bảng), quản lý phiên bản lược đồ qua Alembic migration.<br>• Áp dụng giao dịch (transaction) và ràng buộc ở tầng cơ sở dữ liệu để ngăn chặn tuyệt đối việc đặt trùng bàn. |
| NFR-05 | Độ sẵn sàng, Vận hành & Sao lưu (Availability & Operations) | • Hệ thống hoạt động liên tục 24/7 phục vụ đặt bàn trực tuyến (trừ thời gian bảo trì có thông báo).<br>• Đóng gói bằng Docker và triển khai trên Cloud/VPS (tách biệt Staging và Production); tự động sao lưu (backup) CSDL hằng ngày và có kiểm thử khôi phục (restore).<br>• Có cơ chế fallback an toàn khi dịch vụ Ollama tạm ngưng để không ảnh hưởng luồng đặt bàn truyền thống. |
| NFR-06 | Khả năng bảo trì & Kiểm thử (Maintainability & QA) | • Quản lý mã nguồn qua GitHub với quy trình Pull Request có review; tự động build và chạy unit/integration test qua GitHub Actions CI.<br>• Đạt độ phủ kiểm thử ≥ 40 test case chức năng/API và ≥ 30 câu hỏi kiểm thử chatbot; không còn lỗi mức Nghiêm trọng hoặc Cao khi phát hành v1.0. |

### 1.10 Rủi ro đặc thù và biện pháp kiểm soát kỹ thuật

| Rủi ro đặc thù | Tác động nếu xảy ra | Chức năng / Biện pháp kiểm soát trong hệ thống |
| --- | --- | --- |
| Khách đặt chỗ nhưng không đến (No-show) | Mất doanh thu, bàn trống không bán được cho khách khác, bếp chuẩn bị thừa nguyên liệu. | Bắt buộc đặt cọc trực tuyến (FR-07); tự động nhắc lịch trước 24h và 2h (FR-10); áp dụng chính sách hoàn cọc theo mốc thời gian (FR-09); theo dõi tỷ lệ no-show trên báo cáo (FR-12). |
| Trùng bàn (Double Booking) | Hai nhóm khách cùng được xác nhận một bàn trong cùng khung giờ, gây xung đột vận hành. | Kiểm tra bàn trống và giữ chỗ tạm thời 10 phút trong một giao dịch (transaction) kèm ràng buộc mức cơ sở dữ liệu (FR-05); chặn đổi bàn trùng ở màn hình nhân viên (FR-08). |
| Thực đơn thay đổi sau khi đặt | Món ăn hết hàng hoặc thay đổi giá sau khi khách đã đặt món trước. | Lưu giá chốt (`unit_price_locked`) tại thời điểm xác nhận đơn (FR-06); đánh dấu và cảnh báo nhân viên các đơn bị ảnh hưởng khi món hết/ngừng bán (FR-03); chatbot chỉ truy xuất thực đơn hiện hành (FR-13). |
| Chatbot bịa tin (ảo giác) hoặc rò rỉ PII | Khách nhận sai giá/chính sách; lộ thông tin cá nhân qua hội thoại AI. | Áp dụng RAG chỉ trả lời dựa trên dữ liệu truy xuất từ DB; che PII trước khi gửi lên Ollama; từ chối câu hỏi ngoài phạm vi/y tế; kiểm tra quyền và xác nhận phía server cho thao tác nghiệp vụ; lưu log giám sát (FR-13, FR-14, FR-15, FR-18). |
| Dịch vụ Ollama quá tải hoặc gián đoạn | Chatbot phản hồi chậm hoặc không thể sinh câu trả lời. | Đánh giá và chốt model gọn nhẹ tối ưu RAM/VRAM ở Sprint 2 (US-15); cấu hình timeout và cơ chế fallback thông báo lịch sự, điều hướng khách sang dùng thực đơn và form đặt bàn (FR-13). |

---

## 2. Chức năng hệ thống

Phần này đặc tả chi tiết các yêu cầu chức năng của hệ thống: quy ước phân loại ưu tiên, danh mục 18 chức năng (FR-01 đến FR-18), ma trận phân quyền theo tác nhân, vòng đời trạng thái đơn đặt chỗ và bảng đặc tả từng chức năng.

### 2.1 Tổng quan chức năng

#### 2.1.1 Quy ước

- **Mã chức năng:** `FR-xx`, dùng để truy vết trực tiếp sang Epic (`EP-xx`) và User Story (`US-xx`) trên Jira (khóa SCRUM).
- **Mức ưu tiên:** “MVP (bắt buộc)” là chức năng nghiệp vụ cốt lõi bắt buộc hoàn thành trước khi đóng băng tính năng (hết Sprint 6); “MVP – hỗ trợ” là chức năng cần thiết để luồng MVP vận hành khép kín; “Mở rộng” là chức năng bổ sung nằm trong Backlog dự phòng.
- **Tham số cấu hình:** Các giá trị số trong tài liệu (lượt phục vụ 90 phút, bước khung giờ 30 phút, thời gian giữ chỗ 10 phút, mức cọc 30%, mốc hoàn cọc 24h/2h, mốc nhắc lịch 24h/2h) là giá trị mặc định đề xuất, do Quản lý cấu hình trên hệ thống và được đơn vị áp dụng xác nhận.

#### 2.1.2 Danh mục chức năng (FR-01 đến FR-18)

| Mã | Tên chức năng | Nhóm nghiệp vụ | Tác nhân chính | Mức ưu tiên |
| --- | --- | --- | --- | --- |
| FR-01 | Xác thực và phân quyền | Tài khoản | Mọi người dùng | MVP – hỗ trợ |
| FR-02 | Xem và tìm kiếm thực đơn | Thực đơn | Khách vãng lai, Khách hàng | MVP (bắt buộc) |
| FR-03 | Quản lý thực đơn | Thực đơn | Quản lý (NV cập nhật hết món) | MVP (bắt buộc) |
| FR-04 | Quản lý sơ đồ bàn | Sơ đồ bàn | Quản lý (NV chỉ xem) | MVP (bắt buộc) |
| FR-05 | Đặt bàn theo khung giờ và số khách | Đặt bàn | Khách hàng | MVP (bắt buộc) |
| FR-06 | Đặt món trước | Đặt món & cọc | Khách hàng | MVP (bắt buộc) |
| FR-07 | Đặt cọc trực tuyến | Đặt món & cọc | Khách hàng, Cổng thanh toán | MVP (bắt buộc) |
| FR-08 | Quản lý đặt chỗ | Vận hành | Nhân viên, Quản lý | MVP (bắt buộc) |
| FR-09 | Hủy đặt chỗ và hoàn cọc | Vận hành | Khách hàng, Quản lý | MVP – hỗ trợ |
| FR-10 | Thông báo và nhắc lịch | Vận hành | Hệ thống | MVP – hỗ trợ |
| FR-11 | Tổng hợp món chuẩn bị cho bếp | Vận hành | Nhân viên, Quản lý | MVP – hỗ trợ |
| FR-12 | Báo cáo thống kê | Báo cáo | Quản lý | MVP (bắt buộc) |
| FR-13 | Chatbot tư vấn món và giải đáp thông tin | Chatbot AI | Khách vãng lai, Khách hàng | MVP (bắt buộc) |
| FR-14 | Chatbot hỗ trợ đặt bàn qua hội thoại | Chatbot AI | Khách hàng | MVP (bắt buộc) |
| FR-15 | Quản trị tri thức và giám sát chatbot | Chatbot AI | Quản lý | MVP – hỗ trợ |
| FR-16 | Đặt tiệc / sự kiện | Mở rộng | Khách hàng, Quản lý | Mở rộng |
| FR-17 | Đánh giá nhà hàng | Mở rộng | Khách hàng, Quản lý | Mở rộng |
| FR-18 | Chatbot thao tác nghiệp vụ qua API (tool calling) | Mở rộng | Khách hàng, Chatbot AI | Mở rộng |

#### 2.1.3 Ma trận chức năng – tác nhân

Ký hiệu: `X` = sử dụng đầy đủ; `Xem` = chỉ được phép xem; `Một phần` = sử dụng một phần nghiệp vụ giới hạn.

| Mã | Chức năng | Khách vãng lai | Khách hàng | Nhân viên | Quản lý |
| --- | --- | --- | --- | --- | --- |
| FR-01 | Xác thực và phân quyền | X | X | X | X |
| FR-02 | Xem và tìm kiếm thực đơn | X | X | | |
| FR-03 | Quản lý thực đơn | | | Một phần | X |
| FR-04 | Quản lý sơ đồ bàn | | | Xem | X |
| FR-05 | Đặt bàn theo khung giờ và số khách | | X | | |
| FR-06 | Đặt món trước | | X | | |
| FR-07 | Đặt cọc trực tuyến | | X | | |
| FR-08 | Quản lý đặt chỗ | | | X | X |
| FR-09 | Hủy đặt chỗ và hoàn cọc | | X | Một phần | X |
| FR-10 | Thông báo và nhắc lịch | | Nhận | Nhận | Cấu hình |
| FR-11 | Tổng hợp món chuẩn bị cho bếp | | | X | X |
| FR-12 | Báo cáo thống kê | | | | X |
| FR-13 | Chatbot tư vấn món và giải đáp | X | X | | |
| FR-14 | Chatbot hỗ trợ đặt bàn | | X | | |
| FR-15 | Quản trị và giám sát chatbot | | | | X |
| FR-16 | Đặt tiệc / sự kiện | | X | Xem | X |
| FR-17 | Đánh giá nhà hàng | | X | | X |
| FR-18 | Chatbot thao tác qua API | | X | | |

#### 2.1.4 Vòng đời trạng thái đơn đặt chỗ

| Trạng thái | Ý nghĩa nghiệp vụ | Trạng thái kế tiếp hợp lệ | Tác nhân kích hoạt |
| --- | --- | --- | --- |
| Chờ cọc | Đơn đã khởi tạo, bàn đang được khóa giữ tạm thời (mặc định 10 phút). | Đã xác nhận; Hết hạn; Đã hủy | Hệ thống (cọc thành công / hết hạn); Khách (hủy) |
| Đã xác nhận | Đã thanh toán cọc thành công, bàn được giữ chính thức cho khung giờ. | Đã đến; Đã hủy; Không đến | Nhân viên (check-in); Khách/NV/QL (hủy); NV (không đến) |
| Đã đến | Khách đã đến nhà hàng, nhân viên đã check-in và đang phục vụ. | Hoàn thành | Nhân viên |
| Hoàn thành | Khách đã dùng bữa xong; đơn kết thúc, đủ điều kiện đánh giá. | (Trạng thái cuối) | Nhân viên |
| Đã hủy | Đơn bị hủy bởi khách hàng hoặc nhà hàng; bàn được giải phóng. | (Trạng thái cuối) | Khách hàng; Nhân viên; Quản lý |
| Không đến | Khách không đến quá thời gian chờ (quá 15 phút) và không báo hủy. | (Trạng thái cuối) | Nhân viên |
| Hết hạn | Quá thời gian giữ chỗ tạm thời 10 phút mà chưa hoàn tất đặt cọc. | (Trạng thái cuối) | Hệ thống (tự động) |

### 2.2 Tài khoản và phân quyền

#### FR-01 – Xác thực và phân quyền

| Mã chức năng | FR-01 |
| --- | --- |
| Tên chức năng | Xác thực và phân quyền |
| Mức ưu tiên | MVP – hỗ trợ |
| Tác nhân | Khách vãng lai, Khách hàng, Nhân viên, Quản lý |
| Mô tả | Cho phép đăng ký, đăng nhập, đăng xuất, quản lý hồ sơ cá nhân và phân quyền truy cập chức năng theo vai trò. |
| Tiền điều kiện | Người dùng truy cập hệ thống qua trình duyệt. |
| Luồng sự kiện chính | 1. Người dùng chọn Đăng ký và nhập họ tên, số điện thoại, email, mật khẩu.<br>2. Hệ thống kiểm tra tính hợp lệ và tính duy nhất của email, số điện thoại.<br>3. Hệ thống tạo tài khoản vai trò Khách hàng và gửi email xác thực.<br>4. Người dùng đăng nhập bằng email hoặc số điện thoại cùng mật khẩu.<br>5. Hệ thống cấp phiên đăng nhập (JWT) có thời hạn và điều hướng theo vai trò. |
| Luồng thay thế / ngoại lệ | • Email hoặc số điện thoại đã tồn tại: hệ thống báo lỗi và gợi ý đăng nhập.<br>• Sai mật khẩu quá 5 lần liên tiếp: khóa đăng nhập tạm thời 15 phút.<br>• Quên mật khẩu: hệ thống gửi liên kết đặt lại mật khẩu có thời hạn (dùng 1 lần) qua email.<br>• Truy cập chức năng ngoài quyền: hệ thống từ chối (HTTP 403) và ghi nhật ký. |
| Hậu điều kiện & Quy tắc nghiệp vụ | • **Hậu điều kiện:** Phiên đăng nhập hợp lệ được tạo; sự kiện đăng nhập và lỗi phân quyền được ghi nhật ký.<br>• **Quy tắc nghiệp vụ:**<br>• Có 3 vai trò đăng nhập: Khách hàng, Nhân viên, Quản lý. Tài khoản Nhân viên và Quản lý do Quản lý tạo/khóa.<br>• Khách vãng lai được xem thực đơn và trò chuyện với chatbot; đặt bàn và đặt cọc yêu cầu đăng nhập.<br>• Mật khẩu được lưu dưới dạng băm; toàn bộ truyền tải qua HTTPS. |

### 2.3 Thực đơn

#### FR-02 – Xem và tìm kiếm thực đơn

| Mã chức năng | FR-02 |
| --- | --- |
| Tên chức năng | Xem và tìm kiếm thực đơn |
| Mức ưu tiên | MVP (bắt buộc) |
| Tác nhân | Khách vãng lai, Khách hàng |
| Mô tả | Hiển thị thực đơn theo danh mục kèm hình ảnh, mô tả, giá và tình trạng; hỗ trợ tìm kiếm và lọc món. |
| Tiền điều kiện | Không yêu cầu đăng nhập. |
| Luồng sự kiện chính | 1. Người dùng chọn mục Thực đơn.<br>2. Hệ thống hiển thị danh mục và các món đang bán.<br>3. Người dùng tìm theo từ khóa hoặc lọc theo danh mục, khoảng giá, nhãn món (chay, cay, hải sản…).<br>4. Người dùng chọn một món để xem chi tiết.<br>5. Khách hàng đã có đơn đặt bàn có thể thêm món vào danh sách đặt trước (FR-06). |
| Luồng thay thế / ngoại lệ | • Không có kết quả phù hợp: hệ thống thông báo và gợi ý bỏ bớt bộ lọc.<br>• Món đang tạm hết: hiển thị nhãn “Tạm hết” và khóa nút thêm vào đơn. |
| Hậu điều kiện & Quy tắc nghiệp vụ | • **Hậu điều kiện:** Không thay đổi dữ liệu hệ thống.<br>• **Quy tắc nghiệp vụ:**<br>• Chỉ hiển thị món ở trạng thái “Đang bán” hoặc “Tạm hết”; giá hiển thị bằng VNĐ.<br>• Dữ liệu thực đơn là nguồn dữ liệu duy nhất để chatbot tư vấn (FR-13). |

#### FR-03 – Quản lý thực đơn

| Mã chức năng | FR-03 |
| --- | --- |
| Tên chức năng | Quản lý thực đơn |
| Mức ưu tiên | MVP (bắt buộc) |
| Tác nhân | Quản lý (Nhân viên chỉ cập nhật tình trạng còn/hết) |
| Mô tả | Thêm, sửa, ẩn danh mục và món ăn: tên, mô tả, giá, hình ảnh, nhãn món, trạng thái bán; cập nhật tình trạng còn/hết. |
| Tiền điều kiện | Người dùng đã đăng nhập với vai trò Quản lý (hoặc Nhân viên đối với thao tác đổi tình trạng món). |
| Luồng sự kiện chính | 1. Quản lý vào mục Quản lý thực đơn.<br>2. Chọn Thêm món, Sửa món hoặc Ngừng bán.<br>3. Nhập hoặc chỉnh sửa thông tin món.<br>4. Hệ thống kiểm tra dữ liệu hợp lệ (tên không rỗng, giá > 0, hình ảnh đúng định dạng và dung lượng).<br>5. Hệ thống lưu thay đổi, ghi lịch sử thay đổi giá và cập nhật thực đơn hiển thị cho khách và dữ liệu chatbot sử dụng. |
| Luồng thay thế / ngoại lệ | • Món đang nằm trong đơn đặt chỗ chưa hoàn thành: không cho xóa vật lý, chỉ cho chuyển sang “Ngừng bán”.<br>• Hình ảnh sai định dạng hoặc quá dung lượng: hệ thống báo lỗi, không lưu. |
| Hậu điều kiện & Quy tắc nghiệp vụ | • **Hậu điều kiện:** Thực đơn được cập nhật và có hiệu lực ngay cho các lượt đặt mới và tri thức chatbot.<br>• **Quy tắc nghiệp vụ:**<br>• Xóa mềm; không xóa món đã từng phát sinh đơn.<br>• Đơn đã đặt giữ nguyên giá tại thời điểm khách xác nhận món (lưu giá chốt trong chi tiết đơn).<br>• Khi món chuyển sang “Hết” hoặc “Ngừng bán” mà đã có đơn đặt trước, hệ thống đánh dấu các đơn bị ảnh hưởng và cảnh báo nhân viên để liên hệ khách đổi món. |

### 2.4 Sơ đồ bàn và đặt bàn

#### FR-04 – Quản lý sơ đồ bàn

| Mã chức năng | FR-04 |
| --- | --- |
| Tên chức năng | Quản lý sơ đồ bàn |
| Mức ưu tiên | MVP (bắt buộc) |
| Tác nhân | Quản lý (Nhân viên chỉ xem) |
| Mô tả | Khai báo khu vực, bàn, sức chứa và vị trí bàn trên sơ đồ trực quan; xem trạng thái từng bàn theo ngày và khung giờ. |
| Tiền điều kiện | Người dùng đã đăng nhập với vai trò Quản lý hoặc Nhân viên. |
| Luồng sự kiện chính | 1. Quản lý vào mục Sơ đồ bàn.<br>2. Tạo khu vực (ví dụ: tầng 1, sân vườn, phòng riêng).<br>3. Thêm bàn: mã bàn, số chỗ, khu vực, vị trí trên sơ đồ (kéo thả lưu tọa độ).<br>4. Hệ thống kiểm tra và lưu sơ đồ.<br>5. Người dùng chọn ngày và giờ để xem trạng thái từng bàn: Trống, Đang giữ, Đã đặt, Đang phục vụ, Ngưng sử dụng. |
| Luồng thay thế / ngoại lệ | • Mã bàn trùng trong cùng cơ sở: hệ thống báo lỗi.<br>• Xóa hoặc ngưng bàn đang có đơn đặt trong tương lai: hệ thống chặn và yêu cầu chuyển bàn cho các đơn đó trước. |
| Hậu điều kiện & Quy tắc nghiệp vụ | • **Hậu điều kiện:** Sơ đồ bàn được lưu và được dùng làm cơ sở tính bàn trống cho FR-05.<br>• **Quy tắc nghiệp vụ:**<br>• Sức chứa của bàn tối thiểu là 1.<br>• Bàn ở trạng thái “Ngưng sử dụng” không nhận đơn đặt mới.<br>• Cho phép đánh dấu bàn có thể ghép để phục vụ nhóm đông khách. |

#### FR-05 – Đặt bàn theo khung giờ và số khách

| Mã chức năng | FR-05 |
| --- | --- |
| Tên chức năng | Đặt bàn theo khung giờ và số khách |
| Mức ưu tiên | MVP (bắt buộc) |
| Tác nhân | Khách hàng |
| Mô tả | Cho phép khách chọn ngày, giờ, số khách; hệ thống kiểm tra bàn trống phù hợp, giữ chỗ tạm thời và tạo đơn đặt chỗ. |
| Tiền điều kiện | Khách hàng đã đăng nhập; có ít nhất một bàn đang hoạt động. |
| Luồng sự kiện chính | 1. Khách chọn Đặt bàn.<br>2. Khách nhập ngày, giờ, số khách; có thể chọn thêm khu vực ưa thích và ghi chú (ví dụ: sinh nhật, ghế trẻ em).<br>3. Hệ thống tìm bàn trống có sức chứa phù hợp và không trùng khung giờ với đơn khác.<br>4. Hệ thống hiển thị các khung giờ còn bàn và bàn gợi ý.<br>5. Khách chọn khung giờ (và bàn, nếu nhà hàng cho phép chọn bàn).<br>6. Hệ thống tạo đơn ở trạng thái “Chờ cọc” và giữ bàn tạm thời trong thời gian giữ chỗ (kèm đồng hồ đếm ngược).<br>7. Khách tiếp tục đặt món trước (FR-06, tùy chọn) và đặt cọc (FR-07). |
| Luồng thay thế / ngoại lệ | • Không còn bàn phù hợp: hệ thống gợi ý khung giờ gần nhất hoặc khu vực khác.<br>• Hết thời gian giữ chỗ mà chưa cọc: đơn tự động chuyển “Hết hạn”, bàn được giải phóng.<br>• Hai khách cùng chọn một bàn trong cùng khung giờ: khách giữ chỗ thành công trước được giữ, khách sau nhận thông báo và gợi ý lựa chọn khác.<br>• Số khách vượt sức chứa lớn nhất của một bàn: hệ thống đề xuất ghép bàn hoặc chuyển sang đặt tiệc/sự kiện (FR-16). |
| Hậu điều kiện & Quy tắc nghiệp vụ | • **Hậu điều kiện:** Đơn đặt chỗ “Chờ cọc” được tạo kèm bàn đang khóa giữ tạm thời.<br>• **Quy tắc nghiệp vụ:**<br>• Khung giờ chia theo bước 30 phút; thời lượng mỗi lượt phục vụ mặc định 90 phút.<br>• Đặt trước tối thiểu 2 giờ và tối đa 30 ngày so với giờ hẹn.<br>• Thời gian giữ chỗ chờ cọc mặc định 10 phút.<br>• Tại mỗi thời điểm, một bàn chỉ thuộc về một đơn: việc kiểm tra và giữ bàn phải thực hiện trong một giao dịch (transaction) và có ràng buộc ở cơ sở dữ liệu để chống trùng bàn.<br>• Mọi thời gian tính theo múi giờ Việt Nam (GMT+7). |

### 2.5 Đặt món trước và đặt cọc

#### FR-06 – Đặt món trước

| Mã chức năng | FR-06 |
| --- | --- |
| Tên chức năng | Đặt món trước |
| Mức ưu tiên | MVP (bắt buộc) |
| Tác nhân | Khách hàng |
| Mô tả | Cho phép khách chọn món và số lượng để nhà hàng chuẩn bị trước, gắn với đơn đặt bàn. |
| Tiền điều kiện | Khách hàng đã có đơn đặt chỗ ở trạng thái “Chờ cọc” hoặc “Đã xác nhận” còn trong hạn chỉnh sửa món. |
| Luồng sự kiện chính | 1. Khách chọn Đặt món trước trong đơn.<br>2. Khách duyệt thực đơn, thêm món, nhập số lượng và ghi chú cho từng món.<br>3. Hệ thống tính tạm tính theo giá hiện hành.<br>4. Khách có thể sửa số lượng hoặc xóa món.<br>5. Khách xác nhận danh sách món; hệ thống lưu giá chốt từng món, cập nhật tổng tiền và số tiền cọc yêu cầu. |
| Luồng thay thế / ngoại lệ | • Món hết trong lúc đặt: hệ thống thông báo và loại món khỏi danh sách.<br>• Khách không đặt món: đơn vẫn hợp lệ, tiền cọc tính theo quy tắc cọc khi không có món.<br>• Sửa món sau khi đã cọc: cho phép đến hạn chốt; nếu tổng tiền thay đổi, hệ thống tính lại mức cọc và xử lý phần chênh lệch. |
| Hậu điều kiện & Quy tắc nghiệp vụ | • **Hậu điều kiện:** Đơn lưu danh sách món, giá chốt (`unit_price_locked`) và tổng tiền; số tiền cọc yêu cầu được cập nhật.<br>• **Quy tắc nghiệp vụ:**<br>• Hạn chót chỉnh sửa hoặc hủy món mặc định là 2 giờ trước giờ hẹn.<br>• Số lượng mỗi món từ 1 đến 20 (có thể cấu hình).<br>• Chỉ cho đặt món đang bán; giá lấy từ thực đơn tại thời điểm xác nhận. |

#### FR-07 – Đặt cọc trực tuyến

| Mã chức năng | FR-07 |
| --- | --- |
| Tên chức năng | Đặt cọc trực tuyến |
| Mức ưu tiên | MVP (bắt buộc) |
| Tác nhân | Khách hàng; Cổng thanh toán (hệ thống ngoài) |
| Mô tả | Cho phép khách thanh toán tiền cọc qua cổng thanh toán để xác nhận đơn đặt chỗ. |
| Tiền điều kiện | Đơn ở trạng thái “Chờ cọc” và còn trong thời gian giữ chỗ. |
| Luồng sự kiện chính | 1. Hệ thống hiển thị tóm tắt đơn: bàn, giờ, số khách, món đặt trước, số tiền cọc, chính sách hủy và hoàn cọc.<br>2. Khách đồng ý điều khoản và chọn Thanh toán.<br>3. Hệ thống tạo giao dịch và chuyển khách sang cổng thanh toán Sandbox.<br>4. Khách hoàn tất thanh toán trên cổng.<br>5. Cổng thanh toán gửi kết quả về hệ thống (callback/webhook); hệ thống xác thực chữ ký của kết quả.<br>6. Nếu thành công, đơn chuyển sang “Đã xác nhận”, hệ thống sinh mã đặt chỗ và gửi xác nhận cho khách (FR-10). |
| Luồng thay thế / ngoại lệ | • Thanh toán thất bại hoặc khách hủy: đơn giữ nguyên “Chờ cọc” đến hết thời gian giữ chỗ; khách có thể thử lại.<br>• Kết quả thanh toán thành công đến muộn sau khi đơn đã hết hạn: nếu bàn còn trống, hệ thống xác nhận đơn; nếu không, tự động đánh dấu hoàn cọc và thông báo cho khách.<br>• Kết quả thanh toán gửi trùng lặp: hệ thống xử lý một lần duy nhất (idempotent, không ghi nhận cọc hai lần).<br>• Cổng thanh toán không phản hồi: hệ thống thông báo lỗi và không ghi nhận cọc. |
| Hậu điều kiện & Quy tắc nghiệp vụ | • **Hậu điều kiện:** Giao dịch cọc được lưu; đơn chuyển sang trạng thái “Đã xác nhận” khi cọc thành công.<br>• **Quy tắc nghiệp vụ:**<br>• Mức cọc do Quản lý cấu hình; đề xuất mặc định 30% giá trị món đặt trước, tối thiểu một mức cố định theo số khách khi không đặt món.<br>• Chỉ lưu mã giao dịch, số tiền, thời điểm, trạng thái; không lưu số thẻ hay thông tin thanh toán nhạy cảm.<br>• Khoản cọc được hiển thị trong chi tiết đơn để nhân viên trừ vào hóa đơn khi khách dùng bữa. |

### 2.6 Vận hành đặt chỗ

#### FR-08 – Quản lý đặt chỗ

| Mã chức năng | FR-08 |
| --- | --- |
| Tên chức năng | Quản lý đặt chỗ |
| Mức ưu tiên | MVP (bắt buộc) |
| Tác nhân | Nhân viên, Quản lý |
| Mô tả | Theo dõi và xử lý các đơn đặt chỗ: xem danh sách, xác nhận, đổi bàn hoặc giờ, hủy, check-in, hoàn thành, đánh dấu không đến; tạo đơn thay khách khi khách đặt qua điện thoại. |
| Tiền điều kiện | Người dùng đã đăng nhập với vai trò Nhân viên hoặc Quản lý. |
| Luồng sự kiện chính | 1. Nhân viên vào mục Quản lý đặt chỗ.<br>2. Lọc đơn theo ngày, trạng thái, khu vực, mã đặt chỗ hoặc số điện thoại khách.<br>3. Chọn một đơn để xem chi tiết: khách, bàn, món đặt trước, khoản cọc, lịch sử thay đổi.<br>4. Thực hiện thao tác: đổi bàn/giờ, ghi chú, hủy, check-in khi khách đến, hoàn thành, đánh dấu không đến.<br>5. Hệ thống cập nhật trạng thái đơn, đồng bộ sơ đồ bàn và gửi thông báo cho khách khi cần (FR-10). |
| Luồng thay thế / ngoại lệ | • Đổi sang bàn hoặc giờ đã có đơn khác: hệ thống chặn thao tác.<br>• Hủy đơn đã cọc: áp dụng chính sách hoàn cọc (FR-09); chỉ Quản lý được xử lý ngoại lệ và phải ghi lý do.<br>• Thao tác trên đơn đã ở trạng thái cuối (Hoàn thành, Đã hủy, Không đến, Hết hạn): hệ thống không cho phép.<br>• Khách đặt qua điện thoại (mở rộng US-50): nhân viên tạo đơn thay khách theo luồng FR-05 và gửi liên kết đặt cọc. |
| Hậu điều kiện & Quy tắc nghiệp vụ | • **Hậu điều kiện:** Trạng thái đơn và sơ đồ bàn được cập nhật đồng bộ; mọi thao tác được ghi vào lịch sử.<br>• **Quy tắc nghiệp vụ:**<br>• Tuân theo vòng đời đơn ở mục 2.1.4.<br>• Mọi thay đổi ghi nhật ký: người thực hiện, thời điểm, giá trị cũ và mới.<br>• Quá giờ hẹn 15 phút mà chưa check-in: hệ thống nhắc nhân viên xử lý; nhân viên đánh dấu “Không đến”. |

#### FR-09 – Hủy đặt chỗ và hoàn cọc

| Mã chức năng | FR-09 |
| --- | --- |
| Tên chức năng | Hủy đặt chỗ và hoàn cọc |
| Mức ưu tiên | MVP – hỗ trợ |
| Tác nhân | Khách hàng; Nhân viên, Quản lý (xử lý ngoại lệ) |
| Mô tả | Cho phép khách hủy đơn và hoàn cọc theo chính sách hủy của nhà hàng. |
| Tiền điều kiện | Đơn ở trạng thái “Chờ cọc” hoặc “Đã xác nhận”, chưa đến giờ hẹn. |
| Luồng sự kiện chính | 1. Khách mở mục Đặt chỗ của tôi, chọn đơn và nhấn Hủy.<br>2. Hệ thống hiển thị mức hoàn cọc theo chính sách tại thời điểm hủy.<br>3. Khách xác nhận hủy.<br>4. Hệ thống chuyển đơn sang “Đã hủy”, giải phóng bàn và tạo yêu cầu hoàn cọc (nếu có).<br>5. Hệ thống gửi thông báo kết quả cho khách (FR-10). |
| Luồng thay thế / ngoại lệ | • Hủy trong khoảng thời gian không được hoàn cọc: hệ thống cảnh báo mất cọc trước khi khách xác nhận.<br>• Hoàn cọc qua cổng thanh toán lỗi: yêu cầu hoàn được đánh dấu “Chờ xử lý thủ công” để Quản lý xử lý. |
| Hậu điều kiện & Quy tắc nghiệp vụ | • **Hậu điều kiện:** Đơn chuyển sang “Đã hủy”; bàn được giải phóng; khoản hoàn cọc được ghi nhận.<br>• **Quy tắc nghiệp vụ:**<br>• Chính sách đề xuất: hủy trước giờ hẹn từ 24 giờ trở lên hoàn 100%; từ 2 đến dưới 24 giờ hoàn 50%; dưới 2 giờ không hoàn. Khách không đến không được hoàn cọc.<br>• Các mốc thời gian và tỷ lệ hoàn do Quản lý cấu hình và phải hiển thị cho khách trước khi cọc. |

#### FR-10 – Thông báo và nhắc lịch

| Mã chức năng | FR-10 |
| --- | --- |
| Tên chức năng | Thông báo và nhắc lịch |
| Mức ưu tiên | MVP – hỗ trợ |
| Tác nhân | Hệ thống; Khách hàng, Nhân viên (nhận thông báo); Quản lý (cấu hình mẫu) |
| Mô tả | Gửi xác nhận, nhắc lịch và thông báo thay đổi/hủy qua email và SMS; thông báo đơn mới cho nhân viên trong hệ thống. |
| Tiền điều kiện | Có sự kiện kích hoạt (đơn xác nhận, thay đổi, hủy, đến mốc nhắc lịch). |
| Luồng sự kiện chính | 1. Hệ thống phát hiện sự kiện cần thông báo.<br>2. Hệ thống chọn mẫu nội dung và kênh gửi phù hợp.<br>3. Hệ thống gửi qua dịch vụ email hoặc SMS.<br>4. Hệ thống ghi nhận kết quả gửi vào chi tiết đơn. |
| Luồng thay thế / ngoại lệ | • Gửi thất bại: thử lại tối đa 3 lần; nếu vẫn lỗi thì ghi nhật ký và hiển thị cảnh báo trong chi tiết đơn.<br>• Số điện thoại không hợp lệ: tự động chuyển gửi bằng email. |
| Hậu điều kiện & Quy tắc nghiệp vụ | • **Hậu điều kiện:** Thông báo được gửi và trạng thái gửi được lưu vào nhật ký đơn.<br>• **Quy tắc nghiệp vụ:**<br>• Nhắc lịch mặc định trước 24 giờ và trước 2 giờ so với giờ hẹn (cấu hình được) nhằm giảm tình trạng khách không đến.<br>• SMS chỉ dùng cho sự kiện quan trọng (nhắc lịch trước 2 giờ) để kiểm soát chi phí.<br>• Nội dung gồm mã đặt chỗ, giờ, bàn, chính sách hủy và liên kết quản lý đơn. |

#### FR-11 – Tổng hợp món chuẩn bị cho bếp

| Mã chức năng | FR-11 |
| --- | --- |
| Tên chức năng | Tổng hợp món chuẩn bị cho bếp |
| Mức ưu tiên | MVP – hỗ trợ |
| Tác nhân | Nhân viên, Quản lý |
| Mô tả | Tổng hợp các món đặt trước theo ngày và khung giờ để bếp chuẩn bị. |
| Tiền điều kiện | Người dùng đã đăng nhập với vai trò Nhân viên hoặc Quản lý. |
| Luồng sự kiện chính | 1. Nhân viên chọn ngày và ca hoặc khung giờ cần xem.<br>2. Hệ thống tổng hợp các món và số lượng từ các đơn “Đã xác nhận”, kèm ghi chú của khách.<br>3. Nhân viên xem, in hoặc xuất PDF danh sách.<br>4. Bếp có thể đánh dấu món đã chuẩn bị (tùy chọn). |
| Luồng thay thế / ngoại lệ | • Đơn bị hủy hoặc sửa món sau khi đã in: danh sách trên hệ thống cập nhật và nêu rõ thay đổi.<br>• Không có đơn trong khoảng đã chọn: hệ thống hiển thị danh sách trống. |
| Hậu điều kiện & Quy tắc nghiệp vụ | • **Hậu điều kiện:** Không thay đổi dữ liệu đơn (trừ trạng thái chuẩn bị món nếu có dùng).<br>• **Quy tắc nghiệp vụ:**<br>• Chỉ tính các đơn đã xác nhận (đã cọc).<br>• Danh sách được cập nhật theo dữ liệu mới nhất và có thể xuất PDF hoặc in. |

### 2.7 Báo cáo

#### FR-12 – Báo cáo thống kê

| Mã chức năng | FR-12 |
| --- | --- |
| Tên chức năng | Báo cáo thống kê |
| Mức ưu tiên | MVP (bắt buộc) |
| Tác nhân | Quản lý |
| Mô tả | Cung cấp báo cáo theo khoảng thời gian: số đơn theo trạng thái, tỷ lệ hủy và không đến, doanh thu cọc và hoàn cọc, món được đặt trước nhiều nhất, công suất sử dụng bàn theo khung giờ, số đơn đặt ngoài giờ làm việc và thống kê hoạt động chatbot. |
| Tiền điều kiện | Người dùng đã đăng nhập với vai trò Quản lý. |
| Luồng sự kiện chính | 1. Quản lý vào mục Báo cáo.<br>2. Chọn loại báo cáo, khoảng thời gian và bộ lọc (khu vực, trạng thái).<br>3. Hệ thống tổng hợp dữ liệu và hiển thị dưới dạng bảng và biểu đồ.<br>4. Quản lý xuất báo cáo ra Excel hoặc PDF (mở rộng US-47). |
| Luồng thay thế / ngoại lệ | • Không có dữ liệu trong khoảng thời gian: hệ thống thông báo rõ ràng.<br>• Khoảng thời gian quá dài (trên 1 năm): hệ thống yêu cầu thu hẹp khoảng thời gian. |
| Hậu điều kiện & Quy tắc nghiệp vụ | • **Hậu điều kiện:** Không thay đổi dữ liệu hệ thống.<br>• **Quy tắc nghiệp vụ:**<br>• Tỷ lệ không đến = số đơn không đến / số đơn đã xác nhận đã qua giờ hẹn.<br>• Số liệu lấy từ dữ liệu đơn và giao dịch thực tế; thời gian lọc theo GMT+7.<br>• Thống kê chatbot gồm số hội thoại, tỷ lệ chuyển cho nhân viên và tỷ lệ phản hồi “Không hữu ích”. |

### 2.8 Chatbot AI

#### FR-13 – Chatbot tư vấn món và giải đáp thông tin

| Mã chức năng | FR-13 |
| --- | --- |
| Tên chức năng | Chatbot tư vấn món và giải đáp thông tin |
| Mức ưu tiên | MVP (bắt buộc) |
| Tác nhân | Khách vãng lai, Khách hàng; Máy chủ Ollama (hệ thống ngoài) |
| Mô tả | Chatbot AI trả lời bằng tiếng Việt về món ăn, giờ mở cửa, địa chỉ, chính sách đặt cọc và hủy; gợi ý món theo ngân sách, số người, sở thích. |
| Tiền điều kiện | Khung chat có trên website; dịch vụ Ollama hoạt động. |
| Luồng sự kiện chính | 1. Khách mở khung chat; chatbot chào và nêu rõ đây là trợ lý AI.<br>2. Khách đặt câu hỏi (ví dụ: gợi ý món cho 4 người, món chay, giờ mở cửa, chính sách hủy).<br>3. Hệ thống xác định yêu cầu và truy xuất dữ liệu liên quan (RAG) từ thực đơn, chính sách và thông tin nhà hàng.<br>4. Chatbot soạn câu trả lời dựa trên dữ liệu truy xuất, kèm thẻ món (tên, giá, hình ảnh, nút Thêm vào đơn đặt trước).<br>5. Hệ thống lưu hội thoại và cho phép khách đánh giá câu trả lời là Hữu ích hoặc Không hữu ích. |
| Luồng thay thế / ngoại lệ | • Câu hỏi ngoài phạm vi nhà hàng: chatbot từ chối lịch sự và hướng khách về chủ đề phù hợp.<br>• Không có thông tin để trả lời: chatbot nói rõ chưa có thông tin và cung cấp cách liên hệ nhân viên.<br>• Dịch vụ Ollama lỗi hoặc quá thời gian chờ: hệ thống thông báo chatbot tạm ngưng và hướng dẫn dùng thực đơn, biểu mẫu đặt bàn. |
| Hậu điều kiện & Quy tắc nghiệp vụ | • **Hậu điều kiện:** Hội thoại được lưu vào CSDL phục vụ giám sát (FR-15).<br>• **Quy tắc nghiệp vụ:**<br>• Tên món, giá, tình trạng và chính sách chỉ được lấy từ dữ liệu hệ thống tại thời điểm hỏi; chatbot không được tự suy đoán hay bịa thông tin (hạn chế ảo giác).<br>• Không gửi họ tên, số điện thoại, email của khách lên dịch vụ LLM; dữ liệu cá nhân được loại bỏ hoặc che (PII Masking) trước khi gửi.<br>• Không đưa ra cam kết về dị ứng hoặc y tế; với câu hỏi này, chatbot hướng khách liên hệ nhân viên.<br>• Có giới hạn tần suất (rate limit) và độ dài tin nhắn để tránh lạm dụng. |

#### FR-14 – Chatbot hỗ trợ đặt bàn qua hội thoại

| Mã chức năng | FR-14 |
| --- | --- |
| Tên chức năng | Chatbot hỗ trợ đặt bàn qua hội thoại |
| Mức ưu tiên | MVP (bắt buộc) |
| Tác nhân | Khách hàng |
| Mô tả | Chatbot dẫn dắt khách cung cấp thông tin đặt bàn, tra cứu bàn trống và chuyển khách sang bước xác nhận và đặt cọc với thông tin đã điền sẵn. |
| Tiền điều kiện | Khung chat hoạt động; khách có thể đăng nhập trong quá trình hội thoại. |
| Luồng sự kiện chính | 1. Khách nêu nhu cầu đặt bàn trong khung chat.<br>2. Chatbot hỏi lần lượt các thông tin còn thiếu: ngày, giờ, số khách, khu vực (nếu có).<br>3. Chatbot tra cứu bàn trống qua chức năng kiểm tra bàn trống của FR-05 (chỉ đọc) và đề xuất khung giờ.<br>4. Khách chọn khung giờ.<br>5. Chatbot tạo liên kết đến biểu mẫu đặt bàn đã điền sẵn thông tin (`/booking?...`).<br>6. Khách xác nhận, chọn món (tùy chọn) và đặt cọc theo FR-05, FR-06, FR-07. |
| Luồng thay thế / ngoại lệ | • Khách chưa đăng nhập: chatbot yêu cầu đăng nhập và giữ lại toàn bộ thông tin đặt bàn đã nhập.<br>• Hết bàn ở khung giờ khách chọn: chatbot đề xuất khung giờ hoặc khu vực khác.<br>• Thông tin không hợp lệ (ngày đã qua, quá giới hạn đặt trước 2h–30 ngày): chatbot nêu lý do và hỏi lại. |
| Hậu điều kiện & Quy tắc nghiệp vụ | • **Hậu điều kiện:** Khách nhận liên kết đặt bàn với thông tin điền sẵn; đơn chỉ được tạo khi khách xác nhận trên hệ thống.<br>• **Quy tắc nghiệp vụ:**<br>• Chatbot không được thông báo “đã đặt thành công” khi chưa có xác nhận từ hệ thống.<br>• Ngày giờ do khách nhập bằng ngôn ngữ tự nhiên được chuẩn hóa theo GMT+7 và được hiển thị lại để khách xác nhận.<br>• Dữ liệu bàn trống lấy từ cùng dịch vụ với FR-05 để đảm bảo nhất quán. |

#### FR-15 – Quản trị tri thức và giám sát chatbot

| Mã chức năng | FR-15 |
| --- | --- |
| Tên chức năng | Quản trị tri thức và giám sát chatbot |
| Mức ưu tiên | MVP – hỗ trợ |
| Tác nhân | Quản lý |
| Mô tả | Quản lý nội dung nghiệp vụ chatbot sử dụng (thông tin nhà hàng, chính sách, câu hỏi thường gặp), xem lịch sử hội thoại và theo dõi chất lượng trả lời. |
| Tiền điều kiện | Người dùng đã đăng nhập với vai trò Quản lý. |
| Luồng sự kiện chính | 1. Quản lý vào mục Quản trị chatbot.<br>2. Thêm hoặc sửa mục thông tin: giờ mở cửa, địa chỉ, chính sách đặt cọc và hủy, câu hỏi thường gặp (FAQ).<br>3. Hệ thống lưu và chatbot sử dụng nội dung mới ngay.<br>4. Quản lý xem lịch sử hội thoại, lọc theo phản hồi “Không hữu ích” hoặc hội thoại cần chuyển nhân viên.<br>5. Quản lý đánh dấu câu trả lời sai và ghi chú để chỉnh lại nội dung hoặc kịch bản chatbot. |
| Luồng thay thế / ngoại lệ | • Nội dung để trống hoặc vượt giới hạn độ dài: hệ thống báo lỗi.<br>• Xóa mục đang được dùng: hệ thống yêu cầu xác nhận. |
| Hậu điều kiện & Quy tắc nghiệp vụ | • **Hậu điều kiện:** Tri thức chatbot và đánh dấu chất lượng được cập nhật.<br>• **Quy tắc nghiệp vụ:**<br>• Dữ liệu cá nhân trong lịch sử hội thoại được che khi hiển thị.<br>• Lịch sử hội thoại lưu tối đa 90 ngày (cấu hình được).<br>• Chỉ Quản lý được xem lịch sử hội thoại. |

### 2.9 Chức năng mở rộng (Backlog dự phòng)

#### FR-16 – Đặt tiệc / sự kiện

| Mã chức năng | FR-16 |
| --- | --- |
| Tên chức năng | Đặt tiệc / sự kiện |
| Mức ưu tiên | Mở rộng |
| Tác nhân | Khách hàng; Quản lý (duyệt); Nhân viên (xem) |
| Mô tả | Cho phép khách gửi yêu cầu đặt tiệc hoặc sự kiện cho nhóm đông, nhiều bàn hoặc phòng riêng; Quản lý duyệt, báo giá và yêu cầu cọc. |
| Tiền điều kiện | Khách hàng đã đăng nhập. |
| Luồng sự kiện chính | 1. Khách chọn Đặt tiệc/sự kiện.<br>2. Khách nhập loại sự kiện, ngày giờ, số khách, ngân sách dự kiến và yêu cầu đặc biệt.<br>3. Hệ thống kiểm tra khả năng sắp xếp (ghép bàn hoặc phòng riêng) và tạo yêu cầu “Chờ duyệt”.<br>4. Quản lý xem yêu cầu, điều chỉnh, báo giá và đặt mức cọc.<br>5. Khách xác nhận báo giá và đặt cọc theo FR-07.<br>6. Hệ thống xác nhận đơn tiệc và giữ bàn tương ứng. |
| Luồng thay thế / ngoại lệ | • Không đủ chỗ: Quản lý từ chối hoặc đề xuất thời điểm khác.<br>• Khách không phản hồi báo giá trong thời hạn quy định: yêu cầu chuyển “Hết hạn”. |
| Hậu điều kiện & Quy tắc nghiệp vụ | • **Hậu điều kiện:** Đơn tiệc được xác nhận hoặc đóng với lý do rõ ràng.<br>• **Quy tắc nghiệp vụ:**<br>• Đơn tiệc dùng chung cơ chế giữ bàn và chống trùng bàn với FR-05.<br>• Mức cọc, thời hạn đặt tối thiểu và thời hạn báo giá do Quản lý cấu hình riêng cho đơn tiệc. |

#### FR-17 – Đánh giá nhà hàng

| Mã chức năng | FR-17 |
| --- | --- |
| Tên chức năng | Đánh giá nhà hàng |
| Mức ưu tiên | Mở rộng |
| Tác nhân | Khách hàng; Quản lý |
| Mô tả | Cho phép khách đánh giá trải nghiệm sau khi dùng bữa; Quản lý xem, phản hồi và kiểm duyệt. |
| Tiền điều kiện | Đơn của khách ở trạng thái “Hoàn thành”. |
| Luồng sự kiện chính | 1. Hệ thống mời khách đánh giá sau khi đơn hoàn thành.<br>2. Khách chấm điểm từ 1 đến 5 sao và nhập nhận xét.<br>3. Hệ thống lưu đánh giá (chờ duyệt nếu bật kiểm duyệt).<br>4. Đánh giá hợp lệ được hiển thị trên website; Quản lý có thể phản hồi hoặc ẩn đánh giá vi phạm. |
| Luồng thay thế / ngoại lệ | • Khách chưa có đơn hoàn thành: hệ thống không cho đánh giá.<br>• Khách đã đánh giá đơn này: chỉ cho phép sửa trong 7 ngày. |
| Hậu điều kiện & Quy tắc nghiệp vụ | • **Hậu điều kiện:** Đánh giá được lưu; điểm trung bình của nhà hàng được cập nhật.<br>• **Quy tắc nghiệp vụ:**<br>• Mỗi đơn hoàn thành chỉ có một đánh giá.<br>• Nhận xét chứa từ ngữ không phù hợp bị chặn hoặc chuyển chờ duyệt. |

#### FR-18 – Chatbot thực hiện thao tác nghiệp vụ qua API (tool calling)

| Mã chức năng | FR-18 |
| --- | --- |
| Tên chức năng | Chatbot thực hiện thao tác nghiệp vụ qua API (tool calling) |
| Mức ưu tiên | Mở rộng |
| Tác nhân | Khách hàng; Chatbot AI |
| Mô tả | Chatbot gọi trực tiếp các API nghiệp vụ được cho phép thay cho việc chuyển khách sang biểu mẫu: tra cứu đơn của khách, tạo đơn giữ chỗ, thêm món, hủy đơn, tra cứu mức hoàn cọc. |
| Tiền điều kiện | Khách đã đăng nhập; danh mục công cụ (tool) của chatbot được cấu hình. |
| Luồng sự kiện chính | 1. Khách nêu yêu cầu thao tác bằng ngôn ngữ tự nhiên (ví dụ: “đặt bàn 4 người 19h thứ Sáu”, “hủy đơn của tôi”).<br>2. Mô hình xác định công cụ và tham số cần gọi.<br>3. Back-end kiểm tra quyền của khách và tính hợp lệ của tham số trước khi thực thi.<br>4. Với thao tác làm thay đổi dữ liệu, chatbot hiển thị tóm tắt và yêu cầu khách xác nhận rõ ràng.<br>5. Sau khi khách xác nhận, hệ thống gọi API nghiệp vụ (cùng quy tắc với FR-05 đến FR-09).<br>6. Chatbot thông báo kết quả thực tế do API trả về. |
| Luồng thay thế / ngoại lệ | • Thiếu tham số: chatbot hỏi thêm.<br>• API từ chối (hết bàn, ngoài quyền, vi phạm chính sách): chatbot nêu nguyên nhân.<br>• Khách không xác nhận: thao tác bị hủy, không thay đổi dữ liệu.<br>• Phát hiện gọi bất thường hoặc vượt giới hạn: hệ thống chặn và ghi nhật ký. |
| Hậu điều kiện & Quy tắc nghiệp vụ | • **Hậu điều kiện:** Dữ liệu chỉ thay đổi khi API thực thi thành công sau xác nhận của khách; mọi lần gọi được ghi nhật ký.<br>• **Quy tắc nghiệp vụ:**<br>• Chỉ cho gọi các công cụ nằm trong danh sách cho phép (whitelist) và chỉ trên dữ liệu của chính khách đang đăng nhập.<br>• Back-end không tin tham số do mô hình sinh ra mà luôn kiểm tra lại quyền và dữ liệu.<br>• Việc thanh toán cọc vẫn thực hiện trên trang của cổng thanh toán; chatbot chỉ gửi liên kết thanh toán.<br>• Nhật ký gồm người dùng, công cụ, tham số, kết quả và thời điểm. |

---

## 3. Sản phẩm bàn giao kỹ thuật, Tiêu chí nghiệm thu và Truy vết

### 3.1 Sản phẩm bàn giao kỹ thuật gắn với SRS

| STT | Sản phẩm bàn giao kỹ thuật | Vai trò phụ trách | Tiêu chí chấp nhận |
| --- | --- | --- | --- |
| 1 | Biên bản khảo sát nghiệp vụ & Bộ dữ liệu mẫu ẩn danh | PO/BA | Có biên bản khảo sát nhà hàng; tệp dữ liệu thực đơn, sơ đồ bàn, giờ mở cửa, chính sách, FAQ đã ẩn danh hoàn toàn PII. |
| 2 | Đặc tả SRS v1.1 & Product Backlog trên Jira (SCRUM) | PO/BA | Đủ 18 FR (FR-01..FR-18), 10 Epic, 54 User Story (45 MVP = 202 SP, 9 dự phòng = 50 SP) có tiêu chí chấp nhận rõ ràng. |
| 3 | Tài liệu thiết kế kiến trúc, ERD & Prototype Figma | Dev Fullstack, PO/BA | ERD ≥ 8 bảng (bao gồm bảng core và bảng AI), script Alembic migration sạch; đủ wireframe mobile & desktop được PO duyệt. |
| 4 | Tài liệu REST API (OpenAPI / Swagger) | Dev Fullstack, AI Dev | Đầy đủ endpoint cho toàn bộ chức năng MVP (FR-01..FR-14) và API AI (`/api/v1/chat/*`), có mô tả schema và mã lỗi. |
| 5 | Mã nguồn trên GitHub & Các bản phát hành | Dev Fullstack, AI Dev | Repo private có nhánh main/develop/feature; PR có review; CI xanh; gắn đủ tag v0.1, v0.2, v1.0-rc, v1.0. |
| 6 | Cấu hình Chatbot AI (Ollama) & Bộ ≥ 30 câu kiểm thử | AI Dev, PO/BA | Báo cáo chọn model Ollama (US-15); bộ ≥ 30 câu hỏi chuẩn & dẫn dụ; đạt tỷ lệ trả lời đúng ≥ 80%, phản hồi ≤ 5 giây. |
| 7 | Kế hoạch kiểm thử, ≥ 40 Test Case & Báo cáo UAT | PO/BA, PM/SM | ≥ 40 test case chức năng/API (Postman) chạy đạt; không còn Bug Nghiêm trọng/Cao; có phiếu xác nhận UAT của nhà hàng. |
| 8 | Bản triển khai Production, Hướng dẫn sử dụng & Video demo | Cả nhóm | Hệ thống chạy ổn định trên Cloud/VPS; đủ hướng dẫn cho Khách, Nhân viên, Quản lý & Chatbot; video demo 5–7 phút. |

### 3.2 Ma trận truy vết Yêu cầu chức năng (FR) – Epic – User Story

| Mã FR | Tên chức năng | Ưu tiên SRS | Epic | User Story liên quan | Mức phủ MVP |
| --- | --- | --- | --- | --- | --- |
| FR-01 | Xác thực và phân quyền | MVP – hỗ trợ | EP-01 | US-04, US-05, US-06, US-07 | Đủ (100% MVP) |
| FR-02 | Xem và tìm kiếm thực đơn | MVP (bắt buộc) | EP-02 | US-09, US-10 | Đủ (100% MVP) |
| FR-03 | Quản lý thực đơn | MVP (bắt buộc) | EP-02 | US-11, US-12 (Dự phòng: US-49) | Đủ lõi MVP |
| FR-04 | Quản lý sơ đồ bàn | MVP (bắt buộc) | EP-03 | US-13, US-14, US-23 | Đủ (100% MVP) |
| FR-05 | Đặt bàn theo khung giờ và số khách | MVP (bắt buộc) | EP-03 | US-17, US-18, US-19, US-20 | Đủ (100% MVP) |
| FR-06 | Đặt món trước | MVP (bắt buộc) | EP-04 | US-21, US-22 | Đủ (100% MVP) |
| FR-07 | Đặt cọc trực tuyến | MVP (bắt buộc) | EP-04 | US-20, US-24, US-25 | Đủ (100% MVP) |
| FR-08 | Quản lý đặt chỗ | MVP (bắt buộc) | EP-05 | US-31, US-32, US-33 (Dự phòng: US-50) | Đủ lõi MVP |
| FR-09 | Hủy đặt chỗ và hoàn cọc | MVP – hỗ trợ | EP-04 | US-20, US-26 (Dự phòng: US-48) | Đủ lõi MVP |
| FR-10 | Thông báo và nhắc lịch | MVP – hỗ trợ | EP-05 | US-27, US-38 | Đủ (100% MVP) |
| FR-11 | Tổng hợp món chuẩn bị cho bếp | MVP – hỗ trợ | EP-05 | US-37 | Đủ (100% MVP) |
| FR-12 | Báo cáo thống kê | MVP (bắt buộc) | EP-06 | US-36 (Dự phòng: US-47) | Đủ lõi MVP |
| FR-13 | Chatbot tư vấn món và giải đáp | MVP (bắt buộc) | EP-07 | US-15, US-29, US-30, US-34, US-40 | Đủ (100% MVP) |
| FR-14 | Chatbot hỗ trợ đặt bàn qua chat | MVP (bắt buộc) | EP-07 | US-35, US-40 | Đủ (100% MVP) |
| FR-15 | Quản trị tri thức & giám sát chatbot | MVP – hỗ trợ | EP-07 | US-46 (Backlog dự phòng ưu tiên #1) | Dự phòng |
| FR-16 | Đặt tiệc / sự kiện | Mở rộng | EP-08 | US-54 | Dự phòng |
| FR-17 | Đánh giá nhà hàng | Mở rộng | EP-08 | US-51 | Dự phòng |
| FR-18 | Chatbot thao tác qua API (tool calling) | Mở rộng | EP-08 | US-52, US-53 | Dự phòng |

### 3.3 Tiêu chí nghiệm thu tổng thể và Definition of Done (DoD)

#### Tiêu chí nghiệm thu tổng thể sản phẩm:

- 100% chức năng MVP bắt buộc và hỗ trợ (FR-01 đến FR-14) hoạt động đúng luồng sự kiện và quy tắc nghiệp vụ trên bản triển khai thật (Production v1.0).
- Kiểm thử đồng thời xác nhận 0% tình trạng trùng bàn trên cùng khung giờ; giao dịch đặt cọc và callback/webhook xử lý chính xác, không ghi nhận trùng.
- Chatbot AI chạy ổn định trên Ollama, trả lời đúng ≥ 80% trên bộ ≥ 30 câu hỏi kiểm thử, thời gian phản hồi ≤ 5 giây với 95% câu hỏi, không rò rỉ dữ liệu cá nhân (PII) và không bịa đặt thông tin món/giá.
- Không còn lỗi (Bug) mức Nghiêm trọng hoặc Cao đang mở tại thời điểm phát hành; đơn vị nhà hàng áp dụng ký xác nhận biên bản UAT (mức hài lòng ≥ 4/5).

#### Definition of Done (DoD) áp dụng cho từng chức năng / User Story:

- Mã nguồn đã được review qua Pull Request và merge sạch vào nhánh `develop`/`main`; tên nhánh và commit gắn đúng mã issue Jira (`SCRUM-xx`).
- Toàn bộ test case của chức năng đã chạy đạt trên môi trường Staging; không phát sinh lỗi mức Cao hoặc Nghiêm trọng mới.
- Tài liệu API (Swagger) và tài liệu hướng dẫn liên quan đã được cập nhật đồng bộ; tuân thủ phân quyền RBAC và quy tắc bảo mật.
- Được trình diễn (demo) tại buổi Sprint Review và được Product Owner (PO/BA) chấp nhận chuyển sang trạng thái `Done`.

### 3.4 Ký duyệt tài liệu (Sign-off)

| Vai trò | Họ và tên | Ngày duyệt | Chữ ký xác nhận |
| --- | --- | --- | --- |
| Người lập – Product Owner / Business Analyst (PO/BA) | [Võ Đăng Khoa] | 21/11/2026 | Khoa |
| Giám đốc dự án / Scrum Master (PM/SM) | [Trần Hoàng Phúc] | 21/11/2026 | Phúc |
| Đại diện kỹ thuật – Dev Fullstack & AI Dev | [Nguyễn Văn Tiến - Nguyễn Đoàn Trường Vũ] | 21/11/2026 | Tiến & Vũ |
| Nhà tài trợ dự án – Giảng viên hướng dẫn | [Nguyễn Hữu Trung (GVHD)] | 21/11/2026 | |

**Chú thích (Comments):** (Nhận xét viết tay hoặc đánh máy của Nhà tài trợ, Đại diện đơn vị nhà hàng hoặc các bên liên quan, nếu có.)
