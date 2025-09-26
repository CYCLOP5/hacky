import pandas as pd
import numpy as np

def preprocess_data(input_filepath, output_filepath):
    print(f"Starting final preprocessing of {input_filepath}...")

    all_column_names = [
        'year', 'doy', 'hour', 'imf_sc_id', 'plasma_sc_id', 'imf_magnitude',
        'bx_gsm', 'by_gsm', 'bz_gsm', 'temperature', 'proton_density',
        'flow_speed', 'flow_pressure', 'kp_index', 'dst_index'
    ]

    columns_to_keep = [
        'year', 'doy', 'hour', 'imf_magnitude', 'bx_gsm', 'by_gsm', 'bz_gsm',
        'temperature', 'proton_density', 'flow_speed', 'flow_pressure',
        'kp_index', 'dst_index'
    ]

    fill_values = {
        'imf_magnitude': 999.9,   
        'bx_gsm': 999.9,          
        'by_gsm': 999.9,          
        'bz_gsm': 999.9,          
        'temperature': 9999999.0, 
        'proton_density': 999.9,  
        'flow_speed': 9999.0,     
        'flow_pressure': 99.99,   
        'kp_index': 99,           
        'dst_index': 99999        
    }

    df = pd.read_csv(
        input_filepath,
        delim_whitespace=True,
        header=None,
        names=all_column_names
    )
    print(f"Loaded {len(df)} rows and {len(df.columns)} columns of raw data.")

    df = df[columns_to_keep]
    print(f"Selected the {len(df.columns)} columns required for the project.")

    for col, fill_val in fill_values.items():
        if col in df.columns:
            df[col] = df[col].replace(fill_val, np.nan)
    print("Replaced exact fill values with NaN.")
    df['kp_index'] = df['kp_index'] / 10.0
    df['timestamp'] = pd.to_datetime(df['year'].astype(str) + '-' + df['doy'].astype(str), format='%Y-%j') \
                      + pd.to_timedelta(df['hour'], unit='h')
    df.set_index('timestamp', inplace=True)
    df.drop(['year', 'doy', 'hour'], axis=1, inplace=True)
    print("Created and set datetime index.")

    df.ffill(inplace=True)
    df.bfill(inplace=True)
    print("Handled missing values using forward and backward fill.")

    df.to_parquet(output_filepath)
    print(f"Preprocessing complete. Cleaned data saved to {output_filepath}")
    print("\n--- Data Head ---")
    print(df.head())
    print("\n--- Data Info ---")
    df.info()

if __name__ == "__main__":

    INPUT_FILE = 'omni2_To4UfqWLsP.lst'
    OUTPUT_FILE = 'processed_borealis_data.parquet'
    preprocess_data(INPUT_FILE, OUTPUT_FILE)
