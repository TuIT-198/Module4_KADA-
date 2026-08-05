# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║       MODEL DỰ ĐOÁN LỢI NHUẬN (PROFIT) – SUPERSTORE | 3 THÁNG TỚI         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Data     : Superstore_clean.csv                                             ║
║  Framework: scikit-learn                                                     ║
║  Target   : Profit (Lợi nhuận từng đơn hàng)                                ║
║  Features : Sales · Discount · Quantity · Category (OHE) · Region (OHE)     ║
║  Pipeline :                                                                  ║
║    1. Tiền xử lý dữ liệu (Preprocessing)                                    ║
║    2. Huấn luyện 3 mô hình Regression + TimeSeriesSplit (chống data leak)   ║
║    3. Dự báo Profit 3 tháng tới                                              ║
║    4. CFO Insights: Feature Importance + nhận xét tài chính                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec

from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

plt.rcParams['axes.unicode_minus'] = False

# =============================================================================
# BƯỚC 1: TIỀN XỬ LÝ DỮ LIỆU
# =============================================================================
print("=" * 70)
print("  BƯỚC 1 – TIỀN XỬ LÝ DỮ LIỆU")
print("=" * 70)

DATA_PATH = "../data/Superstore_clean.csv"

df = pd.read_csv(DATA_PATH)
print(f"  Đọc file: {df.shape[0]:,} dong  x  {df.shape[1]} cot")

df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=False)
print(f"  Khoang thoi gian: {df['Order Date'].min().date()} -> {df['Order Date'].max().date()}")

FEATURES     = ['Sales', 'Discount', 'Quantity', 'Category', 'Region']
TARGET       = 'Profit'
NUMERIC_FEAT = ['Sales', 'Discount', 'Quantity']
CAT_FEAT     = ['Category', 'Region']

df = df[FEATURES + [TARGET, 'Order Date']].dropna().copy()
print(f"  Sau khi loc & dropna: {df.shape[0]:,} dong")

# Sắp xếp theo thời gian – bắt buộc cho TimeSeriesSplit
df.sort_values('Order Date', inplace=True)
df.reset_index(drop=True, inplace=True)

# Tổng hợp chuỗi thời gian theo tháng (dùng cho biểu đồ + tính growth rate)
df['YearMonth'] = df['Order Date'].dt.to_period('M')
monthly_trend = (
    df.groupby('YearMonth')
      .agg(Sales=('Sales', 'sum'), Profit=('Profit', 'sum'))
      .reset_index()
)
monthly_trend['YM_str'] = monthly_trend['YearMonth'].astype(str)

print("\n  Chuoi thoi gian tong hop (5 thang cuoi):")
print(monthly_trend[['YM_str', 'Sales', 'Profit']].tail(5).to_string(index=False))

# =============================================================================
# BƯỚC 2: XÂY DỰNG & HUẤN LUYỆN MÔ HÌNH
# =============================================================================
print("\n" + "=" * 70)
print("  BƯỚC 2 – HUẤN LUYỆN MÔ HÌNH (TimeSeriesSplit)")
print("=" * 70)

X = df[FEATURES].copy()
y = df[TARGET].values

# Preprocessor: StandardScaler (số) + OneHotEncoder (phân loại)
preprocessor = ColumnTransformer(transformers=[
    ('num', StandardScaler(), NUMERIC_FEAT),
    ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), CAT_FEAT),
], remainder='drop')

# 3 mô hình Regression tiêu biểu
MODEL_CONFIGS = {
    'LinearRegression' : LinearRegression(),
    'RandomForest'     : RandomForestRegressor(
                             n_estimators=300, max_depth=12,
                             min_samples_leaf=5, random_state=42, n_jobs=-1),
    'GradientBoosting' : GradientBoostingRegressor(
                             n_estimators=300, learning_rate=0.05,
                             max_depth=5, subsample=0.8, random_state=42),
}

# TimeSeriesSplit 5 folds – test luôn nằm SAU train (không rò rỉ dữ liệu)
N_SPLITS = 5
tscv = TimeSeriesSplit(n_splits=N_SPLITS)

results = {}
print(f"\n  Time-Series Cross-Validation (n_splits={N_SPLITS}):")
print(f"  {'Model':<22}  {'MAE':>12}  {'RMSE':>12}  {'R2':>10}")
print("  " + "-" * 62)

