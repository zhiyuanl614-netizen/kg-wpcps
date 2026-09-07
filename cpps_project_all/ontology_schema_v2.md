# 供水-电力信息物理耦合系统本体 v2.0
## ——基于实际材料可提取性的自底向上重构

> 版本：2.0.0 | 日期：2026-08-31
> 核心原则：**本体从材料中来，而非从先验知识中预设**
> 方法论：分析学术论文、技术报告、标准、应急预案、典型事件五类材料的实际信息密度，仅保留**可从材料中稳定提取**的实体与关系

---

## 一、方法论：五类源材料的信息密度分析

### 1.1 各类材料实际可提取的信息粒度

| 材料类型 | 实际可提取粒度 | 典型信息 | 不可提取的信息（需删除或降级） |
|---------|--------------|---------|--------------------------|
| **学术论文** | 模型组件级（Bus/Node/Pump/Pipe） | 电网母线编号、水网节点ID、耦合映射关系、仿真参数 | 具体设备型号、IP地址、固件版本、精确地理坐标 |
| **技术报告** | 系统架构级 | 水电互依赖类型、韧性指标、耦合模式分类 | 具体SCADA通信协议细节、实时数据 |
| **标准规范** | 设计参数级 | 泵站备用电源要求、电压等级、供水压力标准 | 运行状态、实时监测数据 |
| **应急预案** | 响应流程级 | 停电→泵站停运→供水中断的因果链、应急措施 | 精确故障传播时间、设备级参数 |
| **典型事件** | 事件因果级 | 停电范围、受影响人口、恢复时间、级联因果链 | 内部SCADA日志、设备级故障序列 |

### 1.2 关键发现：学术论文的简化模式

学术论文中，**信息物理耦合系统**的建模普遍采用以下简化：

```
电力系统建模简化：
  实际 → 论文中
  变电站/电厂/断路器/变压器 → Bus（母线节点）
  输电线路/配电线路 → Branch/Line（支路/线路）
  发电机组 → Generator（发电机节点）
  负荷（含泵站负荷） → Load（负荷节点）
  
供水系统建模简化：
  实际 → 论文中
  净水厂/泵站/水箱/水库 → Node/Junction（节点）
  输配水管道 → Pipe/Link（管段）
  水泵 → Pump（水泵组件）
  阀门 → Valve（阀门组件）
  水库/水池 → Tank/Reservoir（蓄水设施）
  用水需求 → Demand（需水节点）

信息层建模简化：
  实际 → 论文中
  SCADA/PLC/RTU/PMU/传感器 → Cyber Node（信息节点）
  光纤/无线/以太网 → Communication Link（通信链路）
  控制指令/遥测数据 → Information Flow（信息流）
  
耦合关系简化：
  实际 → 论文中
  变电站→泵站供电 → Load Bus ↔ Pump 映射
  SCADA→设备控制 → Cyber Node ↔ Physical Node 映射
```

---

## 二、重构后的本体体系

### 2.1 核心实体（仅保留材料中可稳定提取的）

#### A. 电力系统实体（Power_System）

| 实体标签 | 英文 | 可提取来源 | 典型属性（材料中可获取） | 不可获取属性（已删除） |
|---------|------|-----------|----------------------|---------------------|
| **Bus** | Bus / 母线 | 学术论文（IEEE 39/118/300等标准测试系统） | bus_id, bus_type(slack/PV/PQ), voltage_level, area, zone | ip_address, firmware_version |
| **Generator** | Generator / 发电机 | 学术论文 | gen_id, bus_id, Pmax, Pmin, Qmax, Qmin, gen_type | 具体型号, 厂家 |
| **Load** | Load / 负荷 | 学术论文、应急预案 | load_id, bus_id, P_demand, Q_demand, load_type(normal/critical) | 实时负荷曲线 |
| **Branch** | Branch / 线路 | 学术论文 | branch_id, from_bus, to_bus, rating, reactance, status | 线路型号, 杆塔类型 |
| **Substation** | Substation / 变电站 | 报告、预案、新闻 | name, voltage_level, region, backup_power(yes/no) | 内部接线图 |

#### B. 供水系统实体（Water_System）

