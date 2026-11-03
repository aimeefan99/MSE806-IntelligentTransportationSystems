# MSE803 ITS Research Paper Analysis and Machine Learning Development Plan

## Research Paper

**Title:** Data analytics for Cooperative Intelligent Transport Systems  
**Authors:** Muhammad Awais Javed, Sherali Zeadally, Elyes Ben Hamida  
**Journal:** Vehicular Communications, Volume 15, 2019, Pages 63-72  
**DOI:** 10.1016/j.vehcom.2018.10.004

This repository uses the paper as the research foundation for developing a machine learning algorithm in the Intelligent Transport Systems (ITS) domain.

## 1. Paper Summary

The paper studies how data analytics can improve Cooperative Intelligent Transport Systems (C-ITS). C-ITS connects vehicles, Road Side Units (RSUs), and Traffic Command Centers (TCCs) so that transport systems can collect real-time mobility data, process it, and send useful feedback to vehicles or infrastructure.

The main argument is that future ITS cannot rely only on communication technology. It also needs data analytics to convert raw transport data into decisions such as:

- selecting a better route,
- detecting congestion,
- improving communication reliability,
- adapting wireless transmission parameters,
- improving vehicle safety awareness,
- identifying abnormal or unreliable sensor data.

The paper presents C-ITS as a data-driven system where vehicles and infrastructure continuously collect data, the TCC or vehicles analyze it, and the output is used to improve traffic efficiency and road safety.

## 2. C-ITS Architecture Explained

The paper describes three main entities in C-ITS:

| Entity | Role in C-ITS | Data Function |
| --- | --- | --- |
| Vehicles | Mobile ITS nodes equipped with On-Board Units (OBUs) | Generate mobility and safety data such as position, speed, direction, and event warnings |
| RSUs | Fixed roadside communication nodes | Collect nearby vehicle data, extend communication range, and forward data to the TCC |
| TCC | Central Traffic Command Center | Performs city-level traffic analysis, route guidance, and parameter adaptation |

The paper also highlights the **Local Dynamic Map (LDM)**, which stores road and traffic information used by C-ITS applications.

LDM data is classified into four types:

| LDM Type | Description | Example |
| --- | --- | --- |
| Type 1 | Permanent static data | Road topology, speed limits, map information |
| Type 2 | Transient static data | Traffic signs, traffic lights |
| Type 3 | Transient dynamic data | Road works, weather, traffic condition changes |
| Type 4 | Highly dynamic data | CAM and DENM messages from vehicles |

For machine learning development, the most useful data types are Type 3 and Type 4 because they change over time and can support prediction.

## 3. Key Data Sources in the Paper

The paper identifies several data sources that can be used for analytics:

- Vehicle position
- Vehicle speed
- Vehicle direction
- Vehicle density
- Traffic flow
- Packet delivery ratio
- Packet loss
- Channel busy time
- Traffic signal state
- Accident or emergency event information
- Historical traffic density
- Road condition data
- Weather data
- Security overhead such as key size or signature verification cost

In a real C-ITS system, this data may be generated through:

- CAMs: Cooperative Awareness Messages
- DENMs: Decentralized Environmental Notification Messages
- RSU sensors
- Vehicle OBUs
- traffic signal systems
- GPS traces
- road sensors
- mobile or cloud applications

## 4. Main Data Analytics Challenges

The paper organizes the C-ITS data analytics problem into several challenges.

### 4.1 Data Collection

C-ITS produces large volumes of mobility and safety data. A key challenge is deciding what data should be collected for each application.

For example:

- Route guidance needs vehicle density, road speed, accident information, and traffic signal state.
- Safety applications need nearby vehicle position, speed, direction, and event warnings.
- Communication reliability needs packet loss, channel load, transmission range, and vehicle density.

For an ML algorithm, this means the feature set must be selected according to the target application.

### 4.2 Data Dissemination

The paper discusses wireless technologies used to share data:

- IEEE 802.11p / DSRC
- LTE-V2X
- 5G V2X
- Bluetooth
- Zigbee

This matters because data quality depends on whether messages are delivered reliably. If packet loss is high, the ML model may receive incomplete or delayed information.

### 4.3 Data Computation

The paper describes two computation models:

- **Centralized computation:** TCC analyzes city-level traffic data and sends decisions to vehicles.
- **Distributed computation:** Vehicles analyze local data and make safety decisions themselves.

For this coursework, a centralized ML model is easier to implement because the dataset can be processed in one Python program.

### 4.4 Metrics

The paper highlights the importance of choosing suitable evaluation metrics.

Possible ITS metrics include:

- travel time,
- delay,
- vehicle density,
- average speed,
- packet delivery ratio,
- safety awareness,
- congestion level,
- prediction accuracy,
- system response time.

For a machine learning assignment, the most practical metrics are:

- MAE or RMSE for delay or travel time prediction,
- accuracy, precision, recall, and F1-score for congestion classification,
- confusion matrix for risk or congestion prediction,
- route travel time reduction compared with a baseline method.

### 4.5 Feedback

The paper emphasizes that analytics is only useful if the result is sent back as feedback.

Examples:

- If congestion is predicted, recommend an alternative route.
- If vehicle density is high, reduce transmission range to reduce packet collision.
- If a sensor reading is abnormal, flag it as an outlier.
- If a vehicle has high breakdown risk, trigger a maintenance alert.

For the ML algorithm, the output should therefore not only be a prediction. It should also produce a decision or recommendation.

## 5. Important Application Scenarios from the Paper

### 5.1 Efficient Route Guidance

Figure 3 of the paper presents the main scenario that this coursework will extend. A vehicle needs to travel from a source to a destination through an urban road network. It can choose between two candidate routes:

| Route | Road Sections | Main Characteristic |
| --- | --- | --- |
| Route 1 | `FG -> GB -> BD -> DP` | Shorter route, but it passes a school zone and can become congested |
| Route 2 | `FH -> HM -> MN -> NP` | Longer route, but it avoids the school zone and may be faster during congestion |

The central problem is therefore not simply to find the route with the shortest physical distance. It is to identify the route with the lowest expected travel time under the current traffic conditions.

#### Scenario Components

| Figure Component | C-ITS Role | Relevant Data |
| --- | --- | --- |
| Vehicles and OBUs | Generate and broadcast Cooperative Awareness Messages (CAMs) | Position, speed, direction, and timestamp |
| Road Side Units (RSUs) | Observe nearby vehicles and estimate current traffic conditions for each road section | Current vehicle count, density, speed, and traffic flow |
| Traffic Command Center (TCC) | Performs centralized traffic analysis and returns a route recommendation | Current RSU data, historical data, and road topology |
| Vehicle density database | Stores long-term observations for the same road and time of day | Historical density, speed, congestion, and travel time |
| Traffic signals | Affect traffic flow and intersection waiting time | Signal state, cycle length, and waiting time |
| School zone | Creates predictable, time-dependent congestion | Active period, reduced speed, and additional delay |
| Data analytics module | Estimates road conditions and compares candidate routes | Estimated density and predicted road or route cost |
| Optimal route guidance | Provides feedback to the traveler | Recommended route and expected travel time |

#### Scenario Data Flow

```text
Vehicles broadcast CAMs
        -> RSUs estimate current density on each road section
        -> RSUs send current traffic data to the TCC
        -> TCC retrieves historical density for the same road and time
        -> Data analytics module estimates road conditions
        -> TCC calculates the total cost of Route 1 and Route 2
        -> TCC recommends the route with the lower expected travel time
```

The paper combines current and historical density using the following weighted estimate:

```text
estimated_density = alpha * current_density
                  + (1 - alpha) * historical_density
```

`alpha` controls the importance of real-time information. A larger value is appropriate when traffic conditions change rapidly, while a smaller value gives more weight to stable historical patterns.

The route costs can be represented conceptually as:

```text
route_1_cost = cost(FG) + cost(GB) + cost(BD) + cost(DP)
route_2_cost = cost(FH) + cost(HM) + cost(MN) + cost(NP)
```

#### Traffic Conditions Tested in the Paper

| Time | Traffic Condition | Expected Decision |
| --- | --- | --- |
| 06:00 | Low traffic density | Route 1 |
| 12:00 | Recurring school-zone congestion | Route 2 |
| 18:00 | Unexpected accident and developing congestion | Route 2 when current data is included |
| 00:00 | Low traffic density | Route 1 |

The school-zone condition represents **recurring congestion**. It can be identified from historical observations because a similar pattern occurs at the same time on multiple days. The accident condition represents **unexpected congestion**. Historical data alone cannot identify the new incident, so current RSU data is necessary.

The paper compares three decision approaches:

1. **Shortest-distance routing:** selects the physically shortest route without considering traffic conditions.
2. **Historical-density routing:** uses traffic patterns stored in the TCC database.
3. **Current-plus-historical analytics:** combines current RSU observations with historical density.

At 12:00, the shortest route takes approximately 5.2 minutes, while the analytics-based alternative takes approximately 3.02 minutes. At 18:00, using current density together with historical information reduces the trip time by approximately four minutes because it responds to the unexpected event.

The scenario can be summarized as the following causal chain:

```text
Time + road properties + traffic event
        -> current and historical vehicle density
        -> estimated congestion or road travel time
        -> route cost
        -> route selection
        -> total trip time
```

#### Scenario Research Question

> How can current vehicle-density data collected by RSUs and historical vehicle-density data stored at the TCC be combined to select the optimal route and reduce travel time under recurring and unexpected congestion?

The original route-guidance scenario is a data analytics and simulation example rather than a trained machine learning model. It uses weighted density estimation and route-cost comparison. No row-level dataset, CSV file, or train/test data is provided in the paper. The authors generated mobility traces in MATLAB and imported them into the NS-3 simulator. Therefore, Figure 3 provides the system architecture and dataset design requirements, but the coursework must develop its own observations.

For a dataset that directly represents Figure 3, the most suitable observation unit is one road segment at one timestamp, for example:

```text
one row = traffic state of road section BD at 12:05
```

This scenario provides a simple analytics baseline that can later be extended with machine learning to learn nonlinear relationships between time, road segment, current density, historical density, speed, incidents, signal delay, travel time, and congestion.

### 5.2 Adaptive Transmission Range Selection

The paper also studies how C-ITS can adapt vehicle wireless transmission range based on vehicle density.

The logic is:

- Low vehicle density: larger transmission range is acceptable.
- High vehicle density: smaller transmission range reduces packet collision.

The paper shows that adaptive transmission range can improve Packet Delivery Ratio (PDR) by about 0.04 to 0.2 in the simulated scenarios.

This is useful as a second possible ML topic, but it requires networking data such as PDR, packet loss, channel busy time, and transmission range.

## 6. Recommended Machine Learning Direction

For this repository and the available Week7 bus data, the best ML development direction is:

## Congestion-Aware Delay Prediction and Route Recommendation

This is strongly connected to the paper's route guidance scenario and can be implemented using the current ITS dataset.

### Research Question

Can a machine learning model predict bus delay or congestion level using ITS traffic data, and can the prediction be used to recommend better route or traffic management decisions?

### Why This Fits the Paper

The paper uses data analytics to improve route guidance by combining current and historical traffic density. The proposed ML algorithm extends this by replacing the simple weighted average with a supervised learning model.

Instead of only using:

```text
current density + historical density
```

the ML model can learn from:

- time of day,
- route ID,
- stop name,
- vehicle speed,
- historical average delay,
- historical average speed,
- congestion indicators,
- operational conditions.

## 7. Proposed Machine Learning Algorithm

### Algorithm Name

**C-ITS Congestion-Aware Delay Prediction Model**

### Algorithm Type

Supervised machine learning.

Two versions can be developed:

| Version | ML Task | Target Variable | Recommended Model |
| --- | --- | --- | --- |
| Version A | Regression | `delay_minutes` | Random Forest Regressor or Gradient Boosting Regressor |
| Version B | Classification | `congestion_level` | Random Forest Classifier or Logistic Regression |

Version A is better if the goal is to predict the number of delay minutes.  
Version B is better if the goal is to classify traffic as Low, Medium, or High congestion.

## 8. Dataset Mapping

The existing Week7 script uses the following relevant fields:

| Field | ITS Meaning | Possible ML Use |
| --- | --- | --- |
| `bus_id` | Vehicle identifier | Grouping, fleet-level analysis |
| `route_id` | Route identifier | Categorical feature |
| `stop_name` | Road segment or stop location | Categorical feature |
| `scheduled_time` | Planned arrival time | Used to extract hour, peak/off-peak period |
| `actual_time` | Actual arrival time | Used to calculate delay target |
| `speed_kmh` | Vehicle operating speed | Real-time traffic feature |
| `engine_temp_c` | Vehicle health indicator | Optional CVO feature |
| `co2_g_km` | Emissions indicator | Optional environmental feature |
| `breakdown_risk` | Vehicle risk label | Optional classification target |

The most relevant fields for the paper-based ML model are:

- `route_id`
- `stop_name`
- `scheduled_time`
- `actual_time`
- `speed_kmh`
- derived `delay_minutes`
- derived `time_of_day`
- derived `peak_period`
- historical average speed by route and stop
- historical average delay by route and stop

## 9. Feature Engineering Plan

### 9.1 Time Features

From `scheduled_time`, create:

- `hour`
- `minute`
- `time_period`
- `is_peak_hour`

Example time periods:

| Time Period | Rule |
| --- | --- |
| Morning peak | 07:00-09:00 |
| Midday | 09:00-15:00 |
| Evening peak | 16:00-18:00 |
| Night | 18:00-24:00 |

This follows the paper's experiment, where performance is compared at 6am, 12pm, 6pm, and 12am.

### 9.2 Traffic Features

Create:

- `avg_speed_by_stop`
- `avg_speed_by_route`
- `avg_delay_by_stop`
- `avg_delay_by_route`
- `low_speed_flag`
- `congestion_level`

Example congestion label:

```text
if speed_kmh < 10:
    congestion_level = "High"
elif speed_kmh < 20:
    congestion_level = "Medium"
else:
    congestion_level = "Low"
```

### 9.3 Delay Target

Create:

```text
delay_minutes = actual_time - scheduled_time
```

For regression:

```text
target = delay_minutes
```

For classification:

```text
target = congestion_level
```

### 9.4 Data Leakage Warning

If the model predicts delay before a bus reaches the stop, do not use `actual_time` as an input feature. It should only be used to calculate the target variable.

Valid input features:

- route ID,
- stop name,
- scheduled hour,
- historical average speed,
- historical average delay,
- current observed speed if available.

Invalid input feature for pre-trip prediction:

- actual arrival time.

## 10. Model Design

### Baseline Model

The paper's formula can be used as a baseline:

```text
predicted_delay = alpha * current_delay_indicator + (1 - alpha) * historical_average_delay
```

This baseline is simple and explainable, but it cannot easily model complex relationships.

### Machine Learning Model

Recommended model:

```text
Random Forest Regressor
```

Reasons:

- works well with small to medium tabular datasets,
- handles nonlinear relationships,
- does not require heavy feature scaling,
- provides feature importance,
- easier to explain than deep learning.

Alternative models:

- Linear Regression as a simple baseline,
- Decision Tree for interpretability,
- Gradient Boosting for stronger prediction performance,
- Random Forest Classifier for congestion level classification.

## 11. Proposed Workflow

```text
1. Load bus_combined.xlsx
2. Convert scheduled_time and actual_time to datetime
3. Calculate delay_minutes
4. Create time-based features
5. Create historical route and stop features
6. Create congestion_level labels
7. Split data into training and testing sets
8. Train baseline model
9. Train machine learning model
10. Evaluate performance
11. Generate ITS decision output
```

## 12. Pseudocode

```python
load dataset

convert scheduled_time to datetime
convert actual_time to datetime

delay_minutes = actual_time - scheduled_time

hour = scheduled_time.hour
is_peak_hour = hour in [7, 8, 16, 17, 18]

avg_delay_by_route = historical average delay grouped by route_id
avg_speed_by_stop = historical average speed grouped by stop_name

if speed_kmh < 10:
    congestion_level = "High"
elif speed_kmh < 20:
    congestion_level = "Medium"
else:
    congestion_level = "Low"

features = [
    route_id,
    stop_name,
    hour,
    is_peak_hour,
    avg_delay_by_route,
    avg_speed_by_stop,
    speed_kmh
]

target = delay_minutes

train RandomForestRegressor
evaluate using MAE, RMSE, R2

for each route option:
    predict delay

recommend route with lowest predicted delay
```

## 13. Evaluation Plan

### Regression Evaluation

Use these metrics for delay prediction:

- MAE: Mean Absolute Error
- RMSE: Root Mean Squared Error
- R2 score

Interpretation:

- Lower MAE means the model predicts delay more accurately.
- Lower RMSE means fewer large prediction errors.
- Higher R2 means the model explains more variation in delay.

### Classification Evaluation

If predicting congestion level:

- Accuracy
- Precision
- Recall
- F1-score
- Confusion matrix

For ITS safety and traffic management, recall for high congestion is especially important because missing a high-congestion case can lead to poor routing decisions.

### ITS Decision Evaluation

Compare:

- shortest route baseline,
- historical average delay baseline,
- machine learning predicted delay route.

Possible result format:

| Method | Predicted Travel Time | Decision Quality |
| --- | --- | --- |
| Shortest route | May fail during congestion | Weak under incidents |
| Historical average | Good for regular patterns | Weak under sudden events |
| ML prediction | Can combine multiple factors | Better for dynamic route guidance |

## 14. Expected Output

The final ML program should produce:

- predicted delay for each bus stop or route,
- congestion level for each route segment,
- list of high-risk bottleneck locations,
- route recommendation based on predicted delay,
- model evaluation report,
- feature importance chart.

Example output:

```text
Route R1 predicted delay: 8.5 minutes
Route R2 predicted delay: 4.1 minutes
Recommended route: R2
Reason: lower predicted delay and lower congestion level
```

## 15. Connection Between Paper and Proposed Algorithm

