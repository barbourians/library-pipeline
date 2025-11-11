from data_processing.cleaning import (
    remove_duplicates,
    handle_missing_values,
    standardize_dates
)

# Load data
df = load_csv('../data/circulation_data.csv')

# Apply cleaning pipeline
df_clean = remove_duplicates(df, subset=['transaction_id'])
df_clean = handle_missing_values(df_clean, strategy='drop')
df_clean = standardize_dates(df_clean, ['checkout_date', 'return_date'])

# Check results
print(f"Original rows: {len(df)}")
print(f"Clean rows: {len(df_clean)}")
print(df_clean.info())