| 实体标签 | 英文 | 可提取来源 | 典型属性（材料中可获取） | 不可获取属性（已删除） |
|---------|------|-----------|----------------------|---------------------|
| **Junction** | Junction / 节点 | 学术论文（EPANET Net3等标准测试系统） | node_id, elevation, base_demand, demand_pattern | 实时压力值 |
| **Pipe** | Pipe / 管段 | 学术论文 | pipe_id, from_node, to_node, length, diameter, roughness | 管材具体型号 |
| **Pump** | Pump / 水泵 | 学术论文、报告、预案 | pump_id, from_node, to_node, power_kw, head_curve, powered_by_bus | PLC型号, 控制逻辑 |
| **Tank** | Tank / 水箱 | 学术论文 | tank_id, elevation, init_level, min_level, max_level, volume | 液位传感器型号 |
| **Reservoir** | Reservoir / 水库 | 学术论文 | res_id, head, node_id | — |
| **Valve** | Valve / 阀门 | 学术论文、预案 | valve_id, from_node, to_node, valve_type(PRV/TCV/FCV), powered(yes/no) | 执行器型号 |
| **WaterFacility** | WaterFacility / 水务设施 | 报告、预案、新闻 | name, facility_type(水厂/泵站), capacity, region, backup_power_type | SCADA架构细节 |

#### C. 信息层实体（Cyber_Layer）

| 实体标签 | 英文 | 可提取来源 | 典型属性 | 说明 |
|---------|------|-----------|---------|------|
| **CyberNode** | CyberNode / 信息节点 | 学术论文（CPS建模） | node_id, node_type(SCADA/PLC/RTU/PMU/Sensor), protocol, coupled_physical_node | 论文中通常只区分类型和耦合关系 |
| **CommLink** | CommLink / 通信链路 | 学术论文 | link_id, from_node, to_node, link_type(wired/wireless), bandwidth, latency | 论文中常简化为拓扑连接 |
| **InfoFlow** | InfoFlow / 信息流 | 学术论文 | flow_type(measurement/command/alarm), direction(upstream/downstream) | 论文中常简化为方向性 |

#### D. 扰动与事件实体（Hazard_and_Event）

| 实体标签 | 英文 | 可提取来源 | 典型属性 |
|---------|------|-----------|---------|
| **Hazard** | Hazard / 扰动 | 学术论文、报告、新闻 | hazard_id, hazard_type(natural/cyber/equipment), intensity, probability |
| **CascadeEvent** | CascadeEvent / 级联事件 | 学术论文、新闻、预案 | event_id, trigger, cascade_chain[], total_impact, recovery_time |
| **CascadeStep** | CascadeStep / 级联步骤 | 学术论文 | step_id, order, failed_component, failure_cause, propagation_mechanism, affected_downstream |

#### E. 方法与指标实体（Method_and_Metric）

| 实体标签 | 英文 | 可提取来源 | 典型属性 |
|---------|------|-----------|---------|
| **SimulationModel** | SimulationModel / 仿真模型 | 学术论文 | model_id, model_type(DC-PF/AC-PF/DistFlow/EPANET/ABM), tool(PowerWorld/MATPOWER/WNTR) |
| **ResilienceMetric** | ResilienceMetric / 韧性指标 | 学术论文、报告 | metric_id, metric_name, formula, dimension(robustness/rapidity/redundancy/resourcefulness) |
| **OptMethod** | OptMethod / 优化方法 | 学术论文 | method_id, method_type(RO/SRO/DRL/MILP), objective, constraint |

#### F. 文献溯源实体（Provenance）

| 实体标签 | 英文 | 可提取来源 | 典型属性 |
|---------|------|-----------|---------|
| **Reference** | Reference / 文献来源 | 所有材料 | ref_id, title, authors, year, source, doi, keywords, abstract |
| **Organization** | Organization / 机构 | 报告、新闻 | org_id, name, org_type(university/national_lab/utility/government) |

---

### 2.2 核心关系（仅保留材料中可稳定提取的）

#### A. 电力系统内部关系

