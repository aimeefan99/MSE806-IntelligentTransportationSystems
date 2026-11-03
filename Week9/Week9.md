# Week9  
  
AI dependent on Machine learning  
  
# ==Machine Learning categorization:==  
Machine Learning is generally categorized into **four main paradigms** based on the nature of the learning signal or feedback available to the learning system, along with a secondary structural categorization based on model generative capability.  
机器学习通常根据**学习信号或反馈的性质**划分为**四大核心范式**，此外还可以根据**模型的生成能力**进行结构层面的分类。  
## 1. Four Primary ML Paradigms / 四大核心范式  
**==1. Supervised Learning== / 监督学习 - labled/ output known**  
* **English**: The model is trained on labeled data consisting of input-output pairs $(X, Y)$. The goal is to learn a mapping function $f(X) \rightarrow Y$.  
    * **Classification (分类)-==discrete==**: Predicts discrete class labels (e.g., transit route mode identification, fraud detection).  
		eg: emails spam or not  
**==		Algorithms: logistic regression, Naive Bayes, Supportive Vector classification==**  
    * **Regression (回归)-==continous==**: Predicts continuous numerical values (e.g., Estimated Time of Arrival [ETA], travel delay duration).  
**==		Algorithms: linear regression, Naive Bayes, Supportive Vector regression ==**  
* **中文**: 模型使用包含“输入-标签”对 $(X, Y)$ 的有标签数据进行训练。其目标是学习映射函数 $f(X) \rightarrow Y$。  
    * **分类**：预测离散的类别标签（例如：公交出行模式识别、欺诈检测）。  
    * **回归**：预测连续的数值（例如：估计到达时间 [ETA]、交通延误时长）。  
**==2. Unsupervised Learning== / 无监督学习 - Unlabled/ output unknown**  
* **English**: The model works with unlabeled data $(X)$ and aims to discover underlying structures, patterns, or probability distributions without human annotations.  
    * **Clustering (聚类)**: Groups similar data points together (e.g., passenger travel pattern profiling).  
    * **Dimensionality Reduction (降维)**: Simplifies data features while retaining essential variance (e.g., PCA).  
    * **Anomaly Detection (异常检测)**: Identifies data points that deviate significantly from expected patterns (e.g., GPS vs. odometry discrepancy, sensor failures).  
* **中文**: 模型处理无标签的数据 $(X)$，旨在无需人工标注的情况下挖掘潜在的结构、模式或概率分布。  
    * **聚类**：将相似的数据点划归为一组（例如：乘客出行模式聚类）。  
    * **降维**：在保留核心方差的同时简化特征维度（例如：主成分分析 PCA）。  
    * **异常检测**：识别显著偏离预期模式的数据点（例如：GPS 与里程计偏差检测、传感器故障识别）。  
**==3. Semi-Supervised Learning / 半监督学习==**  
* **English**: Combines a small amount of labeled data with a large amount of unlabeled data during training. It is used when labeling data is expensive or time-consuming, but unannotated data is abundant.  
* **中文**: 在训练过程中结合少量有标签数据和大量无标签数据。适用于数据标注成本高昂或耗时、但无标注数据极其丰富的场景。  
**==4. Reinforcement Learning (RL)== / 强化学习 ==model based/model free==**  
* **English**: An agent learns to make decisions by taking actions in an environment to maximize a cumulative reward. It relies on a trial-and-error approach governed by States ($S$), Actions ($A$), and Rewards ($R$).  
    * **Applications**: Adaptive Traffic Signal Control (e.g., TSP), autonomous vehicle navigation, dynamic fleet dispatching.  
* **中文**: 智能体（Agent）通过在环境（Environment）中采取动作（Action）以最大化累积奖励（Reward）来学习如何做出决策。它依赖于由状态（State）、动作（Action）和奖励（Reward）主导的“试错”机制。  
    * **典型应用**：自适应交通信号控制（如 TSP 公交信号优先）、自动驾驶车辆导航、动态车队调度。  
    *   
