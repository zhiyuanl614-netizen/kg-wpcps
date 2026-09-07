# -*- coding: utf-8 -*-
"""
Water-Power CPS Ontology v2.0 — Python定义
来源: step5d_ontology_v2_complete.json
设计原则: Bottom-up from material evidence, not top-down from prior knowledge
"""

from enum import Enum
from typing import Dict, List, Optional, Set, Tuple

# ============================================================
# 1. 层级枚举
# ============================================================
class Layer(str, Enum):
    POWER = "power"
    WATER = "water"
    CYBER = "cyber"
    HAZARD = "hazard"
    RESILIENCE = "resilience"
    SYSTEM = "system"

# ============================================================
# 2. 实体定义
# ============================================================
ENTITY_DEFINITIONS = {
    # --- 电力层 ---
    "Bus": {
        "label_zh": "母线/变电站",
        "layer": Layer.POWER,
        "v2_decision": "required",
        "total_materials": 5,
        "granularity": "L4-node (M1) / L2-station (M2-M5)",
        "station_alias": "Substation",
        "attributes": ["voltage_level_kV", "bus_load", "bus_voltage"],
        "description": "电力系统节点。论文中为Bus节点，报告/标准/预案/事件中为Substation站级。",
    },
    "Branch": {
        "label_zh": "线路/支路",
        "layer": Layer.POWER,
        "v2_decision": "keep",
        "total_materials": 2,
        "granularity": "L4-node (M1) / L2-station (M3)",
        "station_alias": "TransmissionLine",
        "attributes": ["branch_capacity", "branch_impedance"],
        "description": "电力系统连接支路。论文中为Branch，标准中为TransmissionLine。",
    },
    "Generator": {
        "label_zh": "发电机/电厂",
        "layer": Layer.POWER,
        "v2_decision": "required",
        "total_materials": 4,
        "granularity": "L4-node (M1) / L2-station (M2/M3/M5)",
        "station_alias": "PowerPlant",
        "attributes": ["generator_output", "power_plant_type"],
        "description": "发电机组。论文中为Generator节点，报告/事件中为PowerPlant站级。",
    },
    # --- 水力层 ---
    "Pump": {
        "label_zh": "水泵/泵站",
        "layer": Layer.WATER,
        "v2_decision": "required",
        "total_materials": 5,
        "granularity": "L4-node (M1) / L2-station (M2-M5)",
        "station_alias": "PumpStation",
        "attributes": ["pump_power", "pump_head", "pump_flow"],
        "description": "水泵设备。水电耦合核心锚点之一。",
    },
    "Node_Junction": {
        "label_zh": "水力节点/水厂",
        "layer": Layer.WATER,
        "v2_decision": "keep",
        "total_materials": 3,
        "granularity": "L4-node (M1) / L2-station (M2/M3)",
        "station_alias": "WaterTreatmentPlant",
        "attributes": ["node_demand", "node_pressure"],
        "description": "给水管网节点。论文中为Node/Junction，报告中为WaterTreatmentPlant站级。",
    },
    "Pipe_Link": {
        "label_zh": "管道/管段",
        "layer": Layer.WATER,
        "v2_decision": "keep",
        "total_materials": 2,
        "granularity": "L4-node (M1) / L2-station (M3)",
        "station_alias": "Pipeline",
        "attributes": ["pipe_diameter", "pipe_length", "pipe_roughness", "pipe_material", "leak_rate_limit"],
        "description": "给水管网连接管段。",
    },
    "Tank": {
        "label_zh": "水池/水库",
        "layer": Layer.WATER,
        "v2_decision": "keep",
        "total_materials": 2,
        "granularity": "L4-node (M1) / L2-station (M3)",
        "station_alias": "Tank",
        "attributes": ["tank_capacity", "tank_level"],
        "description": "蓄水设施。",
    },
    "Valve": {
        "label_zh": "阀门",
        "layer": Layer.WATER,
        "v2_decision": "keep",
        "total_materials": 2,
        "granularity": "L4-node (M1) / L3-device (M3)",
        "station_alias": None,
        "attributes": [],
        "description": "管网控制阀门。",
    },
    # --- 信息层 ---
    "SCADA": {
        "label_zh": "SCADA系统",
        "layer": Layer.CYBER,
        "v2_decision": "required",
        "total_materials": 4,
        "granularity": "L1-mention (M1/M2/M5) / L1-requirement (M3)",
        "station_alias": None,
        "attributes": ["SCADA_requirement"],
        "description": "数据采集与监控系统。",
    },
    "CyberNode": {
        "label_zh": "信息节点",
        "layer": Layer.CYBER,
        "v2_decision": "keep",
        "total_materials": 3,
        "granularity": "L4-node (M1) / L3-device (M2/M3)",
        "station_alias": "CyberDevice",
        "sub_types": ["scada", "plc", "rtu", "pmu", "sensor", "actuator"],
        "attributes": ["type"],
        "description": "信息层设备统一节点。v2.0统一为CyberNode+type属性。",
    },
    "CyberEdge": {
        "label_zh": "通信链路",
        "layer": Layer.CYBER,
        "v2_decision": "optional",
        "total_materials": 1,
        "granularity": "L4-node (M1 only)",
        "station_alias": None,
        "sub_types": ["fiber", "wireless"],
        "attributes": [],
        "description": "信息层通信连接。仅论文中出现，v2.0降级为可选。",
    },
    # --- 扰动层 ---
    "HazardType": {
        "label_zh": "扰动类型",
        "layer": Layer.HAZARD,
        "v2_decision": "required",
        "total_materials": 4,
        "granularity": "L1-system (M2-M5)",
        "station_alias": None,
        "attributes": ["hazard_category"],
        "common_values": ["earthquake", "flood", "typhoon", "cyber_attack", "equipment_failure", "ice_disaster"],
        "description": "外部扰动分类。",
    },
    # --- 韧性层 ---
    "BackupPower": {
        "label_zh": "备用电源",
        "layer": Layer.RESILIENCE,
        "v2_decision": "keep",
        "total_materials": 2,
        "granularity": "L3-device (M3/M4)",
        "station_alias": None,
        "attributes": ["backup_power_type", "backup_duration_h"],
        "common_values": ["diesel_generator", "UPS", "dual_power_supply"],
        "description": "备用供电设施。",
    },
    # --- 系统层 ---
    "WaterSystem": {
        "label_zh": "供水系统",
        "layer": Layer.SYSTEM,
        "v2_decision": "keep",
        "total_materials": 2,
        "granularity": "L1-system (M4/M5)",
        "station_alias": None,
        "attributes": [],
        "description": "供水系统整体。预案和事件中的系统级描述实体。",
    },
    "NaturalGasFacility": {
        "label_zh": "天然气设施",
        "layer": Layer.SYSTEM,
        "v2_decision": "keep",
        "total_materials": 2,
        "granularity": "L2-station (M2/M5)",
        "station_alias": None,
        "attributes": [],
        "description": "天然气系统设施。报告和事件中提及气-电耦合。",
    },
    "Reservoir": {
        "label_zh": "水库",
        "layer": Layer.WATER,
        "v2_decision": "optional",
        "total_materials": 1,
        "granularity": "L4-node (M1 only)",
        "station_alias": None,
        "attributes": [],
        "description": "水源水库。仅论文中出现，可合并到Node_Junction(type=reservoir)。",
    },
    "DMA_District": {
        "label_zh": "DMA分区",
        "layer": Layer.WATER,
        "v2_decision": "optional",
        "total_materials": 1,
        "granularity": "L2-station (M3 only)",
        "station_alias": None,
        "attributes": [],
        "description": "独立计量区域。仅标准中出现。",
    },
    "ResponseLevel": {
        "label_zh": "响应等级",
        "layer": Layer.SYSTEM,
        "v2_decision": "optional",
        "total_materials": 1,
        "granularity": "L1-system (M4 only)",
        "station_alias": None,
        "attributes": ["response_level"],
        "description": "应急响应等级。仅预案中出现(I/II/III/IV级)。",
    },
}

