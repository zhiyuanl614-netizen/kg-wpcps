
// === M1_P001 (M1_academic_paper) ===

// Auto-generated Cypher from extraction result
// Material type: M1_academic_paper
// Ontology version: 2.0

// === Entities ===
MERGE (Bus_1:Bus {id: 'Bus-1', layer: 'power', name_zh: '1号母线', voltage_level_kV: 110, station_alias: 'Substation', source_material: 'M1_academic_paper'})
MERGE (Bus_10:Bus {id: 'Bus-10', layer: 'power', name_zh: '10号母线', voltage_level_kV: 35, station_alias: 'Substation', source_material: 'M1_academic_paper'})
MERGE (Bus_22:Bus {id: 'Bus-22', layer: 'power', name_zh: '22号母线', voltage_level_kV: 10, station_alias: 'Substation', source_material: 'M1_academic_paper'})
MERGE (Bus_24:Bus {id: 'Bus-24', layer: 'power', name_zh: '24号母线', voltage_level_kV: 10, station_alias: 'Substation', source_material: 'M1_academic_paper'})
MERGE (Bus_8:Bus {id: 'Bus-8', layer: 'power', name_zh: '8号母线', voltage_level_kV: 110, station_alias: 'Substation', source_material: 'M1_academic_paper'})
MERGE (Bus_15:Bus {id: 'Bus-15', layer: 'power', name_zh: '15号母线', voltage_level_kV: 35, station_alias: 'Substation', source_material: 'M1_academic_paper'})
MERGE (Gen_1:Generator {id: 'Gen-1', layer: 'power', name_zh: '1号发电机', generator_output: 2.32, power_plant_type: 'thermal', station_alias: 'PowerPlant', source_material: 'M1_academic_paper'})
MERGE (Pump_1:Pump {id: 'Pump-1', layer: 'water', name_zh: '1号水泵(取水)', pump_power: 500, pump_head: 35, pump_flow: 1.0, station_alias: 'PumpStation', source_material: 'M1_academic_paper'})
MERGE (Pump_2:Pump {id: 'Pump-2', layer: 'water', name_zh: '2号水泵(加压)', pump_power: 350, pump_head: 28, pump_flow: 0.8, station_alias: 'PumpStation', source_material: 'M1_academic_paper'})
MERGE (Pump_3:Pump {id: 'Pump-3', layer: 'water', name_zh: '3号水泵(加压)', pump_power: 280, pump_head: 22, pump_flow: 0.6, station_alias: 'PumpStation', source_material: 'M1_academic_paper'})
MERGE (Pump_4:Pump {id: 'Pump-4', layer: 'water', name_zh: '4号水泵(排水)', pump_power: 200, pump_head: 15, pump_flow: 0.4, station_alias: 'PumpStation', source_material: 'M1_academic_paper'})
MERGE (Pump_5:Pump {id: 'Pump-5', layer: 'water', name_zh: '5号水泵(取水)', pump_power: 450, pump_head: 40, pump_flow: 0.9, station_alias: 'PumpStation', source_material: 'M1_academic_paper'})
MERGE (Node_12:Node_Junction {id: 'Node-12', layer: 'water', name_zh: '12号水力节点', node_demand: 0.15, node_pressure: 0.28, station_alias: 'WaterTreatmentPlant', source_material: 'M1_academic_paper'})
MERGE (Tank_1:Tank {id: 'Tank-1', layer: 'water', name_zh: '1号水池', tank_capacity: 5000, tank_level: 4.5, station_alias: 'Tank', source_material: 'M1_academic_paper'})
MERGE (SCADA_1:SCADA {id: 'SCADA-1', layer: 'cyber', name_zh: '1号SCADA系统', source_material: 'M1_academic_paper'})
MERGE (PLC_P1:CyberNode {id: 'PLC-P1', layer: 'cyber', name_zh: '1号水泵PLC', type: 'plc', station_alias: 'CyberDevice', source_material: 'M1_academic_paper'})
MERGE (RTU_B8:CyberNode {id: 'RTU-B8', layer: 'cyber', name_zh: '8号母线RTU', type: 'rtu', station_alias: 'CyberDevice', source_material: 'M1_academic_paper'})
MERGE (HazardType_earthquake:HazardType {name: 'HazardType_earthquake', layer: 'hazard', name_zh: '地震', hazard_category: 'natural', source_material: 'M1_academic_paper'})
MERGE (BP_P1_DG:BackupPower {id: 'BP-P1-DG', layer: 'resilience', name_zh: '1号水泵柴油发电机', backup_power_type: 'diesel_generator', backup_duration_h: 8, source_material: 'M1_academic_paper'})
MERGE (BP_P5_DG:BackupPower {id: 'BP-P5-DG', layer: 'resilience', name_zh: '5号水泵柴油发电机', backup_power_type: 'diesel_generator', backup_duration_h: 8, source_material: 'M1_academic_paper'})

