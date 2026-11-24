# PHÁT BIỂU BÀI TOÁN (PROBLEM STATEMENT)

**Học phần:** Quản lý dự án Công nghệ thông tin • **Mã đề tài:** QL09-W

| Hạng mục | Nội dung |
| --- | --- |
| Tên dự án | Website đặt bàn và đặt món trước cho nhà hàng tích hợp chatbot AI (Restaurant Table Reservation and Pre-order Website with AI Chatbot) |
| Đơn vị áp dụng | Nhà hàng Ẩm thực Vườn Phố – 1 cơ sở tại TP. Hồ Chí Minh; tiền tệ VNĐ; múi giờ GMT+7 |
| Thời gian | 16/11/2026 – 10/01/2027 (8 Sprint × 1 tuần); bàn giao v1.0 ngày 08/01/2027 |
| Ngân sách | 69.987.500 VNĐ (đã gồm 10% dự phòng rủi ro) |
| Nhóm thực hiện | Trần Hoàng Phúc (PM/SM); Võ Đăng Khoa (PO/BA); Nguyễn Văn Tiến (Dev Fullstack); Nguyễn Đoàn Trường Vũ (AI Dev) |
| Nhà tài trợ | Nguyễn Hữu Trung (GVHD) – Khoa CNTT, HUTECH |

---

## 1. Bối cảnh

Nhà hàng Ẩm thực Vườn Phố là nhà hàng phục vụ tại bàn, thường xuyên tiếp nhận khách đặt chỗ trước. Khách có nhu cầu chọn đúng khung giờ, số người, đặt sẵn món và đặt cọc để chắc chắn có bàn; ngược lại nhà hàng cần biết trước lượng khách và món ăn để sắp xếp sơ đồ bàn và chuẩn bị nguyên liệu bếp.

Hiện nay toàn bộ quy trình này được thực hiện thủ công qua điện thoại, tin nhắn mạng xã hội và sổ ghi chép/bảng tính riêng lẻ, phụ thuộc hoàn toàn vào nhân viên trực.

## 2. Hiện trạng và vấn đề tồn tại

Theo số liệu khảo sát sơ bộ (sẽ được chuẩn hóa bằng biên bản khảo sát thực tế ở Sprint 0 – Sprint 1), nhà hàng có khoảng 30 – 50 lượt đặt bàn mỗi ngày và gặp các vấn đề sau:

| Vấn đề | Biểu hiện | Hệ quả |
| --- | --- | --- |
| Chỉ nhận đặt bàn trong giờ làm việc | Ngoài giờ không có người trực; khách nhắn tin không được trả lời | Mất khách, mất doanh thu ngoài giờ |
| Ghi chép thủ công dễ sai | Ghi nhầm hoặc trùng bàn, trùng khung giờ | Xung đột khi khách đến, ảnh hưởng uy tín |
| Khách đặt nhưng không đến (no-show) | 10 – 15% đơn bị hủy hoặc thất thoát; không có đặt cọc, không nhắc lịch | Bàn trống không bán được, bếp chuẩn bị thừa |
| Phản hồi tin nhắn chậm | Khách chờ trung bình 15 – 30 phút | Khách bỏ sang nhà hàng khác |
| Câu hỏi lặp lại | Khoảng 60% tin nhắn hỏi về thực đơn, giá, giờ mở cửa, chính sách cọc/hủy | Nhân viên mất thời gian cho việc lặp lại |
| Thông tin thực đơn thay đổi | Món hết hoặc đổi giá sau khi khách đã đặt trước | Sai lệch thông tin, khiếu nại |

## 3. Phát biểu bài toán

Làm thế nào để nhà hàng nhận đặt bàn và đặt món trước 24/7, loại bỏ tình trạng trùng bàn, giảm rõ rệt tỷ lệ khách không đến, và trả lời tức thì các câu hỏi lặp lại của khách – mà không làm tăng khối lượng công việc của nhân viên và vẫn bảo vệ dữ liệu cá nhân của khách hàng?

Bài toán đòi hỏi một hệ thống tập trung, thay thế cách ghi chép rời rạc hiện nay, đáp ứng đồng thời các yêu cầu sau:

- **Đặt bàn chính xác:** khách chọn khung giờ (bước 30 phút, lượt phục vụ 90 phút) và số khách; hệ thống giữ chỗ tạm thời 10 phút và chặn trùng bàn ngay ở tầng cơ sở dữ liệu, kể cả khi nhiều người đặt cùng lúc.
- **Ràng buộc cam kết của khách:** đặt món trước với giá chốt, đặt cọc trực tuyến, nhắc lịch tự động trước 24 giờ và 2 giờ, hủy và hoàn cọc theo chính sách.
- **Hỗ trợ vận hành:** nhân viên check-in, đổi bàn/giờ, đánh dấu không đến; bếp nhận danh sách món cần chuẩn bị; quản lý xem báo cáo số đơn, tỷ lệ hủy/no-show, doanh thu cọc.
- **Trợ lý hội thoại AI:** chatbot dùng mô hình mở chạy trên Ollama, trả lời dựa trên dữ liệu thực của nhà hàng (RAG), tư vấn món, giải đáp chính sách và dẫn dắt đặt bàn qua chat; có Guardrails chống bịa thông tin và che dữ liệu cá nhân (PII) trước khi gửi lên mô hình.

## 4. Đối tượng liên quan

| Đối tượng | Nhu cầu / Quyền lợi |
| --- | --- |
| Khách vãng lai | Xem và tìm kiếm thực đơn, hỏi chatbot, đăng ký tài khoản. |
| Khách hàng | Đặt bàn, đặt món trước, đặt cọc, xem/hủy đặt chỗ, đặt bàn qua chatbot. |
| Nhân viên | Xem sơ đồ bàn theo giờ, xử lý đơn đặt chỗ, cập nhật món còn/hết, xem danh sách món cho bếp. |
| Quản lý | Quản lý thực đơn, sơ đồ bàn, tham số nghiệp vụ, tài khoản, báo cáo; quản trị tri thức và giám sát chatbot. |
| Hệ thống ngoài | Cổng thanh toán Sandbox, máy chủ Ollama, dịch vụ Email/SMS. |

## 5. Giải pháp đề xuất

Xây dựng ứng dụng web responsive theo kiến trúc Client–Server: front-end ReactJS, back-end Python FastAPI (REST API, tài liệu Swagger), cơ sở dữ liệu PostgreSQL (Alembic migration), chatbot AI trên Ollama, cổng thanh toán Sandbox (VNPay/MoMo/PayOS), dịch vụ Email/SMS; đóng gói Docker, triển khai trên Cloud/VPS, kiểm thử và build tự động bằng GitHub Actions. Dự án thực hiện theo Scrum với 8 Sprint, quản lý bằng Jira (khóa SCRUM), GitHub và Microsoft Project.

## 6. Phạm vi

### Trong phạm vi (MVP, 45 user story – 202 Story Points):

- Xác thực và phân quyền 3 vai trò: Khách hàng, Nhân viên, Quản lý (FR-01).
- Xem, tìm kiếm, lọc và quản lý thực đơn, tình trạng món, lịch sử đổi giá (FR-02, FR-03).
- Quản lý khu vực, sơ đồ bàn kéo thả và trạng thái bàn theo ngày/giờ (FR-04).
- Đặt bàn theo khung giờ, giữ chỗ 10 phút, chống trùng bàn (FR-05).
- Đặt món trước, đặt cọc trực tuyến, hủy và hoàn cọc (FR-06, FR-07, FR-09).
- Quản lý đặt chỗ, thông báo và nhắc lịch, tổng hợp món cho bếp (FR-08, FR-10, FR-11).
- Báo cáo thống kê (FR-12).
- Chatbot AI tư vấn món, giải đáp chính sách, đặt bàn qua hội thoại, quản trị tri thức (FR-13, FR-14, FR-15).
- Mở rộng (Backlog dự phòng 50 SP, chỉ làm nếu velocity vượt kế hoạch trước khi đóng băng tính năng hết Sprint 6): đặt tiệc/sự kiện (FR-16), đánh giá nhà hàng (FR-17), chatbot tool calling có xác nhận (FR-18).

### Ngoài phạm vi:

- Thanh toán toàn bộ hóa đơn tại bàn (POS) và xuất hóa đơn VAT.
- Quản lý kho, nguyên liệu, nhân sự, chấm công.
- Giao hàng tận nơi và mang đi.
- Ứng dụng di động cài đặt riêng (chỉ làm website responsive).
- Huấn luyện hoặc tinh chỉnh mô hình AI; chatbot tự ý hoàn tiền, đổi đơn, cấp mã giảm giá.

## 7. Mục tiêu và chỉ tiêu đo lường