# ============================================================
# 3. 关系定义
# ============================================================
RELATION_DEFINITIONS = {
    "POWERED_BY": {
        "label_zh": "供电",
        "v2_decision": "keep",
        "total_materials": 3,
        "domain": ["Pump"],
        "range": ["Bus"],
        "layer": "cross-layer",
        "is_anchor": True,
        "description": "水泵由母线供电。水电耦合核心锚点关系。",
    },
    "CASCADES_TO": {
        "label_zh": "级联传播",
        "v2_decision": "required",
        "total_materials": 4,
        "domain": ["Bus", "Pump", "Generator"],
        "range": ["Pump", "Node_Junction", "Bus"],
        "layer": "cross-layer",
        "is_anchor": True,
        "description": "跨层级联故障传播。",
    },
    "TRIGGERS": {
        "label_zh": "触发",
        "v2_decision": "keep",
        "total_materials": 3,
        "domain": ["HazardType"],
        "range": ["Bus", "Pump", "Generator", "Pipe_Link"],
        "layer": "hazard→physical",
        "is_anchor": False,
        "description": "外部扰动触发物理层组件故障。",
    },
    "CONTROLS": {
        "label_zh": "控制",
        "v2_decision": "required",
        "total_materials": 4,
        "domain": ["SCADA", "CyberNode"],
        "range": ["Bus", "Pump", "Generator"],
        "layer": "cyber→physical",
        "is_anchor": False,
        "description": "信息层控制物理层。",
    },
    "MONITORS": {
        "label_zh": "监测",
        "v2_decision": "keep",
        "total_materials": 2,
        "domain": ["SCADA", "CyberNode"],
        "range": ["Bus", "Pump", "Node_Junction"],
        "layer": "cyber→physical",
        "is_anchor": False,
        "description": "信息层监测物理层。",
    },
    "CONNECTS_TO": {
        "label_zh": "拓扑连接",
        "v2_decision": "keep_single_high",
        "total_materials": 1,
        "domain": ["Bus", "Node_Junction", "CyberNode"],
        "range": ["Bus", "Node_Junction", "CyberNode"],
        "layer": "intra-layer",
        "is_anchor": False,
        "layer_type_values": ["power_branch", "water_pipe", "cyber_comm"],
        "description": "同层拓扑连接。",
    },
    "HAS_BACKUP": {
        "label_zh": "配备备用电源",
        "v2_decision": "keep",
        "total_materials": 2,
        "domain": ["Pump", "Bus"],
        "range": ["BackupPower"],
        "layer": "resilience",
        "is_anchor": False,
        "description": "设施配备备用电源。",
    },
    "REQUIRES_SCADA": {
        "label_zh": "要求SCADA监控",
        "v2_decision": "keep_single_high",
        "total_materials": 1,
        "domain": ["Pump", "Bus"],
        "range": ["SCADA"],
        "layer": "standard-requirement",
        "is_anchor": False,
        "description": "标准要求关键设施配备SCADA监控。M3标准独有。",
    },
    "DEPENDS_ON": {
        "label_zh": "系统级依赖",
        "v2_decision": "optional",
        "total_materials": 1,
        "domain": ["WaterSystem", "Pump"],
        "range": ["Generator", "Bus"],
        "layer": "cross-layer",
        "is_anchor": False,
        "description": "水系统对电力系统的系统级定性依赖。",
    },
    "AMPLIFIES": {
        "label_zh": "正反馈放大",
        "v2_decision": "optional",
        "total_materials": 1,
        "domain": ["Bus", "Pump"],
        "range": ["Bus", "Pump"],
        "layer": "cross-layer",
        "is_anchor": False,
        "description": "正反馈放大效应。事件独有。",
    },
    "MUST_SATISFY": {
        "label_zh": "必须满足准则",
        "v2_decision": "optional",
        "total_materials": 1,
        "domain": ["WaterSystem"],
        "range": ["HazardType"],  # Criterion → 简化为HazardType或System属性
        "layer": "standard-mandatory",
        "is_anchor": False,
        "description": "标准强制满足安全准则(N-1, Kp>=1.05等)。M3标准独有。",
    },
    "MUST_PREVENT": {
        "label_zh": "必须防止级联",
        "v2_decision": "optional",
        "total_materials": 1,
        "domain": ["WaterSystem"],
        "range": ["HazardType"],  # CascadeFailure → 简化
        "layer": "standard-mandatory",
        "is_anchor": False,
        "description": "标准强制防止级联故障。M3标准独有。",
    },
}

