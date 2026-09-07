# -*- coding: utf-8 -*-
"""
v2.0 Cypher语句生成器
- 从抽取结果JSON生成Cypher CREATE/MERGE语句
- 支持批量导入格式
- 支持关系约束校验
"""

import json, logging, os
from typing import Dict, List, Optional
from pathlib import Path

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.ontology_v2 import (
    ENTITY_DEFINITIONS, RELATION_DEFINITIONS, ATTRIBUTE_DEFINITIONS,
    validate_relation, Layer
)

logger = logging.getLogger(__name__)


class CypherGenerator:
    """v2.0 Cypher语句生成器"""

    def __init__(self, use_merge: bool = True, add_source_material: bool = True):
        """
        Args:
            use_merge: 使用MERGE而非CREATE（幂等导入）
            add_source_material: 自动添加source_material属性
        """
        self.use_merge = use_merge
        self.add_source_material = add_source_material

    # ============================================================
    # 实体Cypher生成
    # ============================================================
    def entity_to_cypher(self, entity: Dict, material_type: str = "") -> str:
        """将单个实体转换为Cypher CREATE/MERGE语句"""
        eid = entity.get("id", "")
        etype = entity.get("type", "")
        elayer = entity.get("layer", "")
        name_zh = entity.get("name_zh", "")
        attrs = entity.get("attributes", {})

        if not eid or not etype:
            logger.warning(f"Skipping entity with missing id/type: {entity}")
            return ""

        # 构建属性字典
        props = {"id": eid, "layer": elayer}
        if name_zh:
            props["name_zh"] = name_zh

        # 添加本体定义的属性
        if etype in ENTITY_DEFINITIONS:
            valid_attrs = ENTITY_DEFINITIONS[etype].get("attributes", [])
            for attr_key in valid_attrs:
                if attr_key in attrs and attrs[attr_key] is not None:
                    props[attr_key] = attrs[attr_key]

            # 添加其他非标准属性（以_extra_前缀）
            for attr_key, attr_val in attrs.items():
                if attr_key not in valid_attrs and attr_val is not None:
                    props[f"_ext_{attr_key}"] = attr_val

        # 站级别名
        station_alias = ENTITY_DEFINITIONS.get(etype, {}).get("station_alias")
        if station_alias:
            props["station_alias"] = station_alias

        # CyberNode子类型
        if etype == "CyberNode":
            cn_type = attrs.get("type", entity.get("sub_type", ""))
            if cn_type:
                props["type"] = cn_type

        # HazardType使用name而非id
        if etype == "HazardType":
            props = {"name": eid, "layer": elayer}
            if name_zh:
                props["name_zh"] = name_zh
            for attr_key, attr_val in attrs.items():
                if attr_val is not None:
                    props[attr_key] = attr_val

        # 材料来源
        if self.add_source_material and material_type:
            props["source_material"] = material_type

        # 生成Cypher
        op = "MERGE" if self.use_merge else "CREATE"
        props_str = self._format_props(props)
        var_name = eid.replace("-", "_").replace(" ", "_").replace(".", "_")

        return f"{op} ({var_name}:{etype} {props_str})"

    # ============================================================
    # 关系Cypher生成
    # ============================================================
    def relation_to_cypher(self, relation: Dict) -> str:
        """将单个关系转换为Cypher CREATE/MERGE语句"""
        source = relation.get("source", "")
        target = relation.get("target", "")
        rtype = relation.get("type", "")

        if not source or not target or not rtype:
            logger.warning(f"Skipping relation with missing fields: {relation}")
            return ""

        # 检查关系是否在本体中
        if rtype not in RELATION_DEFINITIONS:
            logger.warning(f"Unknown relation type: {rtype}")
            return f"// UNKNOWN RELATION TYPE: {rtype} ({source} -> {target})"

        # 构建关系属性
        rel_props = {}
        if relation.get("explicitness"):
            rel_props["explicitness"] = relation["explicitness"]
        if relation.get("evidence"):
            rel_props["evidence"] = relation["evidence"]
        if relation.get("source_material"):
            rel_props["source_material"] = relation["source_material"]
        if relation.get("mandatory_level"):
            rel_props["mandatory_level"] = relation["mandatory_level"]
        if relation.get("layer_type"):
            rel_props["layer_type"] = relation["layer_type"]

        # 变量名
        src_var = source.replace("-", "_").replace(" ", "_").replace(".", "_")
        tgt_var = target.replace("-", "_").replace(" ", "_").replace(".", "_")

        # MATCH + CREATE/MERGE
        op = "MERGE" if self.use_merge else "CREATE"
        rel_props_str = self._format_props(rel_props) if rel_props else ""

        # 特殊处理HazardType（用name匹配）
        source_type = self._infer_entity_type(source)
        target_type = self._infer_entity_type(target)

        src_match = f"MATCH ({src_var}:{source_type} {{id: '{source}'}})"
        if source_type == "HazardType":
            src_match = f"MATCH ({src_var}:HazardType {{name: '{source}'}})"
        tgt_match = f"MATCH ({tgt_var}:{target_type} {{id: '{target}'}})"
        if target_type == "HazardType":
            tgt_match = f"MATCH ({tgt_var}:HazardType {{name: '{target}'}})"

        return f"{src_match}\n{tgt_match}\n{op} ({src_var})-[:{rtype} {rel_props_str}]->({tgt_var})"

    # ============================================================
    # 文档级Cypher生成
    # ============================================================
    def document_to_cypher(self, doc: Dict, material_type: str = "") -> str:
        """将整个抽取结果文档转换为Cypher脚本"""
        lines = []
        lines.append("// Auto-generated Cypher from extraction result")
        lines.append(f"// Material type: {material_type}")
        lines.append(f"// Ontology version: 2.0")
        lines.append("")

        entities = doc.get("entities", [])
        relations = doc.get("relations", [])

        # 实体
        lines.append("// === Entities ===")
        for e in entities:
            cypher = self.entity_to_cypher(e, material_type)
            if cypher:
                lines.append(cypher)

        lines.append("")

        # 关系
        lines.append("// === Relations ===")
        for r in relations:
            cypher = self.relation_to_cypher(r)
            if cypher:
                lines.append(cypher)
                lines.append("")

        # 级联链路转关系
        cascade_rels = self._extract_cascade_relations(doc)
        if cascade_rels:
            lines.append("// === Cascade Relations ===")
            for r in cascade_rels:
                cypher = self.relation_to_cypher(r)
                if cypher:
                    lines.append(cypher)
                    lines.append("")

        return "\n".join(lines)

    # ============================================================
    # 批量生成
    # ============================================================
    def batch_generate(self, json_dir: str, output_file: str, material_type: str = "") -> int:
        """批量生成Cypher脚本"""
        all_cypher = []
        file_count = 0

        for f in sorted(Path(json_dir).glob("extracted_*.json")):
            with open(f, 'r', encoding='utf-8') as fh:
                doc = json.load(fh)

            mt = material_type or doc.get("_meta", {}).get("material_type", "unknown")
            cypher = self.document_to_cypher(doc, mt)
            all_cypher.append(f"\n// === Source: {f.name} ===\n")
            all_cypher.append(cypher)
            file_count += 1

        # 写入输出文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(all_cypher))

        logger.info(f"Generated Cypher from {file_count} files → {output_file}")
        return file_count

    # ============================================================
    # 辅助方法
    # ============================================================
    def _format_props(self, props: Dict) -> str:
        """格式化属性字典为Cypher属性字符串"""
        items = []
        for k, v in props.items():
            if isinstance(v, str):
                # 转义单引号
                v_escaped = v.replace("'", "\\'")
                items.append(f"{k}: '{v_escaped}'")
            elif isinstance(v, bool):
                items.append(f"{k}: {str(v).lower()}")
            elif isinstance(v, (int, float)):
                items.append(f"{k}: {v}")
            elif v is None:
                continue
            else:
                items.append(f"{k}: '{str(v)}'")
        return "{" + ", ".join(items) + "}"

    def _infer_entity_type(self, entity_id: str) -> str:
        """从实体ID推断实体类型"""
        # 格式: Type-xxx 或 Type_xxx
        if "_" in entity_id:
            prefix = entity_id.split("_")[0]
        elif "-" in entity_id:
            prefix = entity_id.split("-")[0]
        else:
            return "Unknown"

        # 直接匹配
        if prefix in ENTITY_DEFINITIONS:
            return prefix

        # HazardType特殊处理
        if prefix.startswith("HazardType"):
            return "HazardType"

        # 常见前缀映射
        prefix_map = {
            "Bus": "Bus", "Branch": "Branch", "Gen": "Generator",
            "Pump": "Pump", "Node": "Node_Junction", "Pipe": "Pipe_Link",
            "Tank": "Tank", "Valve": "Valve", "SCADA": "SCADA",
            "PLC": "CyberNode", "RTU": "CyberNode", "PMU": "CyberNode",
            "BP": "BackupPower", "HazardType": "HazardType",
        }
        return prefix_map.get(prefix, "Unknown")

    def _extract_cascade_relations(self, doc: Dict) -> List[Dict]:
        """从文档中提取级联链路并转换为关系"""
        relations = []

        for cp in doc.get("cascade_paths", []):
            chain = cp.get("chain", [])
            for i in range(len(chain) - 1):
                relations.append({
                    "source": chain[i],
                    "target": chain[i + 1],
                    "type": "CASCADES_TO",
                    "explicitness": cp.get("expression", "model"),
                    "evidence": cp.get("description", ""),
                })

        for cc in doc.get("cascade_chains", []):
            chain = cc.get("chain", [])
            for i in range(len(chain) - 1):
                relations.append({
                    "source": chain[i],
                    "target": chain[i + 1],
                    "type": "CASCADES_TO",
                    "explicitness": "narrative",
                    "evidence": cc.get("description", ""),
                })

        return relations


