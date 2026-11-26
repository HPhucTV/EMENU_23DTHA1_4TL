# Chat API JSON Contract và kịch bản hội thoại

## 1. Phạm vi và nguyên tắc

* Frontend không gọi Ollama trực tiếp. Frontend chỉ gọi backend theo contract này. Nhờ đó đổi model hoặc đổi sang API đám mây không ảnh hưởng frontend.
* Bản v0.1 chỉ có 1 endpoint: `POST /api/v1/chat`. Các tính năng khác (stream, lịch sử) thêm ở các phiên bản sau.
* **Quy ước:** Thêm trường mới thì không phá contract; đổi tên hoặc xóa trường phải báo cả nhóm và lên phiên bản mới.
* **Model AI dự kiến:** `gemma3:4b` (dự phòng `llama3.1:8b`). Model chỉ hiểu câu khách, trích xuất thông tin và viết câu trả lời. Dữ liệu thật (menu, giá, bàn trống) lấy từ hệ thống.

## 2. Phân chia trách nhiệm

| Bên | Phụ trách |
| :--- | :--- |
| **AI (bạn)** | Hiểu ý khách (`intent`), trích xuất thông tin đặt bàn (`slots`), hỏi bổ sung thông tin còn thiếu, viết câu trả lời tiếng Việt, đề xuất hành động (`actions`). |
| **Backend** | Tạo và quản lý `session_id`, lưu lịch sử hội thoại, cung cấp dữ liệu menu cho AI, kiểm tra bàn trống, ghi đặt bàn vào database, gọi AI service. |
| **Frontend** | Giao diện chat, hiển thị `reply`, nút bấm nhanh, thẻ món ăn; gửi tin nhắn và hiển thị lỗi theo contract. |

> **Điểm quan trọng:** AI không tự ghi database. AI chỉ trả về `actions` (ví dụ "tạo đặt bàn với thông tin này"), backend mới thực hiện và kiểm tra trùng bàn.

## 3. Endpoint: `POST /api/v1/chat`

### 3.1. Request

```json
{
  "session_id": null,
  "message": "Đặt bàn 4 người tối mai lúc 7 giờ",
  "locale": "vi-VN",
  "client_context": {
    "channel": "web",
    "timezone": "Asia/Ho_Chi_Minh"
  }
}
```

| Trường | Kiểu | Bắt buộc | Mô tả |
| :--- | :--- | :--- | :--- |
| `session_id` | `string \| null` | Có | `null` ở tin đầu tiên; backend tạo và trả về, các tin sau gửi lại đúng giá trị này |
| `message` | `string` | Có | Tin nhắn của khách, tối đa 1000 ký tự |
| `locale` | `string` | Không | Mặc định `vi-VN` |
| `client_context.channel` | `string` | Không | `web` hoặc `mobile` |
| `client_context.timezone` | `string` | Có | Cần để quy "tối mai", "thứ Sáu" ra ngày cụ thể |

### 3.2. Response thành công (HTTP 200)

```json
{
  "session_id": "b7c1e2f0-3a4d-4f6e-9a10-123456789abc",
  "reply": "Dạ, em ghi nhận bàn 4 người lúc 19:00 ngày 23/11/2026. Anh/chị cho em xin tên ạ?",
  "intent": "reservation",
  "state": "collecting_info",
  "slots": {
    "date": "2026-11-23", "time": "19:00", "guests": 4,
    "name": null, "phone": null, "note": null
  },
  "missing_slots": ["name", "phone"],
  "ui_hints": { "quick_replies": [], "cards": [] },
  "actions": [],
  "handoff_to_human": false,
  "meta": { "model": "gemma3:4b", "latency_ms": 3200 }
}
```

| Trường | Kiểu | Mô tả |
| :--- | :--- | :--- |
| `session_id` | `string` | Mã phiên hội thoại |
| `reply` | `string` | Câu trả lời hiển thị cho khách |
| `intent` | `string` | Ý định của khách (xem 3.3) |
| `state` | `string` | Trạng thái luồng (xem 3.4) |
| `slots` | `object` | Thông tin đặt bàn đã thu thập; trường chưa có là `null`. Ngày `YYYY-MM-DD`, giờ `HH:mm` (24h) |
| `missing_slots` | `string[]` | Các thông tin còn thiếu |
| `ui_hints` | `object` | Gợi ý giao diện: `quick_replies` (nút bấm nhanh), `cards` (thẻ món ăn) |
| `actions` | `object[]` | Hành động AI đề xuất hoặc đã thực hiện (xem 3.5) |
| `handoff_to_human` | `boolean` | `true` khi cần chuyển cho nhân viên thật |
| `meta` | `object` | Thông tin kỹ thuật: `model`, `latency_ms` (dùng để debug) |

### 3.3. Danh sách `intent`