## 2. Alternative Categorization Frameworks / 其他补充分类维度  
**By Model Capability: Discriminative vs. Generative / 按模型能力划分：判别式与生成式**  
* **Discriminative Models (判别式模型)**:  
    * **English**: Models the conditional probability distribution $P(Y\vert{}X)$ to separate different classes or values directly (e.g., Decision Trees, SVM, XGBoost).  
    * **中文**: 对条件概率分布 $P(Y\vert{}X)$ 进行建模，直接对不同的类别或数值进行区分（例如：决策树、SVM、XGBoost）。  
* **Generative Models (生成式模型)**:  
    * **English**: Models the joint probability distribution $P(X, Y)$ or the data distribution $P(X)$ to generate new, synthetic data samples (e.g., GANs, Diffusion Models, LLMs).  
    * **中文**: 对联合概率分布 $P(X, Y)$ 或数据分布 $P(X)$ 进行建模，能够生成新的合成数据样本（例如：GANs、扩散模型、大语言模型 LLMs）。  
  
# ==Deep Learning（DL） - Dual purpose==  
**==Algorithms: Decision Tree, Random forest, Deep learning (Artificial )==**  
  
# 深度学习（Deep Learning, DL）指南与概述  
深度学习（Deep Learning, DL）是机器学习（Machine Learning, ML）的一个重要分支，其核心是以人工神经网络（Artificial Neural Networks, ANNs）为基础，通过构建多层（即“深度”）的非线性转换架构，自动从海量数据中提取多层次的抽象特征。  
以下为深度学习的核心概念、主流架构、应用场景及与传统 ML 的对比解析：  
## 1. Core Concepts / 核心概念  
* **Artificial Neural Networks (ANNs) / 人工神经网络**:  
    * **English**: Mathematical models inspired by the biological human brain, consisting of input layers, hidden layers, and output layers.  
    * **中文**: 受到人类生物大脑启发的数学模型，由输入层、隐藏层（Hidden Layers）和输出层组成。  
* **Deep Neural Networks (DNNs) / 深度神经网络**:  
    * **English**: Neural networks with multiple hidden layers (typically > 3) that enable representation learning at hierarchical levels of abstraction.  
    * **中文**: 包含多个隐藏层（通常在 3 层以上）的网络，能够进行分层的表征学习（从低级边缘/特征到高级语义/对象）。  
* **Backpropagation & Activation Functions / 反向传播与激活函数**:  
    * **Backpropagation (反向传播)**: 使用链式法则（Chain Rule）计算损失函数对每个权重参数的梯度，并配合梯度下降算法更新网络权重。  
    * **Activation Functions (激活函数)**: 如 ReLU、Sigmoid、Tanh 等，为网络引入**非线性**能力，使其能够拟合复杂的非线性函数。  
    *   
## 2. Key DL Architectures / 主流深度学习架构  
**1. Convolutional Neural Networks (CNNs) / 卷积神经网络**  
* **Primary Domain / 适用领域**: Computer Vision (CV) / 计算机视觉（图像识别、目标检测、图像分割）。  
* **Key Mechanism / 核心机制**: 卷积核（Kernels/Filters）进行局部感受野（Local Receptive Fields）的特征提取，具备平移不变性（Translation Invariance）和参数共享特性。  
**2. Recurrent Neural Networks (RNNs) & LSTMs / 循环神经网络与长短期记忆网络**  
* **Primary Domain / 适用领域**: Time-Series Data, NLP / 时间序列预测（如交通流预测、公交行程时间预测）、语音识别。  
* **Key Mechanism / 核心机制**: 引入隐状态（Hidden State）实现时间维度上的信息传递。LSTM 和 GRU 引入门控机制（Gate Mechanisms）解决了传统 RNN 的**梯度消失/爆炸**问题。  
**3. Transformer / 变换器架构**  
* **Primary Domain / 适用领域**: Large Language Models (LLMs), Generative AI, Advanced Vision / 自然语言处理、大语言模型、Vision Transformer (ViT)。  
* **Key Mechanism / 核心机制**: 自注意力机制（Self-Attention Mechanism）与并行化计算，能够捕获超长距离的上下文依赖关系（完全颠覆了传统 Sequential 的 RNN 架构）。  
**4. Autoencoders (AE) & GANs / 自动编码器与生成对抗网络**  
* **Autoencoders (自编码器)**: 由 Encoder（编码器）和 Decoder（解码器）组成，主要用于无监督特征提取、降维与异常检测（Anomaly Detection）。  
* **Generative Adversarial Networks (GANs, 生成对抗网络)**: 由生成器（Generator）和判别器（Discriminator）通过对抗博弈进行训练，用于图像生成、数据增强。  
## 3. Deep Learning vs. Traditional Machine Learning / 深度学习与传统机器学习对比  