// === Relations ===
MATCH (Pump_1:Pump {id: 'Pump-1'})
MATCH (Bus_10:Bus {id: 'Bus-10'})
MERGE (Pump_1)-[:POWERED_BY {explicitness: 'R3-formula', evidence: 'Table 2: Pump-1 (intake, 500kW) powered by Bus-10 (35kV)'}]->(Bus_10)

MATCH (Pump_2:Pump {id: 'Pump-2'})
MATCH (Bus_22:Bus {id: 'Bus-22'})
MERGE (Pump_2)-[:POWERED_BY {explicitness: 'R3-formula', evidence: 'Table 2: Pump-2 (booster, 350kW) powered by Bus-22 (10kV)'}]->(Bus_22)

MATCH (Pump_3:Pump {id: 'Pump-3'})
MATCH (Bus_24:Bus {id: 'Bus-24'})
MERGE (Pump_3)-[:POWERED_BY {explicitness: 'R3-formula', evidence: 'Table 2: Pump-3 (booster, 280kW) powered by Bus-24 (10kV)'}]->(Bus_24)

MATCH (Pump_4:Pump {id: 'Pump-4'})
MATCH (Bus_15:Bus {id: 'Bus-15'})
MERGE (Pump_4)-[:POWERED_BY {explicitness: 'R3-formula', evidence: 'Table 2: Pump-4 (drainage, 200kW) powered by Bus-15 (35kV)'}]->(Bus_15)

MATCH (Pump_5:Pump {id: 'Pump-5'})
MATCH (Bus_8:Bus {id: 'Bus-8'})
MERGE (Pump_5)-[:POWERED_BY {explicitness: 'R3-formula', evidence: 'Table 2: Pump-5 (intake, 450kW) powered by Bus-8 (110kV)'}]->(Bus_8)

MATCH (HazardType_earthquake:HazardType {name: 'HazardType_earthquake'})
MATCH (Bus_8:Bus {id: 'Bus-8'})
MERGE (HazardType_earthquake)-[:TRIGGERS {explicitness: 'R4-probabilistic', evidence: 'Earthquake probability model P(fault|EQ)'}]->(Bus_8)

MATCH (SCADA_1:SCADA {id: 'SCADA-1'})
MATCH (Bus_8:Bus {id: 'Bus-8'})
MERGE (SCADA_1)-[:CONTROLS {explicitness: 'R2-simplified', evidence: 'SCADA controls breaker state on Bus-8'}]->(Bus_8)

MATCH (PLC_P1:CyberNode {id: 'PLC-P1'})
MATCH (Pump_1:Pump {id: 'Pump-1'})
MERGE (PLC_P1)-[:CONTROLS {explicitness: 'R2-simplified', evidence: 'PLC controls Pump-1 on/off state'}]->(Pump_1)

MATCH (RTU_B8:CyberNode {id: 'RTU-B8'})
MATCH (Bus_8:Bus {id: 'Bus-8'})
MERGE (RTU_B8)-[:MONITORS {explicitness: 'R2-simplified', evidence: 'RTU monitors Bus-8 voltage and frequency'}]->(Bus_8)

MATCH (Pump_1:Pump {id: 'Pump-1'})
MATCH (BP_P1_DG:BackupPower {id: 'BP-P1-DG'})
MERGE (Pump_1)-[:HAS_BACKUP {explicitness: 'R2-named', evidence: 'Section 5.3: Pump-1 equipped with 500kW diesel generator, 8h duration'}]->(BP_P1_DG)