| `intent` | Ý nghĩa |
| :--- | :--- |
| `menu_advice` | Hỏi tư vấn, tìm món |
| `reservation` | Đặt bàn mới |
| `pre_order` | Đặt món trước |
| `modify_cancel` | Đổi hoặc hủy đặt bàn |
| `faq` | Hỏi thông tin nhà hàng (giờ mở cửa, địa chỉ, chính sách) |
| `handoff` | Khách muốn gặp nhân viên hoặc phàn nàn |
| `out_of_scope` | Câu hỏi ngoài phạm vi nhà hàng |

### 3.4. Danh sách `state`

| `state` | Ý nghĩa |
| :--- | :--- |
| `idle` | Chưa có luồng nào đang chạy (hỏi đáp thông thường) |
| `collecting_info` | Đang thu thập thông tin còn thiếu |
| `awaiting_confirmation` | Đã đủ thông tin, chờ khách xác nhận |
| `confirmed` | Khách đã xác nhận, hành động đã được thực hiện thành công |
| `failed` | Thực hiện thất bại (ví dụ hết bàn), cần đề xuất phương án khác |

### 3.5. Actions

Mỗi action có `type`, `status` và `payload`. 
* Đề xuất `type` ban đầu: `create_reservation`, `modify_reservation`, `cancel_reservation`. 
* `status` gồm: `proposed` (AI đề xuất), `success`, `failed`.

### 3.6. Lỗi

```json
{
  "error": {
    "code": "MODEL_TIMEOUT",
    "message": "AI phản hồi quá lâu, vui lòng thử lại.",
    "retryable": true
  }
}
```

| `code` | HTTP | Ý nghĩa |
| :--- | :--- | :--- |
| `INVALID_REQUEST` | 400 | Dữ liệu gửi lên sai định dạng hoặc thiếu trường bắt buộc |
| `SESSION_NOT_FOUND` | 404 | `session_id` không tồn tại hoặc đã hết hạn |
| `RATE_LIMITED` | 429 | Gửi quá nhiều tin trong thời gian ngắn |
| `MODEL_UNAVAILABLE` | 503 | AI tạm thời không hoạt động |
| `MODEL_TIMEOUT` | 504 | AI phản hồi quá lâu |
| `INTERNAL_ERROR` | 500 | Lỗi không xác định |

## 4. Kịch bản hội thoại

### 4.1. Quy tắc giọng điệu của chatbot
* Xưng "em", gọi khách là "anh/chị"; lịch sự, thân thiện.
* Chỉ dùng tiếng Việt.
* Trả lời ngắn, tối đa 2 đến 3 câu.
* Mỗi lượt chỉ hỏi 1 thông tin còn thiếu.
* Chỉ tư vấn món có trong menu; không bịa món, giá hay tình trạng bàn.
* Trước khi chốt đặt bàn phải tóm tắt lại và chờ khách xác nhận.
* Câu hỏi ngoài phạm vi: từ chối khéo và đưa khách về chủ đề nhà hàng.

### 4.2. Thông tin đặt bàn cần thu thập

| Slot | Bắt buộc | Ghi chú |
| :--- | :--- | :--- |
| `date` | Có | Quy từ cách nói như "tối mai", "thứ Sáu" theo timezone |
| `time` | Có | Hiểu cách nói như "7 giờ tối", "tầm 7 rưỡi", "19h" |
| `guests` | Có | Số người |
| `name` | Có | Tên khách |
| `phone` | Có | Số điện thoại, backend kiểm tra định dạng |
| `note` | Không | Yêu cầu đặc biệt: ghế trẻ em, sinh nhật, khu ngoài trời... |

### 4.3. Các kịch bản mẫu

| # | Tình huống | Khách nói | Chatbot trả lời (tóm tắt) |
| :--- | :--- | :--- | :--- |
| 1 | Tư vấn món | "Có món nào không cay cho bé 5 tuổi không?" | Gợi ý 2 đến 3 món không cay trong menu, kèm thẻ món. `intent: menu_advice` |
| 2 | Đặt bàn thiếu thông tin | "Đặt bàn 4 người tối mai 7 giờ" | Ghi nhận ngày, giờ, số người; hỏi xin tên. `intent: reservation`, `state: collecting_info` |
| 3 | Đặt bàn đủ thông tin | "Mình tên Lan, 0901234567, bàn 6 người 19h thứ Sáu" | Tóm tắt lại thông tin và hỏi xác nhận. `state: awaiting_confirmation` |
| 4 | Khách xác nhận | "Đúng rồi" | Đề xuất action `create_reservation`; sau khi backend ghi thành công, báo đã giữ bàn. `state: confirmed` |
| 5 | Hết bàn | *(đặt giờ đã hết bàn)* | Báo hết bàn, gợi ý giờ khác. `state: failed` |
| 6 | Đổi hoặc hủy | "Cho mình dời lịch sang 8 giờ" | Hỏi mã đặt bàn hoặc số điện thoại, xác nhận thay đổi. `intent: modify_cancel` |
| 7 | Hỏi thông tin | "Nhà hàng mở cửa mấy giờ?" | Trả lời theo dữ liệu nhà hàng. `intent: faq` |
| 8 | Ngoài phạm vi | "Hôm nay giá vàng bao nhiêu?" | Từ chối khéo, hỏi khách cần hỗ trợ món ăn hay đặt bàn. `intent: out_of_scope` |
| 9 | Phàn nàn, cần gặp người | "Cho mình nói chuyện với nhân viên" | Xin lỗi, thông báo chuyển nhân viên. `handoff_to_human: true` |
| 10 | Lỗi hệ thống | *(AI quá tải)* | Frontend hiển thị lỗi `MODEL_TIMEOUT` và nút thử lại |

