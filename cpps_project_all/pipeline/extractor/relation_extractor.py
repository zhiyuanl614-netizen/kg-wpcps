# -*- coding: utf-8 -*-
"""
v2.0关系抽取器
- 从已抽取的实体结果中进一步抽取/校验关系
- 支持域/范围约束校验
- 支持级联链路提取与规范化
- 支持跨材料关系合并
"""

import json, logging, os
from typing import Dict, List, Optional, Tuple, Set
from collections import defaultdict

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.ontology_v2 import (
    RELATION_DEFINITIONS, ENTITY_DEFINITIONS, validate_relation,
    Layer, MaterialType
)
from extractor.schema_validator import SchemaValidator

logger = logging.getLogger(__name__)


class RelationExtractor:
    """v2.0关系抽取与规范化器"""

    def __init__(self, strict: bool = False):
        self.strict = strict
        self.validator = SchemaValidator(strict=strict)

    # ============================================================
    # 关系规范化
    # ============================================================
    def normalize_relation(self, relation: Dict, entity_index: Dict) -> Dict:
        """
        规范化关系：
        1. 校验域/范围约束
        2. 自动修正方向（如POWERED_BY方向错误）
        3. 补充缺失字段
        """
        source = relation.get("source", "")
        target = relation.get("target", "")
        rtype = relation.get("type", "")

        # 查找实体类型
        source_entity = entity_index.get(source, {})
        target_entity = entity_index.get(target, {})
        source_type = source_entity.get("type", "")
        target_type = target_entity.get("type", "")

        # 校验关系约束
        ok, msg = validate_relation(rtype, source_type, target_type)

        if not ok and source_type and target_type:
            # 尝试反向（如POWERED_BY方向写反）
            ok_rev, msg_rev = validate_relation(rtype, target_type, source_type)
            if ok_rev:
                logger.info(f"Auto-reversing relation: {source}({source_type})-{rtype}->{target}({target_type}) "
                           f"→ {target}({target_type})-{rtype}->{source}({source_type})")
                relation["source"] = target
                relation["target"] = source
                relation["_auto_reversed"] = True
            else:
                if self.strict:
                    raise ValueError(f"Relation constraint violation: {msg}")
                else:
                    relation["_constraint_warning"] = msg

        # 补充字段
        relation.setdefault("explicitness", "R1-qualitative")
        relation.setdefault("evidence", "")

        return relation

    # ============================================================
    # 级联链路提取
    # ============================================================
    def extract_cascade_chains(self, doc: Dict) -> List[Dict]:
        """
        从文档中提取级联链路，规范化为CASCADES_TO关系序列

        支持多种输入格式：
        - cascade_paths (M1论文)
        - cascade_narratives (M2报告)
        - cascade_chains (M4预案/M5事件)
        """
        chains = []

        # M1: cascade_paths
        for cp in doc.get("cascade_paths", []):
            chain = cp.get("chain", [])
            if len(chain) >= 2:
                chains.append({
                    "chain": chain,
                    "relation_type": "CASCADES_TO",
                    "expression": cp.get("expression", "model"),
                    "description": cp.get("description", ""),
                })

        # M2: cascade_narratives
        for cn in doc.get("cascade_narratives", []):
            chain = cn.get("chain", [])
            if len(chain) >= 2:
                chains.append({
                    "chain": chain,
                    "relation_type": "CASCADES_TO",
                    "expression": "narrative",
                    "description": cn.get("description", ""),
                })

        # M4/M5: cascade_chains
        for cc in doc.get("cascade_chains", []):
            chain = cc.get("chain", [])
            if len(chain) >= 2:
                chains.append({
                    "chain": chain,
                    "relation_type": "CASCADES_TO",
                    "expression": cc.get("expression", "narrative"),
                    "description": cc.get("description", ""),
                    "trigger": cc.get("trigger", ""),
                    "response_level": cc.get("response_level", ""),
                    "amplifies": cc.get("amplifies", False),
                })

        return chains

    def cascade_chains_to_relations(self, chains: List[Dict], entity_index: Dict) -> List[Dict]:
        """
        将级联链路转换为CASCADES_TO关系对

        例如: ["Bus-5", "Pump-3", "Node-12"]
        → [CASCADES_TO(Bus-5→Pump-3), CASCADES_TO(Pump-3→Node-12)]
        """
        relations = []
        for chain_data in chains:
            chain = chain_data.get("chain", [])
            for i in range(len(chain) - 1):
                source = chain[i]
                target = chain[i + 1]

                # 尝试匹配实体索引
                source_type = entity_index.get(source, {}).get("type", "")
                target_type = entity_index.get(target, {}).get("type", "")

                rel = {
                    "source": source,
                    "target": target,
                    "type": "CASCADES_TO",
                    "explicitness": "R1-narrative",
                    "evidence": chain_data.get("description", ""),
                    "chain_index": i,
                    "chain_length": len(chain),
                }

                # 如果是AMPLIFIES正反馈环
                if chain_data.get("amplifies"):
                    rel["amplifies"] = True

                relations.append(rel)

        return relations

    # ============================================================
    # 跨材料关系合并
    # ============================================================
    def merge_relations(self,
                        relation_lists: List[List[Dict]],
                        dedup_strategy: str = "strict") -> List[Dict]:
        """
        合并多个来源的关系列表，去重

        Args:
            relation_lists: 多个关系列表
            dedup_strategy: 
                - "strict": source+target+type完全相同才去重
                - "loose": source+type相同即视为重复（保留evidence最多的）
        """
        merged = []
        seen = set()

        for rels in relation_lists:
            for r in rels:
                source = r.get("source", "")
                target = r.get("target", "")
                rtype = r.get("type", "")

                if dedup_strategy == "strict":
                    key = (source, target, rtype)
                else:
                    key = (source, rtype)

                if key not in seen:
                    seen.add(key)
                    merged.append(r)
                else:
                    # 合并evidence
                    for existing in merged:
                        e_key = (existing.get("source"), existing.get("target"), existing.get("type"))
                        if dedup_strategy == "strict" and e_key == key:
                            if r.get("evidence") and r["evidence"] not in existing.get("evidence", ""):
                                existing["evidence"] = (existing.get("evidence", "") + "; " + r["evidence"]).strip("; ")
                            break
                        elif dedup_strategy == "loose" and (existing.get("source"), existing.get("type")) == key:
                            if r.get("evidence") and r["evidence"] not in existing.get("evidence", ""):
                                existing["evidence"] = (existing.get("evidence", "") + "; " + r["evidence"]).strip("; ")
                            break

        return merged

    # ============================================================
    # 关系统计
    # ============================================================
    def relation_statistics(self, relations: List[Dict]) -> Dict:
        """统计关系分布"""
        stats = defaultdict(int)
        domain_stats = defaultdict(int)
        layer_stats = defaultdict(int)

        for r in relations:
            rtype = r.get("type", "UNKNOWN")
            stats[rtype] += 1

            # 域统计
            source = r.get("source", "")
            if "_" in source:
                domain_stats[source.split("_")[0]] += 1
            elif "-" in source:
                domain_stats[source.split("-")[0]] += 1

        # 层级统计
        for r in relations:
            rtype = r.get("type", "")
            if rtype in RELATION_DEFINITIONS:
                layer = RELATION_DEFINITIONS[rtype].get("layer", "unknown")
                layer_stats[layer] += 1

        return {
            "total": len(relations),
            "by_type": dict(stats),
            "by_source_prefix": dict(domain_stats),
            "by_layer": dict(layer_stats),
            "anchor_relations": sum(1 for r in relations
                                   if r.get("type") in ["POWERED_BY", "CASCADES_TO"]),
        }


