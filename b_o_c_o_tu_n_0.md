# Báo cáo Tuần 0: Thử nghiệm model AI với Ollama

* **Đồ án:** Website đặt bàn và đặt món trước cho nhà hàng tích hợp chatbot AI
* **Phần phụ trách:** AI Chat Box

## 1. Môi trường thử nghiệm

| Hạng mục | Thông tin |
| :--- | :--- |
| Hệ điều hành | Windows |
| Phần mềm | Ollama phiên bản 0.40.16 |
| Chế độ chạy | Local (không đăng nhập tài khoản Ollama) |
| Cấu hình máy (RAM/GPU) | 16g RAM/ Intel(R) Graphics (128 MB) |
| CPU hay GPU (`ollama ps`) | 100% CPU (ghi nhận khi chạy `gemma3:4b`, context 4096) |

## 2. Các bước đã thực hiện

1. Cài Ollama trên Windows, chọn `"No thanks, I'll use Ollama locally"` ở màn hình tạo tài khoản.
2. Kiểm tra cài đặt bằng lệnh `ollama`; Ollama hiển thị menu tương tác, cài đặt thành công.
3. Tải 3 model bằng lệnh `ollama pull`: `qwen2.5:7b`, `llama3.1:8b`, `gemma3:4b`.
4. Chạy từng model với lệnh `ollama run <model> --verbose`, cùng một câu hỏi, để lấy thông số tốc độ.

## 3. Câu hỏi test

> "Xin chào, bạn có thể tư vấn món ăn cho mình không?"

**Lệnh sử dụng:**
```bash
ollama pull <model>
ollama run <model> --verbose
ollama ps
```

## 4. Kết quả từng model

### 4.1. qwen2.5:7b

**Câu trả lời:**
> Chào bạn!当然可以，我很乐意为您推荐一道美食。不过，您偏好哪种类型的菜系呢？比如中式、西式、还是其他类型的菜肴？另外，您有什么饮食限制或者偏好吗？比如素食、重口味或者清淡口味等。这样我可以更准确地为您推荐。

| Chỉ số | Giá trị | Ý nghĩa |
| :--- | :--- | :--- |
| total duration | 7.687 s | Tổng thời gian xử lý |
| load duration | 26.2 ms | Thời gian nạp model |
| prompt eval count | 44 token | Số token câu hỏi |
| prompt eval duration | 1.136 s | Thời gian đọc câu hỏi |
| prompt eval rate | 38.73 token/s | Tốc độ đọc câu hỏi |
| eval count | 64 token | Số token câu trả lời |
| eval duration | 6.375 s | Thời gian sinh câu trả lời |
| eval rate | 10.04 token/s | Tốc độ trả lời (chỉ số chính) |

**Nhận xét:** Mở đầu bằng tiếng Việt rồi chuyển sang tiếng Trung. Lỗi nghiêm trọng với chatbot cho khách Việt.

### 4.2. llama3.1:8b

**Câu trả lời:**
> Xin chào! Tôi có thể giúp bạn tìm kiếm các gợi ý món ăn. Bạn có thể cho tôi biết loại thực phẩm hoặc loại món ăn bạn muốn tìm không? Ví dụ: món ăn nhanh, món ăn truyền thống của Việt Nam, món ăn đặc trưng của một vùng, hoặc món ăn dễ làm, v.v.

| Chỉ số | Giá trị | Ý nghĩa |
| :--- | :--- | :--- |
| total duration | 8.222 s | Tổng thời gian xử lý |
| load duration | 19.3 ms | Thời gian nạp model |
| prompt eval count | 26 token | Số token câu hỏi |
| prompt eval duration | 738.9 ms | Thời gian đọc câu hỏi |
| prompt eval rate | 35.19 token/s | Tốc độ đọc câu hỏi |
| eval count | 70 token | Số token câu trả lời |
| eval duration | 7.443 s | Thời gian sinh câu trả lời |
| eval rate | 9.40 token/s | Tốc độ trả lời (chỉ số chính) |

