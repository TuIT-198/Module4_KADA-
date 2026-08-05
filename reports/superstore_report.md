# BÁO CÁO PHÂN TÍCH & CHUẨN HÓA DỮ LIỆU SUPERSTORE

---

## 1. TỔNG QUAN DATASET

| Thuộc tính | Giá trị |
| :--- | :--- |
| **Tên file** | `Superstore.csv` |
| **Lĩnh vực** | Bán lẻ & Quản lý đơn hàng (Retail Sales) |
| **Số dòng** | 9,994 |
| **Số cột** | 21 (gốc) → 21 (sau xử lý: -1 Row ID + 1 Shipping Days) |
| **Khoảng thời gian** | 04/01/2011 → 31/12/2014 (4 năm) |
| **Quốc gia** | United States |
| **Mã hóa gốc** | latin1 |

---

## 2. DATA DICTIONARY (CHI TIẾT CỘT)

### Nhóm Order & Shipping
| Cột | Kiểu (gốc) | Kiểu (sau) | Mô tả |
| :--- | :--- | :--- | :--- |
| Row ID | int64 | ❌ Đã xóa | Số thứ tự dòng (dư thừa) |
| Order ID | str | str | Mã đơn hàng |
| Order Date | str (dd-MM-yyyy) | datetime64 | Ngày đặt hàng |
| Ship Date | str (dd-MM-yyyy) | datetime64 | Ngày giao hàng |
| Ship Mode | str | str | Phương thức vận chuyển |
| **Shipping Days** | ❌ Chưa có | int64 | Số ngày giao hàng (tạo mới) |

### Nhóm Customer & Geography
| Cột | Kiểu (gốc) | Kiểu (sau) | Mô tả |
| :--- | :--- | :--- | :--- |
| Customer ID | str | str | Mã khách hàng |
| Customer Name | str | str | Tên khách hàng |
| Segment | str | str | Phân khúc (Consumer / Corporate / Home Office) |
| Country | str | str | Quốc gia |
| City | str | str | Thành phố |
| State | str | str | Tiểu bang |
| Postal Code | int64 | str (zfill 5) | Mã bưu chính |
| Region | str | str | Khu vực (South / West / Central / East) |

### Nhóm Product
| Cột | Kiểu (gốc) | Kiểu (sau) | Mô tả |
| :--- | :--- | :--- | :--- |
| Product ID | str | str | Mã sản phẩm |
| Category | str | str | Danh mục chính (Furniture / Office Supplies / Technology) |
| Sub-Category | str | str | Danh mục phụ (Bookcases, Chairs, Labels, Tables...) |
| Product Name | str | str | Tên sản phẩm |

### Nhóm Finance
| Cột | Kiểu (gốc) | Kiểu (sau) | Mô tả |
| :--- | :--- | :--- | :--- |
| Sales | float64 | float64 | Doanh số (USD) |
| Quantity | int64 | int64 | Số lượng bán |
| Discount | float64 | float64 | Chiết khấu (0.0 → 0.8) |
| Profit | float64 | float64 | Lợi nhuận (USD) |

---

## 3. CHẤT LƯỢNG DỮ LIỆU GỐC (RAW DATA QUALITY ISSUES)

| # | Vấn đề | Mô tả | Mức độ ảnh hưởng |
| :---: | :--- | :--- | :--- |
| 1 | **Encoding sai** | File lưu mã latin1, đọc UTF-8 báo lỗi | Toàn bộ file, không đọc được |
| 2 | **Ngày tháng dạng chuỗi** | Order Date / Ship Date là str, không phân tích được thời gian | 2 cột x 9,994 dòng |
| 3 | **Mất số 0 Postal Code** | Kiểu int64 → mất số 0 đầu (VD: 05122 → 5122) | **449 dòng** bị mất số 0 |
| 4 | **Cột Row ID dư thừa** | Chỉ là index đánh số, không mang thông tin | 1 cột không cần thiết |
| 5 | **Ký tự lỗi Unicode** | Product Name chứa ký tự � (U+FFFD) | 0 dòng (file latin1 đã đọc đúng) |
| 6 | **Thiếu dữ liệu (Nulls)** | Không có ô nào trống | 0 dòng |
| 7 | **Trùng lặp (Duplicates)** | Có 1 dòng trùng lặp hoàn toàn | 1 dòng |

---

## 4. QUY TRÌNH LÀM SẠCH (CLEANING PIPELINE)

### Bước 1: Đọc đúng Encoding
```python
df = pd.read_csv('Superstore.csv', encoding='latin1')
```
- **Mục tiêu:** Khắc phục lỗi Unicode khi đọc file
- **Kết quả:** Đọc thành công 9,994 dòng

### Bước 2: Chuẩn hóa Datetime
```python
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d-%m-%Y')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='%d-%m-%Y')
```
- **Trước:** `'09-11-2013'` (str)
- **Sau:** `2013-11-09` (datetime64)
- **Tác dụng:** Cho phép lọc theo năm/tháng/quý, tính toán thời gian

### Bước 3: Chuẩn hóa Postal Code
```python
df['Postal Code'] = df['Postal Code'].astype(str).str.split('.').str[0].str.zfill(5)
```
- **Trước:** `5122` (int64) → mất số 0
- **Sau:** `'05122'` (str, 5 chữ số)
- **Số dòng phục hồi:** 449 dòng có ZIP bắt đầu bằng 0