| Paper Concept | Proposed ML Implementation |
| --- | --- |
| TCC collects data from RSUs | Python program loads and aggregates ITS data |
| Vehicle density supports route guidance | Speed and delay indicators estimate congestion |
| Historical and current data are combined | Historical averages and current speed become ML features |
| Route with lower congestion is selected | Model recommends route with lowest predicted delay |
| Data analytics improves C-ITS reliability | ML produces actionable transport decisions |
| Feedback to vehicles | Output route recommendation or congestion warning |

## 16. Critical Analysis of the Paper

### Strengths

- The paper clearly explains the role of data analytics in C-ITS.
- It connects communication systems with transport decision-making.
- It provides practical application scenarios instead of only theory.
- The route guidance example is easy to translate into a machine learning problem.
- The adaptive transmission range example shows that data analytics can improve communication reliability, not only traffic flow.

### Limitations

- The experiments are based on simulation rather than real city deployment.
- The route guidance analytics method is simple and mostly based on weighted density estimation.
- The paper does not provide a complete machine learning model.
- Privacy and cybersecurity risks are not deeply evaluated.
- Large-scale deployment cost is not fully discussed.
- The paper does not compare many ML algorithms.
- The paper does not provide an open dataset.

### How the Coursework Can Improve on the Paper

The coursework can extend the paper by developing an actual machine learning model:

- Use supervised learning instead of only weighted average.
- Train the model on ITS data.
- Evaluate prediction quality using ML metrics.
- Generate route or congestion recommendations.
- Visualize feature importance to explain the model.

## 17. Suggested Implementation Stages

### Stage 1: Data Preparation

- Load the Excel dataset.
- Clean timestamp fields.
- Calculate delay.
- Encode categorical variables.
- Create peak-hour features.

### Stage 2: Exploratory Data Analysis

- Plot average speed by stop.
- Plot average delay by route.
- Identify bottleneck stops.
- Compare peak and off-peak delay.

### Stage 3: Baseline Analytics

- Use historical average delay as the first prediction.
- Compare current speed against bottleneck threshold.
- Create congestion labels.

### Stage 4: Machine Learning Model

- Train Random Forest Regressor for delay prediction.
- Train Random Forest Classifier for congestion classification if needed.
- Tune model parameters.
- Evaluate model performance.

### Stage 5: ITS Decision Layer

- Rank routes by predicted delay.
- Flag high-congestion locations.
- Recommend the route with the lowest predicted travel time.
- Explain the recommendation using feature importance.

## 18. Possible Research Aim for Assignment

**Aim:**  
To develop a machine learning-based congestion-aware delay prediction algorithm for an Intelligent Transport System, inspired by data analytics methods for Cooperative Intelligent Transport Systems.

**Objective 1:**  
Analyze the role of data analytics in C-ITS using the selected research paper.

**Objective 2:**  
Prepare ITS traffic data by calculating delay, congestion level, and time-based features.

**Objective 3:**  
Develop a supervised machine learning model to predict delay or congestion level.

**Objective 4:**  
Evaluate the model and compare it with a simple baseline method.

**Objective 5:**  
Use the model output to support route recommendation or traffic management decisions.

## 19. Recommended Final Algorithm Choice

For this project, the recommended final algorithm is:

```text
Random Forest Regressor for bus delay prediction
```

This should be supported by:

```text
Random Forest Classifier for congestion level detection
```

The reason is practical: the dataset already contains operational ITS variables, and Random Forest is explainable enough for coursework while still being stronger than a simple linear or rule-based method.

## 20. Short Conclusion

The research paper shows that C-ITS can become more effective when vehicles, RSUs, and TCCs use data analytics to make real-time decisions. For this coursework, the most suitable development path is to build a machine learning model that predicts delay or congestion and then uses the prediction to support route guidance. This directly extends the paper's data analytics-based route guidance scenario into a practical supervised machine learning algorithm.

## 21. Paper Chapter-by-Chapter Summary

This section follows the structure of the original research paper and summarizes each chapter. It also explains how each part supports the development of a machine learning algorithm for this coursework.

### Abstract

**Chapter overview:**  
The abstract introduces C-ITS as an important technology for future road traffic management. It explains that vehicles, RSUs, and TCCs generate large amounts of mobility and service-related data. The authors argue that data analytics is needed to extract useful information from this data and improve C-ITS applications.

**Summary:**  
The abstract sets up the main idea of the paper: C-ITS produces large transport datasets, and analytics can improve the reliability and usefulness of ITS services.

**Connection to ML algorithm:**  
The abstract supports the idea that machine learning can be used to transform raw ITS data into useful outputs such as congestion prediction, delay prediction, route recommendation, or reliability improvement.

### 1. Introduction

**Chapter overview:**  
The introduction explains that C-ITS aims to improve road safety, traffic management, and driver comfort through vehicle connectivity. Vehicles communicate with each other, RSUs, and TCCs. The section also explains that C-ITS applications create large volumes of data, making data analytics necessary.