if __name__ == "__main__":
    gen = CypherGenerator(use_merge=True, add_source_material=True)

    # 测试实体Cypher生成
    test_entities = [
        {"id": "Bus-5", "type": "Bus", "layer": "power", "name_zh": "5号母线",
         "attributes": {"voltage_level_kV": 110, "bus_load": 0.85}},
        {"id": "Pump-3", "type": "Pump", "layer": "water", "name_zh": "3号水泵",
         "attributes": {"pump_power": 350, "pump_head": 45}},
        {"id": "HazardType_earthquake", "type": "HazardType", "layer": "hazard",
         "name_zh": "地震", "attributes": {"hazard_category": "natural"}},
    ]

    print("=== 实体Cypher ===")
    for e in test_entities:
        print(gen.entity_to_cypher(e, "M1_academic_paper"))
        print()

    # 测试关系Cypher生成
    test_rels = [
        {"source": "Pump-3", "target": "Bus-5", "type": "POWERED_BY",
         "explicitness": "R3-formula", "evidence": "Table 3"},
        {"source": "HazardType_earthquake", "target": "Bus-5", "type": "TRIGGERS",
         "explicitness": "R4-probabilistic", "evidence": "EQ model"},
    ]

    print("=== 关系Cypher ===")
    for r in test_rels:
        print(gen.relation_to_cypher(r))
        print()

    # 测试文档级生成
    test_doc = {
        "entities": test_entities,
        "relations": test_rels,
        "cascade_paths": [
            {"chain": ["Bus-5", "Pump-3", "Node-12"], "expression": "model",
             "description": "Bus-5 fault → Pump-3 loss → Node-12 pressure drop"}
        ]
    }

    print("=== 文档Cypher ===")
    print(gen.document_to_cypher(test_doc, "M1_academic_paper"))