| 关系 | 方向 | 可提取来源 | 典型场景 |
|------|------|-----------|---------|
| `CONNECTS_BUS` | Bus → Bus (via Branch) | 学术论文 | "Branch 1 connects Bus 2 to Bus 3" |
| `GENERATES_AT` | Generator → Bus | 学术论文 | "Generator 1 at Bus 30" |
| `CONSUMES_AT` | Load → Bus | 学术论文 | "Load at Bus 16 draws 120 MW" |
| `OVERLOADS` | Branch → Branch | 学术论文 | "Line 2-3 overloads after Line 1-2 trips" |
| `TRIPS` | Branch → Branch (protection) | 学术论文 | "Overloaded line trips, load redistributes" |

#### B. 供水系统内部关系

| 关系 | 方向 | 可提取来源 | 典型场景 |
|------|------|-----------|---------|
| `CONNECTS_NODE` | Junction → Junction (via Pipe) | 学术论文 | "Pipe P1 connects Node J1 to Node J2" |
| `PUMPS_THROUGH` | Pump → Pipe | 学术论文 | "Pump PU1 on Pipe P5" |
| `REGULATES` | Valve → Pipe | 学术论文 | "Valve V1 on Pipe P8 (PRV)" |
| `SUPPLIES_DEMAND` | Tank/Reservoir → Junction | 学术论文 | "Tank T1 supplies demand at J5" |

#### C. 跨系统耦合关系（核心！）

| 关系 | 方向 | 可提取来源 | 典型场景 |
|------|------|-----------|---------|
| `POWERED_BY` | Pump/Valve → Bus | 学术论文、报告 | "Pump PU1 powered by Bus 23" |
| `SUPPLIES_POWER_TO` | Bus → Pump/Valve | 学术论文 | "Bus 23 supplies power to Pump PU1" |
| `DEPENDS_ON_POWER` | WaterFacility → Substation | 预案、报告 | "城东泵站依赖城东110kV变电站供电" |
| `AFFECTS_WATER_SUPPLY` | Bus_failure → Junction_pressure_drop | 学术论文 | "Bus 23 outage → Pump PU1 stops → Junction J5 pressure drops" |

#### D. 信息层耦合关系

| 关系 | 方向 | 可提取来源 | 典型场景 |
|------|------|-----------|---------|
| `MONITORS_PHYSICAL` | CyberNode → Bus/Junction | 学术论文 | "PMU at Bus 16 monitors voltage" |
| `CONTROLS_PHYSICAL` | CyberNode → Generator/Pump/Valve | 学术论文 | "PLC controls Pump PU1 speed" |
| `COMMUNICATES_WITH` | CyberNode → CyberNode (via CommLink) | 学术论文 | "RTU sends measurement to SCADA server" |
| `COUPLED_WITH` | CyberNode ↔ PhysicalNode | 学术论文 | "Cyber node i coupled with physical node j (one-to-one/random)" |

#### E. 级联传播关系

| 关系 | 方向 | 可提取来源 | 典型场景 |
|------|------|-----------|---------|
| `TRIGGERS_FAILURE` | Hazard → Component | 学术论文、新闻、预案 | "Earthquake triggers Bus 5 failure" |
| `CASCADES_TO` | Component → Component | 学术论文、新闻 | "Bus 5 outage → Load shedding → Pump PU1 stops" |
| `CAUSES_DEGRADATION` | Component_failure → System_metric_drop | 学术论文 | "3 buses lost → system resilience drops 40%" |
| `PROPAGATES_VIA` | CascadeStep → CascadeStep | 学术论文 | "Step 1 (line trip) propagates via overload to Step 2" |

#### F. 文献溯源关系

| 关系 | 方向 | 可提取来源 | 典型场景 |
|------|------|-----------|---------|
| `DESCRIBED_IN` | Entity → Reference | 所有材料 | "IEEE 39-bus model described in [12]" |
| `PROPOSED_BY` | Method → Reference | 学术论文 | "DistFlow model proposed in Baran & Wu (1989)" |
| `APPLIES_MODEL` | Reference → SimulationModel | 学术论文 | "This paper uses DC power flow + EPANET" |
| `MEASURED_BY` | System → ResilienceMetric | 学术论文 | "Resilience measured by R = ∫Q(t)dt" |

