import pandas as pd
import numpy as np

# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("data/Nassau Candy Distributor.csv")

print("===================================")
print("NASSAU CANDY ROUTE ANALYSIS")
print("===================================")

print("\nOriginal Dataset Shape:")
print(df.shape)


# ==========================================
# 2. CHECK MISSING VALUES & DUPLICATES
# ==========================================

print("\nMissing Values:")
print(df.isnull().sum().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())


# ==========================================
# 3. CONVERT DATE COLUMNS
# ==========================================

df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    dayfirst=True,
    errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"],
    dayfirst=True,
    errors="coerce"
)

print("\nDate Conversion Completed")


# ==========================================
# 4. CHECK INVALID DATES
# ==========================================

print("\nInvalid Order Dates:")
print(df["Order Date"].isna().sum())

print("\nInvalid Ship Dates:")
print(df["Ship Date"].isna().sum())


# ==========================================
# 5. CALCULATE SHIPPING LEAD TIME
# ==========================================

df["Shipping Lead Time"] = (
    df["Ship Date"] - df["Order Date"]
).dt.days

print("\nShipping Lead Time Statistics:")
print(df["Shipping Lead Time"].describe())


# ==========================================
# 6. CHECK NEGATIVE LEAD TIMES
# ==========================================

negative_lead_times = (
    df["Shipping Lead Time"] < 0
).sum()

print("\nNegative Lead Times:")
print(negative_lead_times)


# ==========================================
# 7. REMOVE INVALID RECORDS
# ==========================================

df = df.dropna(
    subset=["Order Date", "Ship Date"]
)

df = df[
    df["Shipping Lead Time"] >= 0
]

print("\nDataset Shape After Cleaning:")
print(df.shape)


# ==========================================
# 8. FACTORY MAPPING
# ==========================================

factory_map = {

    "Wonka Bar - Nutty Crunch Surprise":
        "Lot's O' Nuts",

    "Wonka Bar - Fudge Mallows":
        "Lot's O' Nuts",

    "Wonka Bar -Scrumdiddlyumptious":
    "Lot's O' Nuts",

    "Wonka Bar - Milk Chocolate":
        "Wicked Choccy's",

    "Wonka Bar - Triple Dazzle Caramel":
        "Wicked Choccy's",

    "Laffy Taffy":
        "Sugar Shack",

    "SweeTARTS":
        "Sugar Shack",

    "Nerds":
        "Sugar Shack",

    "Fun Dip":
        "Sugar Shack",

    "Fizzy Lifting Drinks":
        "Sugar Shack",

    "Everlasting Gobstopper":
        "Secret Factory",

    "Lickable Wallpaper":
        "Secret Factory",

    "Wonka Gum":
        "Secret Factory",

    "Hair Toffee":
        "The Other Factory",

    "Kazookles":
        "The Other Factory"
}


df["Factory"] = df["Product Name"].map(factory_map)


# ==========================================
# 9. CHECK UNMAPPED PRODUCTS
# ==========================================

unmapped_products = df[
    df["Factory"].isna()
]["Product Name"].unique()

print("\nUnmapped Products:")

if len(unmapped_products) == 0:
    print("None - All products mapped successfully")
else:
    print(unmapped_products)


# ==========================================
# 10. FACTORY COORDINATES
# ==========================================

factory_coordinates = {

    "Lot's O' Nuts":
        (32.881893, -111.768036),

    "Wicked Choccy's":
        (32.076176, -81.088371),

    "Sugar Shack":
        (48.119140, -96.181150),

    "Secret Factory":
        (41.446333, -90.565487),

    "The Other Factory":
        (35.117500, -89.971107)
}


df["Factory Latitude"] = df["Factory"].map(
    lambda x: factory_coordinates[x][0]
)

df["Factory Longitude"] = df["Factory"].map(
    lambda x: factory_coordinates[x][1]
)