**Summary:**  
The paper argues that connectivity alone is not enough. The collected data must be analyzed so that the system can make better decisions. The authors identify data generation and data transmission as major challenges because C-ITS data requirements change according to the application, network load, and traffic condition.

**Connection to ML algorithm:**  
This chapter justifies the coursework problem. If traffic conditions change dynamically, a fixed rule-based system is limited. A machine learning model can learn patterns from historical and current ITS data and make adaptive predictions.

### 1.1 Main Contributions of This Work

**Chapter overview:**  
The paper lists three main contributions:

- discussion of challenges in applying data analytics to C-ITS,
- demonstration of data analytics benefits through two application scenarios,
- discussion of future research directions.

**Summary:**  
This section clarifies that the paper is partly a review paper and partly an application demonstration paper. It does not mainly propose a new ML algorithm. Instead, it provides a foundation for using analytics in C-ITS.

**Connection to ML algorithm:**  
Because the paper does not provide a complete new ML model, the coursework can extend it by developing one. The most suitable extension is to convert the paper's route guidance analytics into a supervised learning problem.

### 2. Related Works

**Chapter overview:**  
This chapter reviews the C-ITS architecture and existing data analytics techniques used in vehicular communications and ITS applications.

**Summary:**  
The related work shows that previous studies have used analytics for congestion control, cooperative transmission, smart parking, road condition monitoring, and distributed big data processing. It also shows that C-ITS data analytics is a broad area, not limited to traffic routing.

**Connection to ML algorithm:**  
This chapter helps identify possible ML directions. The strongest options for coursework are congestion prediction, delay prediction, route guidance, road condition classification, and vehicle risk detection.

### 2.1 C-ITS Architecture

**Chapter overview:**  
This section explains the core C-ITS components: vehicles, RSUs, and TCCs. Vehicles are mobile nodes, while RSUs and TCCs are fixed infrastructure nodes. Vehicles use OBUs to communicate with other C-ITS entities.

**Summary:**  
RSUs extend the communication range of vehicles and help collect traffic data. TCCs provide centralized traffic monitoring, traffic management, and feedback to vehicles. The paper also introduces the Local Dynamic Map, which stores road topology, signs, traffic conditions, weather, and highly dynamic vehicle messages.

**Connection to ML algorithm:**  
The ML system can be designed as a TCC-like analytics module. It receives traffic data, predicts delay or congestion, and sends feedback such as route recommendations.

### 2.2 Review of Data Analytics Techniques in C-ITS

**Chapter overview:**  
This section reviews different categories of data analytics techniques used in C-ITS. These include congestion control, cooperative transmission, C-ITS applications, and distributed computing of big data.

**Summary:**  
The paper shows that analytics can be used at different levels of ITS:

- communication layer,
- transport management layer,
- application service layer,
- big data processing layer.

**Connection to ML algorithm:**  
This supports a layered design for the coursework algorithm. The model should not only predict a value; it should also support an ITS decision such as route selection or congestion warning.

### 2.2.1 Congestion Control

**Chapter overview:**  
This subsection reviews methods that detect and reduce communication congestion in vehicular networks. It mentions channel usage, channel busy time, V2V messages, K-means clustering, Shapley value, and priority queuing.

**Summary:**  
When many vehicles communicate at the same time, the wireless channel can become congested. Analytics can detect this problem and adapt communication parameters such as transmission rate, transmission range, and contention window size.

**Connection to ML algorithm:**  
If network-level data is available, an ML classifier could predict communication congestion. In this repository, the available bus data is more suitable for traffic congestion and delay prediction, but the same idea applies: use data to detect congestion and recommend adaptation.

### 2.2.2 Cooperative Transmission

**Chapter overview:**  
This subsection reviews cooperative transmission techniques where vehicles help relay data for each other. The goal is to increase packet reception probability and network throughput.

**Summary:**  
The paper explains that relay vehicle selection and power allocation are important problems in vehicular communication. Data such as neighbor lists, time slots, transmission failure, and channel statistics can be used to make better communication decisions.

**Connection to ML algorithm:**  
This chapter is less directly related to the current bus dataset, but it suggests another possible ML extension: predicting the best relay vehicle or optimal transmission power based on network conditions.

### 2.2.3 C-ITS Applications

**Chapter overview:**  
This subsection discusses C-ITS applications that use collected sensor data to provide services. Examples include smart parking and road condition monitoring.

**Summary:**  
The paper mentions smart parking using IoT/RFID data and road condition monitoring using vehicle sensors such as accelerometers and gyroscopes. It also refers to Support Vector Machine classification for road anomaly severity.

