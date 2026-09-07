# Water-Power CPS Ontology v2.0 — 完整定义
> 生成日期: 2026-09-06 | 版本: 2.0
> 设计原则: Bottom-up from material evidence, not top-down from prior knowledge

## 1. 统计概览
| 维度 | 总数 | required | keep | keep_single_high | optional |
|------|------|----------|------|------------------|----------|
| 实体 | 18 | 5 | 9 | — | 4 |
| 关系 | 12 | 2 | 4 | 2 | 4 |
| 属性 | 39 | 3 | 5+8 | 11 | 12 |

## 2. 分层架构
- **power**: Bus, Branch, Generator
- **water**: Pump, Node_Junction, Pipe_Link, Tank, Valve
- **cyber**: SCADA, CyberNode, CyberEdge
- **hazard**: HazardType
- **resilience**: BackupPower
- **system**: WaterSystem, NaturalGasFacility, ResponseLevel

- 跨层关系: POWERED_BY, CASCADES_TO, TRIGGERS, DEPENDS_ON, AMPLIFIES
- 信息物理关系: CONTROLS, MONITORS

## 3. 实体定义
### 🔴 Bus (母线/变电站)
- **层级**: power | **决策**: required | **跨材料数**: 5
- **粒度**: L4-node (M1) / L2-station (M2-M5)
- **描述**: 电力系统节点。论文中为Bus节点，报告/标准/预案/事件中为Substation站级。通过CONTAINS映射双向关联。
- **站级别名**: Substation
- **属性**: voltage_level_kV, bus_load, bus_voltage

### 🟡 Branch (线路/支路)
- **层级**: power | **决策**: keep | **跨材料数**: 2
- **粒度**: L4-node (M1) / L2-station (M3)
- **描述**: 电力系统连接支路。论文中为Branch，标准中为TransmissionLine。统一为Branch。
- **站级别名**: TransmissionLine
- **属性**: branch_capacity, branch_impedance

### 🔴 Generator (发电机/电厂)
- **层级**: power | **决策**: required | **跨材料数**: 4
- **粒度**: L4-node (M1) / L2-station (M2/M3/M5)
- **描述**: 发电机组。论文中为Generator节点，报告/事件中为PowerPlant站级。
- **站级别名**: PowerPlant
- **属性**: generator_output, power_plant_type

### 🔴 Pump (水泵/泵站)
- **层级**: water | **决策**: required | **跨材料数**: 5
- **粒度**: L4-node (M1) / L2-station (M2-M5)
- **描述**: 水泵设备。论文中为Pump节点，报告/标准/预案/事件中为PumpStation站级。水电耦合核心锚点之一。
- **站级别名**: PumpStation
- **属性**: pump_power, pump_head, pump_flow

### 🟡 Node_Junction (水力节点/水厂)
- **层级**: water | **决策**: keep | **跨材料数**: 3
- **粒度**: L4-node (M1) / L2-station (M2/M3)
- **描述**: 给水管网节点。论文中为Node/Junction，报告中为WaterTreatmentPlant站级。
- **站级别名**: WaterTreatmentPlant
- **属性**: node_demand, node_pressure

### 🟡 Pipe_Link (管道/管段)
- **层级**: water | **决策**: keep | **跨材料数**: 2
- **粒度**: L4-node (M1) / L2-station (M3)
- **描述**: 给水管网连接管段。论文中为Pipe/Link，标准中为Pipeline。
- **站级别名**: Pipeline
- **属性**: pipe_diameter, pipe_length, pipe_roughness, pipe_material, leak_rate_limit

### 🟡 Tank (水池/水库)
- **层级**: water | **决策**: keep | **跨材料数**: 2
- **粒度**: L4-node (M1) / L2-station (M3)
- **描述**: 蓄水设施。论文中为Tank节点，标准中为Tank/Reservoir站级。
- **站级别名**: Tank
- **属性**: tank_capacity, tank_level

### 🟡 Valve (阀门)
- **层级**: water | **决策**: keep | **跨材料数**: 2
- **粒度**: L4-node (M1) / L3-device (M3)
- **描述**: 管网控制阀门。论文中为Valve节点（通常简化为Pipe状态），标准中有独立设备级描述。
- **站级别名**: Valve

### 🔴 SCADA (SCADA系统)
- **层级**: cyber | **决策**: required | **跨材料数**: 4
- **粒度**: L1-mention (M1/M2/M5) / L1-requirement (M3)
- **描述**: 数据采集与监控系统。所有材料类型均提及，但精度从定性提及到标准要求不等。
- **属性**: SCADA_requirement

