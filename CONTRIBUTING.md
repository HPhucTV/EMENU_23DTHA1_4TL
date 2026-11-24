# Quy trình làm việc GitHub ↔ Jira (Nhóm 4TL — EMENU_23DTHA1_4TL)

Dự án sử dụng **GitFlow rút gọn** kết hợp tự động hóa đồng bộ với bảng Jira **[ManageProject_Check (MC)](https://tranhoangphuc98765432.atlassian.net/jira/software/c/projects/MC/boards/9/backlog)**.

---

## 1. Cấu trúc nhánh (Branching Strategy)

| Nhánh | Mục đích | Quy tắc |
| :--- | :--- | :--- |
| `main` | Bản ổn định dùng để Release / Demo báo cáo | Khóa push trực tiếp. Chỉ nhận PR từ `develop`, `release/*`, `hotfix/*` (cần ≥ 1 người Approve). |
| `develop` | Nhánh tích hợp code chung của cả nhóm trong Sprint | Khóa push trực tiếp. Mọi task phải tạo PR vào `develop` (cần ≥ 1 người Approve). |
| `feature/MC-<số>-<mô-tả>` | Phát triển tính năng mới | Tách từ `develop`, PR về `develop`. |
| `fix/MC-<số>-<mô-tả>` | Sửa lỗi trong quá trình phát triển | Tách từ `develop`, PR về `develop`. |
| `hotfix/MC-<số>-<mô-tả>` | Sửa lỗi khẩn cấp trên bản đã demo/release | Tách từ `main`, PR về `main` (và merge ngược lại `develop`). |
| `docs/MC-<số>-<mô-tả>` | Viết tài liệu QLDA, biểu đồ, README | Tách từ `develop`, PR về `develop`. |
| `chore/MC-<số>-<mô-tả>` | Cấu hình dự án, CI/CD, cài thư viện | Tách từ `develop`, PR về `develop`. |
| `MC-<số>-<mô-tả>` *(tạo từ Jira)* | Nhánh tạo trực tiếp bằng nút **Create branch** trên Jira | Tách từ `develop`, PR về `develop` (hỗ trợ tiếng Việt có dấu). |

---

## 2. Quy ước đặt tên (Bắt buộc có mã Jira `MC-<số>`)

Để Jira tự động nhận diện và chuyển trạng thái task, luôn gắn đúng mã `MC-<số>`:

1. **Tên nhánh**: `[<loại>/]MC-<số>-<mô-tả>` *(VD: `feature/MC-12-quan-ly-mon-an` hoặc `MC-66-ba-khảo-sat-...` tạo từ Jira)*
2. **Commit message**: `MC-<số> [<PM|BA|FS|AI|US-xx>] <Mô tả>` *(VD: `MC-65 [PM] Khởi tạo Jira (SCRUM), MS Project, Kick-off và Bộ tài liệu D01/D14/D17`)*
3. **Tiêu đề Pull Request**: `[MC-12] Thêm chức năng quản lý món ăn`

> GitHub Actions (`Check Jira Key & PR Convention`) sẽ tự động kiểm tra tên nhánh và tiêu đề PR. Nếu thiếu mã `MC-<số>`, nút Merge sẽ bị khóa cho đến khi sửa lại đúng chuẩn.

---

## 3. Tự động hóa trạng thái trên Jira (`MC`)

| Bước thực hiện trên GitHub | Trạng thái task trên Jira `MC` |
| :--- | :--- |
| Task nằm trong Sprint chưa làm | **`To Do`** |
| Tạo nhánh `feature/MC-xx-...` và push lên GitHub | Tự động chuyển → **`In Progress`** |
| Mở Pull Request vào `develop` | Tự động chuyển → **`In Review`** |
| Đồng đội Approve & bấm **Merge PR** | Tự động chuyển → **`Done`** |

---

## 4. Các bước làm một task chuẩn từ đầu đến cuối

### Bước 1: Cập nhật nhánh `develop` mới nhất
```bash
git checkout develop
git pull origin develop
```

### Bước 2: Tạo nhánh riêng gắn mã Jira (VD: `MC-12`)
```bash
git checkout -b feature/MC-12-quan-ly-mon-an
```

### Bước 3: Code, commit và push nhánh lên GitHub
```bash
git add .
git commit -m "MC-12 [FS] Tạo giao diện danh sách món ăn"
git push -u origin feature/MC-12-quan-ly-mon-an
```
*(Ngay khi push nhánh lên GitHub, Jira tự chuyển `MC-12` sang **In Progress**)*

### Bước 4: Tạo Pull Request trên GitHub
1. Vào GitHub mở Pull Request từ `feature/MC-12-quan-ly-mon-an` → **`develop`**.
2. Đặt tiêu đề có mã Jira, ví dụ: `[MC-12] Thêm giao diện danh sách món ăn`.
3. Điền đầy đủ thông tin theo mẫu PR có sẵn và chọn Reviewer trong nhóm.
4. Chờ check **`Check Jira Key & PR Convention`** báo xanh ✅.
*(Ngay khi mở PR, Jira tự chuyển `MC-12` sang **In Review**)*

### Bước 5: Review & Merge
1. Thành viên trong nhóm review code, trao đổi (nếu cần sửa) và bấm **Approve**.
2. Sau khi tất cả comment đã được giải quyết (`Resolve conversation`) và có ít nhất **1 Approve**, bấm **Squash and merge**.
3. GitHub sẽ **tự động xóa nhánh `feature/MC-12-...`** sau khi merge, và Jira sẽ **tự động chuyển `MC-12` sang `Done`**.

---

## 5. Quy trình Release cuối Sprint (`develop` → `main`)
1. Khi các task trong Sprint đã được merge vào `develop` và kiểm thử ổn định, trưởng nhóm tạo Pull Request từ **`develop` → `main`** (ví dụ tiêu đề: `Release Sprint 1`).
2. Ít nhất 1 thành viên Approve (hoặc trưởng nhóm `HPhucTV` có quyền bypass trong trường hợp khẩn cấp sát giờ nộp).
3. Chọn **Create a merge commit** để giữ lịch sử đồng bộ giữa `develop` và `main`.
