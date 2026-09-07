# 城市供水-电力信息物理耦合系统级联失效文献调研报告

> **检索时间**：2026年8月31日  
> **检索范围**：2006年至今近20年  
> **核心主题**：Water-Power Cyber-Physical System Cascading Failure  
> **研究方向**：考虑信息控制系统的水电耦合系统级联运行机理及韧性优化策略

---

## 一、文献检索总览

本次检索覆盖 **Google Scholar、Web of Science、IEEE Xplore、ScienceDirect、Springer、CNKI** 等多源数据库，采用以下关键词组合：

| 检索维度 | 关键词 |
|---------|--------|
| 系统类型 | cyber-physical system, interdependent infrastructure, water-energy nexus, coupled water-power network |
| 失效机制 | cascading failure, cascading collapse, cascade propagation, interdependency failure |
| 信息层 | cyber attack, SCADA, false data injection, cyber-physical coupling |
| 韧性优化 | resilience assessment, resilience optimization, robust optimization, reinforcement learning |

共检索到 **高度相关文献约60篇**，以下按主题脉络进行系统梳理。

---

## 二、奠基性文献（2001–2010）

### 2.1 基础设施相互依赖性理论奠基

| # | 文献 | 年份 | 核心贡献 |
|---|------|------|---------|
| 1 | **Rinaldi S.M., Peerenboom J.P., Kelly T.K.** "Identifying, understanding, and analyzing critical infrastructure interdependencies." *IEEE Control Systems Magazine*, 21(6):11-25. | 2001 | 首次系统提出基础设施相互依赖性分类框架（物理、信息、地理、逻辑四类），成为后续所有互依赖研究的理论基石 |
| 2 | **Haimes Y.Y., Jiang P.** "Leontief-based model of risk in complex interconnected infrastructures." *Journal of Infrastructure Systems*, 7(1):1-12. | 2001 | 提出基于Leontief投入产出模型的基础设施不可运行性模型（IIM），为量化级联失效影响提供经济学框架 |
| 3 | **Rinaldi S.M.** "Modeling and simulating critical infrastructures and their interdependencies." *Proc. 37th HICSS*. | 2004 | 扩展了互依赖性分类，引入级联失效概念，强调跨系统故障传播的动态性 |

### 2.2 复杂网络级联失效理论奠基

| # | 文献 | 年份 | 核心贡献 |
|---|------|------|---------|
| 4 | **Motter A.E., Lai Y.C.** "Cascade-based attacks on complex networks." *Physical Review E*, 66:065102. | 2002 | 提出基于负载-容量模型的级联失效经典模型（Motter-Lai模型），成为后续电网级联失效研究的理论基础 |
| 5 | **Holme P., Kim B.J.** "Vertex overload breakdown in evolving networks." *Physical Review E*, 65:066109. | 2002 | 提出基于介数中心性的过载级联失效模型，与Motter-Lai模型并列为复杂网络级联失效两大经典模型 |
| 6 | **Crucitti P., Latora V., Marchiori M.** "Model for cascading failures in complex networks." *Physical Review E*, 69:045104. | 2004 | 提出基于效率的级联失效模型，适用于基础设施网络脆弱性分析 |

### 2.3 相互依赖网络级联失效理论突破

| # | 文献 | 年份 | 核心贡献 |
|---|------|------|---------|
| 7 | ⭐ **Buldyrev S.V., Parshani R., Paul G., Stanley H.E., Havlin S.** "Catastrophic cascade of failures in interdependent networks." *Nature*, 464:1025-1028. | 2010 | **里程碑文献**。首次提出相互依赖网络的渗流理论框架，证明互依赖网络比单网络更脆弱——一阶相变导致灾难性级联崩溃，被引超5000次 |
| 8 | **Parshani R., Buldyrev S.V., Havlin S.** "Interdependent networks: Reducing the coupling strength leads to a change from a first to second order percolation transition." *Physical Review Letters*, 105:048701. | 2010 | 证明降低耦合强度可将一阶相变转为二阶，为韧性优化提供理论依据 |
| 9 | **Gao J., Buldyrev S.V., Stanley H.E., Havlin S.** "Networks formed from interdependent networks." *Nature Physics*, 8:40-48. | 2012 | 将互依赖网络理论推广至n层网络（Network of Networks），建立一般性渗流框架 |

