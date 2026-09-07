// ============================================================
// 城市供水-电力信息物理耦合系统 — Neo4j 5.x 图数据库Schema
// 版本: 1.0.0 | 创建日期: 2026-08-31
// ============================================================

// ──────────────────────────────────────────────
// 一、节点标签与约束
// ──────────────────────────────────────────────

// === 物理层：电力设施 ===
CREATE CONSTRAINT pf_id IF NOT EXISTS
FOR (n:PowerFacility) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT pf_type IF NOT EXISTS
FOR (n:PowerFacility) REQUIRE n.facility_type IS NOT NULL;

// 电力设施子标签（可叠加）
// :PowerPlant, :Substation, :TransmissionLine, :DistributionLine,
// :Transformer, :Breaker, :CapacitorBank, :Reactor, :BusBar

// === 物理层：供水设施 ===
CREATE CONSTRAINT wf_id IF NOT EXISTS
FOR (n:WaterFacility) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT wf_type IF NOT EXISTS
FOR (n:WaterFacility) REQUIRE n.facility_type IS NOT NULL;

// 供水设施子标签
// :WaterTreatmentPlant, :IntakePumpStation, :BoosterPumpStation,
// :DrainagePumpStation, :Pipeline, :Valve, :Tank, :Reservoir, :Hydrant, :Well

// === 信息层：信息设备 ===
CREATE CONSTRAINT cd_id IF NOT EXISTS
FOR (n:CyberDevice) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT cd_type IF NOT EXISTS
FOR (n:CyberDevice) REQUIRE n.device_type IS NOT NULL;

// 信息设备子标签
// :SCADA_Server, :HMI_Workstation, :PLC, :RTU, :PMU, :IED,
// :Sensor, :Actuator, :Firewall, :Gateway, :DataServer, :Historian

// === 信息层：通信链路 ===
CREATE CONSTRAINT cl_id IF NOT EXISTS
FOR (n:CommLink) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT cl_type IF NOT EXISTS
FOR (n:CommLink) REQUIRE n.link_type IS NOT NULL;

// === 扰动层 ===
CREATE CONSTRAINT ht_id IF NOT EXISTS
FOR (n:HazardThreat) REQUIRE n.id IS UNIQUE;

CREATE CONSTRAINT ht_type IF NOT EXISTS
FOR (n:HazardThreat) REQUIRE n.hazard_type IS NOT NULL;

// === 状态层 ===
CREATE CONSTRAINT cs_id IF NOT EXISTS
FOR (n:CPSState) REQUIRE n.id IS UNIQUE;

// === 级联事件 ===
CREATE CONSTRAINT ce_id IF NOT EXISTS
FOR (n:CascadeEvent) REQUIRE n.id IS UNIQUE;

// === 文献来源 ===
CREATE CONSTRAINT ref_id IF NOT EXISTS
FOR (n:Reference) REQUIRE n.id IS UNIQUE;

// ──────────────────────────────────────────────
// 二、索引（加速查询）
// ──────────────────────────────────────────────

// 物理设施空间索引
CREATE INDEX pf_spatial IF NOT EXISTS
FOR (n:PowerFacility) ON (n.latitude, n.longitude);

CREATE INDEX wf_spatial IF NOT EXISTS
FOR (n:WaterFacility) ON (n.latitude, n.longitude);

// 设施类型索引
CREATE INDEX pf_type_idx IF NOT EXISTS
FOR (n:PowerFacility) ON (n.facility_type);

CREATE INDEX wf_type_idx IF NOT EXISTS
FOR (n:WaterFacility) ON (n.facility_type);

CREATE INDEX cd_type_idx IF NOT EXISTS
FOR (n:CyberDevice) ON (n.device_type);

// 运行状态索引
CREATE INDEX pf_status IF NOT EXISTS
FOR (n:PowerFacility) ON (n.operating_status);

CREATE INDEX wf_status IF NOT EXISTS
FOR (n:WaterFacility) ON (n.operating_status);

CREATE INDEX cd_status IF NOT EXISTS
FOR (n:CyberDevice) ON (n.operating_status);