# ============================================================
# 4. 属性定义
# ============================================================
ATTRIBUTE_DEFINITIONS = {
    # --- Bus ---
    "voltage_level_kV": {"belongs_to": ["Bus"], "data_type": "float", "unit": "kV", "v2_decision": "required", "common_values": [10, 35, 110, 220, 500]},
    "bus_load": {"belongs_to": ["Bus"], "data_type": "float", "unit": "MW or pu", "v2_decision": "keep_single_high"},
    "bus_voltage": {"belongs_to": ["Bus"], "data_type": "float", "unit": "pu", "v2_decision": "keep_single_high"},
    # --- Branch ---
    "branch_capacity": {"belongs_to": ["Branch"], "data_type": "float", "unit": "MW or pu", "v2_decision": "keep_single_high"},
    "branch_impedance": {"belongs_to": ["Branch"], "data_type": "float", "unit": "pu", "v2_decision": "keep_single_high"},
    # --- Generator ---
    "generator_output": {"belongs_to": ["Generator"], "data_type": "float", "unit": "MW or pu", "v2_decision": "keep"},
    "power_plant_type": {"belongs_to": ["Generator"], "data_type": "string", "unit": None, "v2_decision": "optional", "common_values": ["thermal", "hydro", "nuclear", "wind", "solar"]},
    # --- Pump ---
    "pump_power": {"belongs_to": ["Pump"], "data_type": "float", "unit": "kW", "v2_decision": "keep"},
    "pump_head": {"belongs_to": ["Pump"], "data_type": "float", "unit": "m", "v2_decision": "keep_moderate"},
    "pump_flow": {"belongs_to": ["Pump"], "data_type": "float", "unit": "m³/s", "v2_decision": "keep_moderate"},
    # --- Node_Junction ---
    "node_demand": {"belongs_to": ["Node_Junction"], "data_type": "float", "unit": "m³/s", "v2_decision": "keep_single_high"},
    "node_pressure": {"belongs_to": ["Node_Junction"], "data_type": "float", "unit": "m or MPa", "v2_decision": "keep_single_high"},
    # --- Pipe_Link ---
    "pipe_diameter": {"belongs_to": ["Pipe_Link"], "data_type": "float", "unit": "mm", "v2_decision": "keep_moderate"},
    "pipe_length": {"belongs_to": ["Pipe_Link"], "data_type": "float", "unit": "m", "v2_decision": "optional"},
    "pipe_roughness": {"belongs_to": ["Pipe_Link"], "data_type": "float", "unit": "dimensionless", "v2_decision": "optional"},
    "pipe_material": {"belongs_to": ["Pipe_Link"], "data_type": "string", "unit": None, "v2_decision": "optional", "common_values": ["cast_iron", "steel", "PVC", "concrete"]},
    "leak_rate_limit": {"belongs_to": ["Pipe_Link"], "data_type": "float", "unit": "%", "v2_decision": "optional"},
    # --- Tank ---
    "tank_capacity": {"belongs_to": ["Tank"], "data_type": "float", "unit": "m³", "v2_decision": "keep"},
    "tank_level": {"belongs_to": ["Tank"], "data_type": "float", "unit": "m", "v2_decision": "optional"},
    # --- BackupPower ---
    "backup_power_type": {"belongs_to": ["BackupPower"], "data_type": "string", "unit": None, "v2_decision": "required", "common_values": ["diesel_generator", "UPS", "dual_power_supply"]},
    "backup_duration_h": {"belongs_to": ["BackupPower"], "data_type": "float", "unit": "h", "v2_decision": "keep"},
    # --- Bus/Pump ---
    "station_grade": {"belongs_to": ["Bus", "Pump"], "data_type": "string", "unit": None, "v2_decision": "optional", "common_values": ["grade_1", "grade_2", "grade_3"]},
    # --- HazardType ---
    "hazard_category": {"belongs_to": ["HazardType"], "data_type": "string", "unit": None, "v2_decision": "required", "common_values": ["natural", "technological", "malicious"]},
    # --- SCADA ---
    "SCADA_requirement": {"belongs_to": ["SCADA"], "data_type": "string", "unit": None, "v2_decision": "keep_single_high"},
    # --- System级 ---
    "simulation_model_type": {"belongs_to": ["System"], "data_type": "string", "unit": None, "v2_decision": "keep_single_high", "common_values": ["DC_power_flow", "AC_power_flow", "EPANET", "coupled_simulation"]},
    "load_shedding_pct": {"belongs_to": ["System"], "data_type": "float", "unit": "%", "v2_decision": "keep_moderate"},
    "pressure_satisfaction_pct": {"belongs_to": ["System"], "data_type": "float", "unit": "%", "v2_decision": "optional"},
    "resilience_index": {"belongs_to": ["System"], "data_type": "float", "unit": "dimensionless", "v2_decision": "keep_moderate"},
    "system_performance_Qt": {"belongs_to": ["System"], "data_type": "float", "unit": "dimensionless", "v2_decision": "optional"},
    "stability_criterion": {"belongs_to": ["System"], "data_type": "string", "unit": None, "v2_decision": "optional"},
    "statistical_data": {"belongs_to": ["System"], "data_type": "string", "unit": None, "v2_decision": "keep_single_high"},
    "research_gaps": {"belongs_to": ["System"], "data_type": "string", "unit": None, "v2_decision": "optional"},
    "response_level": {"belongs_to": ["System"], "data_type": "string", "unit": None, "v2_decision": "optional", "common_values": ["I", "II", "III", "IV"]},
    "MW_lost": {"belongs_to": ["System"], "data_type": "float", "unit": "MW", "v2_decision": "keep_moderate"},
    "recovery_time": {"belongs_to": ["System"], "data_type": "float", "unit": "h", "v2_decision": "keep"},
    # --- CascadeEvent ---
    "cascade_step_depth": {"belongs_to": ["CascadeEvent"], "data_type": "int", "unit": "step", "v2_decision": "keep_single_high"},
    "cascade_chain_narrative": {"belongs_to": ["CascadeEvent"], "data_type": "string", "unit": None, "v2_decision": "keep_moderate"},
    "timeline": {"belongs_to": ["CascadeEvent"], "data_type": "string", "unit": None, "v2_decision": "keep_single_high"},
    "impact_population": {"belongs_to": ["CascadeEvent"], "data_type": "int", "unit": "人", "v2_decision": "keep_moderate"},
}