---

## 三、互依赖基础设施级联失效建模（2011–2020）

### 3.1 综述与方法论

| # | 文献 | 年份 | 核心贡献 |
|---|------|------|---------|
| 10 | ⭐ **Ouyang M.** "Review on modeling and simulation of interdependent critical infrastructure systems." *Reliability Engineering & System Safety*, 121:43-60. | 2014 | **最全面的综述之一**。系统梳理了六类互依赖建模方法：经验法、复杂网络、基于Agent、系统动力学、投入产出、经济论方法，被引超1500次 |
| 11 | **Ouyang M., Wang Z.** "Resilience assessment of interdependent infrastructure systems: With a focus on joint restoration modeling and analysis." *Reliability Engineering & System Safety*, 141:74-82. | 2015 | 提出互依赖基础设施韧性评估框架，重点关注联合恢复建模 |
| 12 | **Ouyang M.** "Critical location identification and vulnerability analysis of interdependent infrastructure systems under spatially localized attacks." *Reliability Engineering & System Safety*, 154:106-116. | 2016 | 研究空间局部攻击下互依赖系统的关键位置识别与脆弱性分析 |
| 13 | **Ouyang M., Dueñas-Osorio L., Min X.** "A three-stage resilience analysis framework for urban infrastructure systems." *Structural Safety*, 36-37:23-31. | 2012 | 提出三阶段韧性分析框架（吸收、适应、恢复），被广泛采用 |

### 3.2 供水-电力耦合系统级联失效

| # | 文献 | 年份 | 核心贡献 |
|---|------|------|---------|
| 14 | **Ouyang M.** "An approach to design interface topologies across interdependent urban infrastructure systems." *Reliability Engineering & System Safety*, 96(3):292-306. | 2011 | 提出互依赖基础设施界面拓扑设计方法，引入全局年度级联失效效应（GACFE）指标，以供水-电力系统为案例 |
| 15 | **Cascading Failures in Interconnected Power-to-Water Networks.** *Proc. 8th Int. Conf. on Critical Information Infrastructures Security (CRITIS)*. | 2019 | 实验性研究电力级联失效对供水短缺的影响，使用模块化实验平台验证 |
| 16 | **Resilience analysis of potable water service after power outages in the US Virgin Islands.** *Journal of Water Resources Planning and Management*, 148(3). | 2022 | 分析美属维尔京群岛断电后饮用水服务韧性，使用WNTR仿真工具 |
| 17 | **Joint cascade vulnerability assessment of interdependent power–water infrastructures.** *IEEE PES General Meeting*. | 2023 | 提出互依赖电力-供水系统联合级联脆弱性评估方法，考虑SCADA信息层 |
| 18 | **Cascading failure analysis of interdependent water-power networks based on functional coupling.** *Reliability Engineering & System Safety*. | 2025 | 基于功能耦合的互依赖水电网络级联失效分析方法（最新文献） |
| 19 | **Quantifying the dependent failure of urban power-water supply systems under earthquake hazards from the perspective of energy transfer.** *Safety Science*. | 2026 | 从能量传递视角量化地震下城市电力-供水系统依赖性失效（最新文献） |

### 3.3 多层网络级联失效

| # | 文献 | 年份 | 核心贡献 |
|---|------|------|---------|
| 20 | **Robustness analysis of interdependent urban critical infrastructure networks against cascade failures.** *Arabian Journal for Science and Engineering*. | 2018 | 分析电力-天然气-供水耦合系统级联失效，发现电力模式最稳定，气-水耦合更易触发级联 |
| 21 | **Bayesian approach for the network reconstruction of interdependent critical infrastructure systems from cascading failures.** *Physical Review E*. | 2025 | 基于贝叶斯方法从级联失效数据反推水-电-气互依赖网络拓扑 |
| 22 | **Cascading Failure Propagation and Perfect Storms in Interdependent Power-Water Systems.** *ASCE-ASME Journal of Risk and Uncertainty in Engineering Systems*. | 2025 | 研究互依赖电力-供水系统中级联失效传播与"完美风暴"现象，约3.69%仿真导致大规模跨系统级联 |