# ==========================================
# 11. CREATE ROUTE
# ==========================================

df["Route"] = (
    df["Factory"]
    + " → "
    + df["State/Province"]
)


df["Region Route"] = (
    df["Factory"]
    + " → "
    + df["Region"]
)


# ==========================================
# 12. ROUTE SUMMARY
# ==========================================

route_summary = (
    df.groupby(
        ["Factory", "State/Province"]
    )
    .agg(
        Total_Shipments=(
            "Order ID",
            "nunique"
        ),

        Average_Lead_Time=(
            "Shipping Lead Time",
            "mean"
        ),

        Lead_Time_Variability=(
            "Shipping Lead Time",
            "std"
        ),

        Total_Sales=(
            "Sales",
            "sum"
        ),

        Total_Units=(
            "Units",
            "sum"
        ),

        Gross_Profit=(
            "Gross Profit",
            "sum"
        )
    )
    .reset_index()
)


route_summary["Route"] = (
    route_summary["Factory"]
    + " → "
    + route_summary["State/Province"]
)


# ==========================================
# 13. ROUTE EFFICIENCY SCORE
# ==========================================

min_time = route_summary[
    "Average_Lead_Time"
].min()

max_time = route_summary[
    "Average_Lead_Time"
].max()


if max_time != min_time:

    route_summary["Efficiency Score"] = (
        100
        * (
            max_time
            - route_summary["Average_Lead_Time"]
        )
        / (max_time - min_time)
    )

else:

    route_summary["Efficiency Score"] = 100


# ==========================================
# 14. TOP 10 ROUTES
# ==========================================

top_routes = route_summary.sort_values(
    "Average_Lead_Time"
).head(10)


print("\n===================================")
print("TOP 10 ROUTES")
print("===================================")

print(
    top_routes[
        [
            "Route",
            "Total_Shipments",
            "Average_Lead_Time",
            "Efficiency Score"
        ]
    ].to_string(index=False)
)


# ==========================================
# 15. BOTTOM 10 ROUTES
# ==========================================

bottom_routes = route_summary.sort_values(
    "Average_Lead_Time",
    ascending=False
).head(10)


print("\n===================================")
print("BOTTOM 10 ROUTES")
print("===================================")

print(
    bottom_routes[
        [
            "Route",
            "Total_Shipments",
            "Average_Lead_Time",
            "Efficiency Score"
        ]
    ].to_string(index=False)
)


# ==========================================
# 16. SHIP MODE ANALYSIS
# ==========================================

ship_mode_summary = (
    df.groupby("Ship Mode")
    .agg(
        Total_Shipments=(
            "Order ID",
            "nunique"
        ),

        Average_Lead_Time=(
            "Shipping Lead Time",
            "mean"
        ),

        Total_Sales=(
            "Sales",
            "sum"
        ),

        Gross_Profit=(
            "Gross Profit",
            "sum"
        )
    )
    .reset_index()
)


print("\n===================================")
print("SHIP MODE ANALYSIS")
print("===================================")

print(ship_mode_summary.to_string(index=False))


# ==========================================
# 17. REGION ANALYSIS
# ==========================================

region_summary = (
    df.groupby("Region")
    .agg(
        Total_Shipments=(
            "Order ID",
            "nunique"
        ),

        Average_Lead_Time=(
            "Shipping Lead Time",
            "mean"
        ),

        Total_Sales=(
            "Sales",
            "sum"
        ),

        Gross_Profit=(
            "Gross Profit",
            "sum"
        )
    )
    .reset_index()
)


print("\n===================================")
print("REGION ANALYSIS")
print("===================================")

print(region_summary.to_string(index=False))


# ==========================================
# 18. SAVE CLEANED DATA
# ==========================================

df.to_csv(
    "outputs/cleaned_nassau_data.csv",
    index=False
)


# ==========================================
# 19. SAVE ROUTE SUMMARY
# ==========================================