| 特性 (Feature) | 传统机器学习 (Traditional ML) | 深度学习 (Deep Learning) |
| ----------------------------- | ------------------------------------- | ------------------------------------ |
| 特征提取 (Feature Extraction) | 依赖人工特征工程 (Manual Feature Engineering) | 自动表征学习 (End-to-End Feature Learning) |
| 数据量需求 (Data Dependency) | 在小/中型数据集上表现良好；达到上限后性能趋于平缓 | 极度依赖海量数据；数据量越大，性能表现越强 |
| 算力要求 (Computational Hardware) | 普通 CPU 即可高效运行 | 极度依赖 GPU / TPU 等并行计算加速硬件 |
| 可解释性 (Interpretability) | 较高（如决策树、线性回归易于解释） | 较低（通常被视为“黑盒”模型，需归因分析技术） |
  
****4. Application in Transportation & ITS / 深度学习在智能交通（ITS）中的典型应用****  
结合交通系统（ITS）领域的应用场景：  
1. **Travel Time Prediction (行程时间预测)**: 使用 LSTM/GRU 或 Transformer 结合历史 AVL/GPS 轨迹数据预测公交与道路车辆的到达时间（ETA）。  
2. **Traffic Flow Forecasting (交通流预测)**: 利用图卷积网络（GCN, Graph Convolutional Networks）捕捉交通路网的空间拓扑结构，配合时间序列模型做“时空（Spatio-Temporal）”预测。  
3. **Computer Vision & Incident Detection (计算机视觉与交通事件检测)**: 使用 CNN（如 YOLO、SSD）在摄像头视频流中实时识别道路事故、车道占用、违章行驶与行人过街。  
  
  
# ==Gen AI（prompt Engineering，LLM）==  
## 1. Core Concepts of Generative AI / 生成式 AI 核心概念  
* **Large Language Models (LLMs) / 大语言模型**:  
    * **English**: Deep learning models trained on vast amounts of text data to understand, process, and generate human-like language based on probabilistic token prediction.  
    * **中文**: 基于海量文本数据训练的深度学习模型，通过概率 Token 预测来理解、处理和生成类似人类的自然语言（如 GPT-4、Gemini、Claude）。  
* **Foundation Models / 基础模型**:  
    * **English**: Large-scale models trained on broad data at scale that can be adapted (fine-tuned) to a wide range of downstream tasks.  
    * **中文**: 在大规模通用数据上训练的大型模型，可通过微调（Fine-tuning）或提示适应各种下游特定任务。  
* **Hallucination / 幻觉现象**:  
    * **English**: A phenomenon where a Gen AI model generates plausible-sounding but factually incorrect or unverified information.  
    * **中文**: 生成式模型产生听起来合理但实际上不准确、不真实或未经验证的信息的现象。  