### 🟡 CyberNode (信息节点)
- **层级**: cyber | **决策**: keep | **跨材料数**: 3
- **粒度**: L4-node (M1) / L3-device (M2/M3)
- **描述**: 信息层设备统一节点。论文中包含PLC/RTU/PMU/Sensor/Actuator等子类型，v2.0统一为CyberNode+type属性。
- **站级别名**: CyberDevice
- **子类型**: scada, plc, rtu, pmu, sensor, actuator

### ⚪ CyberEdge (通信链路)
- **层级**: cyber | **决策**: optional | **跨材料数**: 1
- **粒度**: L4-node (M1 only)
- **描述**: 信息层通信连接。仅论文中出现(FiberLink/WirelessLink)，v2.0降级为可选。
- **子类型**: fiber, wireless

### 🔴 HazardType (扰动类型)
- **层级**: hazard | **决策**: required | **跨材料数**: 4
- **粒度**: L1-system (M2-M5)
- **描述**: 外部扰动分类。报告/标准/预案/事件均有分类体系，论文中用概率模型表达。
- **属性**: hazard_category
- **常见取值**: earthquake, flood, typhoon, cyber_attack, equipment_failure, ice_disaster

### 🟡 BackupPower (备用电源)
- **层级**: resilience | **决策**: keep | **跨材料数**: 2
- **粒度**: L3-device (M3/M4)
- **描述**: 备用供电设施。标准要求配备，预案详细描述类型和持续时间。
- **属性**: backup_power_type, backup_duration_h
- **常见取值**: diesel_generator, UPS, dual_power_supply

### 🟡 WaterSystem (供水系统)
- **层级**: system | **决策**: keep | **跨材料数**: 2
- **粒度**: L1-system (M4/M5)
- **描述**: 供水系统整体。预案和事件中的系统级描述实体。

### 🟡 NaturalGasFacility (天然气设施)
- **层级**: system | **决策**: keep | **跨材料数**: 2
- **粒度**: L2-station (M2/M5)
- **描述**: 天然气系统设施。报告和事件中提及气-电耦合，作为扩展互联基础设施。

### ⚪ Reservoir (水库)
- **层级**: water | **决策**: optional | **跨材料数**: 1
- **粒度**: L4-node (M1 only)
- **描述**: 水源水库。仅论文中出现，可合并到Node_Junction(type=reservoir)。

### ⚪ DMA_District (DMA分区)
- **层级**: water | **决策**: optional | **跨材料数**: 1
- **粒度**: L2-station (M3 only)
- **描述**: 独立计量区域。仅标准中出现，管网管理分区概念。

### ⚪ ResponseLevel (响应等级)
- **层级**: system | **决策**: optional | **跨材料数**: 1
- **粒度**: L1-system (M4 only)
- **描述**: 应急响应等级。仅预案中出现(I/II/III/IV级)。
- **属性**: response_level

## 4. 关系定义
| 关系 | 中文 | 决策 | Domain → Range | 层级 | 跨材料数 |
|------|------|------|----------------|------|----------|
| POWERED_BY ⚓ | 供电 | keep | Pump → Bus | cross-layer | 3 |
| CASCADES_TO ⚓ | 级联传播 | required | Bus|Pump|Generator → Pump|Node_Junction|Bus | cross-layer | 4 |
| TRIGGERS | 触发 | keep | HazardType → Bus|Pump|Generator|Pipe_Link | hazard→physical | 3 |
| CONTROLS | 控制 | required | SCADA|CyberNode → Bus|Pump|Generator | cyber→physical | 4 |
| MONITORS | 监测 | keep | SCADA|CyberNode → Bus|Pump|Node_Junction | cyber→physical | 2 |
| CONNECTS_TO | 拓扑连接 | keep_single_high | Bus|Node_Junction|CyberNode → Bus|Node_Junction|CyberNode | intra-layer | 1 |
| HAS_BACKUP | 配备备用电源 | keep | Pump|Bus → BackupPower | resilience | 2 |
| REQUIRES_SCADA | 要求SCADA监控 | keep_single_high | Pump|Bus → SCADA | standard-requirement | 1 |
| DEPENDS_ON | 系统级依赖 | optional | WaterSystem|Pump → Generator|Bus | cross-layer | 1 |
| AMPLIFIES | 正反馈放大 | optional | Bus|Pump → Bus|Pump | cross-layer | 1 |
| MUST_SATISFY | 必须满足准则 | optional | System → Criterion | standard-mandatory | 1 |
| MUST_PREVENT | 必须防止级联 | optional | System → CascadeFailure | standard-mandatory | 1 |