# ============================================================
# 5. 简化映射规则
# ============================================================
POWER_MAPPING = {
    "Substation": "Bus",
    "PowerPlant": "Generator",
    "TransmissionLine": "Branch",
    "DistributionLine": "Branch",
    "Transformer": "Branch",
    "Breaker": "Branch",
    "CapacitorBank": "Bus",
}

WATER_MAPPING = {
    "PumpStation": "Pump",
    "WaterTreatmentPlant": "Node_Junction",
    "IntakePumpStation": "Pump",
    "BoosterPumpStation": "Pump",
    "DrainagePumpStation": "Pump",
    "Pipeline": "Pipe_Link",
    "Valve": "Valve",
    "Tank_Reservoir": "Tank",
    "Hydrant": "Node_Junction",
    "Well": "Node_Junction",
    "Reservoir": "Node_Junction",
}

CYBER_MAPPING = {
    "SCADA_Server": "SCADA",
    "PLC": "CyberNode",
    "RTU": "CyberNode",
    "PMU": "CyberNode",
    "Sensor": "CyberNode",
    "Actuator": "CyberNode",
    "FiberLink": "CyberEdge",
    "WirelessLink": "CyberEdge",
}

# 合并映射
ALL_MAPPING = {**POWER_MAPPING, **WATER_MAPPING, **CYBER_MAPPING}

