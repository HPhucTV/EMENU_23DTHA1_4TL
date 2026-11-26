-- Khởi tạo tiện ích mở rộng bắt buộc cho ràng buộc chống trùng bàn (FR-05)
-- và chuẩn hóa múi giờ GMT+7 cho CSDL Nhà hàng Ẩm thực Vườn Phố.
CREATE EXTENSION IF NOT EXISTS btree_gist;
ALTER DATABASE emenu_db SET timezone TO 'Asia/Ho_Chi_Minh';
