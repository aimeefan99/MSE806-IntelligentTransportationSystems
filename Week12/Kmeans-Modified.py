import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 1. Load Sheet2 explicitly
import os
file_path = 'Generate_Dataset.xlsx'
if not os.path.exists(file_path):
    file_path = os.path.join(os.path.dirname(__file__), 'Generate_Dataset.xlsx')
df = pd.read_excel(file_path, sheet_name='Sheet2')

# Clean leading/trailing spaces in headers
df.columns = df.columns.str.strip()

# 2. Dynamic column detection (handles slight naming variations)
col_density = [c for c in df.columns if 'rho' in c.lower() or 'density' in c.lower()][0]
col_pdr = [c for c in df.columns if 'packet' in c.lower() or 'pdr' in c.lower()][0]

print(f"Detected Density Column: '{col_density}'")
print(f"Detected PDR Column: '{col_pdr}'")

# 3. Extract telemetry features dynamically
X = df[[col_density, col_pdr]]

# 4. Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 5. Fit K-Means (K = 3)
n_clusters = 5
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
raw_clusters = kmeans.fit_predict(X_scaled)

# 6. Map labels dynamically based on Vehicle Density
cluster_means = df.groupby(raw_clusters)[col_density].mean().sort_values()
sorted_ids = cluster_means.index.tolist()


if n_clusters == 3:
    default_names = ['Free-Flow Traffic', 'Moderate Traffic', 'Severe Bottleneck']
    color_dict = {'Free-Flow Traffic': '#4C72B0', 'Moderate Traffic': '#55A868', 'Severe Bottleneck': '#DD8452'}
elif n_clusters == 5:
    default_names = ['Very Free-Flow', 'Light Traffic', 'Moderate Traffic', 'Heavy Bottleneck', 'Severe Bottleneck']
    color_dict = None
else:
    default_names = [f'Cluster {i+1}' for i in range(n_clusters)]
    color_dict = None

label_map = {sorted_ids[i]: default_names[i] for i in range(n_clusters)}
df['Traffic_State'] = [label_map[c] for c in raw_clusters]
sns.set_theme(style='whitegrid')
plt.figure(figsize=(10, 5))

# Identify road segment ID column dynamically if present
segment_col = [c for c in df.columns if 'segment' in c.lower() or 'id' in c.lower()]
style_kw = {'style': segment_col[0]} if segment_col else {}
palette_kw = {'palette': color_dict} if color_dict else {'palette': 'Set1'}

sns.scatterplot(
    data=df,
    x=col_density,
    y=col_pdr,
    hue='Traffic_State',
    s=90,
    alpha=0.9,
    **palette_kw,
    **style_kw
)

plt.title(f'K-Means Clustering (n_clusters = {n_clusters}): Traffic State Regimes', fontsize=13, fontweight='bold')
plt.xlabel(f'Vehicle Density ({col_density})', fontsize=11)
plt.ylabel(f'Signal Quality ({col_pdr})', fontsize=11)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left')
plt.tight_layout()
plt.savefig('Kmeans_Output.png', dpi=150)
print(f"Chart saved as 'Kmeans_Output.png'")
plt.show()
