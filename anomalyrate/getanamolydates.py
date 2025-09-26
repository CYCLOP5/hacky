import pandas as pd

def transform_date_data(input_file_name, output_file_name):
    """
    Reads a CSV, removes EDATE, splits ADATE into Year/Month/Day, 
    removes duplicate rows based on ADATE, and standardizes columns.
    """
    try:
        # 1. Read the CSV, converting 'ADATE' to datetime objects.
        # dayfirst=True ensures DD-MM-YYYY format is correctly parsed.
        df = pd.read_csv(input_file_name, parse_dates=['ADATE'], dayfirst=True)
        
    except FileNotFoundError:
        print(f"Error: The file '{input_file_name}' was not found. Please check the name and path.")
        return
    
    # --- ADDED STEP FOR UNIQUE DATES ---
    # Removes any duplicate rows based on the 'ADATE' column, keeping the first occurrence.
    df.drop_duplicates(subset=['ADATE'], keep='first', inplace=True)
    
    # --- Data Transformation Steps ---
    
    # 2. Drop the 'EDATE' column.
    columns_to_drop = ['EDATE']
    df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)
    
    # 3. Divide the 'ADATE' column into Year, Month, and Day.
    df['Year'] = df['ADATE'].dt.year
    df['Month'] = df['ADATE'].dt.month
    df['Day'] = df['ADATE'].dt.day
    
    # 4. Create Anamolytype from ADIAG and standardize Anamoly.
    df['Anamolytype'] = df['ADIAG']
    df['Anamoly'] = 1
    
    final_columns = ['ADATE', 'Year', 'Month', 'Day', 'Anamolytype', 'Anamoly']
    df_final = df[final_columns]
    
    df_final.to_csv(output_file_name, index=False)
    
    print(f"Transformation successful! The new file '{output_file_name}' has been created.")
    print("\nFirst 5 rows of the transformed data:")
    print(df_final.head().to_markdown(index=False, numalign="left", stralign="left"))
    print(df['ADATE'].min())
    print(df['ADATE'].max())
    
# --- Execution ---
input_file = 'anom5j.csv'
output_file = 'unique_transformed_dates.csv'
transform_date_data(input_file, output_file)