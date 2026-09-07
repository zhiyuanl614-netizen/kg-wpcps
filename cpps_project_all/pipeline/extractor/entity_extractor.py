# -*- coding: utf-8 -*-
"""
v2.0实体抽取器
- 支持v2.0本体约束
- 支持system+user双提示词
- 支持Schema校验+自动修复
- 支持批量抽取+断点续抽
"""

import json, time, logging, re, os
from typing import Optional, Dict, List
from pathlib import Path

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.ontology_v2 import ENTITY_DEFINITIONS, MaterialType, entity_id_format
from config.extraction_prompts import get_system_prompt, get_user_prompt, PROMPT_REGISTRY
from extractor.schema_validator import SchemaValidator

logger = logging.getLogger(__name__)


class EntityExtractor:
    """v2.0实体抽取器"""

    def __init__(self,
                 model_api_url: str = 'YOUR_API_URL',
                 model_name: str = 'S1-Base-Ultra',
                 api_key: str = 'YOUR_API_KEY',
                 max_retries: int = 3,
                 retry_delay: float = 2.0,
                 temperature: float = 0.1,
                 max_tokens: int = 8192,
                 auto_fix: bool = True,
                 validate: bool = True):
        self.model_api_url = model_api_url
        self.model_name = model_name
        self.api_key = api_key
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.auto_fix = auto_fix
        self.validate = validate
        self.validator = SchemaValidator(strict=False)

    def _call_llm(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """调用大模型API"""
        import requests
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        payload = {
            'model': self.model_name,
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
            'response_format': {'type': 'json_object'}
        }
        for attempt in range(self.max_retries):
            try:
                resp = requests.post(
                    self.model_api_url, headers=headers,
                    json=payload, timeout=180
                )
                resp.raise_for_status()
                return resp.json()['choices'][0]['message']['content']
            except Exception as e:
                logger.warning(f'API call failed ({attempt+1}/{self.max_retries}): {e}')
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
        return None

    def _parse_json(self, raw: str) -> Optional[Dict]:
        """解析LLM返回的JSON"""
        if not raw:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # 尝试清理markdown代码块
            cleaned = re.sub(r'```json\s*', '', raw)
            cleaned = re.sub(r'```\s*', '', cleaned).strip()
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                logger.error("Failed to parse LLM output as JSON")
                return None

    def extract(self,
                content: str,
                material_type: str = 'M1_academic_paper',
                material_meta: Optional[Dict] = None) -> Optional[Dict]:
        """
        从单个材料中抽取知识图谱三元组

        Args:
            content: 材料文本内容
            material_type: 材料类型 (M1_academic_paper / M2_report / M3_standard / M4_emergency_plan / M5_event)
            material_meta: 材料元信息 (title, doi, report_id, standard_id, plan_id, event_id等)

        Returns:
            抽取结果Dict，包含entities, relations, metadata等
        """
        # 获取提示词
        system_prompt = get_system_prompt(material_type)

        # 构建user prompt变量
        meta = material_meta or {}
        prompt_vars = {
            "content": content[:60000],  # 防止超长
            "title": meta.get("title", "未知"),
            "extraction_date": time.strftime("%Y-%m-%d"),
        }
        # 根据材料类型注入特定变量
        if material_type == "M1_academic_paper":
            prompt_vars["doi"] = meta.get("doi", "")
            prompt_vars["paper_id"] = meta.get("paper_id", meta.get("doi", "unknown"))
        elif material_type == "M2_report":
            prompt_vars["organization"] = meta.get("organization", "")
            prompt_vars["report_id"] = meta.get("report_id", "unknown")
        elif material_type == "M3_standard":
            prompt_vars["standard_id"] = meta.get("standard_id", "unknown")
        elif material_type == "M4_emergency_plan":
            prompt_vars["region"] = meta.get("region", "")
            prompt_vars["plan_id"] = meta.get("plan_id", "unknown")
        elif material_type == "M5_event":
            prompt_vars["event_date"] = meta.get("event_date", "")
            prompt_vars["event_id"] = meta.get("event_id", "unknown")

        try:
            user_prompt = get_user_prompt(material_type, **prompt_vars)
        except KeyError as e:
            logger.warning(f"Missing template variable: {e}, falling back to simple format")
            user_prompt = f"请从以下内容中抽取知识图谱三元组：\n\n{content[:60000]}"

        # 调用LLM
        raw = self._call_llm(system_prompt, user_prompt)
        if not raw:
            logger.error("LLM returned empty response")
            return None

        # 解析JSON
        result = self._parse_json(raw)
        if not result:
            logger.error("Failed to parse extraction result")
            return None

        # 注入元信息
        result['_meta'] = {
            'material_type': material_type,
            'model': self.model_name,
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'ontology_version': '2.0',
            'content_length': len(content),
        }
        if material_meta:
            result['_meta']['source_meta'] = material_meta

        # 自动修复
        if self.auto_fix:
            result = self.validator.auto_fix_document(result)

        # Schema校验
        if self.validate:
            validation = self.validator.validate_document(result)
            result['_validation'] = validation
            if validation['error_count'] > 0:
                logger.warning(f"Schema validation found {validation['error_count']} errors, {validation['warning_count']} warnings")

        return result

    def batch_extract(self,
                      materials: List[Dict],
                      material_type: str = 'M1_academic_paper',
                      output_dir: str = './extracted',
                      resume: bool = True) -> List[Dict]:
        """
        批量抽取

        Args:
            materials: 材料列表，每个元素为 {"content": str, "meta": dict}
            material_type: 材料类型
            output_dir: 输出目录
            resume: 是否支持断点续抽（跳过已存在的输出文件）

        Returns:
            抽取结果列表
        """
        os.makedirs(output_dir, exist_ok=True)
        results = []
        total = len(materials)

        for idx, mat in enumerate(materials):
            output_file = os.path.join(output_dir, f'extracted_{material_type}_{idx+1:04d}.json')

            # 断点续抽
            if resume and os.path.exists(output_file):
                logger.info(f"[{idx+1}/{total}] Skipping (already exists): {output_file}")
                try:
                    with open(output_file, 'r', encoding='utf-8') as f:
                        existing = json.load(f)
                    results.append(existing)
                    continue
                except Exception:
                    logger.warning(f"Corrupted file, re-extracting: {output_file}")

            logger.info(f"[{idx+1}/{total}] Extracting: {mat.get('meta', {}).get('title', 'N/A')}")

            result = self.extract(
                content=mat['content'],
                material_type=material_type,
                material_meta=mat.get('meta')
            )

            if result:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                results.append(result)
                logger.info(f"[{idx+1}/{total}] Success: {len(result.get('entities', []))} entities, "
                           f"{len(result.get('relations', []))} relations")
            else:
                logger.error(f"[{idx+1}/{total}] Failed to extract")

            # 限速
            time.sleep(1.0)

        # 批量校验汇总
        if self.validate:
            summary = self.validator.validate_directory(output_dir)
            summary_file = os.path.join(output_dir, f'validation_summary_{material_type}.json')
            with open(summary_file, 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            logger.info(f"Batch validation: {summary['total_entities']} entities, "
                       f"{summary['valid_entities']} valid, "
                       f"{summary['total_errors']} errors, "
                       f"{summary['total_warnings']} warnings")

        return results


if __name__ == "__main__":
    # 演示（不调用实际API）
    extractor = EntityExtractor(
        model_api_url='http://localhost:11434/v1/chat/completions',
        model_name='qwen3-embedding:8b',
        api_key='dummy',
        auto_fix=True,
        validate=True,
    )
    print("=== EntityExtractor v2.0 ===")
    print(f"支持材料类型: {list(PROMPT_REGISTRY.keys())}")
    print(f"自动修复: {extractor.auto_fix}")
    print(f"Schema校验: {extractor.validate}")
    print(f"本体实体数: {len(ENTITY_DEFINITIONS)}")