### 4.4. Luồng đặt bàn hoàn chỉnh (ví dụ)

| Vai | Nội dung |
| :--- | :--- |
| **Khách** | Đặt bàn 4 người tối mai 7 giờ |
| **Bot** | Dạ, em ghi nhận bàn 4 người lúc 19:00 ngày 23/11/2026. Anh/chị cho em xin tên ạ? |
| **Khách** | Tên mình là Lan |
| **Bot** | Dạ chị Lan, chị cho em xin số điện thoại để giữ bàn ạ? |
| **Khách** | 0901234567 |
| **Bot** | Em xác nhận lại: bàn 4 người, 19:00 ngày 23/11, chị Lan, SĐT 0901234567. Chị xác nhận để em giữ bàn nhé? |
| **Khách** | Ok |
| **Bot** | Dạ, em đã giữ bàn cho chị Lan. Hẹn gặp chị ạ! |

## 5. JSON mẫu cho frontend làm mock

### 5.1. Tư vấn món (có thẻ món ăn)

```json
{
  "reply": "Dạ, em gợi ý vài món không cay phù hợp cho bé ạ:",
  "intent": "menu_advice",
  "state": "idle",
  "ui_hints": {
    "quick_replies": ["Đặt bàn", "Xem thêm món"],
    "cards": [
      { 
        "dish_id": "d_015", 
        "name": "Cá hồi nướng sốt chanh",
        "price": 189000, 
        "currency": "VND", 
        "tags": ["không cay"] 
      }
    ]
  },
  "actions": [],
  "handoff_to_human": false
}
```

### 5.2. Đặt bàn thành công

```json
{
  "reply": "Dạ, em đã giữ bàn 6 người lúc 19:00 thứ Sáu 27/11 cho chị Lan. Hẹn gặp chị ạ!",
  "intent": "reservation",
  "state": "confirmed",
  "slots": { 
    "date": "2026-11-27", 
    "time": "19:00", 
    "guests": 6,
    "name": "Lan", 
    "phone": "0901234567", 
    "note": null 
  },
  "missing_slots": [],
  "actions": [
    { 
      "type": "create_reservation",
      "status": "success",
      "payload": { "reservation_id": "rsv_2026_0087" } 
    }
  ],
  "handoff_to_human": false
}
```

*Các mẫu khác (thiếu thông tin, ngoài phạm vi, lỗi) xem mục 3.2 và 3.6. Sẽ bổ sung file JSON riêng cho từng tình huống sau khi nhóm thống nhất.*

## 6. Các điểm cần thống nhất với nhóm

*Nhóm điền cột "Quyết định của nhóm" trong buổi họp.*

| # | Nội dung cần thống nhất | Đề xuất của AI | Quyết định của nhóm |
| :--- | :--- | :--- | :--- |
| 1 | Ai tạo `session_id` | Backend tạo, trả về ở tin đầu | |
| 2 | Ai lưu lịch sử hội thoại | Backend lưu và gửi kèm cho AI mỗi lượt | |
| 3 | Ai ghi đặt bàn vào database | Backend; AI chỉ đề xuất `actions` | |
| 4 | Ai cung cấp dữ liệu menu cho AI | Backend cung cấp API tìm món hoặc AI đọc file menu JSON | |
| 5 | Thẻ món ăn (`cards`): ai điền ảnh, giá | AI trả `dish_id`, backend bổ sung ảnh và giá thật | |
| 6 | Có cần hiển thị chữ chạy dần (streaming) không | Chưa cần ở v0.1; thêm ở v0.2 nếu cần | |
| 7 | Giờ mở cửa, số người tối đa mỗi bàn, đặt trước tối thiểu bao lâu | `[Nhóm cung cấp]` | |
| 8 | Định dạng ngày giờ | `YYYY-MM-DD` và `HH:mm` (24h), timezone `Asia/Ho_Chi_Minh` | |
| 9 | Thời gian chờ tối đa của một lượt chat | 30 giây, quá thì trả `MODEL_TIMEOUT` | |
| 10 | Khi nào chuyển cho nhân viên thật | Khách yêu cầu, phàn nàn, hoặc bot không hiểu 2 lần liên tiếp | |