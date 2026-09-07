# -*- coding: utf-8 -*-
"""
五类材料专用结构化抽取提示词模板 — v2.0 Ontology对齐版
来源: step6_extraction_prompts.json
升级: 对齐v2.0本体(18实体+12关系+39属性), 统一输出格式
"""

import json
from typing import Dict, Optional

# ============================================================
# 通用本体规范头（所有模板共享）
# ============================================================
ONTOLOGY_HEADER = """## 本体规范 (v2.0)

### 实体类型（按层级）
- 电力层: Bus(母线/变电站), Branch(支路/线路), Generator(发电机/电厂)
- 水力层: Pump(水泵/泵站), Node_Junction(水力节点/水厂), Pipe_Link(管道), Tank(水池), Valve(阀门)
- 信息层: SCADA(数据采集与监控系统), CyberNode(信息节点, type=plc/rtu/pmu/sensor/actuator), CyberEdge(通信链路, 可选)
- 扰动层: HazardType(扰动类型, hazard_category=natural/technological/malicious)
- 韧性层: BackupPower(备用电源, backup_power_type=diesel_generator/UPS/dual_power_supply)
- 系统层: WaterSystem(供水系统), NaturalGasFacility(天然气设施), ResponseLevel(响应等级, 可选)

### 关系类型
- POWERED_BY: Pump → Bus (水泵由母线供电，核心锚点)
- CASCADES_TO: Bus|Pump|Generator → Pump|Node_Junction|Bus (跨层级联)
- TRIGGERS: HazardType → Bus|Pump|Generator|Pipe_Link (扰动触发)
- CONTROLS: SCADA|CyberNode → Bus|Pump|Generator (信息控制物理)
- MONITORS: SCADA|CyberNode → Bus|Pump|Node_Junction (信息监测物理)
- CONNECTS_TO: 同层拓扑连接 (layer_type=power_branch/water_pipe/cyber_comm)
- HAS_BACKUP: Pump|Bus → BackupPower (配备备用电源)
- REQUIRES_SCADA: Pump|Bus → SCADA (标准要求SCADA监控)
- DEPENDS_ON: WaterSystem|Pump → Generator|Bus (系统级依赖，可选)
- AMPLIFIES: Bus|Pump → Bus|Pump (正反馈放大，事件独有，可选)

### 简化映射规则
- Substation → Bus, PowerPlant → Generator(on Bus)
- TransmissionLine/DistributionLine → Branch
- Transformer → Branch(impedance), Breaker → Branch(on/off)
- PumpStation → Pump + POWERED_BY→Bus
- WaterTreatmentPlant → Node_Junction(type=source)
- Pipeline → Pipe_Link, Valve → Pipe_Link(valve_state) or Valve
- PLC/RTU/PMU/Sensor/Actuator → CyberNode(type=xxx)
- FiberLink/WirelessLink → CyberEdge(type=xxx)

### 通用抽取规则
1. 不抽取：坐标、IP地址、固件版本（C6约束）
2. 属性值保留原始单位和精度，不要转换
3. 如果材料未提及某属性，不要编造
4. 每个实体必须有id、type、layer三个字段
5. 每个关系必须有source、target、type、evidence四个字段"""

# ============================================================
# M1 学术论文
# ============================================================
M1_SYSTEM_PROMPT = f"""你是城市供水-电力信息物理耦合系统(CPS)的知识抽取专家。你的任务是从学术论文中抽取实体、关系和属性，构建知识图谱三元组。

{ONTOLOGY_HEADER}

## M1专用规则
1. 实体ID使用论文中的节点编号（如Bus-5, Pump-3, Node-12）
2. POWERED_BY映射表是最高优先级抽取目标
3. 网络拓扑用CONNECTS_TO表达，区分layer_type
4. 级联路径用CASCADES_TO链式表达
5. 仿真模型类型用simulation_model_type属性记录
6. 属性精度为A4-simulation（标幺值pu、MW、kW、m³/s等）
7. 关系精度为R3-formula（映射表/公式）或R4-probabilistic（故障概率模型）"""