**Connection to ML algorithm:**  
This section confirms that supervised ML is appropriate for ITS. For the coursework, the same principle can be used to classify congestion level or predict delay using bus operation data.

### 2.2.4 Distributed Computing of Big Data

**Chapter overview:**  
This subsection discusses big data tools such as Hadoop, MapReduce, Spark, and MongoDB for processing large ITS datasets.

**Summary:**  
C-ITS can generate data at a scale that is too large for simple local processing. Distributed systems can divide traffic data into smaller parts, process them in parallel, clean the data, and store it efficiently.

**Connection to ML algorithm:**  
The coursework dataset is small enough for Python and pandas, but the algorithm should be described as scalable. In a real C-ITS system, the same ML pipeline could be deployed in a cloud, Spark, or edge computing environment.

### 3. Data Analytics in C-ITS: Challenges

**Chapter overview:**  
This chapter is one of the most important sections of the paper. It identifies the main challenges that must be solved before data analytics can be applied effectively in C-ITS.

**Summary:**  
The paper lists challenges across the full data lifecycle: collection, dissemination, computation, metrics, analysis, and feedback. This is useful because it shows that an ITS analytics system is more than just training a model.

**Connection to ML algorithm:**  
The ML algorithm should be presented as part of a full pipeline:

```text
data collection -> preprocessing -> feature engineering -> model training -> evaluation -> ITS decision feedback
```

### 3.1 Data Collection

**Chapter overview:**  
This subsection discusses the types of data collected by C-ITS stations. CAMs and DENMs are highlighted as key safety-related messages.

**Summary:**  
CAMs provide periodic vehicle status information such as location, speed, and direction. DENMs provide event-driven warnings such as accidents or hazards. The paper also discusses other data sources such as road sensors, parking sensors, and service-related information.

**Connection to ML algorithm:**  
The coursework model should clearly define its input data. For the current dataset, the practical input data includes route, stop, scheduled time, speed, and historical delay.

### 3.2 Data Dissemination

**Chapter overview:**  
This subsection explains how C-ITS data can be shared using different wireless technologies such as IEEE 802.11p, LTE-V2X, 5G V2X, Bluetooth, and Zigbee.

**Summary:**  
Reliable data dissemination is important because ITS decisions depend on timely and accurate data. Safety messages require low latency and high reliability.

**Connection to ML algorithm:**  
The ML model should account for the fact that data may be delayed, missing, or noisy. If extending the project, missing values and delayed observations should be handled during preprocessing.

### 3.3 Data Computation

**Chapter overview:**  
This subsection compares centralized and distributed computation. Vehicles can make local safety decisions, while TCCs can make city-level traffic management decisions.

**Summary:**  
Distributed computation is useful for urgent local safety decisions. Centralized computation is useful for route guidance, city-wide congestion control, and long-term traffic analysis.

**Connection to ML algorithm:**  
The proposed coursework model fits the centralized approach. It behaves like a TCC analytics module that processes historical and current data to recommend a decision.

### 3.4 Metrics

**Chapter overview:**  
This subsection explains that performance measurement is a key challenge. The paper discusses safety awareness and packet success rate as possible metrics.

**Summary:**  
An ITS analytics system needs metrics that match the application goal. For safety applications, awareness and message reliability matter. For route guidance, travel time and delay matter.

**Connection to ML algorithm:**  
For this coursework, useful metrics are MAE, RMSE, R2, accuracy, recall, F1-score, and confusion matrix. If the model predicts high congestion, recall is important because missing a congested route can cause poor traffic decisions.

### 3.5 Data Analysis

**Chapter overview:**  
This subsection explains that C-ITS data must be analyzed to find relationships between variables such as vehicle density, packet loss, security overhead, and safety awareness.

**Summary:**  
The paper gives examples of correlations, such as high vehicle density causing wireless congestion and reducing safety awareness. It also explains that stronger security can increase packet overhead and reduce message delivery performance.

**Connection to ML algorithm:**  
This directly supports feature engineering. The model should learn relationships between operational variables such as speed, stop, route, time period, and delay.

### 3.6 Feedback

**Chapter overview:**  
This subsection explains that analytics output should be used to adapt system behavior. Feedback can affect application parameters, MAC/PHY parameters, or safety decisions.

**Summary:**  
Examples include adjusting transmission power, using fuzzy logic for decision-making, or changing parameters according to traffic conditions.

**Connection to ML algorithm:**  
The model output should be converted into a practical ITS recommendation. For example:

- predicted high congestion -> issue congestion warning,
- predicted high delay -> recommend an alternative route,
- predicted vehicle risk -> flag maintenance action.

### 4. Using Data Analytics for C-ITS Applications

