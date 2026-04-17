import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📊 Retail Sales Forecasting and Inventory Analytics System")
st.caption("Forecasting • Inventory Optimization • Decision Support")

# ---------------- LOAD DATA ----------------
df = pd.read_csv("outputs/inventory_plan.csv")
future_df = pd.read_csv("outputs/future_forecast.csv")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Filters")

store = st.sidebar.multiselect("Select Store", df['store'].unique(), default=df['store'].unique())
product = st.sidebar.multiselect("Select Product", df['product'].unique(), default=df['product'].unique())
category = st.sidebar.selectbox("Category", ["All"] + list(df['category'].unique()))


filtered_df = df.copy()

if store:
    filtered_df = filtered_df[filtered_df['store'].isin(store)]

if product:
    filtered_df = filtered_df[filtered_df['product'].isin(product)]

if category != "All":
    filtered_df = filtered_df[filtered_df['category'] == category]


# ---------------- KPIs ----------------
col1, col2, col3, col4 = st.columns(4)

total = int(filtered_df['predicted_sales'].sum())
avg = int(filtered_df['predicted_sales'].mean())
max_val = int(filtered_df['reorder_point'].max())
risk = (filtered_df['stock_risk']=="HIGH").sum()

col1.metric("Total Demand", total, help="Overall predicted demand volume")
col2.metric("Avg Demand", avg, help="Average daily demand per item")
col3.metric("Max Reorder", max_val, help="Highest stock requirement level")
col4.metric("High Risk Items", risk, help="Products needing urgent attention")

# Add interpretation
st.caption(f"📊 Demand is {'HIGH' if avg > 150 else 'MODERATE' if avg > 100 else 'LOW'} | {risk} items need attention")

st.divider()

# ---------------- ROW 1 (SIDE BY SIDE) ----------------
col1, col2 = st.columns(2)

with col1:
   trend_df = filtered_df.groupby("date")['predicted_sales'].mean().reset_index()

fig = px.line(
    trend_df,
    x="date",
    y="predicted_sales",
    title="Demand Trend (Avg per Day)"
)

st.plotly_chart(fig, use_container_width=True)


with col2:
    diff_df = filtered_df.groupby("date")['actual_vs_predicted_diff'].mean().reset_index()

fig = px.line(
    diff_df,
    x="date",
    y="actual_vs_predicted_diff",
    title="Prediction Error Trend"
)

st.plotly_chart(fig, use_container_width=True)
    

st.divider()

# ---------------- ROW 2 ----------------
col1, col2 = st.columns(2)

with col1:
    fig = px.bar(filtered_df.groupby("category")['predicted_sales'].sum().reset_index(),
                 x="category", y="predicted_sales",
                 title="Category Demand")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(filtered_df.groupby("store")['predicted_sales'].sum().reset_index(),
                 x="store", y="predicted_sales",
                 title="Store Performance")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------- COMPACT HEATMAP + FUTURE ----------------
col1, col2 = st.columns(2)

with col1:
    pivot = filtered_df.pivot_table(
        values='predicted_sales',
        index='store',
        columns='product',
        aggfunc='sum'
    )
    fig = px.imshow(pivot, text_auto=True, title="Demand Heatmap")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # filter-based forecast simulation
    avg = filtered_df['predicted_sales'].mean()

    future_df['adjusted_forecast'] = future_df['predicted_sales'] * (avg / df['predicted_sales'].mean())

    fig = px.line(future_df, x="date", y="adjusted_forecast",
              title="Next 7 Days Forecast (Adjusted to Selection)")
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------- SMART ACTION PANEL ----------------
st.subheader("📢 Inventory Action Center")

high_risk = filtered_df[filtered_df['stock_risk']=="HIGH"]
low_demand = filtered_df[filtered_df['stock_risk']=="LOW"]

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔴 High Demand Risk")
    if len(high_risk) > 0:
        st.error(f"{len(high_risk)} items require urgent restocking")
        st.dataframe(high_risk[['store','product','predicted_sales','reorder_point']].head(5))
    else:
        st.info("No critical high-demand risk detected")

with col2:
    st.markdown("### 🟡 Low Demand / Overstock Risk")
    if len(low_demand) > 0:
        st.warning(f"{len(low_demand)} items may lead to overstock")
        st.dataframe(low_demand[['store','product','predicted_sales']].head(5))
    else:
        st.info("No overstock risk detected")

st.divider()

# ---------------- RECOMMENDED ACTIONS ----------------
st.subheader("📢 Recommended Actions")

high_risk = filtered_df[filtered_df['stock_risk']=="HIGH"]
low_demand = filtered_df[filtered_df['stock_risk']=="LOW"]

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔴 Immediate Restocking Required")
    if len(high_risk) > 0:
        top_critical = high_risk.sort_values(by="predicted_sales", ascending=False).head(5)
        st.dataframe(top_critical[['store','product','predicted_sales','reorder_point']])
        st.write(f"➡ High demand surge detected. Recommend increasing stock by ~{int(high_risk['predicted_sales'].mean()*0.2)} units.")
    else:
        st.info("No immediate restocking required")

with col2:
    st.markdown("### 🟡 Overstock Risk Management")
    if len(low_demand) > 0:
        st.dataframe(low_demand[['store','product','predicted_sales']].head(5))
        st.write("➡ Consider reducing inventory or applying discounts to clear stock.")
    else:
        st.info("No overstock risk detected")

# ---------------- KEY INSIGHTS ----------------
st.subheader("📌 Key Insights")

store_data = filtered_df.groupby("store")['predicted_sales'].sum()
product_data = filtered_df.groupby("product")['predicted_sales'].sum()

st.write(f"""
- 🏬 Highest demand store: **{store_data.idxmax()}**
- 📉 Lowest demand store: **{store_data.idxmin()}**
- 🛍 Top selling product: **{product_data.idxmax()}**
- 📦 Least selling product: **{product_data.idxmin()}**
- ⚠ High-risk items: **{(filtered_df['stock_risk']=='HIGH').sum()}**
- 🟡 Low-demand items: **{(filtered_df['stock_risk']=='LOW').sum()}**
- 📊 Avg daily demand: **{int(filtered_df['predicted_sales'].mean())} units**
""")

st.divider()

# ---------------- DATA ----------------
col1, col2 = st.columns(2)

# Define useful columns
cols = ['store','product','reorder_point','stock_risk']

with col1:
    st.subheader("🔴 High Demand")
    high_df = filtered_df.sort_values(by="predicted_sales", ascending=False)
    st.dataframe(high_df[cols].head(10))

with col2:
    st.subheader("🟡 Low Demand")
    low_df = filtered_df.sort_values(by="predicted_sales")
    st.dataframe(low_df[cols].head(10))

# ---------------- DOWNLOAD ----------------
st.download_button(
    label="Download Report",
    data=filtered_df.to_csv(index=False),
    file_name="inventory_report.csv"
)