// 扰动类型索引
CREATE INDEX ht_type_idx IF NOT EXISTS
FOR (n:HazardThreat) ON (n.hazard_type);

CREATE INDEX ht_category_idx IF NOT EXISTS
FOR (n:HazardThreat) ON (n.hazard_category);

// 全文索引（用于自然语言搜索）
CREATE FULLTEXT INDEX ref_fulltext IF NOT EXISTS
FOR (n:Reference) ON EACH [n.title, n.abstract, n.authors, n.keywords];

// ──────────────────────────────────────────────
// 三、关系类型定义（文档说明）
// ──────────────────────────────────────────────

// === 跨层关系 ===
// (:CyberDevice)-[:CONTROLS {control_type, control_delay_ms, control_reliability}]->(:PowerFacility|WaterFacility)
// (:CyberDevice)-[:MONITORS {monitor_type, sampling_interval_s, measurement_accuracy}]->(:PowerFacility|WaterFacility)
// (:PowerFacility)-[:POWER_SUPPLIES {supply_capacity_kva, supply_reliability, is_primary, backup_available}]->(:WaterFacility)
// (:WaterFacility)-[:DEPENDS_ON_POWER {power_demand_kw, criticality, backup_duration_h}]->(:PowerFacility)

// === 层内关系 ===
// (:PowerFacility)-[:CONNECTS_TO {connection_type, capacity, length_km, impedance}]->(:PowerFacility)
// (:WaterFacility)-[:CONNECTS_TO {connection_type, capacity, length_km, roughness_coefficient}]->(:WaterFacility)
// (:CyberDevice)-[:TRANSMITS_VIA {data_type, data_rate_kbps}]->(:CommLink)

// === 级联关系 ===
// (:PowerFacility|WaterFacility|CyberDevice)-[:CASCADES_TO {propagation_mechanism, propagation_delay_s, probability, amplification_factor}]->(:PowerFacility|WaterFacility|CyberDevice)
// (:HazardThreat)-[:TRIGGERS {trigger_probability, vulnerability_index}]->(:PowerFacility|WaterFacility|CyberDevice|CommLink)

// === 状态关系 ===
// (:PowerFacility|WaterFacility|CyberDevice)-[:HAS_STATE {timestamp}]->(:CPSState)
// (:CascadeEvent)-[:INCLUDES_STEP]->(:CPSState)

// === 文献溯源关系 ===
// (:Reference)-[:DESCRIBES]->(:PowerFacility|WaterFacility|CyberDevice|HazardThreat|CascadeEvent)
// (:Reference)-[:PROPOSES_METHOD]->(:Method)
// (:Reference)-[:CITES]->(:Reference)

// ──────────────────────────────────────────────
// 四、示例数据（验证Schema）
// ──────────────────────────────────────────────

// 创建示例电力设施
CREATE (ps1:PowerFacility:Substation {
  id: 'PF_SUB_001',
  name: '城东110kV变电站',
  facility_type: 'Substation',
  voltage_level_kv: 110,
  rated_capacity_mva: 50,
  latitude: 34.258,
  longitude: 108.942,
  grid_region: '西安城东',
  operating_status: 'normal',
  commissioning_year: 2015,
  backup_generator: false,
  criticality_level: 4
})

CREATE (ps2:PowerFacility:Substation {
  id: 'PF_SUB_002',
  name: '高新220kV变电站',
  facility_type: 'Substation',
  voltage_level_kv: 220,
  rated_capacity_mva: 180,
  latitude: 34.223,
  longitude: 108.883,
  grid_region: '西安高新',
  operating_status: 'normal',
  commissioning_year: 2018,
  backup_generator: true,
  backup_generator_capacity_kva: 500,
  criticality_level: 5
})

