// ============================================================
// Water-Power CPS Ontology v2.0 — Neo4j 5.x Schema
// 生成日期: 2026-09-06
// 本体版本: 2.0
// 设计原则: Bottom-up from material evidence
// ============================================================

// ============================================================
// 1. 唯一性约束（同时创建索引）
// ============================================================
CREATE CONSTRAINT IF NOT EXISTS FOR (b:Bus) REQUIRE b.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (br:Branch) REQUIRE br.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (g:Generator) REQUIRE g.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (p:Pump) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (n:Node_Junction) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (pl:Pipe_Link) REQUIRE pl.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (t:Tank) REQUIRE t.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (v:Valve) REQUIRE v.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (sc:SCADA) REQUIRE sc.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (cn:CyberNode) REQUIRE cn.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (ce:CyberEdge) REQUIRE ce.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (ht:HazardType) REQUIRE ht.name IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (bp:BackupPower) REQUIRE bp.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (ws:WaterSystem) REQUIRE ws.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (ngf:NaturalGasFacility) REQUIRE ngf.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (res:Reservoir) REQUIRE res.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (dma:DMA_District) REQUIRE dma.id IS UNIQUE;
CREATE CONSTRAINT IF NOT EXISTS FOR (rl:ResponseLevel) REQUIRE rl.id IS UNIQUE;

// ============================================================
// 2. 性能索引
// ============================================================
CREATE INDEX IF NOT EXISTS FOR (b:Bus) ON (b.voltage_level_kV);
CREATE INDEX IF NOT EXISTS FOR (p:Pump) ON (p.pump_power);
CREATE INDEX IF NOT EXISTS FOR (ht:HazardType) ON (ht.hazard_category);
CREATE INDEX IF NOT EXISTS FOR (bp:BackupPower) ON (bp.backup_power_type);
CREATE INDEX IF NOT EXISTS FOR (cn:CyberNode) ON (cn.type);

// 层级索引（支持按层查询）
CREATE INDEX IF NOT EXISTS FOR (b:Bus) ON (b.layer);
CREATE INDEX IF NOT EXISTS FOR (p:Pump) ON (p.layer);
CREATE INDEX IF NOT EXISTS FOR (g:Generator) ON (g.layer);
CREATE INDEX IF NOT EXISTS FOR (n:Node_Junction) ON (n.layer);
CREATE INDEX IF NOT EXISTS FOR (sc:SCADA) ON (sc.layer);
CREATE INDEX IF NOT EXISTS FOR (cn:CyberNode) ON (cn.layer);
CREATE INDEX IF NOT EXISTS FOR (ht:HazardType) ON (ht.layer);

// 材料来源索引（支持溯源查询）
CREATE INDEX IF NOT EXISTS FOR (b:Bus) ON (b.source_material);
CREATE INDEX IF NOT EXISTS FOR (p:Pump) ON (p.source_material);
CREATE INDEX IF NOT EXISTS FOR (ht:HazardType) ON (ht.source_material);

// ============================================================
// 3. 关系约束说明（Neo4j 5.x不支持关系约束，通过应用层校验）
// ============================================================
// POWERED_BY: ONLY from Pump to Bus
// CASCADES_TO: ONLY between Bus, Pump, Generator, Node_Junction
// TRIGGERS: ONLY from HazardType to Bus, Pump, Generator, Pipe_Link
// CONTROLS: ONLY from SCADA/CyberNode to Bus, Pump, Generator
// MONITORS: ONLY from SCADA/CyberNode to Bus, Pump, Node_Junction
// CONNECTS_TO: ONLY between same-layer entities
// HAS_BACKUP: ONLY from Pump/Bus to BackupPower
// REQUIRES_SCADA: ONLY from Pump/Bus to SCADA

// ============================================================
// 4. 示例数据 — IEEE 14-bus + Net3 耦合系统
// ============================================================

// --- 电力层 ---
CREATE (b1:Bus {id: 'Bus-1', layer: 'power', name_zh: '1号母线', voltage_level_kV: 110, bus_load: 0.0, bus_voltage: 1.06, source_material: 'M1', station_alias: 'Substation'})
CREATE (b2:Bus {id: 'Bus-2', layer: 'power', name_zh: '2号母线', voltage_level_kV: 110, bus_load: 0.217, bus_voltage: 1.045, source_material: 'M1', station_alias: 'Substation'})
CREATE (b5:Bus {id: 'Bus-5', layer: 'power', name_zh: '5号母线', voltage_level_kV: 110, bus_load: 0.076, bus_voltage: 1.020, source_material: 'M1', station_alias: 'Substation'})