## 5. 核心级联路径
- **标准路径**: `HazardType -[:TRIGGERS]-> Bus -[:CASCADES_TO]-> Pump -[:CASCADES_TO]-> Node_Junction`
- **电→水**: Bus fault → Pump POWERED_BY loss → Node_Junction pressure drop
- **含信息层**: HazardType -[:TRIGGERS]-> SCADA -[:CONTROLS]-> Bus -[:CASCADES_TO]-> Pump -[:CASCADES_TO]-> Node_Junction
- **韧性干预**: Pump -[:HAS_BACKUP]-> BackupPower (prevents POWERED_BY loss)
- **正反馈环**: Bus -[:AMPLIFIES]-> Pump -[:AMPLIFIES]-> Bus (positive feedback)
- **Neo4j查询**: `MATCH path=(h:HazardType)-[:TRIGGERS]->(b:Bus)-[:CASCADES_TO*1..3]->(n:Node_Junction) RETURN path`

## 6. 简化映射规则
### 电力层映射
| 行业术语 | → 本体实体 |
|----------|-----------|
| Substation | Bus |
| PowerPlant | Generator (on Bus) |
| TransmissionLine | Branch |
| DistributionLine | Branch |
| Transformer | Branch (impedance attribute) |
| Breaker | Branch (on/off state attribute) |
| CapacitorBank | Bus (reactive_injection attribute) |

### 水力层映射
| 行业术语 | → 本体实体 |
|----------|-----------|
| PumpStation | Pump + POWERED_BY→Bus |
| WaterTreatmentPlant | Node_Junction (type=source) |
| IntakePumpStation | Pump (type=intake) + POWERED_BY→Bus |
| BoosterPumpStation | Pump (type=booster) + POWERED_BY→Bus |
| DrainagePumpStation | Pump (type=drainage) + POWERED_BY→Bus |
| Pipeline | Pipe_Link |
| Valve | Pipe_Link (valve_state attribute) or Valve entity |
| Tank_Reservoir | Tank |
| Hydrant | Node_Junction (type=demand) |
| Well | Node_Junction (type=well) |
| Reservoir | Node_Junction (type=reservoir) or Tank |

### 信息层映射
| 行业术语 | → 本体实体 |
|----------|-----------|
| SCADA_Server | CyberNode (type=scada) or SCADA |
| PLC | CyberNode (type=plc) |
| RTU | CyberNode (type=rtu) |
| PMU | CyberNode (type=pmu) |
| Sensor | CyberNode (type=sensor) |
| Actuator | CyberNode (type=actuator) |
| FiberLink | CyberEdge (type=fiber) or CONNECTS_TO(layer_type=cyber_comm) |
| WirelessLink | CyberEdge (type=wireless) or CONNECTS_TO(layer_type=cyber_comm) |

### 站级↔节点级双向映射
- **规则**: Substation CONTAINS Bus; PumpStation CONTAINS Pump; PowerPlant CONTAINS Generator
- **描述**: 站级实体与节点级实体通过CONTAINS关系双向映射，支持跨粒度查询
- **Neo4j示例**: `MATCH (ps:PumpStation)-[:CONTAINS]->(p:Pump)-[:POWERED_BY]->(b:Bus)<-[:CONTAINS]-(ss:Substation)`

## 7. 材料专用抽取策略
### M1_academic_paper
- **实体粒度**: L4-node
- **关系精度**: R3-formula / R4-probabilistic
- **属性精度**: A4-simulation (pu values, model parameters)
- **级联表达**: model (DC flow + EPANET coupled simulation)
- **关键抽取项**:
  - POWERED_BY mapping table (Pump→Bus)
  - Network topology (adjacency matrix)
  - Simulation model type and parameters
  - Cascade simulation results (load_shedding, pressure_satisfaction)
  - Resilience index formula and values
- **提示词重点**: Extract node-level entities with IDs (Bus-1, Pump-3), topology connections, and POWERED_BY mapping. Capture simulation parameters in pu units.

### M2_report
- **实体粒度**: L2-station
- **关系精度**: R1-qualitative
- **属性精度**: A1-A2 (qualitative, statistics)
- **级联表达**: narrative (causal chain without formula)
- **关键抽取项**:
  - System-level dependency descriptions (water depends on power)
  - Hazard category and historical statistics
  - Research gaps and policy recommendations
  - Backup power type mentions
- **提示词重点**: Extract station-level entities with names (XX变电站, XX泵站). Capture qualitative dependency descriptions. Map to canonical entity names.

