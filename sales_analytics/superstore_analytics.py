import pandas as pd
import numpy as np
import json
import os

def run_analysis():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "Superstore_clean.csv")
    output_dir = base_dir
    
    print("Loading dataset...")
    df = pd.read_csv(csv_path)
    
    # 1. Feature Engineering
    print("Performing Feature Engineering...")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    
    # Temporal
    df['Year_Month'] = df['Order Date'].dt.to_period('M').astype(str)
    df['Day_Of_Week'] = df['Order Date'].dt.day_name()
    df['Is_Weekend'] = df['Order Date'].dt.dayofweek.isin([5, 6]).astype(int)
    
    def get_seasonality(q):
        if q in [1, 2]:
            return 'Low Season (Q1-Q2)'
        elif q == 3:
            return 'Mid Season (Q3)'
        else:
            return 'Peak Season (Q4)'
            
    df['Seasonality_Phase'] = df['Quarter'].apply(get_seasonality)
    
    # Financial & Discount
    # Gross Sales = Sales / (1 - Discount) if Discount < 1 else Sales
    df['Gross_Sales'] = np.where(df['Discount'] < 1.0, df['Sales'] / (1.0 - df['Discount']), df['Sales'])
    df['Discount_Amount'] = df['Gross_Sales'] - df['Sales']
    
    def get_discount_tier(d):
        if d == 0:
            return 'No Discount (0%)'
        elif d <= 0.15:
            return 'Low Discount (0-15%)'
        elif d <= 0.30:
            return 'Medium Discount (15-30%)'
        else:
            return 'Heavy Discount (>30%)'
            
    df['Discount_Tier'] = df['Discount'].apply(get_discount_tier)
    df['Profit_Margin_%'] = np.where(df['Sales'] > 0, (df['Profit'] / df['Sales']) * 100, 0)
    
    def get_profit_tier(pm):
        if pm < -20:
            return 'Heavy Loss (<-20%)'
        elif pm < 0:
            return 'Minor Loss (-20% to 0%)'
        elif pm <= 25:
            return 'Profitable (0% to 25%)'
        else:
            return 'High Profit (>25%)'
            
    df['Profit_Tier'] = df['Profit_Margin_%'].apply(get_profit_tier)
    
    # Product & Order Dynamics
    df['Unit_Price'] = np.where(df['Quantity'] > 0, df['Gross_Sales'] / df['Quantity'], 0)
    
    # Order Basket Size
    order_totals = df.groupby('Order ID')['Sales'].sum().to_dict()
    df['Total_Order_Value'] = df['Order ID'].map(order_totals)
    
    def get_basket_size(val):
        if val < 100:
            return 'Small Order (<$100)'
        elif val <= 500:
            return 'Medium Order ($100-$500)'
        elif val <= 2000:
            return 'Large Order ($500-$2000)'
        else:
            return 'Enterprise Order (>$2000)'
            
    df['Order_Basket_Size'] = df['Total_Order_Value'].apply(get_basket_size)
    
    # Customer Profiling & Retention
    cust_orders = df.groupby('Customer ID')['Order ID'].nunique().to_dict()
    df['Customer_Order_Count'] = df['Customer ID'].map(cust_orders)
    
    def get_loyalty_tier(c):
        if c == 1:
            return 'New / 1-Time'
        elif c <= 4:
            return 'Repeat (2-4)'
        else:
            return 'VIP (>=5)'
            
    df['Customer_Loyalty_Tier'] = df['Customer_Order_Count'].apply(get_loyalty_tier)
    
    cust_clv = df.groupby('Customer ID')['Sales'].sum().to_dict()
    df['Customer_CLV'] = df['Customer ID'].map(cust_clv)
    
    # Top 20% Customers Pareto
    top_20_cutoff = df.groupby('Customer ID')['Sales'].sum().quantile(0.80)
    df['Is_Top_20_VIP'] = df['Customer_CLV'] >= top_20_cutoff
    
    max_date = df['Order Date'].max()
    cust_last_date = df.groupby('Customer ID')['Order Date'].max().to_dict()
    df['Recency_Days'] = (max_date - df['Customer ID'].map(cust_last_date)).dt.days
    
    # Geographical Market Tier
    state_sales = df.groupby('State')['Sales'].sum().quantile([0.33, 0.66])
    q33, q66 = state_sales.iloc[0], state_sales.iloc[1]
    
    def get_state_tier(state_name):
        val = df[df['State'] == state_name]['Sales'].sum()
        if val >= q66:
            return 'Tier 1 Key State'
        elif val >= q33:
            return 'Tier 2 Secondary State'
        else:
            return 'Tier 3 Niche State'
            
    state_tiers = {s: get_state_tier(s) for s in df['State'].unique()}
    df['State_Sales_Tier'] = df['State'].map(state_tiers)
    
    # Save enriched dataset
    enriched_path = os.path.join(output_dir, "Superstore_enriched.csv")
    df.to_csv(enriched_path, index=False)
    print(f"Enriched dataset saved to: {enriched_path}")
    
    # Summary Insights Output
    print("\n================== EXECUTIVE SALES SUMMARY ==================")
    print(f"Total Sales: ${df['Sales'].sum():,.2f}")
    print(f"Total Profit: ${df['Profit'].sum():,.2f}")
    print(f"Overall Profit Margin: {(df['Profit'].sum() / df['Sales'].sum()) * 100:.2f}%")
    print(f"Total Orders: {df['Order ID'].nunique():,}")
    print(f"Total Customers: {df['Customer ID'].nunique():,}")
    
    print("\n--- Seasonality Breakdown ---")
    seasonality = df.groupby('Seasonality_Phase')['Sales'].agg(['sum', 'count']).rename(columns={'sum': 'Total_Sales', 'count': 'Line_Items'})
    seasonality['Pct_Sales'] = (seasonality['Total_Sales'] / df['Sales'].sum()) * 100
    print(seasonality)
    
    print("\n--- Discount Tier vs Profitability ---")
    discount_perf = df.groupby('Discount_Tier')[['Sales', 'Profit']].sum()
    discount_perf['Margin_%'] = (discount_perf['Profit'] / discount_perf['Sales']) * 100
    print(discount_perf)
    
    print("\n--- Top Loss-Making Sub-Categories under Heavy Discount ---")
    heavy_disc = df[df['Discount'] > 0.15].groupby('Sub-Category')[['Sales', 'Profit', 'Discount']].agg({'Sales': 'sum', 'Profit': 'sum', 'Discount': 'mean'}).sort_values('Profit')
    print(heavy_disc.head(5))
    
    print("\n--- At-Risk Customers (> 180 Days Recency) ---")
    at_risk = df[df['Recency_Days'] > 180]['Customer ID'].nunique()
    print(f"Number of At-Risk Customers: {at_risk} ({at_risk / df['Customer ID'].nunique() * 100:.1f}% of total customers)")
    
    print("\nData enrichment and analysis complete!")

if __name__ == '__main__':
    run_analysis()
