import pandas as pd

INPUT_FILE = "portfolio/service/raw.csv"
OUTPUT_FILE = "portfolio/service/clean_v1.csv"

def load_data(path):
    return pd.read_csv(path)

def clean_data(df):

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Fill missing numeric values with 0
    for col in df.select_dtypes(include='number').columns:
        df[col] = df[col].fillna(0)

    # Fill missing text values with blank string
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].fillna("").astype(str).str.strip()

    # Convert date columns
    for col in df.columns:
        if "date" in col:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d')

    # Standardize selected text columns
    text_columns = ["client"]

    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].str.title()

    return df

def transform_data(df):
    if "price" in df.columns and "quantity" in df.columns:
        df["revenue"] = df["price"] * df["quantity"]
    return df

def validate_data(df):
    print(len(df))
    print(df.head())

def export_data(df, path):
    df.to_csv(path, index=False)

def main():
    df = load_data(INPUT_FILE)
    df = clean_data(df)
    # df = transform_data(df)
    validate_data(df)
    export_data(df, OUTPUT_FILE)

if __name__ == "__main__":
    main()


# # ========================
# # SILVA ANALYTICS TEMPLATE
# # ========================

# import pandas as pd

# # -------- CONFIG --------
# FILE_PATH = "raw_data.xlsx"

# DATE_COLUMN = "date"
# REVENUE_COLUMN = "revenue"
# QUANTITY_COLUMN = "quantity"

# GROUP_BY = "month"

# # -------- LOAD --------
# df = pd.read_excel(FILE_PATH)

# # -------- CLEAN --------
# df.columns = df.columns.str.strip().str.lower()
# df = df.drop_duplicates()
# df = df.dropna(how="all")

# # -------- STANDARDIZE COLUMN NAMES (EDIT PER CLIENT) --------
# # Example:
# # df.rename(columns={
# #     'order date': 'date',
# #     'sales amount': 'revenue'
# # }, inplace=True)

# # -------- DATE HANDLING --------
# df[DATE_COLUMN] = pd.to_datetime(df[DATE_COLUMN], errors='coerce')
# df['month'] = df[DATE_COLUMN].dt.to_period('M').astype(str)

# # -------- METRICS --------
# # Only create if needed
# # df['revenue'] = df['price'] * df['quantity']

# # -------- AGGREGATION --------
# summary = df.groupby('month').agg({
#     REVENUE_COLUMN: 'sum'
# }).reset_index()

# # -------- EXPORT --------
# summary.to_csv("dashboard_ready.csv", index=False)

# print("✅ Data processed successfully")