MATCH (Pump_5:Pump {id: 'Pump-5'})
MATCH (BP_P5_DG:BackupPower {id: 'BP-P5-DG'})
MERGE (Pump_5)-[:HAS_BACKUP {explicitness: 'R2-named', evidence: 'Section 5.3: Pump-5 equipped with 450kW diesel generator, 8h duration'}]->(BP_P5_DG)

// === Cascade Relations ===
MATCH (Bus_10:Bus {id: 'Bus-10'})
MATCH (Pump_1:Pump {id: 'Pump-1'})
MERGE (Bus_10)-[:CASCADES_TO {explicitness: 'model', evidence: 'Bus-10 fault → Pump-1 power loss → Node-12 pressure drop to 0.15MPa'}]->(Pump_1)

MATCH (Pump_1:Pump {id: 'Pump-1'})
MATCH (Node_12:Node_Junction {id: 'Node-12'})
MERGE (Pump_1)-[:CASCADES_TO {explicitness: 'model', evidence: 'Bus-10 fault → Pump-1 power loss → Node-12 pressure drop to 0.15MPa'}]->(Node_12)

MATCH (Bus_8:Bus {id: 'Bus-8'})
MATCH (Pump_5:Pump {id: 'Pump-5'})
MERGE (Bus_8)-[:CASCADES_TO {explicitness: 'model', evidence: 'Bus-8 fault → Pump-5 power loss → Node-12 pressure drop'}]->(Pump_5)

MATCH (Pump_5:Pump {id: 'Pump-5'})
MATCH (Node_12:Node_Junction {id: 'Node-12'})
MERGE (Pump_5)-[:CASCADES_TO {explicitness: 'model', evidence: 'Bus-8 fault → Pump-5 power loss → Node-12 pressure drop'}]->(Node_12)


// === M5_E001 (M5_event) ===

// Auto-generated Cypher from extraction result
// Material type: M5_event
// Ontology version: 2.0

// === Entities ===
MERGE (Bus_Prykarpattya:Bus {id: 'Bus_Prykarpattya', layer: 'power', name_zh: 'Prykarpattya变电站', voltage_level_kV: 110, station_alias: 'Substation', source_material: 'M5_event'})
MERGE (Bus_Chernivtsi:Bus {id: 'Bus_Chernivtsi', layer: 'power', name_zh: 'Chernivtsi变电站', voltage_level_kV: 110, station_alias: 'Substation', source_material: 'M5_event'})
MERGE (Bus_Kyiv:Bus {id: 'Bus_Kyiv', layer: 'power', name_zh: 'Kyiv变电站', voltage_level_kV: 110, station_alias: 'Substation', source_material: 'M5_event'})
MERGE (SCADA_Prykarpattya:SCADA {id: 'SCADA_Prykarpattya', layer: 'cyber', name_zh: 'Prykarpattyaoblenergo SCADA', source_material: 'M5_event'})
MERGE (HazardType_cyber_attack:HazardType {name: 'HazardType_cyber_attack', layer: 'hazard', name_zh: '网络攻击', hazard_category: 'malicious', source_material: 'M5_event'})
MERGE (Pump_Ivano:Pump {id: 'Pump_Ivano', layer: 'water', name_zh: 'Ivano-Frankivsk泵站', station_alias: 'PumpStation', source_material: 'M5_event'})

// === Relations ===
MATCH (HazardType_cyber_attack:HazardType {name: 'HazardType_cyber_attack'})
MATCH (SCADA_Prykarpattya:SCADA {id: 'SCADA_Prykarpattya'})
MERGE (HazardType_cyber_attack)-[:TRIGGERS {explicitness: 'R1-narrative', evidence: 'Spear-phishing email compromised SCADA system'}]->(SCADA_Prykarpattya)

MATCH (SCADA_Prykarpattya:SCADA {id: 'SCADA_Prykarpattya'})
MATCH (Bus_Prykarpattya:Bus {id: 'Bus_Prykarpattya'})
MERGE (SCADA_Prykarpattya)-[:CONTROLS {explicitness: 'R1-narrative', evidence: 'Attackers remotely opened 7 110kV breakers via SCADA'}]->(Bus_Prykarpattya)