CREATE (g1:Generator {id: 'Gen-1', layer: 'power', name_zh: '1号发电机', generator_output: 2.32, power_plant_type: 'thermal', source_material: 'M1', station_alias: 'PowerPlant'})
CREATE (g2:Generator {id: 'Gen-2', layer: 'power', name_zh: '2号发电机', generator_output: 0.40, power_plant_type: 'thermal', source_material: 'M1', station_alias: 'PowerPlant'})

CREATE (br12:Branch {id: 'Branch-1-2', layer: 'power', name_zh: '1-2支路', branch_capacity: 2.0, branch_impedance: 0.01938, source_material: 'M1'})

// --- 水力层 ---
CREATE (p3:Pump {id: 'Pump-3', layer: 'water', name_zh: '3号水泵', pump_power: 350, pump_head: 45, pump_flow: 0.5, source_material: 'M1', station_alias: 'PumpStation'})
CREATE (p10:Pump {id: 'Pump-10', layer: 'water', name_zh: '10号水泵', pump_power: 200, pump_head: 30, pump_flow: 0.3, source_material: 'M1', station_alias: 'PumpStation'})

CREATE (n12:Node_Junction {id: 'Node-12', layer: 'water', name_zh: '12号水力节点', node_demand: 0.15, node_pressure: 0.28, source_material: 'M1', station_alias: 'WaterTreatmentPlant'})
CREATE (n15:Node_Junction {id: 'Node-15', layer: 'water', name_zh: '15号水力节点', node_demand: 0.08, node_pressure: 0.25, source_material: 'M1', station_alias: 'WaterTreatmentPlant'})

CREATE (pl1:Pipe_Link {id: 'Pipe-3-12', layer: 'water', name_zh: '3-12管段', pipe_diameter: 300, pipe_length: 1500, pipe_roughness: 0.02, pipe_material: 'cast_iron', source_material: 'M1'})
CREATE (t1:Tank {id: 'Tank-1', layer: 'water', name_zh: '1号水池', tank_capacity: 5000, tank_level: 4.5, source_material: 'M1'})

// --- 信息层 ---
CREATE (sc1:SCADA {id: 'SCADA-1', layer: 'cyber', name_zh: '1号SCADA系统', SCADA_requirement: '实时监控电力与供水系统运行状态', source_material: 'M1'})
CREATE (cn1:CyberNode {id: 'PLC-Pump-3', layer: 'cyber', name_zh: '3号水泵PLC', type: 'plc', source_material: 'M1'})
CREATE (cn2:CyberNode {id: 'RTU-Bus-5', layer: 'cyber', name_zh: '5号母线RTU', type: 'rtu', source_material: 'M1'})

// --- 扰动层 ---
CREATE (ht1:HazardType {name: 'earthquake', layer: 'hazard', name_zh: '地震', hazard_category: 'natural', source_material: 'M1'})
CREATE (ht2:HazardType {name: 'cyber_attack', layer: 'hazard', name_zh: '网络攻击', hazard_category: 'malicious', source_material: 'M5'})
CREATE (ht3:HazardType {name: 'ice_disaster', layer: 'hazard', name_zh: '冰灾', hazard_category: 'natural', source_material: 'M4'})

// --- 韧性层 ---
CREATE (bp1:BackupPower {id: 'BP-Pump-3-DG', layer: 'resilience', name_zh: '3号水泵柴油发电机', backup_power_type: 'diesel_generator', backup_duration_h: 8, source_material: 'M4'})

// --- 系统层 ---
CREATE (ws1:WaterSystem {id: 'WS-CityA', layer: 'system', name_zh: 'A市供水系统', source_material: 'M4'})

// ============================================================
// 5. 关系创建
// ============================================================

