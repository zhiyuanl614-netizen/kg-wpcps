# -*- coding: utf-8 -*-
"""
v2.0本体Schema校验器
校验抽取结果是否符合本体约束：实体类型、关系域/范围、属性归属、必填字段
"""

import json
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.ontology_v2 import (
    ENTITY_DEFINITIONS, RELATION_DEFINITIONS, ATTRIBUTE_DEFINITIONS,
    Layer, MaterialType, validate_relation, get_entity_attributes,
    CYBERNODE_SUBTYPE_MAP, ALL_MAPPING
)

logger = logging.getLogger(__name__)


class SchemaValidator:
    """v2.0本体Schema校验器"""

    def __init__(self, strict: bool = False):
        """
        Args:
            strict: 严格模式下，任何校验失败都抛异常；非严格模式仅记录警告
        """
        self.strict = strict
        self.errors: List[Dict] = []
        self.warnings: List[Dict] = []

    def reset(self):
        self.errors = []
        self.warnings = []

    def _add_error(self, category: str, entity_id: str, message: str):
        entry = {"category": category, "entity_id": entity_id, "message": message}
        self.errors.append(entry)
        if self.strict:
            raise ValueError(f"[Schema Error] {category}: {entity_id} - {message}")

    def _add_warning(self, category: str, entity_id: str, message: str):
        entry = {"category": category, "entity_id": entity_id, "message": message}
        self.warnings.append(entry)
        logger.warning(f"[Schema Warning] {category}: {entity_id} - {message}")

    # ============================================================
    # 实体校验
    # ============================================================
    def validate_entity(self, entity: Dict) -> bool:
        """校验单个实体是否符合v2.0本体"""
        eid = entity.get("id", "UNKNOWN")
        etype = entity.get("type", "")
        elayer = entity.get("layer", "")
        valid = True

        # 1. 必填字段
        for field in ["id", "type", "layer"]:
            if field not in entity or not entity[field]:
                self._add_error("missing_field", eid, f"Entity missing required field: {field}")
                valid = False

        if not valid:
            return False

        # 2. 实体类型是否在本体中
        if etype not in ENTITY_DEFINITIONS:
            # 尝试映射
            mapped = ALL_MAPPING.get(etype)
            if mapped:
                self._add_warning("entity_type_mapping", eid,
                                  f"Entity type '{etype}' not in v2.0 ontology, should be mapped to '{mapped}'")
            else:
                self._add_error("unknown_entity_type", eid,
                                f"Entity type '{etype}' not in v2.0 ontology and no mapping found")
                valid = False

        # 3. 层级是否匹配
        if etype in ENTITY_DEFINITIONS:
            expected_layer = ENTITY_DEFINITIONS[etype]["layer"].value
            if elayer != expected_layer:
                self._add_error("layer_mismatch", eid,
                                f"Entity {etype} layer should be '{expected_layer}', got '{elayer}'")
                valid = False

        # 4. 属性校验
        attrs = entity.get("attributes", {})
        if etype in ENTITY_DEFINITIONS:
            valid_attrs = get_entity_attributes(etype)
            for attr_key in attrs:
                if attr_key not in valid_attrs and attr_key not in ATTRIBUTE_DEFINITIONS:
                    self._add_warning("unknown_attribute", eid,
                                      f"Attribute '{attr_key}' not defined for entity type '{etype}'")

        # 5. CyberNode子类型校验
        if etype == "CyberNode":
            cn_type = attrs.get("type", entity.get("sub_type", ""))
            if cn_type and cn_type not in ENTITY_DEFINITIONS["CyberNode"].get("sub_types", []):
                self._add_warning("invalid_cybernode_subtype", eid,
                                  f"CyberNode sub_type '{cn_type}' not in allowed list")

        return valid

    # ============================================================
    # 关系校验
    # ============================================================
    def validate_relation(self, relation: Dict, entity_index: Optional[Dict] = None) -> bool:
        """校验单个关系是否符合v2.0本体"""
        source = relation.get("source", "UNKNOWN")
        target = relation.get("target", "UNKNOWN")
        rtype = relation.get("type", "")
        valid = True

        # 1. 必填字段
        for field in ["source", "target", "type"]:
            if field not in relation or not relation[field]:
                self._add_error("missing_field", f"{source}->{target}", f"Relation missing required field: {field}")
                valid = False

        if not valid:
            return False

        # 2. 关系类型是否在本体中
        if rtype not in RELATION_DEFINITIONS:
            self._add_error("unknown_relation_type", f"{source}->{target}",
                            f"Relation type '{rtype}' not in v2.0 ontology")
            return False

        # 3. 域/范围约束校验（需要实体索引）
        if entity_index:
            source_type = entity_index.get(source, {}).get("type")
            target_type = entity_index.get(target, {}).get("type")
            if source_type and target_type:
                ok, msg = validate_relation(rtype, source_type, target_type)
                if not ok:
                    self._add_warning("relation_constraint_violation", f"{source}->{target}", msg)
                    # 不设为error，因为跨材料合并时可能需要宽松校验

        # 4. evidence字段
        if "evidence" not in relation or not relation["evidence"]:
            self._add_warning("missing_evidence", f"{source}->{target}",
                              f"Relation {rtype} missing evidence field")

        return valid

    # ============================================================
    # 整体文档校验
    # ============================================================
    def validate_document(self, doc: Dict) -> Dict:
        """校验整个抽取结果文档"""
        self.reset()

        entities = doc.get("entities", [])
        relations = doc.get("relations", [])

        # 构建实体索引
        entity_index = {e.get("id"): e for e in entities if e.get("id")}

        # 校验实体
        entity_valid_count = 0
        for e in entities:
            if self.validate_entity(e):
                entity_valid_count += 1

        # 校验关系
        relation_valid_count = 0
        for r in relations:
            if self.validate_relation(r, entity_index):
                relation_valid_count += 1

        # 校验metadata
        metadata = doc.get("metadata", {})
        if "ontology_version" not in metadata:
            self._add_warning("missing_metadata", "DOCUMENT", "Missing ontology_version in metadata")
        if "material_type" not in metadata:
            self._add_warning("missing_metadata", "DOCUMENT", "Missing material_type in metadata")

        # 统计
        result = {
            "total_entities": len(entities),
            "valid_entities": entity_valid_count,
            "total_relations": len(relations),
            "valid_relations": relation_valid_count,
            "errors": self.errors,
            "warnings": self.warnings,
            "error_count": len(self.errors),
            "warning_count": len(self.warnings),
            "is_valid": len(self.errors) == 0,
        }

        return result

    # ============================================================
    # 批量校验
    # ============================================================
    def validate_directory(self, json_dir: str) -> Dict:
        """批量校验目录下所有抽取结果JSON"""
        all_results = []
        for f in sorted(Path(json_dir).glob("extracted_*.json")):
            with open(f, 'r', encoding='utf-8') as fh:
                doc = json.load(fh)
            result = self.validate_document(doc)
            result["file"] = str(f)
            all_results.append(result)

        # 汇总
        summary = {
            "total_files": len(all_results),
            "total_entities": sum(r["total_entities"] for r in all_results),
            "valid_entities": sum(r["valid_entities"] for r in all_results),
            "total_relations": sum(r["total_relations"] for r in all_results),
            "valid_relations": sum(r["valid_relations"] for r in all_results),
            "total_errors": sum(r["error_count"] for r in all_results),
            "total_warnings": sum(r["warning_count"] for r in all_results),
            "all_valid": all(r["is_valid"] for r in all_results),
            "details": all_results,
        }
        return summary

    # ============================================================
    # 自动修复（非严格模式）
    # ============================================================
    def auto_fix_entity(self, entity: Dict) -> Dict:
        """尝试自动修复实体"""
        etype = entity.get("type", "")

        # 映射行业术语到本体标准实体
        if etype not in ENTITY_DEFINITIONS:
            mapped = ALL_MAPPING.get(etype)
            if mapped:
                entity["type_original"] = etype
                entity["type"] = mapped
                entity["layer"] = ENTITY_DEFINITIONS[mapped]["layer"].value
                logger.info(f"Auto-mapped entity type: {etype} → {mapped}")

        # 修正层级
        etype = entity.get("type", "")
        if etype in ENTITY_DEFINITIONS:
            expected = ENTITY_DEFINITIONS[etype]["layer"].value
            if entity.get("layer") != expected:
                entity["layer_original"] = entity.get("layer")
                entity["layer"] = expected
                logger.info(f"Auto-fixed layer for {entity.get('id')}: {entity.get('layer_original')} → {expected}")

        # CyberNode子类型处理
        if etype == "CyberNode" and "sub_type" in entity:
            entity.setdefault("attributes", {})
            entity["attributes"]["type"] = entity.pop("sub_type")

        return entity

    def auto_fix_document(self, doc: Dict) -> Dict:
        """自动修复整个文档"""
        entities = doc.get("entities", [])
        doc["entities"] = [self.auto_fix_entity(e) for e in entities]
        doc["_auto_fixed"] = True
        return doc