# CyberNode子类型映射
CYBERNODE_SUBTYPE_MAP = {
    "SCADA_Server": "scada",
    "PLC": "plc",
    "RTU": "rtu",
    "PMU": "pmu",
    "Sensor": "sensor",
    "Actuator": "actuator",
}

# ============================================================
# 6. 材料类型枚举
# ============================================================
class MaterialType(str, Enum):
    M1_ACADEMIC_PAPER = "M1_academic_paper"
    M2_REPORT = "M2_report"
    M3_STANDARD = "M3_standard"
    M4_EMERGENCY_PLAN = "M4_emergency_plan"
    M5_EVENT = "M5_event"

MATERIAL_GRANULARITY = {
    MaterialType.M1_ACADEMIC_PAPER: "L4-node",
    MaterialType.M2_REPORT: "L2-station",
    MaterialType.M3_STANDARD: "L2-station+L3-device",
    MaterialType.M4_EMERGENCY_PLAN: "L2-station",
    MaterialType.M5_EVENT: "L2-station",
}

# ============================================================
# 7. 辅助函数
# ============================================================
def get_entity_layer(entity_type: str) -> Optional[Layer]:
    """获取实体所属层级"""
    defn = ENTITY_DEFINITIONS.get(entity_type)
    return defn["layer"] if defn else None