---

## 三、各类材料的抽取提示词模板

### 3.1 学术论文抽取提示词

```json
{
  "task": "从学术论文中提取供水-电力信息物理耦合系统的实体与关系",
  "source_type": "academic_paper",
  "extraction_prompt": "请从以下学术论文中提取：\n\n1. **仿真模型信息**：\n   - 电力系统模型类型（DC-PF / AC-PF / DistFlow / Transient Stability）\n   - 供水系统模型类型（EPANET / WNTR / 自定义水力模型）\n   - 测试系统名称（IEEE 39-bus / IEEE 118-bus / Net3 / 自定义）\n   - 仿真工具（MATPOWER / PowerWorld / PANDEMONIUM / WNTR / 自定义）\n\n2. **电力系统组件**：\n   - Bus（母线）：编号、类型（slack/PV/PQ）、电压等级\n   - Generator（发电机）：编号、所在母线、容量\n   - Load（负荷）：编号、所在母线、负荷大小\n   - Branch/Line（线路）：编号、起止母线、容量限制\n\n3. **供水系统组件**：\n   - Junction（节点）：编号、高程、需水量\n   - Pipe（管段）：编号、起止节点、管径、管长\n   - Pump（水泵）：编号、起止节点、功率、供电母线\n   - Tank（水箱）：编号、容量、水位范围\n   - Valve（阀门）：编号、类型、是否电动\n   - Reservoir（水库）：编号、水头\n\n4. **跨系统耦合关系**：\n   - 哪些水泵/阀门连接到哪些电力母线（Pump-Bus映射）\n   - 耦合方式（一对一/一对多/随机耦合）\n   - 电力失效对供水的影响机制\n\n5. **信息层组件**（如有）：\n   - 信息节点类型（SCADA/PLC/RTU/PMU/Sensor）\n   - 信息节点与物理节点的耦合关系\n   - 通信链路拓扑\n   - 网络攻击类型（FDI/DoS/命令注入）\n\n6. **级联失效过程**：\n   - 初始扰动/故障\n   - 级联传播步骤序列\n   - 每步的失效组件、失效原因、传播机制\n   - 最终影响（停电范围/供水不足范围）\n\n7. **韧性指标与方法**：\n   - 韧性指标定义与公式\n   - 优化方法类型\n   - 优化目标与约束",
  "output_format": "JSON Schema constrained"
}
```

### 3.2 技术报告抽取提示词

```json
{
  "task": "从技术报告中提取水电互依赖系统信息",
  "source_type": "technical_report",
  "extraction_prompt": "请从以下技术报告中提取：\n\n1. **互依赖类型**：\n   - 物理依赖（供电→泵站）\n   - 信息依赖（SCADA→调度）\n   - 地理依赖（共址设施）\n   - 逻辑依赖（政策/市场）\n\n2. **耦合模式**：\n   - 一对一耦合（一个变电站→一个泵站）\n   - 一对多耦合（一个变电站→多个泵站）\n   - 双馈/备用电源配置\n\n3. **韧性评估框架**：\n   - 评估维度（鲁棒性/快速性/冗余性/资源性）\n   - 关键指标\n   - 评估方法\n\n4. **案例与数据**：\n   - 研究区域/系统\n   - 关键发现\n   - 数据来源\n\n5. **建议与措施**：\n   - 韧性提升策略\n   - 协调机制建议",
  "output_format": "JSON Schema constrained"
}
```

### 3.3 应急预案抽取提示词

```json
{
  "task": "从应急预案中提取停电-供水级联影响信息",
  "source_type": "emergency_plan",
  "extraction_prompt": "请从以下应急预案中提取：\n\n1. **事件分级**：\n   - 停电事件等级（特别重大/重大/较大/一般）\n   - 对应的减供负荷比例\n\n2. **停电对供水的影响链**：\n   - 停电 → 水厂停产 / 泵站停运 → 水压下降 / 供水中断\n   - 具体受影响的供水设施名称\n   - 预计影响范围与人口\n\n3. **应急响应措施**：\n   - 应急供水措施（启用备用电源/应急送水/降压供水）\n   - 电力恢复优先级（哪些供水设施优先恢复供电）\n   - 部门协调机制\n\n4. **备用电源配置**：\n   - 水厂/泵站备用电源类型（柴油发电机/UPS/双回路）\n   - 备用电源持续时间\n\n5. **关键设施清单**：\n   - 重要电力用户（含供水设施）\n   - 供电恢复顺序",
  "output_format": "JSON Schema constrained"
}
```