## 2. Key Framework of Prompt Engineering / 提示工程核心框架  
编写高质量 Prompt（提示词）通常建议包含以下六大核心要素（**C-R-E-A-T-E 框架**）：  
1. **Role / 角色定位**: 赋予模型具体的专家身份（例：*“你是一位资深的交通系统 ITS 专家”*）。  
2. **Context / 背景信息**: 提供任务所需的背景资料、约束条件或源数据（例：*“基于 Dublin Bus 2011 年的历史数据…”*）。  
3. **Instruction/Task / 明确指令**: 用清晰明确的动词说明需要执行的具体任务（例：*“分析并总结… / 审查以下段落中的语法硬伤”*）。  
4. **Examples / 示例 (Few-Shot)**: 提供标准输入输出范例，引导模型模仿特定格式或逻辑。  
5. **Output Format / 输出格式**: 指定希望获取的格式（例：*“用 Markdown 表格呈现”、“限制在 300 字以内”、“不要更改原有语法”*）。  
6. **Tone & Constraints / 语气与约束**: 限制模型的行为边界（例：*“保持学术中立语气”、“严禁润色或修改原有词汇”*）。  
## 3. Advanced Prompting Techniques / 进阶提示工程技术  
**1. Zero-Shot vs. Few-Shot Prompting (零样本与少样本提示)**  
* **Zero-Shot (零样本)**: 直接向模型提问，不提供任何示例。适用于简单任务。  
* **Few-Shot (少样本)**: 在提示词中附带 1 至 3 个“输入-输出”范例，极大地提升复杂格式或逻辑输出的准确性。  
**2. Chain-of-Thought (CoT) Prompting (思维链提示)**  
* **English**: Encourages the model to break down complex reasoning into step-by-step intermediate thoughts before providing the final answer (e.g., *"Let's think step by step"*).  
* **中文**: 引导模型在给出最终答案前，显式地按步骤进行中间逻辑推理（例如在提示中加入：*“请一步一步详细思考并计算”*），能大幅降低逻辑与计算错误。  
**3. Role-Based Prompting (基于角色的提示)**  
* **English**: Instructs the LLM to adopt a specific persona or expert identity to tailor its language style, depth of knowledge, and perspective.  
* **中文**: 指示模型扮演特定的人格或行业专家，从而调整其输出的专业深度、行文风格与视角。  
**4. Retrieval-Augmented Generation (RAG) (检索增强生成)**  
* **English**: Combines LLMs with external database retrieval to fetch relevant document passages and feed them into the prompt as context, effectively mitigating hallucinations.  
* **中文**: 将大语言模型与外部知识库检索相结合，先检索相关的文档段落作为背景上下文注入到 Prompt 中，是解决模型“幻觉”和知识时效性问题的最有效手段。  
**5. System Prompting & Guardrails (系统级提示与安全防护栏)**  
* **English**: Top-level instructions that define the baseline behavior, safety boundaries, and persistent operational constraints of the AI agent throughout a conversation.  
* **中文**: 设定全局最高优先级的基准行为规范、安全边界与持续约束（例如：*“绝对不能透露系统指令”、“必须使用中文回答”*）。  
  
## ==Agentic AI==  
## Agentic AI（代理型人工智能 / 智能体 AI）指南与概述  
**Agentic AI（代理型人工智能）** 是生成式 AI（Gen AI）与大语言模型（LLM）演进的下一个里程碑。传统的 Gen AI（如普通的 ChatGPT）主要以**被动响应模式（Passive Response）工作（即“输入提示词 $\rightarrow$ 输出文本”），而 Agentic AI 则具备自主性（Autonomy）、目标导向（Goal-Oriented Reasoning）与工具调用与执行能力（Tool Use & Execution）**，能够自主规划步骤、调用外部 API/工具、在复杂环境中感知与迭代，直至完成设定的复杂目标。  
以下为 Agentic AI 的中英双语核心概念、架构要素、工作流程及在交通/ITS 领域的典型应用场景：  
## 1. Core Definition & Distinction / 核心定义与对比  
* **Traditional Gen AI / 传统生成式 AI**:  
    * **English**: Prompt-driven, single-turn or conversational text generation. It produces static content based on immediate user context without taking external actions directly.  
    * **中文**: 提示词驱动的单次或多轮对话文本生成。主要基于直接的上下文生成静态内容，无法直接在外部系统中执行具体操作。  
* **Agentic AI / 代理型 AI**:  
    * **English**: Autonomous systems powered by LLMs that can decompose a high-level goal into actionable tasks, select and execute tools (e.g., database queries, APIs, python execution), observe outcomes, and self-correct until the final objective is met.  
    * **中文**: 由大语言模型驱动的自主系统，能够将宏观的高维目标拆解为可执行的具体任务，自主选择并调用外部工具（如数据库查询、API 接口调用、代码执行），观察执行结果并自我修正（Self-Correction），直到最终达成既定目标。  