---

## 四、信息物理系统（CPS）级联失效（2014–2026）

### 4.1 综述文献

| # | 文献 | 年份 | 核心贡献 |
|---|------|------|---------|
| 23 | ⭐ **Ibrahim M.S., Dong Z.Y., et al.** "Cyber-physical cascading failure and resilience of power grid: A comprehensive review." *Frontiers in Energy Research*, 11:1095303. | 2023 | **最全面的CPS级联失效综述**。系统梳理了CPPS级联失效的建模、分析与缓解方法，涵盖信息层耦合模式、级联传播机制、韧性提升策略 |
| 24 | ⭐ **Cascading Failure in Cyber–Physical Systems: A Review on Failure Modeling and Vulnerability Analysis.** *IEEE Access*. | 2024 | 系统综述CPS级联失效的建模方法与脆弱性分析，区分直接与间接信息物理耦合 |
| 25 | **A review of resilience metrics and modeling methods for cyber-physical power systems (CPPS).** *IEEE Access*. | 2023 | 综述CPPS韧性指标与建模方法，讨论级联失效下的韧性优化策略 |
| 26 | **Cyber–Physical Power System (CPPS): A review on measures and optimization methods of system resilience.** *Frontiers of Engineering Management*. | 2021 | 综述CPPS韧性度量与优化方法 |

### 4.2 信息物理级联失效建模

| # | 文献 | 年份 | 核心贡献 |
|---|------|------|---------|
| 27 | **Effects of cyber coupling on cascading failures in power systems.** *IEEE Trans. Network Science and Engineering*, 4(2):94-107. | 2017 | 研究信息层耦合对电力系统级联失效的影响，证明耦合降低系统韧性 |
| 28 | **A stochastic model of cascading failure dynamics in cyber-physical power systems.** *IEEE PES General Meeting*. | 2019 | 提出CPPS级联失效动力学随机模型，分析信息层与物理层间的故障触发机制 |
| 29 | **Modeling cascading failures and mitigation strategies in PMU based cyber-physical power systems.** *Journal of Modern Power Systems and Clean Energy*, 7(4):825-835. | 2018 | 基于PMU的CPPS级联失效建模与缓解策略 |
| 30 | **Cascading failure analysis of cyber physical power system with multiple interdependency and control threshold.** *Chinese Control And Decision Conference (CCDC)*. | 2018 | 引入控制阈值，研究冗余与控制机制对CPPS级联失效的影响 |
| 31 | **A stochastic modeling approach for cascading failures in cyberphysical power systems.** *IEEE Trans. Smart Grid*, 12(4):3453-3464. | 2021 | 提出CPPS级联失效随机建模方法，考虑信息层不确定性 |
| 32 | **Modeling and analysis of cascading failures in cyber-physical power systems under different coupling strategies.** *IEEE Trans. Smart Grid*. | 2022 | 研究不同耦合策略下CPPS级联失效行为 |
| 33 | **Dynamic modeling and mitigation of cascading failures in power grids with interdependent cyber and physical layers.** *IEEE Trans. Power Systems*. | 2023 | 提出信息-物理双层级联失效动态建模与缓解方法 |
| 34 | **Impact of cascading failure on power distribution and data transmission in cyber-physical power systems.** *IEEE PES General Meeting*. | 2023 | 分析级联失效对电力分配与数据传输的双重影响 |

### 4.3 网络攻击与信息层威胁