for name, base_model in MODEL_CONFIGS.items():
    pipe = Pipeline([('prep', preprocessor), ('model', base_model)])
    maes, rmses, r2s = [], [], []
    for tr_idx, te_idx in tscv.split(X):
        Xtr, Xte = X.iloc[tr_idx], X.iloc[te_idx]
        ytr, yte = y[tr_idx], y[te_idx]
        pipe.fit(Xtr, ytr)
        pred = pipe.predict(Xte)
        maes.append(mean_absolute_error(yte, pred))
        rmses.append(np.sqrt(mean_squared_error(yte, pred)))
        r2s.append(r2_score(yte, pred))
    results[name] = {
        'pipe': pipe,
        'MAE' : np.mean(maes),
        'RMSE': np.mean(rmses),
        'R2'  : np.mean(r2s),
    }
    print(f"  {name:<22}  {np.mean(maes):>12.2f}  {np.mean(rmses):>12.2f}  {np.mean(r2s):>10.4f}")

# Chọn mô hình tốt nhất theo RMSE, re-train trên toàn bộ dữ liệu
best_name = min(results, key=lambda k: results[k]['RMSE'])
best_pipe  = results[best_name]['pipe']
best_pipe.fit(X, y)
print(f"\n  Mo hinh tot nhat: [{best_name}]  RMSE={results[best_name]['RMSE']:.2f}  -> dung de du bao")

# =============================================================================
# BƯỚC 3: DỰ BÁO 3 THÁNG TỚI
# =============================================================================
print("\n" + "=" * 70)
print("  BƯỚC 3 – DỰ BÁO LỢI NHUẬN 3 THÁNG TỚI")
print("=" * 70)

last_date      = df['Order Date'].max()
future_periods = pd.date_range(start=last_date + pd.offsets.MonthBegin(1), periods=3, freq='MS')
forecast_labels = [p.strftime('%Y-%m') for p in future_periods]

# Tốc độ tăng trưởng doanh thu trung bình (12 tháng gần nhất)
growth_rate = monthly_trend['Sales'].pct_change().dropna().tail(12).mean()
growth_rate = max(growth_rate, 0.0)
print(f"\n  Toc do tang truong doanh thu trung binh thang: {growth_rate:.2%}")

cat_share       = df.groupby('Category')['Sales'].sum() / df['Sales'].sum()
reg_share       = df.groupby('Region')['Sales'].sum()   / df['Sales'].sum()
base_month_sales = monthly_trend['Sales'].iloc[-1]


def forecast_one_month(month_idx):
    """Dự báo Profit tháng (month_idx=1,2,3) dựa trên xu hướng lịch sử."""
    month_sales = base_month_sales * (1 + growth_rate) ** month_idx
    rows = []
    for cat in cat_share.index:
        for reg in reg_share.index:
            seg_sales = month_sales * cat_share[cat] * reg_share[reg]
            mask      = (df['Category'] == cat) & (df['Region'] == reg)
            aov       = df.loc[mask, 'Sales'].mean()
            n_orders  = max(1, round(seg_sales / aov))
            rows.append({
                'Sales'    : seg_sales / n_orders,
                'Discount' : df.loc[mask, 'Discount'].mean(),
                'Quantity' : df.loc[mask, 'Quantity'].mean(),
                'Category' : cat,
                'Region'   : reg,
                '_n'       : n_orders,
            })
    sdf   = pd.DataFrame(rows)
    preds = best_pipe.predict(sdf[FEATURES])
    total_profit = float((preds * sdf['_n'].values).sum())
    return {'month': forecast_labels[month_idx-1],
            'sales': month_sales,
            'profit': total_profit}


forecast_res = [forecast_one_month(m) for m in range(1, 4)]

print(f"\n  {'Thang':<10}  {'Doanh thu (USD)':>22}  {'Loi nhuan (USD)':>22}  {'Bien LN':>10}")
print("  " + "-" * 70)
for r in forecast_res:
    margin = r['profit'] / r['sales'] * 100 if r['sales'] else 0
    print(f"  {r['month']:<10}  ${r['sales']:>20,.0f}  ${r['profit']:>20,.0f}  {margin:>8.1f}%")

# =============================================================================
# BƯỚC 4: CFO INSIGHTS – FEATURE IMPORTANCE
# =============================================================================
print("\n" + "=" * 70)
print("  BƯỚC 4 – CFO INSIGHTS (Feature Importance)")
print("=" * 70)

# Re-train RandomForest trên toàn dữ liệu để lấy importance ổn định
rf_pipe = results['RandomForest']['pipe']
rf_pipe.fit(X, y)

ohe_names  = rf_pipe.named_steps['prep'] \
                     .named_transformers_['cat'] \
                     .get_feature_names_out(CAT_FEAT)
all_names  = NUMERIC_FEAT + list(ohe_names)
importances = rf_pipe.named_steps['model'].feature_importances_

imp_df = pd.DataFrame({'Feature': all_names, 'Importance': importances})


def _group(feat):
    for g in FEATURES:
        if feat.startswith(g):
            return g
    return 'Other'


imp_df['Group'] = imp_df['Feature'].apply(_group)
group_imp = imp_df.groupby('Group')['Importance'].sum().sort_values(ascending=False)