**Chapter overview:**  
This chapter provides two practical examples showing how analytics can improve C-ITS: efficient route guidance and adaptive transmission range selection.

**Summary:**  
This is the most useful chapter for the coursework because it moves from theory to application. The authors use simulation to show how analytics can improve traffic and communication outcomes.

**Connection to ML algorithm:**  
The route guidance example should be used as the main inspiration for the proposed ML algorithm.

### 4.1 Efficient Route Guidance Application

**Chapter overview:**  
This subsection presents a route guidance scenario where the TCC chooses a route based on current and historical vehicle density. The paper compares shortest route selection with data analytics-based route selection.

**Summary:**  
The paper shows that shortest distance is not always the best route. During congestion or accidents, a longer route may produce a shorter travel time. The TCC estimates traffic density using both current RSU data and historical density data.

**Connection to ML algorithm:**  
This is the strongest foundation for the coursework algorithm. A machine learning model can improve the paper's weighted density formula by learning from multiple variables:

- route,
- stop,
- time of day,
- speed,
- historical delay,
- historical speed,
- congestion label.

The ML output can be used to recommend the route with the lowest predicted delay.

### 4.2 Adaptive Transmission Range Selection

**Chapter overview:**  
This subsection presents a method for adjusting vehicle transmission range according to vehicle density.

**Summary:**  
When vehicle density is low, vehicles can use a larger transmission range. When vehicle density is high, reducing transmission range can reduce packet collisions and improve packet delivery ratio. The paper reports that adaptive range selection improves PDR by about 0.04 to 0.2.

**Connection to ML algorithm:**  
This is a possible alternative ML topic if network data is available. A model could predict the best transmission range using density, packet loss, PDR, and channel busy time. However, the current repository's bus dataset is better suited for delay and congestion prediction.

### 5. Potential Future Use Cases of Data Analytics in C-ITS

**Chapter overview:**  
This chapter discusses future directions where analytics can further improve C-ITS.

**Summary:**  
The paper identifies three future use cases:

- traffic management in smart cities,
- vehicle safety with network security analysis,
- data outlier detection.

**Connection to ML algorithm:**  
These future use cases can be used as extension ideas in the assignment discussion or future work section.

### 5.1 Traffic Management in Smart Cities

**Chapter overview:**  
This subsection discusses how TCCs can use city-level traffic data to improve routing and reduce congestion.

**Summary:**  
Instead of optimizing travel for a single vehicle, a smart city traffic system should optimize traffic flow across the network. The paper mentions deep learning as a promising approach for traffic flow prediction.

**Connection to ML algorithm:**  
The proposed delay prediction model is a small-scale version of smart city traffic management. It can later be extended to predict city-wide traffic flow.

### 5.2 Enhancing Vehicle Safety with Network Security Analysis

**Chapter overview:**  
This subsection explains that C-ITS must protect vehicles from false or malicious messages, but security mechanisms add communication overhead.

**Summary:**  
There is a trade-off between security and communication performance. Stronger security may increase packet size and verification delay, which may reduce safety awareness.

**Connection to ML algorithm:**  
An advanced ML extension could classify suspicious messages, prioritize important messages, or predict when security overhead may harm real-time safety performance.

### 5.3 Data Outlier Detection

**Chapter overview:**  
This subsection discusses the problem of incorrect data from faulty sensors or attacks.

**Summary:**  
Vehicle sensor errors can create dangerous decisions. For example, sudden unrealistic changes in GPS position or speed may indicate faulty data or malicious input.

**Connection to ML algorithm:**  
This is another strong ML direction. An anomaly detection model could identify unusual speed, delay, route, or sensor readings. For the current coursework, this can be mentioned as future work after the delay prediction model.

### 6. Conclusion

**Chapter overview:**  
The conclusion summarizes that data analytics can improve C-ITS applications such as route guidance and wireless communication reliability.

**Summary:**  
The paper concludes that C-ITS can benefit from analytics across multiple areas: traffic management, adaptive network security, data forensics, and reliable communication.

**Connection to ML algorithm:**  
The conclusion supports the final coursework direction: develop an ML-based ITS analytics model that uses transport data to predict congestion or delay and generate useful traffic management recommendations.

## 22. Overall Chapter-Based Takeaway

The paper's structure moves from background to application:

```text
Introduction -> Architecture -> Existing analytics techniques -> Challenges -> Application scenarios -> Future use cases
```

The main lesson is that C-ITS needs a complete analytics pipeline, not just vehicle communication. For the coursework, the most practical algorithm is a supervised ML model for delay prediction or congestion classification because it directly extends the paper's route guidance scenario and can be implemented using the available bus operation dataset.