if __name__ == "__main__":
    re = RelationExtractor(strict=False)

    # 测试级联链路提取
    test_doc = {
        "cascade_paths": [
            {"chain": ["Bus-5", "Pump-3", "Node-12"], "expression": "model",
             "description": "Bus-5 fault → Pump-3 power loss → Node-12 pressure drop"}
        ],
        "cascade_narratives": [
            {"chain": ["极端高温", "朝阳变电站过载", "城北泵站断电"],
             "description": "高温导致变电站过载跳闸，泵站断电"}
        ],
    }

    chains = re.extract_cascade_chains(test_doc)
    print(f"提取级联链路: {len(chains)} 条")
    for c in chains:
        print(f"  {' → '.join(c['chain'])}")

    # 测试级联链路转关系
    entity_index = {
        "Bus-5": {"type": "Bus"},
        "Pump-3": {"type": "Pump"},
        "Node-12": {"type": "Node_Junction"},
    }
    rels = re.cascade_chains_to_relations(chains[:1], entity_index)
    print(f"\n级联关系: {len(rels)} 条")
    for r in rels:
        print(f"  {r['source']} -[{r['type']}]-> {r['target']}")

    # 测试关系统计
    all_rels = [
        {"source": "Pump-3", "target": "Bus-5", "type": "POWERED_BY"},
        {"source": "Bus-5", "target": "Pump-3", "type": "CASCADES_TO"},
        {"source": "HazardType_earthquake", "target": "Bus-5", "type": "TRIGGERS"},
        {"source": "SCADA-1", "target": "Pump-3", "type": "CONTROLS"},
    ]
    stats = re.relation_statistics(all_rels)
    print(f"\n关系统计: {json.dumps(stats, indent=2, ensure_ascii=False)}")
