import pandas as pd

# Path to your txt file
file_path = "kp1932.txt"   # change this to your file name

# Read the file, skipping 30 header lines
cols = ["Year", "Month", "Day", "UT_start", "UT_mid", "days", "days_m", "Kp", "ap", "D"]
df = pd.read_csv(file_path, sep="\s+", skiprows=30, names=cols)

# Compute daily means
daily_means = df.groupby(["Year", "Month", "Day"])[["Kp", "ap"]].mean().reset_index()

# Save as CSV
daily_means.to_csv("kp_ap_daily_means.csv", index=False)

print("Saved as kp_ap_daily_means.csv")
print(daily_means.head())
