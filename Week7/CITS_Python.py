from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configure visual style
sns.set_theme(style="whitegrid")

# ==========================================
# STEP 1: LOAD & PREPARE DATA
# ==========================================
# Ingest dataset sheet
DATA_FILE = Path(__file__).resolve().parent / 'bus_combined.xlsx'
if not DATA_FILE.exists():
    raise FileNotFoundError(f"Expected dataset at: {DATA_FILE}")

df = pd.read_excel(DATA_FILE, sheet_name='bus_combined')

# Clean timestamps safely using format='mixed' to eliminate format warnings
df['scheduled_time'] = pd.to_datetime(df['scheduled_time'].astype(str), format='mixed', errors='coerce')
df['actual_time'] = pd.to_datetime(df['actual_time'].astype(str), format='mixed', errors='coerce')

# Derive Schedule Delay metric in minutes
df['delay_minutes'] = (df['actual_time'] - df['scheduled_time']).dt.total_seconds() / 60.0

# ==========================================
# STEP 2: DATA AGGREGATIONS
# ==========================================
# Aggregation for Figure 1: Average speed per bus stop (sorted ascending for bottleneck identification)
pivot_a = df.groupby('stop_name')['speed_kmh'].mean().reset_index().sort_values(by='speed_kmh', ascending=True)

# Aggregation for Figure 2: Thermal stress vs emissions per vehicle
cvo_summary = df.groupby(['bus_id', 'breakdown_risk']).agg(
    avg_temp=('engine_temp_c', 'mean'),
    avg_co2=('co2_g_km', 'mean')
).reset_index()

# Aggregation for Figure 3: High-risk vehicle recall attributes
high_risk_table = df[df['breakdown_risk'] == 'High'].groupby('bus_id').agg(
    avg_engine_temp=('engine_temp_c', 'mean'),
    avg_co2_emissions=('co2_g_km', 'mean'),
    breakdown_risk=('breakdown_risk', 'first'),
    ping_count=('ping_id', 'count')
).reset_index().sort_values(by='avg_engine_temp', ascending=False)

# ==========================================
# STEP 3: GENERATE MULTI-PLOT DASHBOARD
# ==========================================
# Create a 1x2 subplot grid canvas so all visuals display concurrently
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6))

# --- FIGURE 1: ATMS Urban Bottleneck Analysis (Bar Chart) ---
sns.barplot(
    data=pivot_a, 
    x='speed_kmh', 
    y='stop_name', 
    hue='stop_name', 
    palette='Reds_r', 
    legend=False,
    ax=ax1
)
ax1.axvline(12.43, color='blue', linestyle='--', linewidth=1.5, label='Network Avg (12.43 km/h)')
ax1.set_title('Figure 1: ATMS Urban Bottleneck Analysis (stop_name vs. speed_kmh)', fontsize=11, fontweight='bold')
ax1.set_xlabel('Average Operating Speed (km/h)')
ax1.set_ylabel('Bus Stop Location')
ax1.legend(loc='lower right')

# --- FIGURE 2: CVO Fleet Diagnostics (Scatter Plot) ---
sns.scatterplot(
    data=cvo_summary,
    x='avg_temp',
    y='avg_co2',
    hue='breakdown_risk',
    style='breakdown_risk',
    palette={'High': 'red', 'Low': 'green'},
    s=180,
    ax=ax2
)

# Overlay vehicle IDs on scatter points
for i in range(len(cvo_summary)):
    ax2.text(
        cvo_summary.loc[i, 'avg_temp'] + 0.3,
        cvo_summary.loc[i, 'avg_co2'] + 6,
        cvo_summary.loc[i, 'bus_id'],
        fontsize=9,
        fontweight='bold'
    )

ax2.axvline(100.0, color='darkred', linestyle=':', linewidth=1.5, label='Maintenance Threshold (100°C)')
ax2.set_title('Figure 2: CVO Fleet Diagnostics (engine_temp_c vs. co2_g_km)', fontsize=11, fontweight='bold')
ax2.set_xlabel('Average Engine Temperature (°C)')
ax2.set_ylabel('Average CO2 Emissions (g/km)')
ax2.legend(title='Breakdown Risk')

plt.tight_layout()
plt.show()

# ==========================================
# STEP 4: PRINT KPI SCORECARDS & RECALL TABLE
# ==========================================
print("==========================================================")
print("FIGURE 3: CVO HIGH-RISK DISPATCH RECALL TABLE")
print("==========================================================")
print(high_risk_table.to_string(index=False))
print("==========================================================")
print("FIGURE 4: TOP KPI SCORECARDS")
print("==========================================================")
print(f" Average Fleet Speed: {df['speed_kmh'].mean():.2f} km/h")
print(f" Average Engine Temperature: {df['engine_temp_c'].mean():.2f} °C")
high_risk_count = (df['breakdown_risk'] == 'High').sum()
print(f" High Breakdown Risk Pings: {high_risk_count} Pings ({high_risk_count / len(df) * 100:.0f}%)\n")

