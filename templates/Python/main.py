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