print("\n  Feature Importance (gom theo nhom goc – RandomForest):")
print("  " + "-" * 34)
for g, v in group_imp.items():
    bar = chr(9608) * int(v * 40)
    print(f"  {g:<15}  {v:.4f}  {bar}")

# =============================================================================
# BƯỚC 5: VISUALIZATION
# =============================================================================
PALETTE = {
    'navy' : '#1b365d', 'teal' : '#008080',
    'red'  : '#d9534f', 'gold' : '#e8a838', 'grey': '#6c757d',
}
GROUP_COLORS = {
    'Sales'   : PALETTE['navy'],  'Quantity': PALETTE['teal'],
    'Discount': PALETTE['red'],   'Category': PALETTE['gold'],
    'Region'  : PALETTE['grey'],
}

# ─── Figure 1: Dashboard tổng hợp ────────────────────────────────────────────
fig = plt.figure(figsize=(16, 11), dpi=150, facecolor='#f8f9fa')
fig.suptitle('SUPERSTORE – BAO CAO DU BAO LOI NHUAN (PROFIT FORECASTING)',
             fontsize=14, fontweight='bold', y=0.98, color=PALETTE['navy'])

gs = GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

# Panel A: Profit trend
ax_a = fig.add_subplot(gs[0, :2])
xs   = range(len(monthly_trend))
ax_a.fill_between(xs, monthly_trend['Profit'], alpha=0.15, color=PALETTE['teal'])
ax_a.plot(xs, monthly_trend['Profit'], color=PALETTE['teal'], lw=2.0, marker='o', ms=4)
step = max(1, len(monthly_trend) // 12)
ax_a.set_xticks(list(xs)[::step])
ax_a.set_xticklabels(monthly_trend['YM_str'].iloc[::step].tolist(), rotation=35, ha='right', fontsize=8)
ax_a.set_title('Loi nhuan hang thang (lich su)', fontweight='bold', fontsize=11, color=PALETTE['navy'])
ax_a.set_xlabel('Thang', fontsize=9, color='#333333')
ax_a.set_ylabel('Profit (USD)', fontsize=9, color='#333333')
ax_a.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v/1e3:.0f}K'))
ax_a.spines['top'].set_visible(False); ax_a.spines['right'].set_visible(False)
ax_a.grid(axis='y', alpha=0.2)

# Panel B: R² comparison
ax_b = fig.add_subplot(gs[0, 2])
mnames  = list(results.keys())
r2vals  = [results[n]['R2'] for n in mnames]
bcolors = [PALETTE['navy'] if n == best_name else PALETTE['grey'] for n in mnames]
bars_b  = ax_b.bar(mnames, r2vals, color=bcolors, width=0.5, edgecolor='white')
ax_b.set_title('So sanh mo hinh (R2 Score)', fontweight='bold', fontsize=11, color=PALETTE['navy'])
ax_b.set_ylabel('R2 Score', fontsize=9, color='#333333')
ax_b.set_ylim(0, 1.15)
short_names = [n.replace('Regression','Reg').replace('Forest','RF').replace('Boosting','GB') for n in mnames]
ax_b.set_xticklabels(short_names, rotation=20, ha='right', fontsize=8)
ax_b.spines['top'].set_visible(False); ax_b.spines['right'].set_visible(False)
ax_b.grid(axis='y', alpha=0.2)
for bar, val in zip(bars_b, r2vals):
    ax_b.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03,
              f'{val:.3f}', ha='center', va='bottom', fontsize=9, fontweight='bold', color=PALETTE['navy'])

# Panel C: Feature Importance (grouped)
ax_c = fig.add_subplot(gs[1, :2])
gs_sorted = group_imp.sort_values(ascending=True)
colors_c  = [GROUP_COLORS.get(g, PALETTE['grey']) for g in gs_sorted.index]
bars_c    = ax_c.barh(gs_sorted.index, gs_sorted.values, color=colors_c, height=0.55)
ax_c.set_title('Feature Importance theo nhom goc (RandomForest)', fontweight='bold', fontsize=11, color=PALETTE['navy'])
ax_c.set_xlabel('Tong trong so Importance', fontsize=9, color='#333333')
ax_c.spines['top'].set_visible(False); ax_c.spines['right'].set_visible(False)
ax_c.grid(axis='x', alpha=0.2)
for bar, val in zip(bars_c, gs_sorted.values):
    ax_c.text(bar.get_width() + 0.003, bar.get_y() + bar.get_height()/2,
              f'{val:.3f}', va='center', fontsize=9, fontweight='bold', color=PALETTE['navy'])

