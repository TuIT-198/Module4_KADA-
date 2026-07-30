# 📊 Superstore Sales Analysis

> **Phân tích dữ liệu bán hàng Superstore — Khám phá insight kinh doanh từ dữ liệu thực tế**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C?style=for-the-badge)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

---

## 👥 Thông tin Nhóm

> 🏫 **Môn học:** Khoa học Dữ liệu & Phân tích (Module 4 — KADA)

> 🏷️ **Tên Nhóm:** THEMIS

| # | Họ và Tên |
|:-:|:----------|
| 1 | **Đàm Công Tú** |
| 2 | **Hà Anh Tuấn** |
| 3 | **Huỳnh Hoàng Quân** |
| 4 | **Chăm Rốch Thi** |
| 5 | **Nguyễn Tiến Thành** |
| 6 | **Phạm Thành Long** |

---

## 📖 Giới thiệu Dự án

Dự án phân tích bộ dữ liệu **Superstore** — một dataset kinh doanh bán lẻ thực tế của Mỹ,
ghi nhận **9.994 giao dịch** trong giai đoạn **2011–2014** trên toàn nước Mỹ.

Mục tiêu chính của dự án:

- 🔍 **Khám phá & làm sạch dữ liệu** — xử lý encoding, chuẩn hóa kiểu dữ liệu, feature engineering
- 📈 **Phân tích thống kê** — phân phối doanh thu, lợi nhuận, discount theo segment & category
- 🗺️ **Trực quan hóa địa lý** — vẽ bản đồ phân bố đơn hàng theo tiểu bang
- 🎯 **Xây dựng CEO Dashboard** — tổng hợp KPI chiến lược cho ban lãnh đạo

---

## 🗂️ Cấu trúc Dự án

```
Module4_KADA/
|
|── read_dataset.ipynb          # Notebook đọc & khám phá dữ liệu ban đầu
|── superstore_analysis.ipynb   # Notebook phân tích chuyên sâu (EDA, thống kê)
|── ceo_dashboard.ipynb         # Notebook xây dựng CEO Dashboard
|
|── superstore_report.md        # Báo cáo chi tiết: Data Dictionary + Cleaning Pipeline
|── data_comparison.md          # Bảng so sánh Raw vs Cleaned Data
|
|── Superstore.csv              # Dataset gốc (raw, encoding latin1)
|── Superstore_clean.csv        # Dataset sau khi làm sạch
|
|── ceo_dashboard.png           # Ảnh xuất CEO Dashboard
|── geo_charts_all.png          # Biểu đồ phân tích địa lý
|── geo_map_all.png             # Bản đồ phân bố địa lý
|
|── explore.py                  # Script Python khám phá nhanh dữ liệu
|── README.md                   # Tài liệu dự án (file này)
```

---

## 📊 Dataset Overview

| Thuộc tính | Chi tiết |
|:-----------|:---------|
| **Tên file** | `Superstore.csv` |
| **Số dòng** | 9.994 giao dịch |
| **Số cột** | 21 cột |
| **Khoảng thời gian** | 01/04/2011 — 31/12/2014 (4 năm) |
| **Quốc gia** | United States |
| **Mã hóa gốc** | `latin1` |

### Nhóm cột chính

| Nhóm | Cột |
|:-----|:----|
| 📦 **Order & Shipping** | Order ID, Order Date, Ship Date, Ship Mode, Shipping Days |
| 👤 **Customer & Geography** | Customer ID, Customer Name, Segment, Country, City, State, Region, Postal Code |
| 🏷️ **Product** | Product ID, Category, Sub-Category, Product Name |
| 💰 **Finance** | Sales, Quantity, Discount, Profit |

---

## 🔧 Quy trình Làm sạch Dữ liệu

### Vấn đề phát hiện trong Raw Data

| # | Vấn đề | Mức độ ảnh hưởng |
|:-:|:-------|:-----------------|
| 1 | Encoding sai (`latin1` đọc như UTF-8) | Toàn bộ file |
| 2 | `Order Date` / `Ship Date` lưu dạng chuỗi | 9.994 dòng |
| 3 | `Postal Code` mất số 0 đầu (int64 → str) | **449 dòng** |
| 4 | Cột `Row ID` dư thừa | 1 cột |
| 5 | 1 dòng duplicate hoàn toàn | 1 dòng |