// 创建示例供水设施
CREATE (wp1:WaterFacility:BoosterPumpStation {
  id: 'WF_PUMP_001',
  name: '城东加压泵站',
  facility_type: 'BoosterPumpStation',
  capacity_m3d: 50000,
  pump_power_kw: 450,
  pump_head_m: 35,
  latitude: 34.260,
  longitude: 108.945,
  service_area: '城东片区',
  operating_status: 'normal',
  power_supply_source_id: 'PF_SUB_001',
  backup_power_type: 'diesel_generator',
  backup_power_duration_h: 8,
  criticality_level: 4
})

CREATE (wt1:WaterFacility:WaterTreatmentPlant {
  id: 'WF_WTP_001',
  name: '曲江净水厂',
  facility_type: 'WaterTreatmentPlant',
  capacity_m3d: 300000,
  latitude: 34.210,
  longitude: 108.920,
  service_area: '曲江新区',
  operating_status: 'normal',
  power_supply_source_id: 'PF_SUB_002',
  backup_power_type: 'dual_feed',
  backup_power_duration_h: 24,
  criticality_level: 5
})

// 创建示例信息设备
CREATE (scada1:CyberDevice:SCADA_Server {
  id: 'CD_SCADA_001',
  name: '供水调度中心SCADA',
  device_type: 'SCADA_Server',
  communication_protocol: 'OPC-UA',
  ip_address: '10.0.1.100',
  redundancy: true,
  security_level: 4,
  operating_status: 'normal'
})

CREATE (plc1:CyberDevice:PLC {
  id: 'CD_PLC_001',
  name: '城东泵站PLC',
  device_type: 'PLC',
  communication_protocol: 'Modbus',
  controlled_physical_id: 'WF_PUMP_001',
  monitored_physical_id: 'WF_PUMP_001',
  redundancy: false,
  security_level: 3,
  operating_status: 'normal'
})

CREATE (sensor1:CyberDevice:Sensor {
  id: 'CD_SENSOR_001',
  name: '城东泵站出口压力传感器',
  device_type: 'Sensor',
  sensor_type: 'pressure',
  communication_protocol: 'IEC104',
  monitored_physical_id: 'WF_PUMP_001',
  redundancy: true,
  security_level: 2,
  operating_status: 'normal'
})

// 创建示例通信链路
CREATE (link1:CommLink:FiberLink {
  id: 'CL_FIBER_001',
  name: '调度中心-城东泵站光纤',
  link_type: 'FiberLink',
  bandwidth_mbps: 1000,
  latency_ms: 2,
  reliability: 0.9999,
  source_device_id: 'CD_SCADA_001',
  target_device_id: 'CD_PLC_001',
  redundancy_path: true,
  encryption: true,
  operating_status: 'normal'
})

// 创建示例扰动
CREATE (hazard1:HazardThreat:NaturalHazard {
  id: 'HT_FLOOD_001',
  name: '2021郑州7·20特大暴雨',
  hazard_type: 'Flood',
  hazard_category: 'NaturalHazard',
  intensity: 0.95,
  probability: 0.02,
  spatial_extent: '郑州市全域',
  reference_event: '2021 Zhengzhou Flood'
})

// 创建示例级联事件
CREATE (cascade1:CascadeEvent {
  id: 'CE_ZZ_2021_001',
  name: '郑州7·20暴雨水电级联失效',
  trigger_hazard_id: 'HT_FLOOD_001',
  total_failed_count: 29,
  total_affected_population: 6000000,
  recovery_time_h: 72,
  reference_source: 'Cascading failures in urban infrastructure systems (2025)'
})

// ──────────────────────────────────────────────
// 五、核心关系创建
// ──────────────────────────────────────────────

// 供电支持：变电站→泵站
MATCH (ps:PowerFacility {id: 'PF_SUB_001'}), (wp:WaterFacility {id: 'WF_PUMP_001'})
CREATE (ps)-[:POWER_SUPPLIES {supply_capacity_kva: 800, supply_reliability: 0.999, is_primary: true, backup_available: true}]->(wp)

// 依赖供电：泵站→变电站
MATCH (wp:WaterFacility {id: 'WF_PUMP_001'}), (ps:PowerFacility {id: 'PF_SUB_001'})
CREATE (wp)-[:DEPENDS_ON_POWER {power_demand_kw: 450, criticality: 'critical', backup_duration_h: 8}]->(ps)