MATCH (SCADA_Prykarpattya:SCADA {id: 'SCADA_Prykarpattya'})
MATCH (Bus_Chernivtsi:Bus {id: 'Bus_Chernivtsi'})
MERGE (SCADA_Prykarpattya)-[:CONTROLS {explicitness: 'R1-narrative', evidence: 'Attackers remotely opened 23 35kV breakers via SCADA'}]->(Bus_Chernivtsi)

MATCH (Pump_Ivano:Pump {id: 'Pump_Ivano'})
MATCH (Bus_Prykarpattya:Bus {id: 'Bus_Prykarpattya'})
MERGE (Pump_Ivano)-[:POWERED_BY {explicitness: 'R0-implicit', evidence: 'Pump station lost power when substation breakers were opened'}]->(Bus_Prykarpattya)

// === Cascade Relations ===
MATCH (cyber_attack:Unknown {id: 'cyber_attack'})
MATCH (SCADA被控:Unknown {id: 'SCADA被控'})
MERGE (cyber_attack)-[:CASCADES_TO {explicitness: 'narrative', evidence: '网络攻击→SCADA控制权丧失→变电站跳闸→泵站断电→供水压力下降'}]->(SCADA被控)

MATCH (SCADA被控:Unknown {id: 'SCADA被控'})
MATCH (变电站断路器断开:Unknown {id: '变电站断路器断开'})
MERGE (SCADA被控)-[:CASCADES_TO {explicitness: 'narrative', evidence: '网络攻击→SCADA控制权丧失→变电站跳闸→泵站断电→供水压力下降'}]->(变电站断路器断开)

MATCH (变电站断路器断开:Unknown {id: '变电站断路器断开'})
MATCH (大面积停电:Unknown {id: '大面积停电'})
MERGE (变电站断路器断开)-[:CASCADES_TO {explicitness: 'narrative', evidence: '网络攻击→SCADA控制权丧失→变电站跳闸→泵站断电→供水压力下降'}]->(大面积停电)

MATCH (大面积停电:Unknown {id: '大面积停电'})
MATCH (泵站断电:Unknown {id: '泵站断电'})
MERGE (大面积停电)-[:CASCADES_TO {explicitness: 'narrative', evidence: '网络攻击→SCADA控制权丧失→变电站跳闸→泵站断电→供水压力下降'}]->(泵站断电)

MATCH (泵站断电:Unknown {id: '泵站断电'})
MATCH (供水压力下降:Unknown {id: '供水压力下降'})
MERGE (泵站断电)-[:CASCADES_TO {explicitness: 'narrative', evidence: '网络攻击→SCADA控制权丧失→变电站跳闸→泵站断电→供水压力下降'}]->(供水压力下降)


// === M5_E003 (M5_event) ===

// Auto-generated Cypher from extraction result
// Material type: M5_event
// Ontology version: 2.0

// === Entities ===
MERGE (Bus_ERCOT_Grid:Bus {id: 'Bus_ERCOT_Grid', layer: 'power', name_zh: 'ERCOT电网', voltage_level_kV: 345, station_alias: 'Substation', source_material: 'M5_event'})
MERGE (Gen_NaturalGas:Generator {id: 'Gen_NaturalGas', layer: 'power', name_zh: '天然气发电机组', power_plant_type: 'thermal', station_alias: 'PowerPlant', source_material: 'M5_event'})
MERGE (Pump_Austin_Ullrich:Pump {id: 'Pump_Austin_Ullrich', layer: 'water', name_zh: 'Austin Ullrich水厂泵站', pump_power: 800, station_alias: 'PumpStation', source_material: 'M5_event'})
MERGE (Pump_Houston:Pump {id: 'Pump_Houston', layer: 'water', name_zh: 'Houston泵站', station_alias: 'PumpStation', source_material: 'M5_event'})
MERGE (HazardType_ice_disaster:HazardType {name: 'HazardType_ice_disaster', layer: 'hazard', name_zh: '冰灾', hazard_category: 'natural', source_material: 'M5_event'})
MERGE (BP_Austin_DG:BackupPower {id: 'BP_Austin_DG', layer: 'resilience', name_zh: 'Austin备用柴油发电机', backup_power_type: 'diesel_generator', backup_duration_h: 8, source_material: 'M5_event'})
MERGE (NaturalGasFacility_TX:NaturalGasFacility {id: 'NaturalGasFacility_TX', layer: 'system', name_zh: '德州天然气设施', source_material: 'M5_event'})

