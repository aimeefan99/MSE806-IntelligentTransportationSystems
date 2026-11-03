# 1. Install required libraries
!pip install pygwalker pandas openpyxl -q
import os
import pandas as pd
import pygwalker as pyg
# 2. Automatically locate 'bus_combined.xlsx' wherever it is in Colab
file_path = None
for root, dirs, files in os.walk('/'):
    if 'bus_combined.xlsx' in files:
        file_path = os.path.join(root, 'bus_combined.xlsx')
        break
if file_path:
    print(f" Found file at: {file_path}")
    df = pd.read_excel(file_path)
else:
    raise FileNotFoundError("Could not locate 'bus_combined.xlsx'. Please re-upload the file.")
# 3. Convert time strings to datetime for ITS delay calculations
df['scheduled_dt'] = pd.to_datetime(df['scheduled_time'].astype(str), format='%H:%M:%S', errors='coerce')
df['actual_dt'] = pd.to_datetime(df['actual_time'].astype(str), format='%H:%M:%S', errors='coerce')
# Calculate Delay in Minutes (APTS Metric)
df['delay_min'] = (df['actual_dt'] - df['scheduled_dt']).dt.total_seconds() / 60.0
# 4. ATMS Analytics: Identify Traffic Bottlenecks (Speed < 10 km/h)
bottlenecks = df[df['speed_kmh'] < 10][['stop_name', 'route_id', 'speed_kmh', 'delay_min']]
# 5. CVO Analytics: Fleet Risk Assessment
high_risk_fleet = df[df['breakdown_risk'] == 'High'][['bus_id', 'engine_temp_c', 'co2_g_km']].drop_duplicates()
# Print summary reports
print("=== ATMS: CONGESTION BOTTLENECK REPORT ===")
print(bottlenecks.head())
print("\n=== CVO: FLEET MAINTENANCE ALERT ===")
print(high_risk_fleet)
# 6. Convert text/time columns to strings and launch interactive canvas
for col in df.columns:
    if df[col].dtype == 'object' or 'time' in col.lower():
        df[col] = df[col].astype(str)
pyg.walk(df)