**Nhận xét:** Trả lời hoàn toàn bằng tiếng Việt, đúng ý, hỏi lại hợp lý. Câu chữ hơi máy móc (lặp "loại thực phẩm hoặc loại món ăn"), xưng "Tôi" thay vì giọng nhân viên nhà hàng (chỉnh được bằng system prompt). Chậm nhất trong 3 model.

### 4.3. gemma3:4b

**Câu trả lời (rút gọn danh sách câu hỏi):**
> Chào bạn! Để tôi có thể tư vấn món ăn phù hợp nhất cho bạn, tôi cần biết thêm một chút thông tin. Bạn muốn ăn gì? Hãy trả lời những câu hỏi sau nhé:
> - Bạn đang thèm gì? (đồ ngọt, đồ mặn, món cay, món mát, món nóng...)
> - Bạn muốn ăn món nào? (cơm, bún, phở, mì, món nướng, salad...)
> - Bạn thích hương vị nào? (Việt Nam, Á Đông, Á Tây, Hàn Quốc, Nhật Bản...)
> - Bạn có yêu cầu đặc biệt nào không? (ăn chay, ăn kiêng, dị ứng...)
> - Bạn muốn ăn món nào cho bữa ăn nào? (sáng, trưa, tối, ăn vặt...)
> - Bạn muốn món ăn đó dễ làm không? (tự nấu, mua ngoài, giao tận nơi...)
> 
> Sau khi bạn trả lời, tôi sẽ đưa ra một vài gợi ý món ăn phù hợp với bạn đấy! 😊

| Chỉ số | Giá trị | Ý nghĩa |
| :--- | :--- | :--- |
| total duration | 15.890 s | Tổng thời gian xử lý |
| load duration | 20.2 ms | Thời gian nạp model |
| prompt eval count | 24 token | Số token câu hỏi |
| prompt eval duration | 423.7 ms | Thời gian đọc câu hỏi |
| prompt eval rate | 56.65 token/s | Tốc độ đọc câu hỏi |
| eval count | 259 token | Số token câu trả lời |
| eval duration | 15.430 s | Thời gian sinh câu trả lời |
| eval rate | 16.79 token/s | Tốc độ trả lời (chỉ số chính) |

**Nhận xét:** Tiếng Việt đúng ngôn ngữ, trình bày rõ ràng, có emoji thân thiện, tốc độ cao nhất. Tuy nhiên trả lời quá dài (259 token) và hỏi một lúc 6 câu, không phù hợp chat đặt bàn cần ngắn gọn. Có vài chỗ lạ ("Á Tây", "bữa ăn nào cho bữa ăn nào"). Cần system prompt giới hạn độ dài và chỉ hỏi 1 câu mỗi lượt. Dùng ít bộ nhớ nhất (2.9 GB).

## 5. Bảng so sánh

| Model | Tốc độ (token/s) | Tổng thời gian | Ngôn ngữ trả lời | Nhận xét |
| :--- | :--- | :--- | :--- | :--- |
| `qwen2.5:7b` | 10.04 | 7.7 s | Lẫn tiếng Trung | Lỗi ngôn ngữ, loại nếu không khắc phục được |
| `llama3.1:8b` | 9.40 | 8.2 s | Tiếng Việt | Đúng ý, ngắn gọn, hơi máy móc, chậm nhất |
| `gemma3:4b` | 16.79 | 15.9 s | Tiếng Việt | Nhanh nhất, nhẹ nhất (2.9 GB), nhưng trả lời dài dòng |

*Lưu ý:* Mỗi model mới test một câu hỏi duy nhất nên kết luận chỉ mang tính sơ bộ. Tổng thời gian của `gemma3:4b` cao hơn vì câu trả lời dài hơn nhiều, không phải do model chậm.

## 6. Ưu điểm và nhược điểm của từng model trong đồ án