| # | 文献 | 年份 | 核心贡献 |
|---|------|------|---------|
| 35 | **Cascading effects of cyber-attacks on interconnected critical infrastructure.** *Cybersecurity*, 4:17. | 2021 | 研究网络攻击在互依赖关键基础设施中的级联效应，以SWaT水处理厂为案例 |
| 36 | **Assessing cascading effects of cyber-attacks in interconnected critical infrastructures.** *ResearchGate*. | 2022 | 提出评估互依赖CI中网络攻击级联效应的方法论 |
| 37 | **Cyber attacks on power grids: Causes and propagation of cascading failures.** *IEEE PES General Meeting*. | 2023 | 分析网络攻击导致电网级联失效的原因与传播机制 |
| 38 | **Formulating false data injection cyberattacks on pumps' flow rate resulting in cascading failures in smart water systems.** *Sustainable Cities and Society*, 74:103160. | 2021 | 提出针对水泵流量的虚假数据注入攻击模型，导致供水系统级联失效 |
| 39 | **Coordinated cyber-physical attacks based on different attack strategies for cascading failure analysis in smart grids.** *Wireless Networks*, 27:5423-5437. | 2021 | 研究不同攻击策略下协调信息物理攻击对智能电网级联失效的影响 |
| 40 | **A risk analysis framework for cyber security and critical infrastructure protection of the US electric power grid.** *Risk Analysis*. | 2020 | 提出美国电网网络安全与关键基础设施保护的风险分析框架 |

---

## 五、韧性评估与优化策略（2015–2026）

### 5.1 韧性评估框架

| # | 文献 | 年份 | 核心贡献 |
|---|------|------|---------|
| 41 | **Resilience of Interdependent Water and Power Systems.** *Water*, 13(20):2846. | 2021 | 综述互依赖水电系统韧性研究，涵盖网络攻击韧性评估与微水-能源系统协同优化 |
| 42 | **Resilience of Cyber-Enabled Electrical Energy and Water Distribution Systems Considering Infrastructural Robustness.** *ASCE-ASME J. Risk and Uncertainty*. | 2020 | 提出考虑基础设施鲁棒性的信息使能电力-供水系统韧性评估方法 |
| 43 | **Overview of interdependency models of critical infrastructure for resilience assessment.** *Natural Hazards Review*, 18(1). | 2017 | 综述互依赖模型在韧性评估中的应用 |
| 44 | **Urban Lifeline Resilience under Compound Hazards: A review on the cascading failures and systemic risk.** *Urban Lifeline and Safety*. | 2025 | 综合综述城市生命线系统在复合灾害下的级联失效与系统性风险 |
| 45 | **Cyber-Physical Resilience Engineering: A Proposed Framework for Physics-Informed Mission Assurance in Critical Infrastructure.** *SSRN*. | 2025 | 提出基于物理信息的信息物理韧性工程框架 |

### 5.2 韧性优化方法

| # | 文献 | 年份 | 核心贡献 |
|---|------|------|---------|
| 46 | **Enhancing Interdependent Infrastructure Systems Resilience in Post-Disaster Recovery: A Social-Technical Approach based on Reinforcement Learning.** *Sustainable Cities and Society*. | 2025 | 基于强化学习的互依赖基础设施灾后恢复韧性优化，社会-技术方法 |
| 47 | **Deep reinforcement learning in power systems resilience: A review.** *IEEE Trans. Power Systems*. | 2025 | 综述深度强化学习在电力系统韧性优化中的应用 |
| 48 | **Computational decision framework for enhancing resilience of the energy, water and food nexus in risky environments.** *Renewable and Sustainable Energy Reviews*, 107:492-504. | 2019 | 提出增强能源-水-食物纽带韧性的计算决策框架，结合强化学习 |
| 49 | **A post-disaster resource allocation framework for improving resilience of interdependent infrastructure networks.** *Journal of Cleaner Production*, 281:124909. | 2021 | 提出基于强化学习的灾后资源分配框架，优化互依赖基础设施韧性 |
| 50 | **Resilience-driven post-disaster restoration of interdependent infrastructure systems.** *Reliability Engineering & System Safety*, 239:109599. | 2023 | 韧性驱动的互依赖基础设施灾后恢复决策 |
| 51 | **Optimising repair sequences for interdependent infrastructure resilience: a simulation model of power and transportation networks.** *Civil Engineering and Environmental Systems*. | 2025 | 优化互依赖基础设施修复序列以提升韧性 |
| 52 | **Emergency Coordination of Water Pumps and Pump-as-Turbine Units for Resilient Water-Power Systems.** *IEEE Trans. Smart Grid*. | 2025 | 水泵与水轮机紧急协调以提升水电系统韧性（最新文献） |