### Bước 4: Feature Engineering (Shipping Days)
```python
df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days
```
- **Công dụng:** KPI đo tốc độ giao hàng
- **Giá trị:** 0 → 7 ngày, trung bình ~4 ngày

### Bước 5: Làm sạch Text & Xóa cột rác
```python
df['Product Name'] = df['Product Name'].str.replace('\ufffd', ' ', regex=False)
df = df.drop(columns=['Row ID'])
```
- Xóa cột Row ID (không mang giá trị phân tích)

---

## 5. KẾT QUẢ KIỂM ĐỊNH (VALIDATION RESULTS)

| Kiểm tra | Công thức | Kết quả | Trạng thái |
| :--- | :--- | :---: | :---: |
| Missing values | `df.isnull().sum().sum()` | **0** | ✅ PASS |
| Duplicate rows | `df.duplicated().sum()` | **1** | ⚠️ 1 dòng trùng |
| Ship Date < Order Date | `(df['Ship Date'] < df['Order Date']).sum()` | **0** | ✅ PASS |
| Sales <= 0 | `(df['Sales'] <= 0).sum()` | **0** | ✅ PASS |
| Quantity <= 0 | `(df['Quantity'] <= 0).sum()` | **0** | ✅ PASS |

> **Kết luận:** Dữ liệu sạch, không có lỗi logic kinh doanh. 1 dòng duplicate có thể loại bỏ bằng `df.drop_duplicates()` nếu cần.

---

## 6. THỐNG KÊ KINH DOANH (BUSINESS STATISTICS)

### 6.1 Phân phối các biến tài chính

| Chỉ số | Mean | Std | Min | 25% | 50% | 75% | Max |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Sales** | 229.86 | 623.25 | 0.44 | 17.28 | 54.49 | 209.94 | 22,638.48 |
| **Quantity** | 3.79 | 2.23 | 1.00 | 2.00 | 3.00 | 5.00 | 14.00 |
| **Discount** | 0.16 | 0.21 | 0.00 | 0.00 | 0.20 | 0.20 | 0.80 |
| **Profit** | 28.66 | 234.26 | -6,599.98 | 1.73 | 8.67 | 29.36 | 8,399.98 |
| **Shipping Days** | 3.96 | 1.75 | 0.00 | 3.00 | 4.00 | 5.00 | 7.00 |

### 6.2 Thời gian giao hàng theo phương thức vận chuyển

| Ship Mode | Trung bình (ngày) | Độ lệch | Số đơn |
| :--- | :---: | :---: | :---: |
| **Same Day** | 0.04 | 0.21 | 543 |
| **First Class** | 2.18 | 0.77 | 1,538 |
| **Second Class** | 3.24 | 1.19 | 1,945 |
| **Standard Class** | 5.01 | 1.01 | 5,968 |

### 6.3 Lợi nhuận theo phân khúc khách hàng

| Segment | Tổng lợi nhuận | Trung bình | Số đơn |
| :--- | ---: | ---: | ---: |
| **Consumer** | $134,119.21 | $25.84 | 5,191 |
| **Corporate** | $91,979.13 | $30.46 | 3,020 |
| **Home Office** | $60,298.68 | $33.82 | 1,783 |

### 6.4 Lợi nhuận theo danh mục sản phẩm

| Category | Tổng lợi nhuận | Trung bình | Số đơn |
| :--- | ---: | ---: | ---: |
| **Technology** | $145,454.95 | $78.75 | 1,847 |
| **Office Supplies** | $122,490.80 | $20.33 | 6,026 |
| **Furniture** | $18,451.27 | $8.70 | 2,121 |

### 6.5 Phân phối Shipping Days

| Số ngày | Số đơn |
| :---: | :---: |
| 0 | 519 |
| 1 | 368 |
| 2 | 1,332 |
| 3 | 1,007 |
| 4 | 2,771 |
| 5 | 2,175 |
| 6 | 1,201 |
| 7 | 621 |

---

## 7. KẾT LUẬN & GIÁ TRỊ KINH DOANH

### Dữ liệu sau cleaning
- ✅ **Analytics-Ready:** Datetime, Postal Code, Shipping Days đã chuẩn hóa hoàn toàn
- ✅ **0 lỗi logic:** Không có đơn giao trước ngày đặt, không có Sales/Quantity âm
- ✅ **0 missing values:** Toàn bộ 21 cột × 9,994 dòng đầy đủ
- ⚠️ **1 duplicate:** Có thể drop nếu cần dữ liệu unique

### Insight kinh doanh nhanh
- **Standard Class** chiếm ~60% đơn hàng, giao trung bình 5 ngày
- **Home Office** là segment có lợi nhuận trung bình cao nhất ($33.82/đơn)
- **Technology** là category lời nhất ($78.75/đơn), **Furniture** thấp nhất ($8.70/đơn)
- Lợi nhuận biến động mạnh: lỗ nhất -$6,599, lời nhất +$8,399
- 50% đơn hàng có doanh số dưới $54.49 (phân phối lệch phải)