Chatbot của đồ án cần: trả lời tiếng Việt tự nhiên, trả lời ngắn gọn, thu thập thông tin đặt bàn (ngày, giờ, số người, tên, SĐT), gọi được chức năng của hệ thống (tool calling) và chạy đủ nhanh trên máy cấu hình thường. Các đánh giá dưới đây dựa trên kết quả test thực tế ở trên, kèm thông tin chung về model.

### 6.1. qwen2.5:7b

| Ưu điểm | Nhược điểm |
| :--- | :--- |
| - Hỗ trợ tool calling tốt, phù hợp để gọi chức năng kiểm tra bàn, tạo đặt bàn.<br>- Có hỗ trợ nhiều ngôn ngữ trong đó có tiếng Việt, và thường mạnh về trích xuất thông tin có cấu trúc (JSON).<br>- Giấy phép Apache 2.0 (rất thoáng, dùng thương mại được) *[nên kiểm tra lại trên trang model]*.<br>- Tốc độ 10.04 token/s, nhỉnh hơn `llama3.1:8b`. | - Trong test thực tế, trả lời lẫn tiếng Trung. Với khách Việt đây là lỗi nghiêm trọng.<br>- Nặng (4.7 GB), chạy CPU khá chậm.<br>- Cần system prompt chặt để ép tiếng Việt, và vẫn có rủi ro lẫn ngôn ngữ ở một số câu.<br>- Văn phong tiếng Việt chưa chắc tự nhiên bằng `gemma3`. |

### 6.2. llama3.1:8b

| Ưu điểm | Nhược điểm |
| :--- | :--- |
| - Trong test, trả lời hoàn toàn bằng tiếng Việt, đúng ý, ngắn gọn.<br>- Hỗ trợ tool calling, phù hợp kiến trúc chatbot có gọi hàm.<br>- Cộng đồng lớn, nhiều tài liệu và ví dụ, dễ tìm cách xử lý khi gặp lỗi.<br>- Câu trả lời gọn nên tiết kiệm thời gian chờ của khách. | - Tiếng Việt không nằm trong danh sách hỗ trợ chính thức, chất lượng có thể không ổn định ở câu dài hoặc phức tạp.<br>- Văn phong máy móc, lặp từ, xưng "Tôi" (cần chỉnh bằng system prompt).<br>- Chậm nhất trong 3 model (9.40 token/s) và nặng (khoảng 4.9 GB).<br>- Giấy phép Llama Community License có một số điều khoản riêng, không phải mã nguồn mở theo nghĩa chuẩn. |

### 6.3. gemma3:4b

| Ưu điểm | Nhược điểm |
| :--- | :--- |
| - Nhanh nhất trên CPU (16.79 token/s), phù hợp vì máy chạy 100% CPU.<br>- Nhẹ nhất (2.9 GB trong RAM), chạy được trên máy yếu hơn và nhiều người dùng cùng lúc dễ hơn.<br>- Tiếng Việt đúng ngôn ngữ, trình bày rõ, giọng thân thiện (có emoji).<br>- Google xây dựng hỗ trợ đa ngôn ngữ rộng nên tiềm năng tiếng Việt tốt. | - Trả lời dài dòng, hỏi nhiều câu cùng lúc (6 câu), không hợp chat đặt bàn; cần system prompt giới hạn độ dài.<br>- Có chỗ dùng từ lạ ("Á Tây", "bữa ăn nào cho bữa ăn nào").<br>- Model 4B nhỏ nên dễ bịa món hoặc nhầm khi ngữ cảnh dài; bắt buộc phải có dữ liệu menu thật (RAG).<br>- Tool calling có thể chưa được hỗ trợ chính thức trong Ollama, cần kiểm tra trên `ollama.com/library`; nếu không có thì phải để backend điều khiển luồng đặt bàn thay vì để model tự gọi hàm. |

### 6.4. Tổng hợp