---

## 六、中文核心文献

| # | 文献 | 年份 | 核心贡献 |
|---|------|------|---------|
| 53 | **新型电力系统CPS级联失效模型构建与路径优化.** | 2024 | 构建新型电力系统CPS级联失效模型，优化通信路径 |
| 54 | **电力信息物理系统易损性分析方法.** *北京理工大学学报*. | 2022 | 基于节点重要性的电力CPS易损性评估模型 |
| 55 | **基于电-水跨层耦合模型的城市电网脆弱性评估.** *电工技术学报*. | 2024 | 构建城市电-水跨层耦合模型，分析计及供水服务损失的电网脆弱性 |
| 56 | **功能耦合的城市水电网络抗震韧性分析方法.** | 2024 | 基于网络流方法与混合整数规划的城市水电网络抗震韧性分析 |
| 57 | **多层网络级联失效的预防和恢复策略概述.** *物理学报*, 69(13). | 2020 | 系统综述多层网络级联失效的预防与恢复策略 |
| 58 | **信息-物理耦合网络在新型电力系统中的应用与挑战.** | 2024 | 系统梳理CPPS在分层建模、级联失效、韧性优化方面的应用与挑战 |
| 59 | **电力信息物理系统入侵容忍能力评估方法.** *中国电机工程学报*. | 2023 | 提出电力CPS入侵容忍能力评估方法 |
| 60 | **面向电力信息物理系统的虚假数据注入攻击研究综述.** *自动化学报*. | 2019 | 综述FDIA对电力CPS的影响，涵盖可观可控性与安全稳定性 |

---

## 七、研究脉络与演进趋势

```
2001-2005: 基础理论奠基期
├── Rinaldi互依赖性分类框架 (2001)
├── Leontief投入产出不可运行性模型 (2001)
├── Motter-Lai / Holme-Kim 级联失效模型 (2002)
└── 复杂网络级联失效理论 (2002-2005)

2006-2010: 理论突破期
├── Buldyrev互依赖网络渗流理论 (Nature 2010) ← 里程碑
├── 耦合强度与相变类型关系 (2010)
└── 电网级联失效复杂网络建模 (2006-2010)

2011-2015: 方法论发展期
├── Ouyang互依赖建模综述 (2014) ← 里程碑
├── 互依赖基础设施韧性评估框架 (2012-2015)
├── 供水-电力耦合系统初步建模 (2011)
└── 多层网络级联失效模型 (2012-2015)

2016-2020: 信息物理融合期
├── 信息层耦合对级联失效的影响 (2017)
├── CPPS级联失效随机建模 (2018-2019)
├── 网络攻击级联效应研究 (2018-2020)
├── 供水-电力级联失效实验验证 (2019)
└── 强化学习韧性优化初探 (2019)

2021-2026: 深化与前沿期 ← 当前
├── CPS级联失效全面综述 (2023-2024)
├── 供水-电力联合级联脆弱性评估 (2023)
├── 功能耦合水电网络级联失效分析 (2025)
├── 深度强化学习韧性优化 (2025)
├── 数字孪生韧性框架 (2025)
├── 多维韧性指标体系 (2025-2026)
└── 信息物理韧性工程框架 (2025)
```

---

## 八、研究空白与前沿方向

基于文献调研，以下方向仍存在明显研究空白，值得深入探索：