M1_USER_TEMPLATE = """请从以下学术论文中抽取知识图谱三元组。

论文标题: {title}
论文DOI: {doi}
论文摘要/正文:
{content}

请按以下JSON格式输出：

```json
{{
  "entities": [
    {{
      "id": "Bus-5",
      "type": "Bus",
      "layer": "power",
      "name_zh": "5号母线",
      "attributes": {{
        "voltage_level_kV": 110,
        "bus_load": 0.85,
        "bus_voltage": 0.98
      }}
    }}
  ],
  "relations": [
    {{
      "source": "Pump-3",
      "target": "Bus-5",
      "type": "POWERED_BY",
      "explicitness": "R3-formula",
      "evidence": "Table 3 shows Pump-3 is powered by Bus-5"
    }}
  ],
  "cascade_paths": [
    {{
      "chain": ["Bus-5", "Pump-3", "Node-12"],
      "relation_type": "CASCADES_TO",
      "expression": "model",
      "description": "Bus-5 fault -> Pump-3 power loss -> Node-12 pressure drop to 0.15MPa"
    }}
  ],
  "system_info": {{
    "simulation_model_type": "DC_power_flow + EPANET",
    "cascade_step_depth": 5,
    "load_shedding_pct": 23.5,
    "resilience_index": 0.72
  }},
  "metadata": {{
    "paper_id": "{paper_id}",
    "extraction_date": "{extraction_date}",
    "ontology_version": "2.0",
    "material_type": "M1_academic_paper"
  }}
}}
```

注意：
- 每个实体必须有id、type、layer三个字段
- 关系必须有source、target、type、evidence四个字段
- evidence字段引用论文原文（表格号、公式号、页码）
- 属性值保留原始单位，不要转换
- 如果论文未提及某属性，不要编造"""

# ============================================================
# M2 研究报告
# ============================================================
M2_SYSTEM_PROMPT = f"""你是城市供水-电力信息物理耦合系统(CPS)的知识抽取专家。你的任务是从研究报告中抽取实体、关系和属性。

{ONTOLOGY_HEADER}

## M2专用规则
1. 实体使用报告中的站级名称（如朝阳变电站、城北泵站）
2. 实体ID格式：类型_站名（如Bus_朝阳变电站, Pump_城北泵站）
3. 关系多为定性描述(R1)，evidence字段引用原文叙述
4. 重点关注：系统级依赖描述、扰动分类、统计数据、研究空白
5. 属性精度通常为A1-A2（定性或半定量），不要编造精确数值
6. CASCADES_TO在报告中通常是因果叙述，不是公式模型"""

M2_USER_TEMPLATE = """请从以下研究报告中抽取知识图谱三元组。

报告标题: {title}
报告机构: {organization}
报告内容:
{content}

请按以下JSON格式输出：

```json
{{
  "entities": [
    {{
      "id": "Bus_朝阳变电站",
      "type": "Bus",
      "layer": "power",
      "name_zh": "朝阳变电站",
      "attributes": {{
        "voltage_level_kV": 110
      }}
    }}
  ],
  "relations": [
    {{
      "source": "Pump_城北泵站",
      "target": "Bus_朝阳变电站",
      "type": "POWERED_BY",
      "explicitness": "R1-qualitative",
      "evidence": "报告指出城北泵站由朝阳变电站供电"
    }}
  ],
  "cascade_narratives": [
    {{
      "chain": ["极端高温", "朝阳变电站过载", "城北泵站断电", "片区水压下降"],
      "relation_type": "CASCADES_TO",
      "expression": "narrative",
      "description": "极端高温导致用电激增，变电站过载跳闸，泵站失去电源，供水压力下降"
    }}
  ],
  "system_info": {{
    "hazard_category": "natural",
    "statistical_data": "2023年夏季高峰负荷增长15%",
    "research_gaps": "水-电耦合量化模型缺乏"
  }},
  "metadata": {{
    "report_id": "{report_id}",
    "extraction_date": "{extraction_date}",
    "ontology_version": "2.0",
    "material_type": "M2_report"
  }}
}}
```

注意：
- 站级实体ID格式：类型_站名（如Bus_朝阳变电站）
- 关系evidence必须引用报告原文
- 属性值只记录报告中明确给出的，不要推算
- cascade_narratives记录因果叙述链，不是仿真模型"""