// === Relations ===
MATCH (HazardType_ice_disaster:HazardType {name: 'HazardType_ice_disaster'})
MATCH (NaturalGasFacility_TX:NaturalGasFacility {id: 'NaturalGasFacility_TX'})
MERGE (HazardType_ice_disaster)-[:TRIGGERS {explicitness: 'R1-narrative', evidence: 'Extreme cold froze natural gas wellheads'}]->(NaturalGasFacility_TX)

MATCH (HazardType_ice_disaster:HazardType {name: 'HazardType_ice_disaster'})
MATCH (Bus_ERCOT_Grid:Bus {id: 'Bus_ERCOT_Grid'})
MERGE (HazardType_ice_disaster)-[:TRIGGERS {explicitness: 'R1-narrative', evidence: 'Ice on transmission lines caused outages'}]->(Bus_ERCOT_Grid)

MATCH (NaturalGasFacility_TX:NaturalGasFacility {id: 'NaturalGasFacility_TX'})
MATCH (Gen_NaturalGas:Generator {id: 'Gen_NaturalGas'})
MERGE (NaturalGasFacility_TX)-[:CASCADES_TO {explicitness: 'R1-narrative', evidence: 'Gas supply reduction caused generator failures'}]->(Gen_NaturalGas)

MATCH (Bus_ERCOT_Grid:Bus {id: 'Bus_ERCOT_Grid'})
MATCH (Pump_Austin_Ullrich:Pump {id: 'Pump_Austin_Ullrich'})
MERGE (Bus_ERCOT_Grid)-[:CASCADES_TO {explicitness: 'R1-narrative', evidence: 'Power outage caused pump station failure'}]->(Pump_Austin_Ullrich)

MATCH (Bus_ERCOT_Grid:Bus {id: 'Bus_ERCOT_Grid'})
MATCH (Pump_Houston:Pump {id: 'Pump_Houston'})
MERGE (Bus_ERCOT_Grid)-[:CASCADES_TO {explicitness: 'R1-narrative', evidence: 'Power outage caused Houston pump failure'}]->(Pump_Houston)

MATCH (Pump_Austin_Ullrich:Pump {id: 'Pump_Austin_Ullrich'})
MATCH (BP_Austin_DG:BackupPower {id: 'BP_Austin_DG'})
MERGE (Pump_Austin_Ullrich)-[:HAS_BACKUP {explicitness: 'R1-narrative', evidence: 'Ullrich plant had backup generators that failed after 8 hours'}]->(BP_Austin_DG)

// === Cascade Relations ===
MATCH (冰灾:Unknown {id: '冰灾'})
MATCH (天然气井口冻结:Unknown {id: '天然气井口冻结'})
MERGE (冰灾)-[:CASCADES_TO {explicitness: 'narrative', evidence: '冰灾→天然气供应中断→发电停运→电网崩溃→泵站断电→水压下降→管道冻裂→供水中断（正反馈放大）'}]->(天然气井口冻结)

MATCH (天然气井口冻结:Unknown {id: '天然气井口冻结'})
MATCH (发电机组停运:Unknown {id: '发电机组停运'})
MERGE (天然气井口冻结)-[:CASCADES_TO {explicitness: 'narrative', evidence: '冰灾→天然气供应中断→发电停运→电网崩溃→泵站断电→水压下降→管道冻裂→供水中断（正反馈放大）'}]->(发电机组停运)

MATCH (发电机组停运:Unknown {id: '发电机组停运'})
MATCH (电网大面积停电:Unknown {id: '电网大面积停电'})
MERGE (发电机组停运)-[:CASCADES_TO {explicitness: 'narrative', evidence: '冰灾→天然气供应中断→发电停运→电网崩溃→泵站断电→水压下降→管道冻裂→供水中断（正反馈放大）'}]->(电网大面积停电)

