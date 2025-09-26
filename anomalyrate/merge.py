import pandas as pd

# Load your CSVs
anomaly_df = pd.read_csv("anomaly.csv")   # ADATE, Year, Month, Day, Anamolytype, Anamoly
kp_df = pd.read_csv("kpval.csv")          # Year, Month, Day, Kp, ap

# Convert to datetime
anomaly_df["ADATE"] = pd.to_datetime(anomaly_df[["Year", "Month", "Day"]])
kp_df["Date"] = pd.to_datetime(kp_df[["Year", "Month", "Day"]])

# Filter kp dataset by given date range
start = "1963-02-14"
end = "1994-09-11"
kp_df = kp_df[(kp_df["Date"] >= start) & (kp_df["Date"] <= end)]

# Right join (all kp dates kept)
merged = pd.merge(
    anomaly_df,
    kp_df,
    on=["Year", "Month", "Day"],
    how="right"
)

# Fill missing anomaly values with 0
merged["Anamoly"] = merged["Anamoly"].fillna(0).astype(int)
merged["Anamolytype"] = merged["Anamolytype"].fillna("NA")
merged["ADATE"] = merged["ADATE"].fillna(merged["Date"].dt.strftime("%Y-%m-%d"))

# Save or preview
print(merged.head(15))
merged.to_csv("merged_output.csv", index=False)