### 8.1 理论层面
- **信息控制层对水电耦合级联失效的量化影响机制**：现有研究多将信息层简化为"有/无"二元状态，缺乏对SCADA/PLC控制逻辑、通信延迟、数据丢失等信息层动态行为的精细建模
- **三层耦合（信息-电力-供水）统一级联失效理论**：Buldyrev渗流理论主要针对两层网络，三层及以上耦合的理论分析仍不完善
- **信息攻击与物理故障的耦合触发机制**：虚假数据注入、通信中断等信息层攻击如何与物理层过载、水力失调形成正反馈循环

### 8.2 方法层面
- **高保真度信息物理耦合仿真平台**：现有工具（如WNTR、PowerWorld）多为单系统仿真，缺乏信息-电力-供水三层联合仿真平台
- **数据驱动的级联失效预测**：利用图神经网络、时序深度学习等方法从历史数据中学习级联传播模式
- **不确定性下的韧性优化**：考虑信息层攻击不确定性、物理层故障随机性的鲁棒/分布式鲁棒优化

### 8.3 应用层面
- **城市尺度水电耦合系统韧性优化**：现有案例多为理论网络或小规模系统，缺乏真实城市级供水-电力网络的实证研究
- **韧性提升的工程化策略**：如何将理论优化结果转化为可操作的基础设施加固、备用配置、应急调度方案
- **数字孪生驱动的实时韧性管理**：利用数字孪生技术实现水电耦合系统级联失效的实时监测、预测与韧性调度

---

## 九、推荐必读文献（Top 10）

| 优先级 | 文献 | 理由 |
|--------|------|------|
| ⭐⭐⭐ | Buldyrev et al. (2010) Nature | 互依赖网络级联失效理论基石 |
| ⭐⭐⭐ | Ouyang M. (2014) RESS | 互依赖建模方法最全面综述 |
| ⭐⭐⭐ | Ibrahim et al. (2023) Frontiers | CPS级联失效与韧性最全面综述 |
| ⭐⭐⭐ | Cascading Failure in CPS: Review (2024) IEEE Access | CPS级联失效建模与脆弱性综述 |
| ⭐⭐ | Rinaldi et al. (2001) IEEE CSM | 互依赖性分类理论奠基 |
| ⭐⭐ | Motter & Lai (2002) PRE | 级联失效经典模型 |
| ⭐⭐ | Joint cascade vulnerability (2023) IEEE PES | 供水-电力联合级联脆弱性评估 |
| ⭐⭐ | 基于电-水跨层耦合模型 (2024) 电工技术学报 | 中文水电耦合脆弱性评估代表 |
| ⭐⭐ | 功能耦合水电网络韧性 (2024) | 中文水电网络抗震韧性代表 |
| ⭐ | Deep RL in power resilience (2025) IEEE TPWRS | 深度强化学习韧性优化前沿 |

---

## 参考文献

