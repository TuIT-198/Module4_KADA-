# 📊 Superstore Analytics & AI Profit Forecasting

> **Hệ thống Phân tích Kinh doanh Đa chiều, Trực quan hóa Dashboard CEO & Dự báo Lợi nhuận Superstore bằng Machine Learning**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C?style=for-the-badge)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

---

## 👥 Thông tin Nhóm Dự án

> 🏫 **Môn học:** Khoa học Dữ liệu & Phân tích (Module 4 — TuIT-198 / KADA)  
> 🏷️ **Tên Nhóm:** THEMIS

| # | Họ và Tên | Vai trò |
|:-:|:----------|:-------:|
| 1 | **Đàm Công Tú** | Thành viên |
| 2 | **Hà Anh Tuấn** | Thành viên |
| 3 | **Huỳnh Hoàng Quân** | Thành viên |
| 4 | **Chăm Rốch Thi** | Thành viên |
| 5 | **Nguyễn Tiến Thành** | Thành viên |
| 6 | **Phạm Thành Long** | Thành viên |

---

## 📖 Tổng quan Dự án

Dự án nghiên cứu và khai thác toàn diện dữ liệu bán lẻ **Superstore** (Mỹ) với **9,994 đơn hàng giao dịch** từ năm **2011 đến 2014**. Dự án kết hợp giữa **Data Engineering**, **Business Intelligence (BI)** và **Machine Learning (AI)** qua 4 trụ cột chính:

```
┌─────────────────────────┐     ┌─────────────────────────┐
│ 1. Data Cleaning        │ ──► │ 2. Business Analytics   │
│ Raw Data ➔ Clean Data   │     │ EDA & Customer Segment  │
└─────────────────────────┘     └─────────────────────────┘
             │                               │
             ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│ 3. CEO Strategic Dash   │ ──► │ 4. AI Profit Forecast   │
│ Geographic & KPI Map    │     │ Gradient Boosting (5-St)│
└─────────────────────────┘     └─────────────────────────┘
```

---

## 🗂️ Cấu trúc Thư mục Hệ thống

Mã nguồn và tài nguyên được tổ chức phân vùng theo tiêu chuẩn dự án Khoa học Dữ liệu:

```
module_4/
│
├── 📂 data/                           # Lưu trữ Dữ liệu gốc & Dữ liệu sạch
│   ├── Superstore.csv                 # Dataset gốc (Raw, encoding latin1, 9,994 dòng)
│   └── Superstore_clean.csv           # Dataset đã làm sạch (UTF-8, chuẩn hóa Datetime & Postal Code)
│
├── 📂 notebooks/                      # Tập hợp các Jupyter Notebooks thực thi
│   ├── profit_forecast_notebook.ipynb # 🌟 Notebook AI 5 Bước Dự báo Lợi nhuận (Gradient Boosting)
│   ├── ceo_dashboard.ipynb            # Notebook thiết kế CEO Dashboard & KPI Ban Lãnh đạo
│   ├── superstore_analysis.ipynb      # Notebook Phân tích Khám phá EDA & Thống kê kinh doanh
│   └── read_dataset.ipynb             # Notebook Khám phá ban đầu & Kiểm tra cấu trúc Data
│
├── 📂 outputs/                        # Tài nguyên Biểu đồ & Dashboard xuất ra
│   ├── profit_forecast_dashboard.png  # Báo cáo tổng hợp dự báo lợi nhuận
│   ├── profit_feature_importance.png  # Biểu đồ mức độ quan trọng đặc trưng (Feature Importance)
│   ├── ceo_dashboard.png              # Hình ảnh CEO Strategic Dashboard
│   ├── geo_charts_all.png             # Biểu đồ trực quan địa lý theo State / City
│   └── geo_map_all.png                # Bản đồ phân bổ đơn hàng theo khu vực
│
├── 📂 reports/                        # Báo cáo kỹ thuật & Tài liệu đối chiếu
│   ├── superstore_report.md           # Báo cáo kỹ thuật: Data Dictionary & Cleaning Pipeline
│   └── data_comparison.md             # Bảng đối chiếu so sánh Raw Data vs Cleaned Data
│
├── 📂 scripts/                        # Các Script Python độc lập
│   ├── profit_forecast.py             # Script Python chạy tự động Pipeline AI & CFO Insights
│   └── explore.py                     # Script Python kiểm tra nhanh thông tin dữ liệu
│
└── README.md                          # Tài liệu tổng quan dự án (File này)
```

---

## 🧹 1. Quy trình Làm sạch Dữ liệu (Data Cleaning & Engineering)

Dữ liệu thô (`Superstore.csv`) chứa các lỗi mã hóa và định dạng được xử lý qua pipeline:

### Vấn đề xử lý trong Raw Data

| # | Vấn đề phát hiện | Mức độ ảnh hưởng | Giải pháp xử lý |
|:-:|:---|:---:|:---|
| 1 | Mã hóa ký tự sai (`latin1`) | File gốc | Đọc file bằng `encoding='latin1'`, xuất file sạch `utf-8-sig` |
| 2 | `Order Date` & `Ship Date` dạng chuỗi | 9,994 dòng | Chuyển đổi sang `pd.to_datetime` định dạng chuẩn |
| 3 | `Postal Code` bị mất số `0` đầu | 449 dòng | Chuẩn hóa dạng chuỗi 5 chữ số (`zfill(5)`) |
| 4 | Cột dư thừa `Row ID` | 1 cột | Xóa khỏi bộ dữ liệu để tối ưu kích thước |
| 5 | Feature Engineering | Dòng thời gian | Tạo thêm cột `Shipping Days = Ship Date - Order Date` |

*Tài liệu chi tiết:* 📄 [Báo cáo Làm sạch Dữ liệu (reports/superstore_report.md)](./reports/superstore_report.md) | 📄 [So sánh Raw vs Cleaned (reports/data_comparison.md)](./reports/data_comparison.md)

---

## 📈 2. Phân tích Kinh doanh & Insight (EDA & Customer Analysis)

Thực hiện trong `notebooks/superstore_analysis.ipynb`:

### Key Insights Kinh doanh
* **Lợi nhuận theo Ngành hàng (Category)**:
  * 🏆 **Technology** dẫn đầu lợi nhuận: Tổng LN **$145,455** (Trung bình **$78.75/đơn**).
  * 📦 **Office Supplies**: Tổng LN **$122,491** (Trung bình **$20.33/đơn**).
  * ⚠️ **Furniture** biên lợi nhuận mỏng nhất: Tổng LN **$18,451** (Trung bình chỉ **$8.70/đơn**).
* **Tác động của Chiết khấu (Discount vs Profitability)**:
  * Khi mức Discount $\le 20\%$, lợi nhuận đạt mức tối ưu.
  * Khi Discount $> 20\%$, biên lợi nhuận tụt dốc thảm hại (gây lỗ cho đơn hàng).
* **Khách hàng theo Phân đoạn (Segment)**:
  * **Consumer** chiếm thị phần lớn nhất ($51\%$), nhưng **Home Office** đạt lợi nhuận trung bình trên đơn cao nhất (**$33.82/đơn**).

---

## 🗺️ 3. Dashboard Ban Lãnh Đạo (CEO Strategic Dashboard)

Thực hiện trong `notebooks/ceo_dashboard.ipynb` và xuất ra `outputs/ceo_dashboard.png`:

* **Khung KPI Chiến lược**:
  * 💰 **Tổng Doanh thu (Sales)**: $\$2,297,201$
  * 📈 **Tổng Lợi nhuận (Profit)**: $\$286,397$
  * 🏷️ **Tỷ lệ Chiết khấu trung bình**: $15.62\%$
  * 🚚 **Thời gian giao hàng trung bình**: $3.96 \text{ ngày}$
* **Bản đồ Phân bổ Địa lý (Geographic Map)**:
  * Trực quan hóa thị phần đơn hàng theo 4 vùng Region (West, East, Central, South) và các tiểu bang trọng điểm (California, New York).

---

## 🤖 4. Mô hình AI Dự báo Lợi nhuận (Profit Forecasting Pipeline)

Thực hiện trong `notebooks/profit_forecast_notebook.ipynb` và `scripts/profit_forecast.py`:

Pipeline huấn luyện Machine Learning 5 bước sử dụng **Gradient Boosting Regressor**:

```
[1. Preprocessing] ──► [2. Train/Test Split] ──► [3. Iteration & Early Stop] ──► [4. Evaluation & 4 Charts] ──► [5. 3-Month Forecast]
```

### Chi tiết 5 Bước triển khai:

1. **Bước 1 – Preprocessing**: 
   * Chọn 5 features: `Sales`, `Discount`, `Quantity`, `Category`, `Region`.
   * Sử dụng `StandardScaler` cho biến số, `OneHotEncoder` cho biến danh mục.
2. **Bước 2 – Train/Test Split (80% / 20%)**:
   * Chia 80% Train, 20% Test theo chuỗi thời gian (`shuffle=False`).
3. **Bước 3 – Huấn luyện với Early Stopping & Nhật ký Iteration**:
   * Thiết lập siêu tham số: `n_estimators=300`, `learning_rate=0.05`, `max_depth=5`, `subsample=0.8`.
   * Tích hợp **Early Stopping** (`n_iter_no_change=15`, `tol=1e-4`).
   * Ghi nhật ký chi tiết `Train Loss`, `Val Loss`, `Train R²`, `Val R²`, `Val MAE` theo từng vòng lặp. Mô hình tự động **dừng tối ưu tại Vòng thứ 38 (`🏆 BEST`)**.
