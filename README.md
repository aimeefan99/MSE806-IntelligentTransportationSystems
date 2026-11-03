# MSE806 - Intelligent Transportation Systems (ITS)

This repository holds the course materials, data processing scripts, and machine learning models for **MSE806 Intelligent Transportation Systems (ITS)**. The work focuses on Cooperative ITS (C-ITS) architectures, telemetry data analytics, and practical machine learning applications in urban traffic management.

---

## Table of Contents

- [Overview & Course Scope](#overview--course-scope)
- [Weekly Activities](#weekly-activities)
  - [Week 2: ITS Taxonomy and System Architecture](#week-2-its-taxonomy-and-system-architecture)
  - [Week 4: Subsystems & Public Transit Telemetry](#week-4-subsystems--public-transit-telemetry)
  - [Week 7: Data Analytics & Visualization Pipeline](#week-7-data-analytics--visualization-pipeline)
  - [Week 8: C-ITS Research Foundation & Route Guidance](#week-8-c-its-research-foundation--route-guidance)
  - [Week 9: Machine Learning Paradigms & Agentic AI](#week-9-machine-learning-paradigms--agentic-ai)
  - [Week 10: LDM Architecture, Density Estimation & Telemetry Dataset](#week-10-ldm-architecture-density-estimation--telemetry-dataset)
  - [Week 11: Supervised Learning (Classification, Regression & ANN)](#week-11-supervised-learning-classification-regression--ann)
  - [Week 12: Unsupervised Learning (K-Means Clustering & Apriori Rules)](#week-12-unsupervised-learning-k-means-clustering--apriori-rules)
  - [Week 13: PCA Feature Compression & Autoencoder Anomaly Detection](#week-13-pca-feature-compression--autoencoder-anomaly-detection)
- [Dataset Architecture](#dataset-architecture)
- [Repository Structure](#repository-structure)
- [Quick Start](#quick-start)

---

## Overview & Course Scope

Intelligent Transportation Systems rely on connected sensors, wireless communication, and data analytics to optimize traffic flow, reduce delays, and improve safety. This course explores the transition from standalone transport infrastructure to Cooperative ITS (C-ITS), where vehicles, roadside equipment, and traffic centers exchange real-time telemetry to make dynamic routing and control decisions.

Key technical domains covered across the course include:

- **ITS Architecture & Standards**: Subsystem categorization (ATMS, ATIS, AVCS, CVO, APTS, ARTS, RWIS) and Local Dynamic Map (LDM) data layering (Type 1 static topology, Type 2 transient static signs, Type 3 dynamic events, Type 4 high-frequency CAM/DENM vehicle messages).
- **C-ITS Telemetry Analytics**: Real-time vehicle density estimation using weighted current and historical data ($\hat{\rho} = \alpha \rho_{\text{current}} + (1 - \alpha) \rho_{\text{past}}$), convex combination boundary analysis, and V2X Packet Delivery Ratio (PDR) degradation modeling.
- **Route Guidance Modeling**: Scenario evaluation based on Awais Javed et al. (*Data Analytics for Cooperative Intelligent Transport Systems*), comparing a physically shorter route subject to school zones and incidents against an alternative bypass route.
- **Supervised Machine Learning**: Feature engineering and model fitting for discrete classification (route selection, event type) and continuous regression (estimated density, travel time, signal quality) using Logistic Regression, SVC, Linear Regression, SVR, Decision Trees, Random Forests, and Artificial Neural Networks (ANN).
- **Unsupervised Learning & Anomaly Detection**: K-Means clustering for traffic regime profiling, Apriori association rule mining for incident-signal correlation, Principal Component Analysis (PCA) for 5D feature reduction, and deep autoencoders for detecting non-recurrent traffic anomalies via reconstruction error thresholding.
- **Agentic AI & Prompt Engineering**: LLM prompt design (CREATE, CoT, RAG) and autonomous agent frameworks (ReAct loops, multi-agent collaboration) for closed-loop traffic management.

---

## Weekly Activities

### Week 2: ITS Taxonomy and System Architecture
* **Focus**: Fundamentals of Intelligent Transportation Systems and functional classification.
* **Topics Covered**:
  - Core definition of ITS: Integrating smart technologies, sensor networks, and data processing to improve mobility, safety, and environmental sustainability.
  - Four functional areas: Road Transport Systems, Public Transport Systems (APTS), Commercial Vehicle Operations (CVO), and Traveller Information Systems (ATIS).
  - Operational closed-loop chain: $\text{Data Collection} \longrightarrow \text{Processing} \longrightarrow \text{Communication} \longrightarrow \text{Service Delivery}$.
  - Stakeholder roles and governance across transport planning, traffic operations, safety management, and customer services.

---

### Week 4: Subsystems & Public Transit Telemetry
* **Focus**: Subsystem breakdowns and practical transit data processing in Python.
* **Topics Covered**:
  - Detailed examination of key ITS functional subsystems: ATMS, ATIS, AVCS, CVO, APTS, ARTS, and RWIS.
  - Python data analysis on public bus telemetry ():
    - Computing schedule delay () from scheduled and actual arrival timestamps.
    - Filtering low-speed bottleneck segments ($\text{speed} < 10\text{ km/h}$) for ATMS traffic monitoring.
    - Assessing fleet maintenance risks based on engine temperature () and CO2 emissions () for CVO management.
    - Exploratory visual profiling using .

---

### Week 7: Data Analytics & Visualization Pipeline
* **Focus**: Standard data analytics workflow for transport telemetry.
* **Topics Covered**:
  - End-to-end data pipeline: Data Cleaning $\rightarrow$ Aggregation $\rightarrow$ Visualization $\rightarrow$ Predictive Modeling.
  - Role of Python libraries: Pandas for tabular data manipulation, NumPy for numerical array operations, Matplotlib for low-level plot control, and Seaborn for statistical visual styling.
  - Constructing transport KPIs, operational scorecards, and executive summaries.

---

### Week 8: C-ITS Research Foundation & Route Guidance
* **Focus**: In-depth analysis of Cooperative ITS literature and route choice scenario modeling.
* **Topics Covered**:
  - Review of *Data Analytics for Cooperative Intelligent Transport Systems* (Awais Javed et al., *Vehicular Communications*).
  - C-ITS entity roles: On-Board Units (OBUs) in vehicles, Roadside Units (RSUs), and Traffic Command Centers (TCCs).
  - Weighted vehicle density estimation:
    61105\hat{\rho} = \alpha \rho_{\text{current}} + (1 - \alpha) \rho_{\text{past}}61105
    where $\rho_{\text{current}}$ is sampled by RSUs, $\rho_{\text{past}}$ is retrieved from historical TCC logs, and $\alpha$ adjusts dynamically to real-time traffic volatility.
  - Evaluation of Figure 3 route guidance scenario: Route 1 (, shorter, exposed to school zone delay) vs. Route 2 (, longer bypass route activated during congestion or accidents).

---

### Week 9: Machine Learning Paradigms & Agentic AI
* **Focus**: ML categorizations, deep learning architectures, and agentic AI in traffic control.
* **Topics Covered**:
  - Four primary ML paradigms: Supervised Learning (Classification & Regression), Unsupervised Learning (Clustering, Dimensionality Reduction, Anomaly Detection), Semi-Supervised Learning, and Reinforcement Learning (reward-based signal control and dispatch).
  - Model capabilities: Discriminative (Y|X)$ vs. Generative (X, Y)$.
  - Overview of deep learning architectures: ANNs, CNNs for computer vision, RNNs/LSTMs for time-series travel time prediction, Transformers, Autoencoders, and GANs.
  - Prompt engineering (CREATE framework, Chain-of-Thought, RAG) and Agentic AI (ReAct reasoning loops, function calling, multi-agent coordination for automated traffic intervention).

---

### Week 10: LDM Architecture, Density Estimation & Telemetry Dataset
* **Focus**: LDM data layering, mathematical bounds, and dataset design.
* **Topics Covered**:
  - Four Local Dynamic Map (LDM) data layers: Type 1 permanent static, Type 2 transient static, Type 3 transient dynamic, and Type 4 highly dynamic CAM/DENM vehicle messages.
  - Proof of convex combination density bounds:
    61105\min(\rho_{\text{past}}, \rho_{\text{current}}) \le \hat{\rho} \le \max(\rho_{\text{past}}, \rho_{\text{current}})61105
  - Density classification regimes: Low (-60\text{ veh/km}$), Moderate (-120\text{ veh/km}$), and High Bottleneck (-200+\text{ veh/km}$).
  - Telemetry network performance: Calculating Packet Delivery Ratio ($\text{PDR} = \frac{\text{Packets Received}}{\text{Packets Sent}} \times 100\%$) and observing signal degradation under high vehicle density.
  - Dataset construction: Structuring  (Sheet1 static snapshot and Sheet2 dynamic time-series steps).

---

### Week 11: Supervised Learning (Classification, Regression & ANN)
* **Focus**: Supervised learning model training and multi-step inference.
* **Topics Covered**:
  - Formulating supervised mapping  = f(X)$ on transport telemetry data.
  - Discrete classification tasks: Predicting  ( vs ) and  using Logistic Regression, Naive Bayes, and Support Vector Classification (SVC).
  - Continuous regression tasks: Estimating , , and  using Linear Regression, Ridge/Lasso, and Support Vector Regression (SVR).
  - Dual-purpose multi-layer models: Decision Trees, Random Forests, and Artificial Neural Networks (ANN).
  - Modular python implementation: , , , , and .

---

### Week 12: Unsupervised Learning (K-Means Clustering & Apriori Rules)
* **Focus**: Clustering traffic regimes and association rule mining.
* **Topics Covered**:
  - K-Means Clustering (): Partitioning normalized  and  into three traffic regimes: Free-Flow, Moderate Traffic, and Severe Bottleneck. Comparing interpretability between =3$ and =5$ ().
  - Apriori Association Rule Mining (): Converting continuous telemetry into boolean items (, , ) to mine co-occurrence patterns, confirming that high traffic density correlates with signal degradation and triggers route redirection to Route 2.

---

### Week 13: PCA Feature Compression & Autoencoder Anomaly Detection
* **Focus**: High-dimensional feature reduction and neural network anomaly detection.
* **Topics Covered**:
  - Principal Component Analysis (): Compressing 5D continuous telemetry (, , , , ) down to 2D. PC1 (density/congestion) accounts for **72.5%** variance, and PC2 (PDR quality) accounts for **15.0%** variance, retaining **87.5%** total information.
  - Deep Autoencoder (): Building an Encoder-Decoder neural network trained on normal traffic patterns. Monitoring MSE reconstruction error over 50 training epochs (converging to $\approx 0.22$).
  - Anomaly Alert Dashboard: Setting a statistical threshold ($\mu + 2\sigma \approx 0.80$). Non-recurrent construction events on segment AD exhibit high reconstruction errors (/bin/zsh.90 \sim 1.00$) exceeding the threshold, while baseline traffic segments remain well below /bin/zsh.40$.
  - Comparison: PCA provides global 2D spatial visualization for exploratory analysis, while Deep Autoencoders provide automated real-time incident detection.

---

## Dataset Architecture

The primary dataset is , comprising static snapshot observations (Sheet1) and dynamic time-series steps (Sheet2):

| Column Name | Data Type | Description | Sample Value |
| :--- | :--- | :--- | :--- |
|  | Numeric | Simulation timestamp in minutes (sampled every 5 min) | , ,  |
|  | Categorical | Topological road segment from Figure 3 (, , , , , , , , ) |  |
|  | Numeric (veh/km) | Real-time vehicle density sampled by RSU ($\rho_{\text{current}}$) |  |
|  | Numeric (veh/km) | Historical average vehicle density from TCC logs ($\rho_{\text{past}}$) |  |
|  | Numeric (veh/km) | Weighted vehicle density estimate ($\hat{\rho}$) |  |
|  | Categorical | Incident state (, , ) |  |
|  | Numeric | Wireless Packet Delivery Ratio (PDR, range 0.0–1.0) |  |
|  | Categorical | Route guidance recommendation ( vs ) |  |
|  | Numeric | Actual or estimated travel time in minutes |  |

---

## Repository Structure



---

## Quick Start

### 1. Prerequisites & Virtual Environment

Setup using Python 3.10+:

Requirement already satisfied: pandas in ./.venv/lib/python3.14/site-packages (3.0.6)
Requirement already satisfied: numpy in ./.venv/lib/python3.14/site-packages (2.5.3)

### 2. Executing Core Algorithmic Modules

#### (1) Supervised Learning & ANN Neural Networks (Week 11)


#### (2) Unsupervised K-Means & Apriori Association Rules (Week 12)


#### (3) PCA Feature Compression & Deep Autoencoder Anomaly Detection (Week 13)