### M3_standard
- **实体粒度**: L2-station + L3-device
- **关系精度**: R1-qualitative-requirement / R1-qualitative-mandatory
- **属性精度**: A3-rated (design parameters, safety thresholds)
- **级联表达**: requirement (must prevent cascading failure)
- **关键抽取项**:
  - Mandatory requirements (N-1, backup power, SCADA monitoring)
  - Safety thresholds (Kp>=1.05, leak_rate<=12%)
  - Design parameters (pump rated power/head/flow, pipe diameter)
  - Facility classification (station grade)
- **提示词重点**: Extract mandatory requirements with SHALL/MUST keywords. Capture rated parameters and safety thresholds. Distinguish requirement from recommendation.

### M4_emergency_plan
- **实体粒度**: L2-station
- **关系精度**: R2-named (concrete facility names)
- **属性精度**: A2-semi-quantitative
- **级联表达**: narrative (planned response chain)
- **关键抽取项**:
  - NAMED facility interdependency (XX泵站由XX变电站供电)
  - Backup power details (type, duration, capacity)
  - Response level classification (I/II/III/IV)
  - Cascade chain narrative (qualitative causal chain)
- **提示词重点**: Extract NAMED facility mappings with specific station names. Capture backup power details. Map station names to canonical entities.

### M5_event
- **实体粒度**: L2-station
- **关系精度**: R0-implicit / R1-narrative
- **属性精度**: A1-qualitative (impact statistics)
- **级联表达**: narrative (complete event timeline with impact)
- **关键抽取项**:
  - COMPLETE cascade chain with timeline
  - Impact statistics (population, MW lost, recovery time)
  - AMPLIFIES positive feedback loops
  - Cyber attack kill chain details (if applicable)
- **提示词重点**: Extract complete cascade chain with timeline and impact data. Capture AMPLIFIES feedback loops. Reconstruct implicit dependencies from event narrative.

## 8. v1.0 → v2.0 变更摘要
### 删除
- ~~coordinates (C6: no material can extract)~~
- ~~ip_address (C6: no material can extract)~~
- ~~firmware_version (C6: no material can extract)~~
- ~~PLC/RTU/PMU/Sensor/Actuator (C3: merged into CyberNode with type attribute)~~
- ~~FiberLink/WirelessLink (C3: merged into CyberEdge or CONNECTS_TO)~~
### 新增
- ✅ BackupPower (M3/M4 unique, resilience key)
- ✅ SCADA (promoted from mention to entity, 4 materials)
- ✅ WaterSystem (M4/M5 system-level entity)
- ✅ NaturalGasFacility (M2/M5 extended infrastructure)
- ✅ ResponseLevel (M4 emergency response)
### 提升
- ⬆️ CONTROLS: keep→required (4 materials after M3 SCADA requirement added)
- ⬆️ CASCADES_TO: keep→required (4 materials confirmed)
### 核心原则变更
- v1.0 was top-down (prior knowledge), v2.0 is bottom-up (material evidence). Only entities/relations/attributes that can be extracted from >=1 material type are retained.

## 9. Neo4j 唯一性约束
```cypher
CREATE CONSTRAINT IF NOT EXISTS FOR (b:Bus) REQUIRE b.id IS UNIQUE
```
```cypher
CREATE CONSTRAINT IF NOT EXISTS FOR (p:Pump) REQUIRE p.id IS UNIQUE
```
```cypher
CREATE CONSTRAINT IF NOT EXISTS FOR (g:Generator) REQUIRE g.id IS UNIQUE
```
```cypher
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Node_Junction) REQUIRE n.id IS UNIQUE
```
```cypher
CREATE CONSTRAINT IF NOT EXISTS FOR (br:Branch) REQUIRE br.id IS UNIQUE
```
```cypher
CREATE CONSTRAINT IF NOT EXISTS FOR (pl:Pipe_Link) REQUIRE pl.id IS UNIQUE
```
```cypher
CREATE CONSTRAINT IF NOT EXISTS FOR (t:Tank) REQUIRE t.id IS UNIQUE
```
```cypher
CREATE CONSTRAINT IF NOT EXISTS FOR (cn:CyberNode) REQUIRE cn.id IS UNIQUE
```
```cypher
CREATE CONSTRAINT IF NOT EXISTS FOR (ht:HazardType) REQUIRE ht.name IS UNIQUE
```
```cypher
CREATE CONSTRAINT IF NOT EXISTS FOR (sc:SCADA) REQUIRE sc.id IS UNIQUE
```
```cypher
CREATE CONSTRAINT IF NOT EXISTS FOR (bp:BackupPower) REQUIRE bp.id IS UNIQUE
```