if __name__ == "__main__":
    # 测试
    validator = SchemaValidator(strict=False)

    # 测试实体校验
    test_entity_ok = {"id": "Bus-5", "type": "Bus", "layer": "power", "attributes": {"voltage_level_kV": 110}}
    test_entity_bad_type = {"id": "Sub-1", "type": "Substation", "layer": "power", "attributes": {}}
    test_entity_bad_layer = {"id": "Pump-3", "type": "Pump", "layer": "cyber", "attributes": {}}

    print("=== 实体校验测试 ===")
    print(f"合法实体: {validator.validate_entity(test_entity_ok)}")
    print(f"行业术语实体: {validator.validate_entity(test_entity_bad_type)}")
    print(f"层级错误实体: {validator.validate_entity(test_entity_bad_layer)}")

    # 测试自动修复
    print("\n=== 自动修复测试 ===")
    fixed = validator.auto_fix_entity(test_entity_bad_type.copy())
    print(f"修复后: type={fixed.get('type')}, layer={fixed.get('layer')}")

    # 测试关系校验
    print("\n=== 关系校验测试 ===")
    entity_index = {"Pump-3": {"type": "Pump"}, "Bus-5": {"type": "Bus"}}
    test_rel_ok = {"source": "Pump-3", "target": "Bus-5", "type": "POWERED_BY", "evidence": "Table 3"}
    test_rel_bad = {"source": "Bus-5", "target": "Pump-3", "type": "POWERED_BY", "evidence": "wrong direction"}
    print(f"合法关系: {validator.validate_relation(test_rel_ok, entity_index)}")
    print(f"方向错误: {validator.validate_relation(test_rel_bad, entity_index)}")

    # 测试文档校验
    print("\n=== 文档校验测试 ===")
    test_doc = {
        "entities": [test_entity_ok, test_entity_bad_type],
        "relations": [test_rel_ok],
        "metadata": {"ontology_version": "2.0", "material_type": "M1_academic_paper"}
    }
    result = validator.validate_document(test_doc)
    print(f"总实体: {result['total_entities']}, 合法: {result['valid_entities']}")
    print(f"总关系: {result['total_relations']}, 合法: {result['valid_relations']}")
    print(f"错误: {result['error_count']}, 警告: {result['warning_count']}")
    print(f"文档合法: {result['is_valid']}")