MATCH (电网大面积停电:Unknown {id: '电网大面积停电'})
MATCH (泵站断电:Unknown {id: '泵站断电'})
MERGE (电网大面积停电)-[:CASCADES_TO {explicitness: 'narrative', evidence: '冰灾→天然气供应中断→发电停运→电网崩溃→泵站断电→水压下降→管道冻裂→供水中断（正反馈放大）'}]->(泵站断电)

MATCH (泵站断电:Unknown {id: '泵站断电'})
MATCH (水压下降:Unknown {id: '水压下降'})
MERGE (泵站断电)-[:CASCADES_TO {explicitness: 'narrative', evidence: '冰灾→天然气供应中断→发电停运→电网崩溃→泵站断电→水压下降→管道冻裂→供水中断（正反馈放大）'}]->(水压下降)

MATCH (水压下降:Unknown {id: '水压下降'})
MATCH (管道冻裂:Unknown {id: '管道冻裂'})
MERGE (水压下降)-[:CASCADES_TO {explicitness: 'narrative', evidence: '冰灾→天然气供应中断→发电停运→电网崩溃→泵站断电→水压下降→管道冻裂→供水中断（正反馈放大）'}]->(管道冻裂)

MATCH (管道冻裂:Unknown {id: '管道冻裂'})
MATCH (供水中断:Unknown {id: '供水中断'})
MERGE (管道冻裂)-[:CASCADES_TO {explicitness: 'narrative', evidence: '冰灾→天然气供应中断→发电停运→电网崩溃→泵站断电→水压下降→管道冻裂→供水中断（正反馈放大）'}]->(供水中断)


// === M4_PL001 (M4_emergency_plan) ===

// Auto-generated Cypher from extraction result
// Material type: M4_emergency_plan
// Ontology version: 2.0

// === Entities ===
MERGE (Bus_朝阳门变电站:Bus {id: 'Bus_朝阳门变电站', layer: 'power', name_zh: '朝阳门220kV变电站', voltage_level_kV: 220, station_alias: 'Substation', source_material: 'M4_emergency_plan'})
MERGE (Bus_孙河变电站:Bus {id: 'Bus_孙河变电站', layer: 'power', name_zh: '孙河220kV变电站', voltage_level_kV: 220, station_alias: 'Substation', source_material: 'M4_emergency_plan'})
MERGE (Bus_田村变电站:Bus {id: 'Bus_田村变电站', layer: 'power', name_zh: '田村110kV变电站', voltage_level_kV: 110, station_alias: 'Substation', source_material: 'M4_emergency_plan'})
MERGE (Bus_花乡变电站:Bus {id: 'Bus_花乡变电站', layer: 'power', name_zh: '花乡110kV变电站', voltage_level_kV: 110, station_alias: 'Substation', source_material: 'M4_emergency_plan'})
MERGE (Pump_第三水厂:Pump {id: 'Pump_第三水厂', layer: 'water', name_zh: '第三水厂泵站', pump_power: 800, station_alias: 'PumpStation', source_material: 'M4_emergency_plan'})
MERGE (Pump_第九水厂:Pump {id: 'Pump_第九水厂', layer: 'water', name_zh: '第九水厂泵站', pump_power: 1200, station_alias: 'PumpStation', source_material: 'M4_emergency_plan'})
MERGE (Pump_田村山水厂:Pump {id: 'Pump_田村山水厂', layer: 'water', name_zh: '田村山净水厂泵站', pump_power: 500, station_alias: 'PumpStation', source_material: 'M4_emergency_plan'})
MERGE (Pump_郭公庄水厂:Pump {id: 'Pump_郭公庄水厂', layer: 'water', name_zh: '郭公庄水厂泵站', pump_power: 600, station_alias: 'PumpStation', source_material: 'M4_emergency_plan'})
MERGE (BP_第三水厂_DG:BackupPower {id: 'BP_第三水厂_DG', layer: 'resilience', name_zh: '第三水厂柴油发电机', backup_power_type: 'diesel_generator', backup_duration_h: 8, source_material: 'M4_emergency_plan'})
MERGE (BP_第九水厂_DG:BackupPower {id: 'BP_第九水厂_DG', layer: 'resilience', name_zh: '第九水厂柴油发电机', backup_power_type: 'diesel_generator', backup_duration_h: 12, source_material: 'M4_emergency_plan'})
MERGE (BP_田村山_DG:BackupPower {id: 'BP_田村山_DG', layer: 'resilience', name_zh: '田村山柴油发电机', backup_power_type: 'diesel_generator', backup_duration_h: 6, source_material: 'M4_emergency_plan'})
MERGE (BP_郭公庄_DG:BackupPower {id: 'BP_郭公庄_DG', layer: 'resilience', name_zh: '郭公庄柴油发电机', backup_power_type: 'diesel_generator', backup_duration_h: 8, source_material: 'M4_emergency_plan'})
MERGE (HazardType_极端低温:HazardType {name: 'HazardType_极端低温', layer: 'hazard', name_zh: '极端低温', hazard_category: 'natural', source_material: 'M4_emergency_plan'})
MERGE (WS_北京供水系统:WaterSystem {id: 'WS_北京供水系统', layer: 'system', name_zh: '北京市供水系统', source_material: 'M4_emergency_plan'})

