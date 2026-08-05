# 📊 Superstore Sales Analytics & AI Profit Forecasting

> **Hệ thống Phân tích Kinh doanh & Dự báo Lợi nhuận Superstore bằng Machine Learning**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-Machine%20Learning-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C?style=for-the-badge)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

---

## 👥 Thông tin Nhóm

> 🏫 **Môn học:** Khoa học Dữ liệu & Phân tích (Module 4 — TuIT-198 / KADA)  
> 🏷️ **Tên Nhóm:** THEMIS

| # | Họ và Tên | Thành viên |
|:-:|:----------|:----------:|
| 1 | **Đàm Công Tú** | Thành viên |
| 2 | **Hà Anh Tuấn** | Thành viên |
| 3 | **Huỳnh Hoàng Quân** | Thành viên |
| 4 | **Chăm Rốch Thi** | Thành viên |
| 5 | **Nguyễn Tiến Thành** | Thành viên |
| 6 | **Phạm Thành Long** | Thành viên |

---

## 📖 Giới thiệu Dự án

Dự án khai thác toàn diện bộ dữ liệu **Superstore** — dataset giao dịch bán lẻ của Mỹ với **9,994 đơn hàng** trong giai đoạn **2011–2014**.

Dự án bao gồm 2 phần chính:
1. 🔍 **Phân tích dữ liệu kinh doanh (EDA & Dashboard)**: Khám phá doanh số, lợi nhuận, hành vi chiết khấu và địa lý.
2. 🤖 **Mô hình AI Dự báo Lợi nhuận (Profit Forecasting)**: Xây dựng pipeline Machine Learning 5 bước sử dụng thuật toán **Gradient Boosting Regressor** tích hợp **Early Stopping** & **Per-Iteration Tracking** để dự báo Lợi nhuận 3 tháng tiếp theo.

---

## 📂 Cấu trúc Thư mục Dự án

Workspace được tổ chức chuẩn hóa theo từng phân vùng chức năng:

```
module_4/
│
├── 📂 data/                           # Dữ liệu dự án
│   ├── Superstore.csv                 # Dataset gốc (encoding latin1, 9,994 dòng)
│   └── Superstore_clean.csv           # Dataset làm sạch (UTF-8, đã xử lý missing & date)
│
├── 📂 notebooks/                      # Jupyter Notebooks phân tích & AI
│   ├── profit_forecast_notebook.ipynb # 🌟 Notebook AI 5 Bước Dự báo Lợi nhuận (Gradient Boosting)
│   ├── ceo_dashboard.ipynb            # Notebook xây dựng CEO Dashboard & KPI
│   ├── superstore_analysis.ipynb      # Notebook phân tích khám phá EDA & Thống kê
│   └── read_dataset.ipynb             # Notebook đọc & làm sạch dữ liệu ban đầu
│
├── 📂 outputs/                        # Hình ảnh biểu đồ & Dashboard xuất ra
│   ├── profit_forecast_dashboard.png  # Bảng điều khiển dự báo lợi nhuận
│   ├── profit_feature_importance.png  # Biểu đồ độ quan trọng biến
│   ├── ceo_dashboard.png              # Ảnh chụp CEO Dashboard
│   ├── geo_charts_all.png             # Biểu đồ phân tích địa lý
│   └── geo_map_all.png                # Bản đồ phân bổ đơn hàng
│
├── 📂 reports/                        # Báo cáo Markdown & Đối chiếu
│   ├── superstore_report.md           # Báo cáo chi tiết: Data Dictionary & Cleaning Pipeline
│   └── data_comparison.md             # Bảng đối chiếu Raw Data vs Cleaned Data
│
├── 📂 scripts/                        # Script Python chạy độc lập
│   ├── profit_forecast.py             # Script Python chạy huấn luyện & dự báo tự động
│   └── explore.py                     # Script Python kiểm tra & khám phá nhanh dữ liệu
│
└── README.md                          # Tài liệu dự án (File này)
```

---

## 🤖 Pipeline Training AI Dự báo Lợi nhuận (5 Bước Chuẩn hóa)

Mô hình dự báo Lợi nhuận được xây dựng theo quy trình 5 bước nghiêm ngặt:

```
[1. Preprocessing] ──► [2. Train/Test Split] ──► [3. Gradient Boosting CV] ──► [4. Evaluation] ──► [5. 3-Month Forecast]
```

### 1️⃣ Bước 1 – Tiền xử lý Dữ liệu
* **Features**: Select 5 đặc trưng quan trọng: `Sales`, `Discount`, `Quantity`, `Category`, `Region`.
* **Preprocessing Pipeline**: `StandardScaler` cho biến số, `OneHotEncoder` cho biến danh mục.

### 2️⃣ Bước 2 – Phân chia Train / Test (80% / 20%)
* Chia **80% Train** (học) / **20% Test** (thi).
* Áp dụng `shuffle=False` giữ đúng dòng thời gian thực tế (tránh rò rỉ dữ liệu / Look-ahead bias).

### 3️⃣ Bước 3 – Huấn luyện Gradient Boosting & Early Stopping
* **Thuật toán**: `GradientBoostingRegressor(n_estimators=300, learning_rate=0.05, max_depth=5, subsample=0.8)`.
* **Cơ chế Early Stopping**: Dừng sớm sau 15 vòng nếu Validation Loss không cải thiện (`n_iter_no_change=15`).
* **Tracking**: Ghi nhật ký đầy đủ `Train Loss`, `Val Loss`, `Train R²`, `Val R²`, `Val MAE` theo từng vòng lặp (Iteration). Mô hình đạt trạng thái **tối ưu nhất tại Vòng 38 (`🏆 BEST`)**.

### 4️⃣ Bước 4 – Đánh giá Mô hình & Trực quan hóa Matplotlib
Trực quan hóa bộ 4 biểu đồ chuyên nghiệp:
1. **Train vs Validation Metric (R² Score)** theo từng Iteration.
2. **Train Loss vs Validation Loss (MSE)** theo từng Iteration.
3. **Actual vs Predicted Profit** (Scatter plot 1:1).
4. **Feature Importance** (Biểu đồ đóng góp % của các đặc trưng).

| Chỉ số | Lúc Học (5-Fold CV) | Lúc Thi (Test Set 20%) | Ý nghĩa Business |
|:---|:---:|:---:|:---|
| **$R^2$ Score** | $58.20\%$ | **$68.96\%$** | Mô hình giải thích được $68.96\%$ biến động Profit |
| **MAE** | $\$31.20$ | **$\pm \$26.97$** | Mức chênh lệch trung bình từng đơn hàng |
| **RMSE** | $\$135.10$ | **$\$126.45$** | Thước đo phạt nặng các đơn hàng bất thường |

### 5️⃣ Bước 5 – Dự báo Lợi nhuận 3 Tháng tiếp theo
Re-train trên 100% dữ liệu lịch sử và kết hợp với tốc độ tăng trưởng doanh thu hàng tháng:

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
# Kích hoạt môi trường venv
.\.venv\Scripts\Activate.ps1

# Cài đặt các thư viện cần thiết
pip install pandas numpy scikit-learn matplotlib seaborn jupyter ipykernel
```

### 3. Đăng ký Kernel Jupyter
```powershell
python -m ipykernel install --user --name "module4-venv" --display-name "Python (Module4 venv)"
```

### 4. Chạy Dự án

#### 👉 Chạy bằng Script Python tự động:
```powershell
python scripts/profit_forecast.py
```

#### 👉 Chạy bằng Jupyter Lab:
```powershell
jupyter lab
```
1. Truy cập thư mục `notebooks/`.
2. Mở notebook `profit_forecast_notebook.ipynb`.
3. Chọn Kernel **`Python (Module4 venv)`** ở góc trên bên phải.
4. Chọn **`Kernel` → `Restart Kernel and Run All Cells...`**.

---

## 📑 Tài liệu Tham khảo

- 📄 [Báo cáo chi tiết dataset (reports/superstore_report.md)](./reports/superstore_report.md) — Data Dictionary & Cleaning Pipeline
- 📄 [So sánh Raw vs Cleaned (reports/data_comparison.md)](./reports/data_comparison.md) — Bảng đối chiếu trước/sau làm sạch

---

<p center="align">
  <i>© 2026 Nhóm THEMIS — Module 4 KADA (TuIT-198)</i>
</p>