[1. Rinaldi et al. (2001) - Identifying, understanding, and analyzing critical infrastructure interdependencies](https://ieeexplore.ieee.org/document/969131)

[2. Haimes & Jiang (2001) - Leontief-based model of risk in complex interconnected infrastructures](https://ascelibrary.org/doi/abs/10.1061/(ASCE)1076-0342(2001)7:1(1))

[3. Motter & Lai (2002) - Cascade-based attacks on complex networks](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.66.065102)

[4. Buldyrev et al. (2010) - Catastrophic cascade of failures in interdependent networks](https://www.nature.com/articles/nature08932)

[5. Parshani et al. (2010) - Interdependent networks: Reducing the coupling strength leads to a change from a first to second order percolation transition](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.105.048701)

[6. Gao et al. (2012) - Networks formed from interdependent networks](https://www.nature.com/articles/nphys2180)

[7. Ouyang M. (2014) - Review on modeling and simulation of interdependent critical infrastructure systems](https://www.sciencedirect.com/science/article/abs/pii/S0951832013002056)

[8. Ouyang & Wang (2015) - Resilience assessment of interdependent infrastructure systems](https://www.sciencedirect.com/science/article/pii/S0951832015000691)

[9. Effects of cyber coupling on cascading failures in power systems (2017)](https://ieeexplore.ieee.org/abstract/document/7924309/)

[10. Cascading Failures in Interconnected Power-to-Water Networks (2019)](https://eprints.whiterose.ac.uk/id/eprint/165735/1/Cascading-Failures-in-Interconnected-Power-to-Water-Networks.pdf)

[11. Resilience of Interdependent Water and Power Systems (2021)](https://www.mdpi.com/2073-4441/13/20/2846)

[12. Resilience of Cyber-Enabled Electrical Energy and Water Distribution Systems (2020)](https://www.researchgate.net/publication/335895542)

[13. Ibrahim et al. (2023) - Cyber-physical cascading failure and resilience of power grid](https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2023.1095303/full)

[14. Cascading Failure in CPS: A Review on Failure Modeling and Vulnerability Analysis (2024)](https://ieeexplore.ieee.org/abstract/document/10585322/)

[15. A review of resilience metrics and modeling methods for CPPS (2023)](https://ieeexplore.ieee.org/abstract/document/10361280/)

[16. Joint cascade vulnerability assessment of interdependent power–water infrastructures (2023)](https://ieeexplore.ieee.org/abstract/document/10261437/)

[17. Cascading failure analysis of interdependent water-power networks based on functional coupling (2025)](https://www.sciencedirect.com/science/article/abs/pii/S095183202500153X)

[18. Quantifying the dependent failure of urban power-water supply systems under earthquake hazards (2026)](https://www.sciencedirect.com/science/article/pii/S0951832026011725)

[19. Cascading Failure Propagation and Perfect Storms in Interdependent Power-Water Systems (2025)](https://ascelibrary.asu.edu/doi/10.1061/AOMJAH.AOENG-0045)

[20. Robustness analysis of interdependent urban critical infrastructure networks against cascade failures (2018)](https://link.springer.com/article/10.1007/s13369-018-3656-6)

[21. Bayesian approach for the network reconstruction of interdependent critical infrastructure systems (2025)](https://link.aps.org/pdf/10.1103/vswp-h4hx)

[22. A stochastic model of cascading failure dynamics in cyber-physical power systems (2019)](https://ieeexplore.ieee.org/abstract/document/8970593/)

[23. Modeling and analysis of cascading failures in CPPS under different coupling strategies (2022)](https://ieeexplore.ieee.org/abstract/document/9915392/)

[24. Dynamic modeling and mitigation of cascading failures in power grids with interdependent cyber and physical layers (2023)](https://ieeexplore.ieee.org/abstract/document/10336916/)

[25. Cascading effects of cyber-attacks on interconnected critical infrastructure (2021)](https://link.springer.com/article/10.1186/s42400-021-00071-z)

[26. Formulating false data injection cyberattacks on pumps' flow rate (2021)](https://www.sciencedirect.com/science/article/pii/S2210670721006442)

[27. Deep reinforcement learning in power systems resilience: A review (2025)](https://ieeexplore.ieee.org/abstract/document/11181573/)

[28. Enhancing Interdependent Infrastructure Systems Resilience based on Reinforcement Learning (2025)](https://www.sciencedirect.com/science/article/pii/S2210670726004919)

[29. Computational decision framework for enhancing resilience of the EWF nexus (2019)](https://www.sciencedirect.com/science/article/pii/S1364032119304083)

[30. 基于电-水跨层耦合模型的城市电网脆弱性评估 (2024)](https://dgjsxb.ces-transaction.com/fileup/HTML/2024-16-5075.htm)

[31. 多层网络级联失效的预防和恢复策略概述 (2020)](https://wulixb.iphy.ac.cn/article/doi/10.7498/aps.69.20192000)

[32. 功能耦合的城市水电网络抗震韧性分析方法 (2024)](https://ir.bjut.edu.cn/irpui/item/321244)

[33. Urban Lifeline Resilience under Compound Hazards (2025)](https://www.sciopen.com/article/10.26599/LLES.2025.9660015)

[34. Cyber-Physical Resilience Engineering Framework (2025)](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7144278)

[35. Emergency Coordination of Water Pumps and Pump-as-Turbine Units (2025)](https://ieeexplore.ieee.org/abstract/document/11655565/)