// === Relations ===
MATCH (Pump_第三水厂:Pump {id: 'Pump_第三水厂'})
MATCH (Bus_朝阳门变电站:Bus {id: 'Bus_朝阳门变电站'})
MERGE (Pump_第三水厂)-[:POWERED_BY {explicitness: 'R2-named', evidence: '预案第三节：第三水厂由朝阳门220kV变电站供电'}]->(Bus_朝阳门变电站)

MATCH (Pump_第九水厂:Pump {id: 'Pump_第九水厂'})
MATCH (Bus_孙河变电站:Bus {id: 'Bus_孙河变电站'})
MERGE (Pump_第九水厂)-[:POWERED_BY {explicitness: 'R2-named', evidence: '预案第三节：第九水厂由孙河220kV变电站供电'}]->(Bus_孙河变电站)

MATCH (Pump_田村山水厂:Pump {id: 'Pump_田村山水厂'})
MATCH (Bus_田村变电站:Bus {id: 'Bus_田村变电站'})
MERGE (Pump_田村山水厂)-[:POWERED_BY {explicitness: 'R2-named', evidence: '预案第三节：田村山净水厂由田村110kV变电站供电'}]->(Bus_田村变电站)

MATCH (Pump_郭公庄水厂:Pump {id: 'Pump_郭公庄水厂'})
MATCH (Bus_花乡变电站:Bus {id: 'Bus_花乡变电站'})
MERGE (Pump_郭公庄水厂)-[:POWERED_BY {explicitness: 'R2-named', evidence: '预案第三节：郭公庄水厂由花乡110kV变电站供电'}]->(Bus_花乡变电站)

MATCH (Pump_第三水厂:Pump {id: 'Pump_第三水厂'})
MATCH (BP_第三水厂_DG:BackupPower {id: 'BP_第三水厂_DG'})
MERGE (Pump_第三水厂)-[:HAS_BACKUP {explicitness: 'R2-named', evidence: '预案第四节：第三水厂配备2台800kW柴油发电机，8小时'}]->(BP_第三水厂_DG)

MATCH (Pump_第九水厂:Pump {id: 'Pump_第九水厂'})
MATCH (BP_第九水厂_DG:BackupPower {id: 'BP_第九水厂_DG'})
MERGE (Pump_第九水厂)-[:HAS_BACKUP {explicitness: 'R2-named', evidence: '预案第四节：第九水厂配备3台1200kW柴油发电机，12小时'}]->(BP_第九水厂_DG)

MATCH (Pump_田村山水厂:Pump {id: 'Pump_田村山水厂'})
MATCH (BP_田村山_DG:BackupPower {id: 'BP_田村山_DG'})
MERGE (Pump_田村山水厂)-[:HAS_BACKUP {explicitness: 'R2-named', evidence: '预案第四节：田村山配备1台500kW柴油发电机，6小时'}]->(BP_田村山_DG)

MATCH (Pump_郭公庄水厂:Pump {id: 'Pump_郭公庄水厂'})
MATCH (BP_郭公庄_DG:BackupPower {id: 'BP_郭公庄_DG'})
MERGE (Pump_郭公庄水厂)-[:HAS_BACKUP {explicitness: 'R2-named', evidence: '预案第四节：郭公庄配备2台600kW柴油发电机，8小时'}]->(BP_郭公庄_DG)