| Tiêu chí | qwen2.5:7b | llama3.1:8b | gemma3:4b |
| :--- | :--- | :--- | :--- |
| Tiếng Việt (test thực tế) | Kém (lẫn tiếng Trung) | Tốt, hơi máy móc | Tốt, tự nhiên hơn |
| Tốc độ trên CPU | Trung bình | Chậm nhất | Nhanh nhất |
| Độ nặng | 4.7 GB | Khoảng 4.9 GB | 2.9 GB |
| Độ gọn của câu trả lời | Ngắn | Ngắn | Dài |
| Tool calling | Hỗ trợ | Hỗ trợ | Cần kiểm tra |
| Phù hợp đồ án | Thấp | Khá | Khá, cần chỉnh prompt |

*Lưu ý:* Các mục về tool calling, giấy phép và dung lượng là thông tin chung về model, cần xác nhận lại trên `ollama.com/library` trước khi chốt. Các mục về tiếng Việt và tốc độ là kết quả test thực tế trên máy của nhóm (một câu hỏi mỗi model).

## 7. Lựa chọn model cho đồ án

* **Model được chọn:** `gemma3:4b` (lựa chọn tạm thời, tiếp tục kiểm chứng ở các bước sau).
* **Phương án dự phòng:** `llama3.1:8b`.

### 7.1. Lý do chọn gemma3:4b
* **Tốc độ cao nhất:** 16.79 token/s, gần gấp đôi `llama3.1:8b` (9.40) và cao hơn nhiều so với `qwen2.5:7b` (10.04). Máy thử nghiệm chạy 100% CPU nên model nhỏ có lợi thế rõ, giúp khách không phải chờ lâu.
* **Nhẹ nhất:** Chỉ dùng 2.9 GB, dễ chạy trên máy nhóm khi demo và dễ phục vụ nhiều người dùng hơn.
* Trả lời đúng ngôn ngữ, văn phong tiếng Việt thân thiện, trình bày rõ ràng.
* Nhược điểm chính (trả lời dài, hỏi nhiều câu cùng lúc) có thể khắc phục bằng system prompt: giới hạn độ dài, mỗi lượt chỉ hỏi một thông tin.

### 7.2. Lý do không chọn qwen2.5:7b
* Trả lời lẫn tiếng Trung khi khách hỏi tiếng Việt. Với chatbot phục vụ khách Việt, đây là lỗi nghiêm trọng và khó đảm bảo khắc phục hoàn toàn.
* Nặng hơn (4.7 GB) và chậm hơn `gemma3:4b` khi chạy trên CPU.
* Chỉ cân nhắc lại nếu system prompt ép được tiếng Việt ổn định trong nhiều lần test.

### 7.3. Lý do không chọn llama3.1:8b (giữ làm dự phòng)
* Chậm nhất trong 3 model (9.40 token/s) và nặng hơn (khoảng 4.9 GB), trong khi chất lượng tiếng Việt không vượt trội `gemma3:4b`.
* Tiếng Việt không nằm trong danh sách ngôn ngữ hỗ trợ chính thức; văn phong máy móc, lặp từ.
* Ưu điểm vẫn đáng giá: trả lời ngắn gọn và hỗ trợ tool calling. Vì vậy giữ làm phương án dự phòng, đặc biệt nếu `gemma3:4b` không đáp ứng được phần gọi hàm.

### 7.4. Rủi ro và điều kiện đổi lựa chọn
* **Tool calling:** Cần kiểm tra `gemma3:4b` có được hỗ trợ trong Ollama không (`ollama.com/library`). Nếu không, backend sẽ điều khiển luồng đặt bàn, model chỉ trích xuất thông tin thành JSON và viết câu trả lời tự nhiên.
* Model 4B nhỏ dễ bịa món hoặc nhầm khi ngữ cảnh dài, nên bắt buộc dùng dữ liệu menu thật (RAG) và kiểm tra giá, tình trạng bàn qua hệ thống, không để model tự nhớ.
* Kết luận mới dựa trên một câu hỏi mỗi model. Nếu test thêm (đặt bàn thiếu thông tin, trích xuất tên/SĐT/giờ, câu ngoài phạm vi) cho thấy `llama3.1:8b` vượt trội rõ rệt về trích xuất thông tin, sẽ đổi sang `llama3.1:8b`.