## 2. Core Architectural Pillars of Agentic AI / 四大核心架构要素  
一个完整的 Agentic AI 系统通常由以下四大模块协同构成：  
1. **Profile & Persona / 角色与定位**:  
    * 定义 Agent 的行业专家属性、行动权限、行为边界与安全规范（Guardrails）。  
2. **Memory / 记忆系统**:  
    * **Short-Term Memory (短期记忆)**: 当前任务执行路径中的上下文（如 Chain-of-Thought 推理链）。  
    * **Long-Term Memory (长期记忆)**: 借助向量数据库（RAG / Vector DB）保存历史经验、业务规则与长期知识。  
3. **Planning & Reasoning / 规划与推理能力**:  
    * **Sub-goal Decomposition (子目标拆解)**: 利用 Task Planning 将复杂的大任务分解为可依次执行的小步骤。  
    * **Reflection & Self-Correction (反思与自我修正)**: 在执行失败时重新评估路径（如 ReAct 范式：Reasoning + Acting）。  
4. **Tools & Action / 工具与行动执行**:  
    * 赋予 AI 超越文本生成的能力，允许其调用函数（Function Calling）、执行 Code、访问网络 API、读写数据库或向硬件控制器下发指令。  
## 3. Key Operational Workflows / 典型工作流范式  
**1. ReAct Framework (Reasoning + Acting / 推理与行动模式)**  
* **English**: The agent interleaves thought processes ("Reasoning") with concrete executions ("Acting") and observational feedback ("Observation") in a continuous loop.  
* **中文**: 智能体将思考过程（推理）与具体执行（行动）以及环境反馈（观察）交织在连续的循环回路中（思考 $\rightarrow$ 行动 $\rightarrow$ 观察 $\rightarrow$ 重新思考）。  
**2. Multi-Agent Collaboration / 多智能体协作**  
* **English**: Orchestrating multiple specialized AI Agents (e.g., a Planning Agent, a Coding Agent, and an Auditor Agent) that communicate and negotiate with each other to solve complex enterprise-grade problems.  
* **中文**: 编排多个具有专业分工的智能体（如：规划 Agent、代码执行 Agent、安全审计 Agent），通过彼此协作、互相质询与监督来解决复杂的企业级系统问题。  
## 4. Application in Transportation & ITS / 在智能交通（ITS）中的典型应用场景  
在智慧交通系统（ITS）中，Agentic AI 正在从“提供分析建议”向“闭环自动化调控”跨越：  
1. **Autonomous Incident Response (自主交通事件响应与闭环调控)**:  
    * **场景**: 当感知层（如 CCTV/雷达）检测到道路拥堵或事故时，Agentic AI 可以**自主规划救援方案**，调用 SCATS/SCOOT 接口**动态调整信号灯相位**，同时自动向 RTPI 系统发布乘客告警，并向调度员推送最优车辆重排方案。  
2. **Predictive Maintenance Agent (预测性维护智能体)**:  
    * **场景**: 监控车联网及 onboard ETM/AVLC 硬件日志。当检测到 missing polling 或传感器漂移时，Agent 不仅能诊断出故障原因，还能**自主在 ERP 系统中创建维修工单**，并协调调度系统将受影响车辆安全关断或下线。  
3. **Dynamic Fleet & Priority Dispatching (动态车队与 TSP 信号优先决策)**:  
    * **场景**: 结合路侧 V2I 通信，Agentic AI 在毫秒级时间内评估整条公交走廊的运行状态（延误时长、横向道路排队长度、行人延迟），**自主做出“早绿灯/延长绿灯/暂不优先”的优化决策**并直接向信号机下发控制指令。  
  