// === Cascade Relations ===
MATCH (线路覆冰:Unknown {id: '线路覆冰'})
MATCH (变电站跳闸:Unknown {id: '变电站跳闸'})
MERGE (线路覆冰)-[:CASCADES_TO {explicitness: 'narrative', evidence: '极端低温→线路覆冰→变电站跳闸→水厂泵站断电→启动备用电源'}]->(变电站跳闸)

MATCH (变电站跳闸:Unknown {id: '变电站跳闸'})
MATCH (水厂泵站断电:Unknown {id: '水厂泵站断电'})
MERGE (变电站跳闸)-[:CASCADES_TO {explicitness: 'narrative', evidence: '极端低温→线路覆冰→变电站跳闸→水厂泵站断电→启动备用电源'}]->(水厂泵站断电)

MATCH (水厂泵站断电:Unknown {id: '水厂泵站断电'})
MATCH (片区水压下降:Unknown {id: '片区水压下降'})
MERGE (水厂泵站断电)-[:CASCADES_TO {explicitness: 'narrative', evidence: '极端低温→线路覆冰→变电站跳闸→水厂泵站断电→启动备用电源'}]->(片区水压下降)

MATCH (片区水压下降:Unknown {id: '片区水压下降'})
MATCH (启动柴油发电机:Unknown {id: '启动柴油发电机'})
MERGE (片区水压下降)-[:CASCADES_TO {explicitness: 'narrative', evidence: '极端低温→线路覆冰→变电站跳闸→水厂泵站断电→启动备用电源'}]->(启动柴油发电机)

MATCH (启动柴油发电机:Unknown {id: '启动柴油发电机'})
MATCH (备用电源耗尽则供水中断:Unknown {id: '备用电源耗尽则供水中断'})
MERGE (启动柴油发电机)-[:CASCADES_TO {explicitness: 'narrative', evidence: '极端低温→线路覆冰→变电站跳闸→水厂泵站断电→启动备用电源'}]->(备用电源耗尽则供水中断)


// === M3_S001 (M3_standard) ===

// Auto-generated Cypher from extraction result
// Material type: M3_standard
// Ontology version: 2.0

// === Entities ===
MERGE (Pump_一级泵站:Pump {id: 'Pump_一级泵站', layer: 'water', name_zh: '一级泵站', pump_power: 500, pump_head: 35, pump_flow: 1.0, _ext_station_grade: 'grade_1', station_alias: 'PumpStation', source_material: 'M3_standard'})
MERGE (Pump_二级泵站:Pump {id: 'Pump_二级泵站', layer: 'water', name_zh: '二级泵站', pump_power: 200, _ext_station_grade: 'grade_2', station_alias: 'PumpStation', source_material: 'M3_standard'})
MERGE (SCADA_监控系统:SCADA {id: 'SCADA_监控系统', layer: 'cyber', name_zh: '给水系统SCADA', SCADA_requirement: '必须配备SCADA监控系统', source_material: 'M3_standard'})
MERGE (BP_一级泵站_备用电源:BackupPower {id: 'BP_一级泵站_备用电源', layer: 'resilience', name_zh: '一级泵站备用电源', backup_power_type: 'diesel_generator', backup_duration_h: 8, source_material: 'M3_standard'})

// === Relations ===
MATCH (Pump_一级泵站:Pump {id: 'Pump_一级泵站'})
MATCH (SCADA_监控系统:SCADA {id: 'SCADA_监控系统'})
MERGE (Pump_一级泵站)-[:REQUIRES_SCADA {explicitness: 'R1-qualitative-requirement', evidence: '第5.3.1条：城市给水系统必须配备SCADA监控系统', mandatory_level: 'MUST'}]->(SCADA_监控系统)

MATCH (Pump_一级泵站:Pump {id: 'Pump_一级泵站'})
MATCH (BP_一级泵站_备用电源:BackupPower {id: 'BP_一级泵站_备用电源'})
MERGE (Pump_一级泵站)-[:HAS_BACKUP {explicitness: 'R1-qualitative-requirement', evidence: '第5.1.2条：一级泵站必须配备备用电源', mandatory_level: 'MUST'}]->(BP_一级泵站_备用电源)