def get_entity_attributes(entity_type: str) -> List[str]:
    """获取实体的v2.0属性列表"""
    defn = ENTITY_DEFINITIONS.get(entity_type)
    return defn.get("attributes", []) if defn else []

def validate_relation(rel_type: str, source_type: str, target_type: str) -> Tuple[bool, str]:
    """校验关系是否符合v2.0本体约束"""
    defn = RELATION_DEFINITIONS.get(rel_type)
    if not defn:
        return False, f"Unknown relation type: {rel_type}"
    domain = defn["domain"]
    range_ = defn["range"]
    if source_type not in domain:
        return False, f"Relation {rel_type} domain mismatch: expected {domain}, got {source_type}"
    if target_type not in range_:
        return False, f"Relation {rel_type} range mismatch: expected {range_}, got {target_type}"
    return True, "OK"

def map_industry_term(term: str) -> Optional[str]:
    """将行业术语映射为本体标准实体名"""
    return ALL_MAPPING.get(term)

def get_required_entities() -> List[str]:
    """获取所有required实体"""
    return [k for k, v in ENTITY_DEFINITIONS.items() if v["v2_decision"] == "required"]

def get_required_relations() -> List[str]:
    """获取所有required关系"""
    return [k for k, v in RELATION_DEFINITIONS.items() if v["v2_decision"] == "required"]

def get_anchor_relations() -> List[str]:
    """获取锚点关系"""
    return [k for k, v in RELATION_DEFINITIONS.items() if v.get("is_anchor")]

def get_layer_entities(layer: Layer) -> List[str]:
    """获取指定层级的所有实体"""
    return [k for k, v in ENTITY_DEFINITIONS.items() if v["layer"] == layer]

def entity_id_format(entity_type: str, raw_name: str, material_type: MaterialType) -> str:
    """根据材料类型生成规范化实体ID"""
    if material_type == MaterialType.M1_ACADEMIC_PAPER:
        # 论文: 节点级ID (如 Bus-5, Pump-3)
        return f"{entity_type}-{raw_name}"
    else:
        # 其他材料: 站级ID (如 Bus_朝阳变电站)
        return f"{entity_type}_{raw_name}"

# ============================================================
# 8. 统计信息
# ============================================================
STATISTICS = {
    "entities": {"total": 18, "required": 5, "keep": 9, "optional": 4},
    "relations": {"total": 12, "required": 2, "keep": 4, "keep_single_high": 2, "optional": 4},
    "attributes": {"total": 39, "required": 3, "keep": 5, "keep_moderate": 8, "keep_single_high": 11, "optional": 12},
    "layers": {
        "power": ["Bus", "Branch", "Generator"],
        "water": ["Pump", "Node_Junction", "Pipe_Link", "Tank", "Valve"],
        "cyber": ["SCADA", "CyberNode", "CyberEdge"],
        "hazard": ["HazardType"],
        "resilience": ["BackupPower"],
        "system": ["WaterSystem", "NaturalGasFacility", "ResponseLevel"],
    },
    "cross_layer_relations": ["POWERED_BY", "CASCADES_TO", "TRIGGERS", "DEPENDS_ON", "AMPLIFIES"],
    "cyber_physical_relations": ["CONTROLS", "MONITORS"],
}

if __name__ == "__main__":
    print("=== Water-Power CPS Ontology v2.0 ===")
    print(f"实体: {STATISTICS['entities']}")
    print(f"关系: {STATISTICS['relations']}")
    print(f"属性: {STATISTICS['attributes']}")
    print(f"\nRequired实体: {get_required_entities()}")
    print(f"Required关系: {get_required_relations()}")
    print(f"锚点关系: {get_anchor_relations()}")
    print(f"\n映射测试:")
    print(f"  Substation → {map_industry_term('Substation')}")
    print(f"  PumpStation → {map_industry_term('PumpStation')}")
    print(f"  PLC → {map_industry_term('PLC')}")
    print(f"\n关系校验测试:")
    ok, msg = validate_relation("POWERED_BY", "Pump", "Bus")
    print(f"  POWERED_BY(Pump→Bus): {ok} ({msg})")
    ok, msg = validate_relation("POWERED_BY", "Bus", "Pump")
    print(f"  POWERED_BY(Bus→Pump): {ok} ({msg})")
