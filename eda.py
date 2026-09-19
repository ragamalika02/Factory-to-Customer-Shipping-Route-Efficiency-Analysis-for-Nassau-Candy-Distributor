import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# LOAD CLEANED DATA
# ==========================================

df = pd.read_csv("outputs/cleaned_nassau_data.csv")

os.makedirs("outputs/charts", exist_ok=True)


# ==========================================
# 1. FACTORY SALES
# ==========================================

factory_sales = (
    df.groupby("Factory")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))

factory_sales.plot(kind="bar")

plt.title("Total Sales by Factory")
plt.xlabel("Factory")
plt.ylabel("Sales")
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    "outputs/charts/factory_sales.png",
    dpi=300
)

plt.close()


# ==========================================
# 2. REGION SALES
# ==========================================

region_sales = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(9, 6))

region_sales.plot(kind="bar")

plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Sales")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    "outputs/charts/region_sales.png",
    dpi=300
)

plt.close()


# ==========================================
# 3. TOP 10 PRODUCTS BY SALES
# ==========================================

product_sales = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(11, 7))

product_sales.sort_values().plot(kind="barh")

plt.title("Top 10 Products by Sales")
plt.xlabel("Sales")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig(
    "outputs/charts/top_products_sales.png",
    dpi=300
)

plt.close()


# ==========================================
# 4. TOP 10 STATES BY SALES
# ==========================================

state_sales = (
    df.groupby("State/Province")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))

state_sales.sort_values().plot(kind="barh")

plt.title("Top 10 States by Sales")
plt.xlabel("Sales")
plt.ylabel("State")

plt.tight_layout()

plt.savefig(
    "outputs/charts/top_states_sales.png",
    dpi=300
)

plt.close()


# ==========================================
# 5. SHIP MODE DISTRIBUTION
# ==========================================

ship_mode = (
    df.groupby("Ship Mode")["Order ID"]
    .nunique()
)

plt.figure(figsize=(8, 6))

ship_mode.plot(
    kind="bar"
)

plt.title("Orders by Ship Mode")
plt.xlabel("Ship Mode")
plt.ylabel("Number of Orders")
plt.xticks(rotation=20)

plt.tight_layout()

plt.savefig(
    "outputs/charts/ship_mode_orders.png",
    dpi=300
)

plt.close()


# ==========================================
# 6. FACTORY → STATE ROUTE SALES
# ==========================================

route_sales = (
    df.groupby(
        ["Factory", "State/Province"]
    )["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(15)
)

route_labels = [
    f"{factory} → {state}"
    for factory, state in route_sales.index
]

plt.figure(figsize=(12, 8))

plt.barh(
    route_labels[::-1],
    route_sales.values[::-1]
)

plt.title("Top 15 Factory → State Routes by Sales")
plt.xlabel("Sales")
plt.ylabel("Route")

plt.tight_layout()

plt.savefig(
    "outputs/charts/top_routes_sales.png",
    dpi=300
)

plt.close()


# ==========================================
# COMPLETED
# ==========================================

print("===================================")
print("EDA COMPLETED SUCCESSFULLY")
print("===================================")

print("\nCharts created:")

print("1. factory_sales.png")
print("2. region_sales.png")
print("3. top_products_sales.png")
print("4. top_states_sales.png")
print("5. ship_mode_orders.png")
print("6. top_routes_sales.png")