———————————————————————————  
**English:** The paper uses current RSU data and historical TCC data to recommend the fastest route. We choose supervised regression, using traffic conditions as inputs and actual travel time as the label. Therefore, we will simulate labeled road-segment data before selecting an algorithm.  
**中文：** 论文结合 RSU 实时数据和 TCC 历史数据推荐最快路线。我们选择监督回归，以交通状况为输入、实际行程时间为标签。因此先仿真生成带标签的路段数据，再选择算法。  
  
  
只描述收集机制，没有提供实际 dataset：  
* 车辆通过 CAM 定期发送位置、速度等信息；RSU 统计约 500–1000 米范围内的车辆，得到当前车辆密度，再通过 LTE 发送给 TCC。  
* TCC 将这些数据长期保存，并按道路和时间形成 historical density。  
所以 dataset 的核心确实是这两类数据，但历史数据不应单独随意生成，而应由早期的 current observations 累积计算：  
```
早期 RSU 数据 → TCC historical data
当天 RSU 数据 → current data

```
另外还需加入时间、路段、school zone、事故等场景信息，以及实际行程时间作为结果标签。  
  
  
  
**3.1 Data Collection 正是在回答数据从哪里来**。论文明确指出：  
* **CAM**：车辆周期发送的位置、速度、方向和状态数据；  
* **DENM**：事故、危险等事件数据；  
* **Road sensors / RSUs**：收集车辆消息及道路交通数据；  
* **RSU**：根据 CAM 计算车辆数量、速度和 current density；  
* **TCC**：保存过去的 RSU 数据，形成 historical density。  
所以我们的 dataset 应按这个链路构建：  
```
CAM + DENM
→ RSU current traffic data
→ TCC historical data
→ 根据车辆时间戳计算 travel time

```
  
  
最稳妥的做法是：使用交通仿真生成数据，而不是凭空填写 Excel，也不是先使用机器学习算法。推荐用 SUMO 重建 Figure 3。  
# 具体流程  
## 1. 建立道路网络  
创建两条路线及八个路段：  
```
Route 1: FG → GB → BD → DP
Route 2: FH → HM → MN → NP

```
为每个路段设置长度、车道数、限速、信号灯和 RSU。  
## 2. 设置三种场景  
* Normal：06:00、00:00，低流量。  
* School zone：12:00，Route 1 限速、延误增加。  
* Accident：部分日期18:00发生事故，减少 Route 1 的道路容量。  
交通密度参考论文设置为 50–200 vehicles/km。  
## 3. 重复运行仿真  
建议模拟30天，每5分钟记录一次。若每天模拟4个一小时的时段：  
```
30天 × 4时段 × 12个时间点 × 8路段
= 11,520条记录

```
## 4. 收集 current RSU data  
SUMO 中每个路段、每个时间点记录：  
* vehicle count  
* current density  
* average speed  
* traffic flow  
* signal delay  
* school-zone status  
* accident status  
## 5. 生成 historical TCC data  
历史数据不能独立随机生成，而是从前几天的 RSU 数据计算：  
```
historical_density
= 相同路段、相同时段、过去日期的平均密度

```
例如 Day 21 的 historical density 只能使用 Day 1–20。  
## 6. 获取 target output  
车辆完成路段后，由仿真记录：  
```
actual_segment_travel_time_seconds

```
最终一行数据类似：  

| timestamp | segment | current density | historical density | speed | school zone | accident | actual travel time |
| --------- | ------- | --------------- | ------------------ | ----- | ----------- | -------- | ------------------ |
| 12:05 | BD | 180 | 152 | 12 | 1 | 0 | 142 |
  
****7. 形成最终数据集****  
核心字段为：  
```
timestamp
segment_id
route_id
road_length_km
current_vehicle_count
current_density_veh_km
historical_density_veh_km
average_speed_kmh
traffic_flow_veh_hour
signal_delay_seconds
school_zone_active
accident_present
actual_segment_travel_time_seconds

```
完整逻辑是：  
```
SUMO车辆运行
→ RSU当前观测
→ 过去观测形成TCC历史数据
→ 仿真记录实际行程时间
→ 形成监督回归数据集

```
这一步只是在生成带标签的数据，还没有使用任何机器学习算法。  