route_summary.to_csv(
    "outputs/route_summary.csv",
    index=False
)


# ==========================================
# 20. SAVE REGION SUMMARY
# ==========================================

region_summary.to_csv(
    "outputs/region_summary.csv",
    index=False
)


# ==========================================
# 21. SAVE SHIP MODE SUMMARY
# ==========================================

ship_mode_summary.to_csv(
    "outputs/ship_mode_summary.csv",
    index=False
)


print("\n===================================")
print("ANALYSIS COMPLETED SUCCESSFULLY")
print("===================================")

print("\nFiles created inside outputs folder:")
print("1. cleaned_nassau_data.csv")
print("2. route_summary.csv")
print("3. region_summary.csv")
print("4. ship_mode_summary.csv")
# ==========================================
# DATE VALIDATION CHECK
# ==========================================

print("\n===================================")
print("DATE VALIDATION")
print("===================================")

print("\nOrder Date Range:")
print(df["Order Date"].min())
print("to")
print(df["Order Date"].max())

print("\nShip Date Range:")
print(df["Ship Date"].min())
print("to")
print(df["Ship Date"].max())

print("\nShip Mode vs Lead Time:")
print(
    df.groupby("Ship Mode")["Shipping Lead Time"]
    .agg(["min", "mean", "max"])
)

print("\nSample Date Records:")
print(
    df[
        [
            "Order ID",
            "Order Date",
            "Ship Date",
            "Ship Mode",
            "Shipping Lead Time"
        ]
    ].head(20).to_string(index=False)
)
# ==========================================
# BUSINESS ANALYSIS
# ==========================================

print("\n===================================")
print("BUSINESS ANALYSIS")
print("===================================")

# Factory performance
factory_summary = (
    df.groupby("Factory")
    .agg(
        Total_Orders=("Order ID", "nunique"),
        Total_Units=("Units", "sum"),
        Total_Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum"),
        Total_Cost=("Cost", "sum")
    )
    .reset_index()
)

print("\nFACTORY PERFORMANCE")
print(factory_summary.to_string(index=False))


# Region performance
region_business = (
    df.groupby("Region")
    .agg(
        Total_Orders=("Order ID", "nunique"),
        Total_Units=("Units", "sum"),
        Total_Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

print("\nREGION BUSINESS PERFORMANCE")
print(region_business.to_string(index=False))


# State performance
state_summary = (
    df.groupby("State/Province")
    .agg(
        Total_Orders=("Order ID", "nunique"),
        Total_Units=("Units", "sum"),
        Total_Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
    .sort_values("Total_Sales", ascending=False)
)

print("\nTOP STATES BY SALES")
print(state_summary.head(10).to_string(index=False))


# Product performance
product_summary = (
    df.groupby("Product Name")
    .agg(
        Total_Units=("Units", "sum"),
        Total_Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
    .sort_values("Total_Sales", ascending=False)
)

print("\nTOP PRODUCTS BY SALES")
print(product_summary.head(10).to_string(index=False))


# Route volume
route_volume = (
    df.groupby(["Factory", "State/Province"])
    .agg(
        Total_Orders=("Order ID", "nunique"),
        Total_Units=("Units", "sum"),
        Total_Sales=("Sales", "sum"),
        Gross_Profit=("Gross Profit", "sum")
    )
    .reset_index()
    .sort_values("Total_Orders", ascending=False)
)

print("\nTOP ROUTES BY ORDER VOLUME")
print(route_volume.head(15).to_string(index=False))


# Save business summaries
factory_summary.to_csv(
    "outputs/factory_summary.csv",
    index=False
)

state_summary.to_csv(
    "outputs/state_summary.csv",
    index=False
)

product_summary.to_csv(
    "outputs/product_summary.csv",
    index=False
)

route_volume.to_csv(
    "outputs/route_volume.csv",
    index=False
)

print("\nBusiness analysis files created successfully.")