# ============================================================
# M3 技术标准
# ============================================================
M3_SYSTEM_PROMPT = f"""你是城市供水-电力信息物理耦合系统(CPS)的知识抽取专家。你的任务是从技术标准中抽取实体、关系和属性。

{ONTOLOGY_HEADER}

## M3专用规则
1. 重点关注应/必须/不得/严禁等规范性用语
2. 区分强制要求(MUST/SHALL)和推荐建议(SHOULD/MAY)
3. 安全阈值精确记录（如Kp>=1.05、漏损率<=12%）
4. 额定参数记录标准给出的设计值
5. 标准中通常没有级联模型，但有防止级联的强制要求
6. 标准中通常没有POWERED_BY映射，但有SCADA监控和备用电源要求
7. REQUIRES_SCADA和HAS_BACKUP是M3的核心关系"""

M3_USER_TEMPLATE = """请从以下技术标准中抽取知识图谱三元组。

标准名称: {title}
标准编号: {standard_id}
标准内容:
{content}

请按以下JSON格式输出：

```json
{{
  "entities": [
    {{
      "id": "Pump_一级泵站",
      "type": "Pump",
      "layer": "water",
      "name_zh": "一级泵站",
      "attributes": {{
        "station_grade": "grade_1",
        "pump_power": 500,
        "pump_head": 45,
        "pump_flow": 1.2
      }}
    }}
  ],
  "relations": [
    {{
      "source": "Pump_一级泵站",
      "target": "SCADA_监控系统",
      "type": "REQUIRES_SCADA",
      "explicitness": "R1-qualitative-requirement",
      "mandatory_level": "MUST",
      "evidence": "第6.2.1条：一级泵站必须配备SCADA监控系统"
    }}
  ],
  "mandatory_requirements": [
    {{
      "requirement_type": "HAS_BACKUP",
      "target_entity": "Pump_一级泵站",
      "mandatory_level": "MUST",
      "detail": "一级泵站应配置备用电源，柴油发电机容量不低于主泵功率的120%",
      "clause": "第7.1.3条"
    }}
  ],
  "safety_thresholds": [
    {{
      "criterion": "N-1",
      "description": "任一元件故障时系统应保持稳定运行",
      "clause": "第5.1.1条"
    }}
  ],
  "metadata": {{
    "standard_id": "{standard_id}",
    "extraction_date": "{extraction_date}",
    "ontology_version": "2.0",
    "material_type": "M3_standard"
  }}
}}
```

注意：
- mandatory_level字段区分MUST(强制)/SHOULD(推荐)/MAY(可选)
- 安全阈值精确记录原文表述
- clause字段记录标准条款号
- 额定参数只记录标准明确给出的设计值"""

# ============================================================
# M4 应急预案
# ============================================================
M4_SYSTEM_PROMPT = f"""你是城市供水-电力信息物理耦合系统(CPS)的知识抽取专家。你的任务是从应急预案中抽取实体、关系和属性。

{ONTOLOGY_HEADER}

## M4专用规则
1. 预案是唯一提供具名站间映射的材料（XX泵站由XX变电站供电）
2. 实体ID格式：类型_站名（如Pump_城北泵站, Bus_朝阳变电站）
3. 重点关注备用电源详情（类型、容量、持续时间）
4. 响应等级分类（I/II/III/IV级）及触发条件
5. 级联链通常是定性因果叙述
6. POWERED_BY关系在预案中为R2-named精度（具名映射）
7. HAS_BACKUP关系是M4的核心关系之一"""

