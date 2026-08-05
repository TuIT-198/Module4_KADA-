# BẢNG SO SÁNH: RAW vs CLEANED — SUPERSTORE

> Tài liệu đối chiếu chi tiết sự thay đổi trước và sau khi làm sạch dataset Superstore (9,994 dòng).

---

## 1. SO SÁNH TỔNG QUAN

| Tiêu chí | Raw Data | Cleaned Data | Thay đổi |
| :--- | :--- | :--- | :---: |
| **Số dòng** | 9,994 | 9,994 | Giữ nguyên |
| **Số cột** | 21 | 21 | -1 Row ID + 1 Shipping Days |
| **Missing values** | 0 | 0 | Không đổi |
| **Duplicate rows** | 1 | 1 | Chưa xử lý |
| **Encoding** | latin1 | latin1 (đọc) | Fix khi đọc file |
| **Dung lượng** | 2.2 MB | 2.2 MB (raw) | Clean trong memory |

---

## 2. SO SÁNH CHI TIẾT TỪNG CỘT

| # | Cột | Raw | Cleaned | Số dòng ảnh hưởng | Tác dụng |
| :---: | :--- | :--- | :--- | ---: | :--- |
| 1 | **Row ID** | int64 (1→9994) | ❌ Đã xóa | 9,994 | Xóa cột dư thừa |
| 2 | **Order Date** | str '09-11-2013' | datetime64 2013-11-09 | 9,994 | Cho phép phân tích thời gian |
| 3 | **Ship Date** | str '12-11-2013' | datetime64 2013-11-12 | 9,994 | Tính hiệu suất giao hàng |
| 4 | **Shipping Days** | ❌ Chưa có | int64 (0→7 ngày) | **Thêm mới** | KPI Logistics |
| 5 | **Postal Code** | int64 (mất số 0) | str zfill(5) | **449** | Vẽ bản đồ GIS chính xác |
| 6 | **Product Name** | str (có ký tự lỗi) | str (sạch) | 0 | Tên sản phẩm hiển thị chuẩn |

---

## 3. TRƯỚC KHI CLEAN (RAW DATA)

### 3.1 Kiểu dữ liệu gốc
- **Order Date, Ship Date:** str → không thể tính toán ngày tháng
- **Postal Code:** int64 → mất số 0 đầu (VD: 05122 → 5122)
- **Row ID:** int64 → không mang giá trị phân tích

### 3.2 Vấn đề encoding
- File lưu mã latin1, không đọc được bằng UTF-8 thông thường

### 3.3 Vấn đề khác
- 1 dòng duplicate chưa xử lý

---

## 4. SAU KHI CLEAN (CLEANED DATA)

### 4.1 Kiểu dữ liệu chuẩn
| Nhóm cột | Kiểu mới | Giá trị |
| :--- | :--- | :--- |
| Datetime (2 cột) | datetime64 | 04/01/2011 → 31/12/2014 |
| Postal Code | str (zfill 5) | 06824, 07090, 07960... |
| Shipping Days | int64 | 0 → 7 ngày |
| Sales, Profit, Discount | float64 | Không đổi |
| Quantity | int64 | Không đổi |

### 4.2 Feature Engineering
- **Shipping Days** = Ship Date - Order Date
- Trung bình: ~4 ngày
- Standard Class: 5 ngày (chiếm ~60% đơn)

### 4.3 Validation
- 0 missing values
- 0 lỗi Ship Date < Order Date
- 0 Sales/Quantity âm
- 1 duplicate (cần xử lý)

---

## 5. BẢNG TỔNG HỢP INSIGHT

| Chỉ số | Raw | Cleaned | Giá trị mang lại |
| :--- | :--- | :--- | :--- |
| **Phân tích thời gian** | Không thể | Có thể lọc theo năm/tháng/quý | Phân tích mùa vụ, xu hướng |
| **Vẽ bản đồ** | Sai ZIP code (thiếu số 0) | Đúng chuẩn US 5 số | GIS visualization chính xác |
| **Tính KPI** | Không có Shipping Days | Có sẵn | Đo lường hiệu suất logistics |
| **Báo cáo BI** | Lỗi encoding | Tương thích UTF-8 | Import được vào Power BI, Tableau |
| **Mô hình ML** | Thiếu feature | Có thêm feature | Tăng độ chính xác dự báo |