| Mục tiêu | Chỉ tiêu | Cách kiểm chứng |
| --- | --- | --- |
| Nhận đặt bàn 24/7 | Ghi nhận rõ số đơn đặt ngoài giờ làm việc | Báo cáo FR-12 |
| Không trùng bàn | 0% đơn trùng bàn; xử lý đúng 100% yêu cầu đặt cùng bàn đồng thời | Concurrent test, UAT |
| Giảm no-show | Giảm rõ rệt tỷ lệ không đến nhờ đặt cọc và nhắc lịch 24h/2h | Báo cáo FR-12 |
| Chatbot hiệu quả | Đúng ≥ 80% trên bộ ≥ 30 câu kiểm thử; phản hồi ≤ 5 giây với 95% câu hỏi | Bộ test chatbot, log phản hồi |
| Giá chốt chính xác | 100% đơn đặt trước lưu giá chốt tại thời điểm xác nhận | Test nghiệp vụ FR-03, FR-06 |
| Hiệu năng | Tải trang ≤ 3 giây (4G); chịu 50 người dùng đồng thời | Kiểm thử tải |
| Tiến độ – chi phí | Bàn giao 08/01/2027; SPI ≥ 0,9; CPI ≥ 0,9; trong ngân sách | MS Project, Earned Value |
| Chất lượng | 100% user story đạt Definition of Done; không còn lỗi Cao/Nghiêm trọng; ≥ 40 test case | Jira, báo cáo kiểm thử, UAT |

## 8. Ràng buộc, giả định và phụ thuộc

- **Ràng buộc:** bộ công nghệ chuẩn hóa (ReactJS, FastAPI, PostgreSQL, Ollama); chatbot dùng mô hình mở có sẵn, tuyệt đối không gửi PII lên dịch vụ AI; không lưu số thẻ thanh toán; HTTPS, mật khẩu băm; thay đổi phạm vi sau mốc Baseline (M2) phải qua CR và Hội đồng kiểm soát thay đổi (CCB); thời gian 8 tuần, nhóm 4 người, mỗi người khoảng 20 giờ công/Sprint.
- **Giả định:** nhà hàng vận hành một cơ sở; giao diện tiếng Việt, tiền VNĐ, múi giờ GMT+7; các tham số nghiệp vụ (lượt ăn 90 phút, bước 30 phút, giữ chỗ 10 phút, cọc 30%, mốc hoàn cọc và nhắc lịch 24h/2h) là giá trị mặc định do Quản lý cấu hình và nhà hàng xác nhận.
- **Phụ thuộc:** nhà hàng cung cấp đúng hạn dữ liệu thực đơn (≥ 30 – 50 món), sơ đồ bàn, giờ mở cửa, chính sách cọc/hủy đã ẩn danh; cử đại diện dự Sprint Review và UAT; môi trường cổng thanh toán Sandbox, VPS, Ollama, Email/SMS sẵn sàng trong suốt dự án.

## 9. Rủi ro chính và hướng xử lý

| Rủi ro | Biện pháp kiểm soát |
| --- | --- |
| Khách không đến | Bắt buộc đặt cọc, nhắc lịch 24h/2h, hoàn cọc theo mốc thời gian, theo dõi tỷ lệ no-show. |
| Trùng bàn | Kiểm tra và giữ chỗ trong một transaction kèm ràng buộc ở cơ sở dữ liệu; chặn đổi bàn trùng. |
| Thực đơn đổi sau khi đặt | Lưu giá chốt; cảnh báo nhân viên các đơn bị ảnh hưởng khi món hết hoặc ngừng bán. |
| Chatbot bịa tin hoặc lộ PII | RAG chỉ dựa trên dữ liệu đã duyệt; che PII; từ chối câu hỏi ngoài phạm vi/y tế; kiểm tra phía server; ghi log giám sát. |
| Ollama quá tải hoặc gián đoạn | Chọn mô hình gọn nhẹ ở Sprint 2; timeout và fallback điều hướng sang thực đơn và form đặt bàn. |

## 10. Lợi ích kỳ vọng

- Khách đặt bàn, đặt món và đặt cọc bất cứ lúc nào, được chatbot trả lời trong vài giây.
- Nhà hàng không còn trùng bàn, giảm thất thoát do no-show, chuẩn bị bếp chính xác nhờ danh sách món đặt trước.
- Nhân viên giảm thời gian trả lời tin nhắn lặp lại và ghi chép thủ công.
- Quản lý có số liệu báo cáo để theo dõi công suất bàn và doanh thu cọc.
