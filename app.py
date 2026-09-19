import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Nassau Candy Route Analysis",
    page_icon="🍫",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("🍫 Nassau Candy Route Analysis Dashboard")
st.markdown(
    "Interactive dashboard for analyzing sales, profit, shipments, "
    "factories, regions, products and shipping modes."
)


# =========================================================
# LOAD DATA
# =========================================================

DATA_FILE = "outputs/cleaned_nassau_data.csv"

try:
    df = pd.read_csv(DATA_FILE)
except FileNotFoundError:
    st.error(
        f"Dataset not found: {DATA_FILE}\n\n"
        "Please run `python analysis.py` first."
    )
    st.stop()


# =========================================================
# DATA PREPARATION
# =========================================================

# Convert numeric columns
numeric_columns = [
    "Sales",
    "Units",
    "Gross Profit",
    "Cost"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")


# Convert date columns
if "Order Date" in df.columns:
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

if "Ship Date" in df.columns:
    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        errors="coerce"
    )


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.header("🔎 Dashboard Filters")


# ---------------------------------------------------------
# Factory Filter
# ---------------------------------------------------------

factory_options = sorted(
    df["Factory"].dropna().unique()
)

selected_factory = st.sidebar.multiselect(
    "Select Factory",
    factory_options,
    default=factory_options
)


# ---------------------------------------------------------
# Region Filter
# ---------------------------------------------------------

region_options = sorted(
    df["Region"].dropna().unique()
)

selected_region = st.sidebar.multiselect(
    "Select Region",
    region_options,
    default=region_options
)


# ---------------------------------------------------------
# Ship Mode Filter
# ---------------------------------------------------------

ship_mode_options = sorted(
    df["Ship Mode"].dropna().unique()
)

selected_ship_mode = st.sidebar.multiselect(
    "Select Ship Mode",
    ship_mode_options,
    default=ship_mode_options
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df[
    (df["Factory"].isin(selected_factory))
    & (df["Region"].isin(selected_region))
    & (df["Ship Mode"].isin(selected_ship_mode))
].copy()



# =========================================================
# KPI CALCULATIONS
# =========================================================

total_sales = filtered_df["Sales"].sum()

total_units = filtered_df["Units"].sum()

total_profit = filtered_df["Gross Profit"].sum()

total_orders = filtered_df["Order ID"].nunique()


# =========================================================
# KPI SECTION
# =========================================================

st.subheader("📊 Key Performance Indicators")

kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "💰 Total Sales",
        f"${total_sales:,.2f}"
    )

with kpi2:
    st.metric(
        "📦 Total Units",
        f"{total_units:,.0f}"
    )

with kpi3:
    st.metric(
        "📈 Gross Profit",
        f"${total_profit:,.2f}"
    )

with kpi4:
    st.metric(
        "🧾 Total Orders",
        f"{total_orders:,.0f}"
    )


st.markdown("---")


# =========================================================
# FACTORY ANALYSIS
# =========================================================

st.subheader("🏭 Factory Performance")

factory_data = (
    filtered_df
    .groupby("Factory")
    .agg(
        Sales=("Sales", "sum"),
        Units=("Units", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)


fig_factory = px.bar(
    factory_data,
    x="Factory",
    y="Sales",
    title="Sales by Factory",
    text_auto=".2s"
)

fig_factory.update_layout(
    xaxis_title="Factory",
    yaxis_title="Sales",
    height=450
)

st.plotly_chart(
    fig_factory,
    width="stretch"
)


# =========================================================
# REGION ANALYSIS
# =========================================================

st.subheader("🌎 Region Performance")

region_data = (
    filtered_df
    .groupby("Region")
    .agg(
        Sales=("Sales", "sum"),
        Units=("Units", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)


fig_region = px.bar(
    region_data,
    x="Region",
    y="Sales",
    title="Sales by Region",
    text_auto=".2s"
)

fig_region.update_layout(
    xaxis_title="Region",
    yaxis_title="Sales",
    height=450
)

st.plotly_chart(
    fig_region,
    width="stretch"
)


# =========================================================
# SHIP MODE ANALYSIS
# =========================================================

st.subheader("🚚 Shipping Mode Analysis")

ship_mode_data = (
    filtered_df
    .groupby("Ship Mode")
    .agg(
        Orders=("Order ID", "nunique"),
        Sales=("Sales", "sum"),
        Profit=("Gross Profit", "sum")
    )
    .reset_index()
)


fig_ship = px.bar(
    ship_mode_data,
    x="Ship Mode",
    y="Orders",
    title="Orders by Ship Mode",
    text_auto=True
)

fig_ship.update_layout(
    xaxis_title="Ship Mode",
    yaxis_title="Orders",
    height=450
)

st.plotly_chart(
    fig_ship,
    width="stretch"
)


# =========================================================
# PRODUCT ANALYSIS
# =========================================================

st.subheader("🍬 Top Products by Sales")

product_data = (
    filtered_df
    .groupby("Product Name")
    .agg(
        Sales=("Sales", "sum"),
        Units=("Units", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
    .sort_values(
        "Sales",
        ascending=False
    )
    .head(10)
)


fig_product = px.bar(
    product_data,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="Top 10 Products by Sales",
    text_auto=".2s"
)

fig_product.update_layout(
    yaxis=dict(
        categoryorder="total ascending"
    ),
    height=500
)

st.plotly_chart(
    fig_product,
    width="stretch"
)


# =========================================================
# STATE ANALYSIS
# =========================================================

st.subheader("🗺️ Top States by Sales")

state_data = (
    filtered_df
    .groupby("State/Province")
    .agg(
        Sales=("Sales", "sum"),
        Units=("Units", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
    .sort_values(
        "Sales",
        ascending=False
    )
    .head(10)
)


fig_state = px.bar(
    state_data,
    x="Sales",
    y="State/Province",
    orientation="h",
    title="Top 10 States by Sales",
    text_auto=".2s"
)

fig_state.update_layout(
    yaxis=dict(
        categoryorder="total ascending"
    ),
    height=500
)

st.plotly_chart(
    fig_state,
    width="stretch"
)


# =========================================================
# ROUTE ANALYSIS
# =========================================================

st.subheader("🛣️ Top Routes by Sales")

route_data = (
    filtered_df
    .groupby(
        ["Factory", "State/Province"]
    )
    .agg(
        Orders=("Order ID", "nunique"),
        Units=("Units", "sum"),
        Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

route_data["Route"] = (
    route_data["Factory"]
    + " → "
    + route_data["State/Province"]
)

route_data = (
    route_data
    .sort_values(
        "Sales",
        ascending=False
    )
    .head(15)
)


fig_route = px.bar(
    route_data,
    x="Sales",
    y="Route",
    orientation="h",
    title="Top 15 Routes by Sales",
    text_auto=".2s"
)

fig_route.update_layout(
    yaxis=dict(
        categoryorder="total ascending"
    ),
    height=600
)

st.plotly_chart(
    fig_route,
    width="stretch"
)


# =========================================================
# DATA TABLE
# =========================================================

st.subheader("📋 Filtered Data")

st.write(
    f"Showing **{len(filtered_df):,}** records"
)

st.dataframe(
    filtered_df,
    width="stretch",
    height=400
)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "Nassau Candy Route Analysis | "
    "Interactive Data Analytics Dashboard"
)