4. **Bước 4 – Đánh giá Chi tiết & Bộ 4 Biểu đồ Matplotlib**:
   * **Biểu đồ 1**: Train vs Validation R² Score theo Iteration.
   * **Biểu đồ 2**: Train Loss vs Validation Loss (MSE) theo Iteration.
   * **Biểu đồ 3**: Biểu đồ Actual vs Predicted Profit ($1:1$).
   * **Biểu đồ 4**: Feature Importance (Mức độ đóng góp đặc trưng).
5. **Bước 5 – Dự báo Lợi nhuận 3 Tháng tiếp theo**:
   * Re-train mô hình trên 100% dữ liệu lịch sử và kết hợp với tỷ lệ tăng trưởng doanh thu.

### Bảng Kết quả Đánh giá Mô hình AI

| Chỉ số Đánh giá | Lúc Học (5-Fold CV) | Lúc Thi (Test Set 20%) | Ý nghĩa Quản trị Tài chính |
|:---|:---:|:---:|:---|
| **$R^2$ Score** | $58.20\%$ | **$68.96\%$** | AI giải thích được $68.96\%$ biến động Lợi nhuận |
| **MAE** | $\$31.20$ | **$\pm \$26.97$** | Mức chênh lệch trung bình từng đơn hàng |
| **RMSE** | $\$135.10$ | **$\$126.45$** | Thước đo phạt nặng các đơn hàng bất thường |

### Kết quả Dự báo Lợi nhuận 3 Tháng tới

| Tháng Dự báo | Doanh thu ước tính | Lợi nhuận ước tính | Biên LN (%) |
|:---:|:---:|:---:|:---:|
| **Tháng +1 (2015-01)** | $\$100,761$ | **$\$10,134$** | $10.1\%$ |
| **Tháng +2 (2015-02)** | $\$112,217$ | **$\$11,191$** | $10.0\%$ |
| **Tháng +3 (2015-03)** | $\$124,975$ | **$\$12,507$** | $10.0\%$ |

---

## 🛠️ Hướng dẫn Cài đặt & Khởi chạy

### 1. Môi trường yêu cầu
* Python $\ge 3.10$
* Jupyter Lab / Jupyter Notebook

### 2. Cài đặt Virtual Environment & Dependencies
```powershell
# Kích hoạt môi trường venv sẵn có trong repo
.\.venv\Scripts\Activate.ps1

# Cài đặt thư viện phụ thuộc (nếu cần)
pip install pandas numpy scikit-learn matplotlib seaborn jupyter ipykernel
```

### 3. Đăng ký Kernel Jupyter
```powershell
python -m ipykernel install --user --name "module4-venv" --display-name "Python (Module4 venv)"
```

### 4. Khởi chạy Mô hình & Notebooks

#### 👉 Cách 1: Chạy bằng Script Python tự động
```powershell
python scripts/profit_forecast.py
```

#### 👉 Cách 2: Chạy bằng Jupyter Lab
```powershell
jupyter lab
```
1. Mở thư mục `notebooks/`.
2. Chọn Notebook muốn chạy (ví dụ: `profit_forecast_notebook.ipynb` hoặc `ceo_dashboard.ipynb`).
3. Chọn Kernel **`Python (Module4 venv)`** ở góc trên bên phải.
4. Chọn **`Kernel` → `Restart Kernel and Run All Cells...`**.

---

## 📑 Danh mục Tài liệu & Đầu ra Dự án

- 📓 **Notebook AI Dự báo**: [`notebooks/profit_forecast_notebook.ipynb`](./notebooks/profit_forecast_notebook.ipynb)
- 📓 **Notebook CEO Dashboard**: [`notebooks/ceo_dashboard.ipynb`](./notebooks/ceo_dashboard.ipynb)
- 📓 **Notebook Phân tích EDA**: [`notebooks/superstore_analysis.ipynb`](./notebooks/superstore_analysis.ipynb)
- 📄 **Báo cáo Kỹ thuật Làm sạch Data**: [`reports/superstore_report.md`](./reports/superstore_report.md)
- 📄 **So sánh Data Trước & Sau**: [`reports/data_comparison.md`](./reports/data_comparison.md)
- 🐍 **Script Python Dự báo**: [`scripts/profit_forecast.py`](./scripts/profit_forecast.py)

---

<p align="center">
  <b>© 2026 Nhóm THEMIS — Module 4 KADA (TuIT-198)</b>
</p>