M4_USER_TEMPLATE = """请从以下应急预案中抽取知识图谱三元组。

预案名称: {title}
预案区域: {region}
预案内容:
{content}

请按以下JSON格式输出：

```json
{{
  "entities": [
    {{
      "id": "Pump_城北泵站",
      "type": "Pump",
      "layer": "water",
      "name_zh": "城北泵站",
      "attributes": {{
        "pump_power": 800
      }}
    }},
    {{
      "id": "BackupPower_城北泵站_柴油发电机",
      "type": "BackupPower",
      "layer": "resilience",
      "name_zh": "城北泵站柴油发电机",
      "attributes": {{
        "backup_power_type": "diesel_generator",
        "backup_duration_h": 8
      }}
    }}
  ],
  "relations": [
    {{
      "source": "Pump_城北泵站",
      "target": "Bus_朝阳变电站",
      "type": "POWERED_BY",
      "explicitness": "R2-named",
      "evidence": "预案附件2：城北泵站由朝阳变电站110kV母线供电"
    }},
    {{
      "source": "Pump_城北泵站",
      "target": "BackupPower_城北泵站_柴油发电机",
      "type": "HAS_BACKUP",
      "explicitness": "R2-named",
      "evidence": "预案第4.3节：城北泵站配备800kW柴油发电机，可持续运行8小时"
    }}
  ],
  "cascade_chains": [
    {{
      "trigger": "HazardType_极端低温",
      "chain": ["朝阳变电站覆冰跳闸", "城北泵站断电", "城北片区水压下降", "启动柴油发电机"],
      "response_level": "II",
      "description": "极端低温导致线路覆冰，变电站跳闸，泵站断电，启动备用电源"
    }}
  ],
  "metadata": {{
    "plan_id": "{plan_id}",
    "extraction_date": "{extraction_date}",
    "ontology_version": "2.0",
    "material_type": "M4_emergency_plan"
  }}
}}
```

注意：
- 具名站间映射是最高优先级抽取目标
- 备用电源详情（类型+持续时间）必须完整记录
- 响应等级和触发条件必须记录
- cascade_chains记录预案中的因果链和应对措施"""

# ============================================================
# M5 事件案例
# ============================================================
M5_SYSTEM_PROMPT = f"""你是城市供水-电力信息物理耦合系统(CPS)的知识抽取专家。你的任务是从真实事件案例中抽取实体、关系和属性。

{ONTOLOGY_HEADER}

## M5专用规则
1. 事件是唯一提供完整级联链+时间线的材料
2. 实体ID格式：类型_设施名（如Bus_Prykarpattia变电站）
3. 重点关注AMPLIFIES正反馈环（如停电→泵停→消防失效→火灾→更大停电）
4. 网络攻击事件需抽取信息层级联链（kill chain）
5. 影响统计数据（人口、MW、恢复时间）必须记录
6. 时间线精确到小时/分钟
7. 从叙述中重建隐含的依赖关系（R0-implicit到R1-narrative）"""

M5_USER_TEMPLATE = """请从以下事件案例中抽取知识图谱三元组。

事件名称: {title}
事件日期: {event_date}
事件描述:
{content}

请按以下JSON格式输出：

```json
{{
  "entities": [
    {{
      "id": "Bus_Prykarpattia变电站",
      "type": "Bus",
      "layer": "power",
      "name_zh": "Prykarpattia变电站",
      "attributes": {{
        "voltage_level_kV": 110
      }}
    }}
  ],
  "relations": [
    {{
      "source": "HazardType_cyber_attack",
      "target": "Bus_Prykarpattia变电站",
      "type": "TRIGGERS",
      "explicitness": "R1-narrative",
      "evidence": "黑客通过钓鱼邮件入侵SCADA系统，远程断开变电站断路器"
    }},
    {{
      "source": "SCADA_监控系统",
      "target": "Bus_Prykarpattia变电站",
      "type": "CONTROLS",
      "explicitness": "R1-narrative",
      "evidence": "攻击者通过SCADA系统远程控制断路器"
    }}
  ],
  "event_timeline": [
    {{
      "time": "2015-12-23 15:30",
      "event": "黑客远程断开7个110kV断路器",
      "affected_entities": ["Bus_Prykarpattia变电站"]
    }}
  ],
  "cascade_chains": [
    {{
      "chain": ["cyber_attack", "SCADA被控", "变电站断路器断开", "大面积停电", "泵站断电", "供水中断"],
      "relation_type": "CASCADES_TO",
      "expression": "narrative",
      "amplifies": false,
      "description": "网络攻击→SCADA控制权丧失→变电站跳闸→泵站断电→供水中断"
    }}
  ],
  "amplification_loops": [],
  "impact_statistics": {{
    "impact_population": 225000,
    "MW_lost": 73,
    "recovery_time": 6
  }},
  "metadata": {{
    "event_id": "{event_id}",
    "extraction_date": "{extraction_date}",
    "ontology_version": "2.0",
    "material_type": "M5_event"
  }}
}}
```

注意：
- 时间线必须精确，按时间排序
- amplification_loops记录正反馈环（如果存在）
- 影响统计数据只记录原文明确给出的
- 网络攻击事件需抽取cyber kill chain
- 从叙述中推断隐含依赖关系，但evidence标注为implicit"""

