import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("data/telco_churn.csv")

# Page title
st.title("📉 Customer Churn Predictor Dashboard")
with st.expander("ℹ️ About this app"):
    st.markdown("""
    This dashboard helps visualize customer churn trends using the Telco dataset.  
    Use the sidebar to filter by contract type and gain insights from interactive visualizations.
    """)
# Replace spaces in column names
df.columns = df.columns.str.replace(' ', '_')

# --- 1. Basic Churn Stats ---
st.subheader("🔍 Churn Summary")

# Churn counts
churn_counts = df['Churn'].value_counts()
st.write("### Churn Breakdown")
st.bar_chart(churn_counts)

# Churn Rate
churn_rate = churn_counts.get("Yes", 0) / churn_counts.sum()
st.metric(label="📊 Churn Rate", value=f"{churn_rate:.2%}")

# Optional Pie Chart
fig = px.pie(df, names='Churn', title='🔄 Churn Distribution')
st.plotly_chart(fig, use_container_width=True)

# --- 2. Filter by Contract Type ---
st.sidebar.header("📋 Filter Options")
selected_contract = st.sidebar.selectbox("Choose contract type", df['Contract'].unique())
filtered_df = df[df['Contract'] == selected_contract]

st.write(f"Showing results for **{selected_contract}** contract")

# --- 3. Churn by Internet Service ---
st.subheader("🌐 Churn by Internet Service Type")
internet_churn = filtered_df.groupby(['InternetService', 'Churn']).size().unstack().fillna(0)
st.bar_chart(internet_churn)

# --- 4. Monthly Charges vs. Churn ---
st.subheader("💵 Monthly Charges Comparison")
fig = px.box(
    filtered_df,
    x='Churn',
    y='MonthlyCharges',
    color='Churn',
    title='💵 Monthly Charges vs Churn'
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- 5. Download Filtered Data ---
st.subheader("⬇️ Download Filtered Dataset")
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download CSV",
    data=csv,
    file_name='filtered_churn_data.csv',
    mime='text/csv'
)

# --- 6. Churn Rate by Contract Type ---
st.subheader("📊 Churn Rate by Contract Type")
contract_churn = filtered_df.groupby("Contract")["Churn"].value_counts(normalize=True).unstack().fillna(0)
contract_churn = contract_churn.reset_index()

fig = px.bar(
    contract_churn,
    x="Contract",
    y="Yes",
    color="Contract",
    labels={"Yes": "Churn Rate"},
    title="📉 Churn Rate by Contract Type"
)
st.plotly_chart(fig, use_container_width=True)

# --- 7. Best Optional Insight: Churn Rate by Internet Service ---
st.subheader("📶 Churn Rate by Internet Service")
internet_churn = filtered_df.groupby("InternetService")["Churn"].value_counts(normalize=True).unstack().fillna(0)
internet_churn = internet_churn.reset_index()

fig = px.bar(
    internet_churn,
    x="InternetService",
    y="Yes",
    color="InternetService",
    labels={"Yes": "Churn Rate"},
    title="🌐 Churn Rate by Internet Service"
)
st.plotly_chart(fig, use_container_width=True)

# --- 8. Correlation Heatmap (Numerical Features vs. Churn) ---
st.subheader("📊 Correlation Heatmap")

# Convert 'Churn' to numeric for correlation
corr_df = filtered_df.copy()
corr_df['Churn'] = corr_df['Churn'].map({'Yes': 1, 'No': 0})

# Select only numerical features
num_cols = corr_df.select_dtypes(include='number')
corr_matrix = num_cols.corr()

# Plot heatmap using plotly
fig = px.imshow(
    corr_matrix,
    text_auto=True,
    color_continuous_scale='RdBu_r',
    title='📈 Correlation Heatmap'
)
st.plotly_chart(fig, use_container_width=True)

# --- 9. Download Insights as CSV ---
st.subheader("📥 Download Churn Insights")

churn_contract_export = contract_churn.copy()
churn_internet_export = internet_churn.copy()

churn_contract_export['Insight'] = 'Churn by Contract'
churn_internet_export['Insight'] = 'Churn by Internet Service'

final_insights = pd.concat([churn_contract_export, churn_internet_export], ignore_index=True)

csv = final_insights.to_csv(index=False).encode('utf-8')
st.download_button("📥 Download Churn Insights (CSV)", data=csv, file_name="churn_insights.csv", mime="text/csv")

st.markdown("---")
st.markdown("🚀 Built by [Mohammed Taqi Uddin Farz](https://github.com/yourprofile) | Powered by Streamlit & Plotly")
