# Week4  
  
Python standard library  
panda， PYG   
  
S1 -> Lequired libraries  
S2 -> Locate & load the file  
S3 - > Calculate the delays  
S4 -> ATMS  
S5 -> CVO(**Commercial Vehicle Operations **)  
S6 -> Visitation   
  
**ATPS**  
```
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

```
  
  
**Advanced Traffic Management Systems(ATMS):** integrates various sub-systems (such as CCTV, vehicle detection, communication, variable message systems, etc.)into a coherent single interface that provides a real-time data on traffic status and predicts traffic conditions for more efficient planning and operations. Dynamic traffic control systems, freeway operations management systems, incident response systems etc., respond in real time to changing conditions.   
  
**Advanced Traveler Information System (ATIS):** provide to users of transportation systems, travel-related information to assist decision making on route choices, estimate travel times, and avoid congestion. This can be enabled by providing different information using various technologies such as:   
a)Dynamic road messages signs for real communication of information on traffic congestions, bottlenecks, accidents, and alternate route information during road closures and maintenance.   
b)GPS enabled in-vehicle navigation systems.   
c)Web-site to provide a color-coded network map showing congestion levels on highways (a.k.a congestion index)  
  
**Advanced Vehicle Control Systems (AVCS):** are tools and concepts that enhance the driver’s control of the vehicle to make travel safer and more efficient. For example, in vehicle collision warning systems alert the driver to a possible imminent collision. In more advanced AVCS applications, the vehicle could automatically break or steer away from collision, based on input from sensors on the vehicle. Both systems are autonomous to the vehicle and can provide substantial benefits by improving safety and reducing accident induced congestion. The installation of high tech gadget's and processors in vehicles allow incorporation of software applications and artificial intelligence systems that control internal operations, ubiquitous computing, and other programs designed to be integrated into a greater transportation system.   
  
**Commercial Vehicle Operations (CVO):** comprises an ensemble of satellite navigation system, a small computer and a digital radio, which can be used in commercial vehicles such as trucks, vans, and taxis. This system affords constant monitoring of truck operations by the central office and provides traceability and safety.    
  
**Advanced Public Transportation Systems (APTS)**: applies state-of-art transportation management and information technologies to public transit systems to enhance efficiency operation and improve safety. It includes real-time passenger information systems, automatic vehicle location systems, bus arrival notification systems, and systems providing priority of passage to busses at signalized intersections (transit signal priority)  
  
**Advanced Rural Transportation Systems (ARTS):** provide information about remote road and other transportation systems. Example include automated road weather conditions reporting and directional information. This type of information is valuable to motorists travelling to remote or rural areas.   
  
**Road Weather Information Systems (RWIS)**: These systems collect and disseminate information about weather conditions on roadways, helping drivers make informed decisions and improving safety during adverse weather.   
  
  
CITS 在课件里主要写作 **C-ITS**。  
全称是：**Cooperative Intelligent Transport Systems**。  
  
  