# ============================================================
# 提示词注册表
# ============================================================
PROMPT_REGISTRY = {
    "M1_academic_paper": {
        "material_type": "学术论文",
        "system_prompt": M1_SYSTEM_PROMPT,
        "user_template": M1_USER_TEMPLATE,
        "granularity": "L4-node",
        "relation_explicitness": "R3-formula / R4-probabilistic",
        "attribute_precision": "A4-simulation",
    },
    "M2_report": {
        "material_type": "研究报告",
        "system_prompt": M2_SYSTEM_PROMPT,
        "user_template": M2_USER_TEMPLATE,
        "granularity": "L2-station",
        "relation_explicitness": "R1-qualitative",
        "attribute_precision": "A1-A2",
    },
    "M3_standard": {
        "material_type": "技术标准",
        "system_prompt": M3_SYSTEM_PROMPT,
        "user_template": M3_USER_TEMPLATE,
        "granularity": "L2-station + L3-device",
        "relation_explicitness": "R1-qualitative-requirement",
        "attribute_precision": "A3-rated",
    },
    "M4_emergency_plan": {
        "material_type": "应急预案",
        "system_prompt": M4_SYSTEM_PROMPT,
        "user_template": M4_USER_TEMPLATE,
        "granularity": "L2-station",
        "relation_explicitness": "R2-named",
        "attribute_precision": "A2-semi-quantitative",
    },
    "M5_event": {
        "material_type": "事件案例",
        "system_prompt": M5_SYSTEM_PROMPT,
        "user_template": M5_USER_TEMPLATE,
        "granularity": "L2-station",
        "relation_explicitness": "R0-implicit / R1-narrative",
        "attribute_precision": "A1-qualitative",
    },
}

# 兼容旧接口的别名映射
_ALIAS_MAP = {
    "academic_paper": "M1_academic_paper",
    "technical_report": "M2_report",
    "standard_spec": "M3_standard",
    "emergency_plan": "M4_emergency_plan",
    "news_report": "M5_event",
}

def get_system_prompt(material_type: str) -> str:
    """获取材料类型对应的system prompt"""
    key = _ALIAS_MAP.get(material_type, material_type)
    entry = PROMPT_REGISTRY.get(key)
    if not entry:
        raise ValueError(f"Unknown material type: {material_type}. Valid: {list(PROMPT_REGISTRY.keys())}")
    return entry["system_prompt"]

def get_user_prompt(material_type: str, **kwargs) -> str:
    """获取材料类型对应的user prompt（已填充变量）"""
    key = _ALIAS_MAP.get(material_type, material_type)
    entry = PROMPT_REGISTRY.get(key)
    if not entry:
        raise ValueError(f"Unknown material type: {material_type}. Valid: {list(PROMPT_REGISTRY.keys())}")
    # 注入默认值
    kwargs.setdefault("extraction_date", __import__("time").strftime("%Y-%m-%d"))
    return entry["user_template"].format(**kwargs)

def get_prompt(material_type: str) -> str:
    """兼容旧接口：返回合并的system+user prompt模板（content占位符）"""
    key = _ALIAS_MAP.get(material_type, material_type)
    entry = PROMPT_REGISTRY.get(key)
    if not entry:
        raise ValueError(f"Unknown material type: {material_type}")
    return entry["system_prompt"] + "\n\n## 材料内容\n{content}"

def list_material_types() -> list:
    """返回所有支持的材料类型"""
    return list(PROMPT_REGISTRY.keys())

def get_material_info(material_type: str) -> Dict:
    """获取材料类型的元信息"""
    key = _ALIAS_MAP.get(material_type, material_type)
    entry = PROMPT_REGISTRY.get(key)
    if not entry:
        raise ValueError(f"Unknown material type: {material_type}")
    return {k: v for k, v in entry.items() if k not in ("system_prompt", "user_template")}

if __name__ == "__main__":
    print("=== Extraction Prompts v2.0 ===")
    for mt, info in PROMPT_REGISTRY.items():
        print(f"\n{mt}: {info['material_type']}")
        print(f"  粒度: {info['granularity']}")
        print(f"  关系精度: {info['relation_explicitness']}")
        print(f"  属性精度: {info['attribute_precision']}")
        print(f"  System prompt长度: {len(info['system_prompt'])} chars")
        print(f"  User template长度: {len(info['user_template'])} chars")