### Cleaning Pipeline

```python
import pandas as pd

# 1. Đọc đúng encoding
df = pd.read_csv("Superstore.csv", encoding="latin1")

# 2. Chuẩn hóa Datetime
df["Order Date"] = pd.to_datetime(df["Order Date"], format="%d-%m-%Y")
df["Ship Date"]  = pd.to_datetime(df["Ship Date"],  format="%d-%m-%Y")

# 3. Chuẩn hóa Postal Code (giữ số 0 đầu)
df["Postal Code"] = df["Postal Code"].astype(str).str.split(".").str[0].str.zfill(5)

# 4. Feature Engineering: Shipping Days
df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

# 5. Xóa cột dư thừa
df = df.drop(columns=["Row ID"])

# 6. Xuất file sạch
df.to_csv("Superstore_clean.csv", index=False, encoding="utf-8-sig")
```

---

## 📈 Key Business Insights

### Thống kê tài chính tổng quan

| Chỉ số | Mean | Median | Max |
|:-------|-----:|-------:|----:|
| **Sales** | $229.86 | $54.49 | $22,638 |
| **Profit** | $28.66 | $8.67 | $8,400 |
| **Discount** | 16% | 20% | 80% |
| **Shipping Days** | 3.96 ngày | 4 ngày | 7 ngày |

### Lợi nhuận theo Segment

| Segment | Tổng lợi nhuận | Trung bình/đơn |
|:--------|---------------:|---------------:|
| **Consumer** | $134,119 | $25.84 |
| **Corporate** | $91,979 | $30.46 |
| **Home Office** | $60,299 | $33.82 ✅ cao nhất |

### Lợi nhuận theo Category

| Category | Tổng lợi nhuận | Trung bình/đơn |
|:---------|---------------:|---------------:|
| **Technology** | $145,455 | $78.75 🏆 |
| **Office Supplies** | $122,491 | $20.33 |
| **Furniture** | $18,451 | $8.70 ⚠️ thấp nhất |

### Thời gian giao hàng theo Ship Mode

| Ship Mode | Trung bình | Số đơn |
|:----------|:-----------:|-------:|
| Same Day | 0.04 ngày | 543 |
| First Class | 2.18 ngày | 1,538 |
| Second Class | 3.24 ngày | 1,945 |
| Standard Class | 5.01 ngày | **5,968** (~60%) |

---

## 🚀 Hướng dẫn Chạy Dự án

### Yêu cầu môi trường

```
Python >= 3.10
```

### Cài đặt thư viện

```bash
pip install pandas matplotlib seaborn jupyter folium geopandas
```

### Chạy notebooks theo thứ tự

```bash
# 1. Khám phá dữ liệu ban đầu
jupyter notebook read_dataset.ipynb

# 2. Phân tích chuyên sâu
jupyter notebook superstore_analysis.ipynb

# 3. CEO Dashboard
jupyter notebook ceo_dashboard.ipynb
```

---

## 📑 Tài liệu Tham khảo

- 📄 [Báo cáo chi tiết dataset](./superstore_report.md) — Data Dictionary, Cleaning Pipeline, Validation
- 📄 [So sánh Raw vs Cleaned](./data_comparison.md) — Bảng đối chiếu trước/sau làm sạch

---

## ✅ Kết quả Đạt được

- ✔️ **Analytics-Ready Dataset:** Datetime, Postal Code, Shipping Days đã chuẩn hóa hoàn toàn
- ✔️ **0 lỗi logic:** Không có đơn giao trước ngày đặt, không có Sales/Quantity âm
- ✔️ **0 missing values:** Toàn bộ 21 cột x 9.994 dòng đầy đủ
- ✔️ **CEO Dashboard:** Tổng hợp đầy đủ KPI chiến lược với visualizations chuyên nghiệp
- ✔️ **Geo Visualization:** Bản đồ phân bố đơn hàng theo tiểu bang nước Mỹ

---

<p align="center">
  Made with ❤️ by <strong>Nhóm THEMIS — Module 4</strong>
</p>