### 3.4 典型事件抽取提示词

```json
{
  "task": "从典型事件报道中提取级联失效因果链",
  "source_type": "case_event",
  "extraction_prompt": "请从以下事件报道中提取：\n\n1. **事件基本信息**：\n   - 事件名称、时间、地点\n   - 直接原因（自然灾害/设备故障/网络攻击/人为失误）\n\n2. **级联因果链**：\n   - 按时间顺序列出因果步骤\n   - 每步：触发原因 → 失效组件 → 影响范围\n   - 特别关注：电力→供水的跨系统传播\n\n3. **影响量化**：\n   - 停电规模（负荷损失/受影响人口）\n   - 供水影响（水压下降/供水中断/水质风险）\n   - 持续时间\n\n4. **恢复过程**：\n   - 恢复顺序\n   - 恢复时间\n   - 经验教训",
  "output_format": "JSON Schema constrained"
}
```

### 3.5 标准规范抽取提示词

```json
{
  "task": "从标准规范中提取供水/电力系统设计参数与安全要求",
  "source_type": "standard",
  "extraction_prompt": "请从以下标准中提取：\n\n1. **设计参数**：\n   - 供水压力标准值\n   - 供电可靠性要求\n   - 备用电源配置要求\n\n2. **安全稳定要求**：\n   - 电力系统安全稳定三级标准\n   - N-1/N-2校验要求\n\n3. **应急供水要求**：\n   - 应急供水标准\n   - 供水保障优先级\n\n4. **检测与控制要求**：\n   - SCADA系统配置要求\n   - 监测参数要求",
  "output_format": "JSON Schema constrained"
}
```

---

## 四、v1.0 → v2.0 的关键变化

### 4.1 删除的实体（先验知识中有，但材料中提取不到）

| 删除实体 | 原因 | 替代方案 |
|---------|------|---------|
| `PowerPlant`（作为独立实体） | 学术论文中通常简化为Generator节点 | 用 `Generator` + `bus_type=slack` 表示 |
| `Transformer` | 论文中通常合并到Branch参数中 | 用 `Branch` + `transformer_ratio` 属性 |
| `Breaker` | 论文中通常隐含在线路保护逻辑中 | 用 `Branch.status` + 保护规则表示 |
| `CapacitorBank` / `Reactor` | 仅在特定无功优化论文中出现 | 降级为 `Bus` 的可选属性 |
| `Hydrant` / `Well` | 论文中极少单独建模 | 合并到 `Junction` |
| `IED` / `Firewall` / `Gateway` / `Historian` | 论文中统一为CyberNode | 用 `CyberNode.node_type` 区分 |
| `SatelliteLink` / `SerialLink` | 论文中统一为CommLink | 用 `CommLink.link_type` 区分 |

### 4.2 新增的实体（材料中实际存在但v1.0遗漏）

| 新增实体 | 来源 | 说明 |
|---------|------|------|
| `SimulationModel` | 学术论文 | 每篇论文都明确说明使用的模型类型 |
| `ResilienceMetric` | 学术论文/报告 | 韧性指标是论文核心产出 |
| `OptMethod` | 学术论文 | 优化方法是论文核心贡献 |
| `CascadeStep` | 学术论文/事件 | 级联步骤是级联失效分析的基本单元 |
| `Organization` | 报告/新闻 | 机构信息对溯源和态势分析重要 |

### 4.3 简化的关系

| v1.0关系 | v2.0关系 | 简化原因 |
|---------|---------|---------|
| `CONTROLS`（含control_type/delay/reliability） | `CONTROLS_PHYSICAL`（仅type） | 论文中通常只说明控制类型，不提供延迟/可靠性参数 |
| `MONITORS`（含sampling_interval/accuracy） | `MONITORS_PHYSICAL`（仅type） | 论文中通常只说明监测类型 |
| `POWER_SUPPLIES` + `DEPENDS_ON_POWER` | `POWERED_BY`（Pump→Bus） | 论文中核心耦合就是Pump-Bus映射，双向关系冗余 |
| `TRANSMITS_VIA` | `COMMUNICATES_WITH` | 论文中通信链路通常只描述拓扑 |