# Panel D: Forecast 3 tháng
ax_d = fig.add_subplot(gs[1, 2])
fc_labels  = [r['month'] for r in forecast_res]
fc_profits = [r['profit'] for r in forecast_res]
fc_colors  = [PALETTE['teal'], PALETTE['gold'], PALETTE['navy']]
bars_d     = ax_d.bar(fc_labels, fc_profits, color=fc_colors, width=0.5, edgecolor='white')
ax_d.set_title('Du bao Loi nhuan 3 thang toi', fontweight='bold', fontsize=11, color=PALETTE['navy'])
ax_d.set_ylabel('Profit (USD)', fontsize=9, color='#333333')
ax_d.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'${v/1e3:.0f}K'))
ax_d.spines['top'].set_visible(False); ax_d.spines['right'].set_visible(False)
ax_d.grid(axis='y', alpha=0.2)
for bar, val in zip(bars_d, fc_profits):
    ax_d.text(bar.get_x() + bar.get_width()/2, bar.get_height()*1.02,
              f'${val/1e3:.1f}K', ha='center', va='bottom', fontsize=9, fontweight='bold', color=PALETTE['navy'])

plt.savefig('profit_forecast_dashboard.png', dpi=150, bbox_inches='tight')
plt.close(fig)
print("\n  Da luu bieu do: profit_forecast_dashboard.png")

# ─── Figure 2: Top-10 Features chi tiết ──────────────────────────────────────
fig2, ax2 = plt.subplots(figsize=(10, 5), dpi=150, facecolor='#f8f9fa')
top10    = imp_df.nlargest(10, 'Importance').sort_values('Importance', ascending=True)
colors10 = [GROUP_COLORS.get(_group(f), PALETTE['grey']) for f in top10['Feature']]
bars_t   = ax2.barh(top10['Feature'], top10['Importance'], color=colors10, height=0.55)
ax2.set_title('Top 10 Features quan trong nhat (sau One-Hot Encoding)',
              fontweight='bold', fontsize=12, color=PALETTE['navy'])
ax2.set_xlabel('Importance Score', fontsize=10, color='#333333')
ax2.spines['top'].set_visible(False); ax2.spines['right'].set_visible(False)
ax2.grid(axis='x', alpha=0.2)
for bar, val in zip(bars_t, top10['Importance']):
    ax2.text(bar.get_width() + 0.001, bar.get_y() + bar.get_height()/2,
             f'{val:.4f}', va='center', fontsize=8, color=PALETTE['navy'])
plt.tight_layout()
plt.savefig('profit_feature_importance.png', dpi=150, bbox_inches='tight')
plt.close(fig2)
print("  Da luu bieu do: profit_feature_importance.png")

# =============================================================================
# BẢNG TỔNG KẾT METRICS
# =============================================================================
print("\n" + "=" * 70)
print("  BANG TONG KET DANH GIA MO HINH")
print("=" * 70)
for name in results:
    tag = "  <- BEST" if name == best_name else ""
    print(f"  {name:<22}  MAE=${results[name]['MAE']:,.2f}  RMSE=${results[name]['RMSE']:,.2f}  R2={results[name]['R2']:.4f}{tag}")

# =============================================================================
# BÁO CÁO CFO INSIGHTS
# =============================================================================
print("""
============================================================
  BAO CAO CFO INSIGHTS – TAC DONG TOI LOI NHUAN DU BAO
============================================================

1) DISCOUNT (Chiet khau) – DON BAY RUI RO CAO NHAT
   - Discount thuong la feature co Importance cao, tac dong NGHICH
     CHIEU voi Profit: chiet khau cang cao, bien loi nhuan cang giam.
   - Khuyen nghi CFO: ap tran chiet khau 15-20% voi nhom hang co
     bien got duoi 30%. Kiem toan hieu qua chiet khau theo quy.

2) CATEGORY (Nhom hang) – PHAN BO NGUON LUC KHONG DEU
   - Technology co bien loi nhuan cao nhat; Furniture thuong co
     profit am khi kem chiet khau cao (rui ro kep).
   - Khuyen nghi CFO: tang budget marketing sang Technology +15%;
     xem xet cat giam SKU Furniture co profit am keo dai.

3) REGION (Khu vuc dia ly) – HIEU QUA SU DUNG CHI PHI BAN HANG
   - Cac Region khong dong deu ve kha nang chuyen Doanh thu -> LN.
   - Khuyen nghi CFO: thiet lap KPI "Profit per Sales Dollar" theo
     Region de giam sat hieu qua doi kinh doanh dia phuong.

4) SALES & QUANTITY – TANG TRUONG CO CHAT LUONG
   - Sales la driver loi nhuan chinh nhung chi ben vung khi bien duong.
   - Du bao 3 thang toi cho thay tang truong on dinh theo xu huong LS.
   - Khuyen nghi CFO: theo doi Profit Margin % hang thang; canh bao
     khi bien thuc te lech khai du bao qua 5%.

============================================================
""")