// 核心锚点关系: POWERED_BY
CREATE (p3)-[:POWERED_BY {explicitness: 'R3-formula', evidence: 'Table 3: Pump-3 powered by Bus-5', source_material: 'M1'}]->(b5)
CREATE (p10)-[:POWERED_BY {explicitness: 'R3-formula', evidence: 'Table 3: Pump-10 powered by Bus-2', source_material: 'M1'}]->(b2)

// 级联传播: CASCADES_TO
CREATE (b5)-[:CASCADES_TO {explicitness: 'R3-formula', evidence: 'Simulation step 3: Bus-5 fault causes Pump-3 power loss', source_material: 'M1'}]->(p3)
CREATE (p3)-[:CASCADES_TO {explicitness: 'R3-formula', evidence: 'Simulation step 5: Pump-3 loss causes Node-12 pressure drop', source_material: 'M1'}]->(n12)

// 扰动触发: TRIGGERS
CREATE (ht1)-[:TRIGGERS {explicitness: 'R4-probabilistic', evidence: 'Earthquake probability model P(fault|EQ)', source_material: 'M1'}]->(b5)
CREATE (ht2)-[:TRIGGERS {explicitness: 'R1-narrative', evidence: 'Ukraine 2015: cyber attack caused substation breaker trip', source_material: 'M5'}]->(b5)

// 信息控制: CONTROLS
CREATE (sc1)-[:CONTROLS {explicitness: 'R2-simplified', evidence: 'SCADA controls breaker state on Bus-5', source_material: 'M1'}]->(b5)
CREATE (cn1)-[:CONTROLS {explicitness: 'R2-simplified', evidence: 'PLC controls Pump-3 on/off state', source_material: 'M1'}]->(p3)

// 信息监测: MONITORS
CREATE (cn2)-[:MONITORS {explicitness: 'R2-simplified', evidence: 'RTU monitors Bus-5 voltage and frequency', source_material: 'M1'}]->(b5)

// 拓扑连接: CONNECTS_TO
CREATE (b1)-[:CONNECTS_TO {layer_type: 'power_branch', via: 'Branch-1-2', source_material: 'M1'}]->(b2)
CREATE (p3)-[:CONNECTS_TO {layer_type: 'water_pipe', via: 'Pipe-3-12', source_material: 'M1'}]->(n12)

// 韧性: HAS_BACKUP
CREATE (p3)-[:HAS_BACKUP {explicitness: 'R2-named', evidence: 'Emergency plan: Pump-3 equipped with 350kW diesel generator', source_material: 'M4'}]->(bp1)

// ============================================================
// 6. 常用查询模板
// ============================================================

// Q1: 完整级联路径（扰动→电力→供水）
// MATCH path = (h:HazardType)-[:TRIGGERS]->(b:Bus)-[:CASCADES_TO*1..3]->(n:Node_Junction)
// RETURN path

// Q2: 水电耦合核心查询（所有POWERED_BY关系）
// MATCH (p:Pump)-[:POWERED_BY]->(b:Bus)
// RETURN p.id, b.id, p.pump_power, b.voltage_level_kV

// Q3: 信息物理耦合查询（SCADA控制/监测的物理设备）
// MATCH (c:SCADA)-[:CONTROLS|MONITORS]->(target)
// RETURN c.id, labels(target), target.id

// Q4: 韧性干预查询（有备用电源的泵站）
// MATCH (p:Pump)-[:HAS_BACKUP]->(bp:BackupPower)
// RETURN p.id, bp.backup_power_type, bp.backup_duration_h

// Q5: 跨层级联深度查询
// MATCH path = (b:Bus)-[:CASCADES_TO*1..5]->(end)
// RETURN path, length(path) AS depth
// ORDER BY depth DESC

// Q6: 按扰动类型查询级联影响
// MATCH (h:HazardType {hazard_category: 'natural'})-[:TRIGGERS]->(target)
// RETURN h.name, labels(target), target.id

// Q7: 供电依赖脆弱性分析（单点故障）
// MATCH (b:Bus)<-[:POWERED_BY]-(p:Pump)
// WITH b, collect(p) AS pumps
// WHERE size(pumps) >= 2
// RETURN b.id, size(pumps) AS dependent_pumps, [p IN pumps | p.id] AS pump_ids

// Q8: 材料溯源查询
// MATCH (n)
// WHERE n.source_material = 'M1'
// RETURN labels(n), n.id, n.name_zh
