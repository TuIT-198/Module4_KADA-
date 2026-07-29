import pandas as pd
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')

df = pd.read_csv('Superstore.csv', encoding='latin1')

print('=== NULL VALUES PER COLUMN ===')
null_counts = df.isnull().sum()
null_pct = (df.isnull().sum() / len(df) * 100).round(2)
null_df = pd.DataFrame({'Null Count': null_counts, 'Null %': null_pct})
print(null_df.to_string())

print()
print('=== DUPLICATES ===')
dupes = df.duplicated().sum()
print(f'Full duplicate rows: {dupes}')
dupes_orderid = df.duplicated(subset=['Order ID', 'Product ID']).sum()
print(f'Duplicate (Order ID + Product ID): {dupes_orderid}')

print()
print('=== DATE COLUMNS ===')
print('Order Date sample:', df['Order Date'].head(3).tolist())
print('Ship Date sample:', df['Ship Date'].head(3).tolist())

print()
print('=== NUMERIC COLUMNS STATS ===')
print(df[['Sales','Quantity','Discount','Profit']].describe().to_string())

print()
print('=== NEGATIVE VALUES ===')
print(f'Sales < 0: {(df["Sales"] < 0).sum()}')
print(f'Quantity < 0: {(df["Quantity"] < 0).sum()}')
print(f'Discount < 0 or > 1: {((df["Discount"] < 0) | (df["Discount"] > 1)).sum()}')
print(f'Profit < 0 (losses): {(df["Profit"] < 0).sum()}')

print()
print('=== UNIQUE VALUES PER CATEGORICAL COLUMN ===')
cat_cols = ['Segment','Category','Sub-Category','Region','Ship Mode','Country']
for col in cat_cols:
    print(f'{col} ({df[col].nunique()} unique): {df[col].unique().tolist()}')

print()
print('=== POSTAL CODE ===')
print(f'Postal Code dtype: {df["Postal Code"].dtype}')
print(f'Postal Code nulls: {df["Postal Code"].isnull().sum()}')
print(f'Postal Code sample: {df["Postal Code"].head(5).tolist()}')

print()
print('=== SHIPPING DATE LOGIC CHECK ===')
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True, errors='coerce')
df['Ship Date'] = pd.to_datetime(df['Ship Date'], dayfirst=True, errors='coerce')
ship_before_order = (df['Ship Date'] < df['Order Date']).sum()
print(f'Ship Date before Order Date: {ship_before_order}')
date_parse_errors = df['Order Date'].isnull().sum() + df['Ship Date'].isnull().sum()
print(f'Date parse errors: {date_parse_errors}')

print()
print('=== WHITESPACE IN STRING COLUMNS ===')
str_cols = df.select_dtypes(include='object').columns
for col in str_cols:
    stripped = df[col].str.strip()
    diff = (df[col] != stripped).sum()
    if diff > 0:
        print(f'{col}: {diff} rows with leading/trailing spaces')

print()
print('=== CHECKING ROW ID UNIQUENESS ===')
print(f'Row ID unique: {df["Row ID"].nunique()} / {len(df)} total rows')