// 下行控制：SCADA→PLC→泵站
MATCH (scada:CyberDevice {id: 'CD_SCADA_001'}), (plc:CyberDevice {id: 'CD_PLC_001'})
CREATE (scada)-[:CONTROLS {control_type: 'setpoint', control_delay_ms: 50, control_reliability: 0.999}]->(plc)

MATCH (plc:CyberDevice {id: 'CD_PLC_001'}), (wp:WaterFacility {id: 'WF_PUMP_001'})
CREATE (plc)-[:CONTROLS {control_type: 'direct_control', control_delay_ms: 10, control_reliability: 0.9995}]->(wp)

// 上行遥测：传感器→SCADA
MATCH (sensor:CyberDevice {id: 'CD_SENSOR_001'}), (scada:CyberDevice {id: 'CD_SCADA_001'})
CREATE (sensor)-[:MONITORS {monitor_type: 'real_time', sampling_interval_s: 1, measurement_accuracy: 0.995}]->(scada)

// 通信传输
MATCH (scada:CyberDevice {id: 'CD_SCADA_001'}), (link:CommLink {id: 'CL_FIBER_001'})
CREATE (scada)-[:TRANSMITS_VIA {data_type: 'command', data_rate_kbps: 64}]->(link)

// 扰动触发
MATCH (hazard:HazardThreat {id: 'HT_FLOOD_001'}), (ps:PowerFacility {id: 'PF_SUB_001'})
CREATE (hazard)-[:TRIGGERS {trigger_probability: 0.3, vulnerability_index: 0.7}]->(ps)

// ──────────────────────────────────────────────
// 六、常用查询模板
// ──────────────────────────────────────────────

// Q1: 查找某变电站供电的所有供水设施
// MATCH (ps:PowerFacility {id: 'PF_SUB_001'})-[:POWER_SUPPLIES]->(wf:WaterFacility)
// RETURN ps.name, wf.name, wf.facility_type

// Q2: 查找某泵站的完整控制链路（SCADA→PLC→泵站）
// MATCH path = (scada:CyberDevice:SCADA_Server)-[:CONTROLS*1..3]->(wf:WaterFacility {id: 'WF_PUMP_001'})
// RETURN path

// Q3: 查找从变电站停电到供水受影响的级联路径（多跳）
// MATCH path = (ps:PowerFacility)-[:CASCADES_TO*1..5]->(wf:WaterFacility)
// WHERE ps.operating_status = 'faulted'
// RETURN path
// ORDER BY length(path)

// Q4: 查找所有受自然灾害威胁的关键供水设施
// MATCH (ht:HazardThreat {hazard_category: 'NaturalHazard'})-[:TRIGGERS]->(wf:WaterFacility)
// WHERE wf.criticality_level >= 4
// RETURN ht.name, wf.name, wf.facility_type, ht.hazard_type

// Q5: 计算各设施类型的级联脆弱性（出度统计）
// MATCH (n)-[c:CASCADES_TO]->(m)
// RETURN labels(n)[0] AS source_type, labels(m)[0] AS target_type,
//        count(c) AS cascade_count, avg(c.probability) AS avg_probability
// ORDER BY cascade_count DESC

// Q6: 查找无备用电源的关键泵站（高脆弱性节点）
// MATCH (wf:WaterFacility:BoosterPumpStation)
// WHERE wf.backup_power_type = 'none' AND wf.criticality_level >= 3
// RETURN wf.name, wf.criticality_level, wf.power_demand_kw

// Q7: 查找信息层单点故障风险（无冗余的PLC）
// MATCH (plc:CyberDevice:PLC {redundancy: false})-[:CONTROLS]->(wf:WaterFacility)
// WHERE wf.criticality_level >= 3
// RETURN plc.name, wf.name, wf.criticality_level

// Q8: 查找特定文献描述的所有实体与关系
// MATCH (ref:Reference {id: 'REF_001'})-[:DESCRIBES]->(entity)
// RETURN ref.title, labels(entity), entity.name