---

## 五、v2.0本体与材料对应关系验证

### 5.1 学术论文验证

| 论文 | 可提取实体 | 可提取关系 | 验证结果 |
|------|-----------|-----------|---------|
| Cascading Failures in Interconnected Power-to-Water Networks (2019) | Bus, Load, Pump, Valve, Tank, Pipe, Junction | POWERED_BY(Pump→Bus), CASCADES_TO | ✅ 完全覆盖 |
| Cyber-physical cascading failure and resilience of power grid (2023) | Bus, Generator, Branch, CyberNode, CommLink | COUPLED_WITH, MONITORS_PHYSICAL, CONTROLS_PHYSICAL | ✅ 完全覆盖 |
| Cascading failure analysis of interdependent water-power networks (2025) | Bus, Pump, Tank, Pipe, Junction | POWERED_BY, CASCADES_TO, PROPAGATES_VIA | ✅ 完全覆盖 |
| 基于电-水跨层耦合模型的城市电网脆弱性评估 (2024) | Bus, Load, Pump, WaterFacility | POWERED_BY, AFFECTS_WATER_SUPPLY | ✅ 完全覆盖 |

### 5.2 应急预案验证

| 预案 | 可提取实体 | 可提取关系 | 验证结果 |
|------|-----------|-----------|---------|
| 国家大面积停电事件应急预案 | Substation, WaterFacility, Hazard | DEPENDS_ON_POWER, TRIGGERS_FAILURE | ✅ 完全覆盖 |
| 深圳罗湖供排水应急预案 | WaterFacility, Substation | DEPENDS_ON_POWER, CASCADES_TO | ✅ 完全覆盖 |

### 5.3 典型事件验证

| 事件 | 可提取实体 | 可提取关系 | 验证结果 |
|------|-----------|-----------|---------|
| 2021德州极寒 | Substation, WaterFacility, Hazard, CascadeEvent | TRIGGERS_FAILURE, CASCADES_TO | ✅ 完全覆盖 |
| 2021郑州暴雨 | Substation, WaterFacility, Hazard, CascadeEvent | TRIGGERS_FAILURE, CASCADES_TO | ✅ 完全覆盖 |

---

## 六、v2.0 JSON Schema（精简版）

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Water-Power CPPS Ontology v2.0",
  "version": "2.0.0",
  "principle": "bottom-up from actual materials",

  "entity_types": {
    "Power_System": ["Bus", "Generator", "Load", "Branch", "Substation"],
    "Water_System": ["Junction", "Pipe", "Pump", "Tank", "Reservoir", "Valve", "WaterFacility"],
    "Cyber_Layer": ["CyberNode", "CommLink"],
    "Hazard_Event": ["Hazard", "CascadeEvent", "CascadeStep"],
    "Method_Metric": ["SimulationModel", "ResilienceMetric", "OptMethod"],
    "Provenance": ["Reference", "Organization"]
  },

  "relationship_types": {
    "power_internal": ["CONNECTS_BUS", "GENERATES_AT", "CONSUMES_AT", "OVERLOADS", "TRIPS"],
    "water_internal": ["CONNECTS_NODE", "PUMPS_THROUGH", "REGULATES", "SUPPLIES_DEMAND"],
    "cross_system": ["POWERED_BY", "AFFECTS_WATER_SUPPLY"],
    "cyber_coupling": ["MONITORS_PHYSICAL", "CONTROLS_PHYSICAL", "COMMUNICATES_WITH", "COUPLED_WITH"],
    "cascade": ["TRIGGERS_FAILURE", "CASCADES_TO", "CAUSES_DEGRADATION", "PROPAGATES_VIA"],
    "provenance": ["DESCRIBED_IN", "PROPOSED_BY", "APPLIES_MODEL", "MEASURED_BY"]
  }
}
```
