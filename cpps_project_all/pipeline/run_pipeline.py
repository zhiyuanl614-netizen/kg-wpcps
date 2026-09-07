# -*- coding: utf-8 -*-
"""
Water-Power CPS Knowledge Graph Pipeline — v2.0
端到端流水线入口

用法:
  python run_pipeline.py extract --material_type M1_academic_paper --input_dir ./raw_data --output_dir ./extracted
  python run_pipeline.py validate --input_dir ./extracted
  python run_pipeline.py generate_cypher --input_dir ./extracted --output_file ./import.cypher
  python run_pipeline.py import_neo4j --input_dir ./extracted --uri bolt://localhost:7687
  python run_pipeline.py full --material_type M1_academic_paper --input_dir ./raw_data --output_dir ./extracted
"""

import argparse
import json
import logging
import os
import sys
import time

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.ontology_v2 import ENTITY_DEFINITIONS, RELATION_DEFINITIONS, STATISTICS
from config.extraction_prompts import PROMPT_REGISTRY, list_material_types
from extractor.schema_validator import SchemaValidator
from extractor.entity_extractor import EntityExtractor
from extractor.relation_extractor import RelationExtractor
from graph_builder.cypher_generator import CypherGenerator
from graph_builder.neo4j_importer import Neo4jImporter

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger("pipeline")


def cmd_extract(args):
    """执行知识抽取"""
    extractor = EntityExtractor(
        model_api_url=args.api_url,
        model_name=args.model,
        api_key=args.api_key,
        auto_fix=True,
        validate=True,
    )

    # 加载材料
    materials = []
    input_dir = args.input_dir
    for f in sorted(os.listdir(input_dir)):
        if f.endswith('.json'):
            with open(os.path.join(input_dir, f), 'r', encoding='utf-8') as fh:
                data = json.load(fh)
            if isinstance(data, list):
                materials.extend(data)
            else:
                materials.append(data)
        elif f.endswith('.txt') or f.endswith('.md'):
            with open(os.path.join(input_dir, f), 'r', encoding='utf-8') as fh:
                content = fh.read()
            materials.append({"content": content, "meta": {"title": f}})

    logger.info(f"Loaded {len(materials)} materials from {input_dir}")

    # 批量抽取
    results = extractor.batch_extract(
        materials=materials,
        material_type=args.material_type,
        output_dir=args.output_dir,
        resume=True,
    )

    logger.info(f"Extraction complete: {len(results)} results")


def cmd_validate(args):
    """校验抽取结果"""
    validator = SchemaValidator(strict=False)
    summary = validator.validate_directory(args.input_dir)

    print(f"\n=== Validation Summary ===")
    print(f"Files: {summary['total_files']}")
    print(f"Entities: {summary['valid_entities']}/{summary['total_entities']} valid")
    print(f"Relations: {summary['valid_relations']}/{summary['total_relations']} valid")
    print(f"Errors: {summary['total_errors']}")
    print(f"Warnings: {summary['total_warnings']}")
    print(f"All valid: {summary['all_valid']}")

    # 保存汇总
    output_file = os.path.join(args.input_dir, 'validation_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    logger.info(f"Validation summary saved to {output_file}")


def cmd_generate_cypher(args):
    """生成Cypher导入脚本"""
    gen = CypherGenerator(use_merge=True, add_source_material=True)
    file_count = gen.batch_generate(
        json_dir=args.input_dir,
        output_file=args.output_file,
    )
    logger.info(f"Generated Cypher from {file_count} files → {args.output_file}")


def cmd_import_neo4j(args):
    """导入Neo4j"""
    importer = Neo4jImporter(
        uri=args.uri,
        user=args.user,
        password=args.password,
        database=args.database,
    )

    if not importer.is_connected():
        logger.error("Cannot connect to Neo4j")
        return

    # 初始化Schema
    logger.info("Initializing schema...")
    importer.init_schema()

    # 导入数据
    logger.info("Importing extracted data...")
    total_e, total_r = importer.import_extracted(args.input_dir)

    # 验证
    node_counts = importer.count_nodes()
    rel_counts = importer.count_relationships()

    print(f"\n=== Import Summary ===")
    print(f"Entities imported: {total_e}")
    print(f"Relationships imported: {total_r}")
    print(f"\nNode counts by label:")
    for label, count in sorted(node_counts.items()):
        if count > 0:
            print(f"  {label}: {count}")
    print(f"\nRelationship counts by type:")
    for rtype, count in sorted(rel_counts.items()):
        if count > 0:
            print(f"  {rtype}: {count}")

    importer.close()


def cmd_info(args):
    """显示本体和Pipeline信息"""
    print("=" * 60)
    print("Water-Power CPS Knowledge Graph Pipeline v2.0")
    print("=" * 60)
    print(f"\n--- Ontology Statistics ---")
    print(f"Entities: {STATISTICS['entities']}")
    print(f"Relations: {STATISTICS['relations']}")
    print(f"Attributes: {STATISTICS['attributes']}")
    print(f"\n--- Layer Architecture ---")
    for layer, entities in STATISTICS['layers'].items():
        print(f"  {layer}: {', '.join(entities)}")
    print(f"\n--- Cross-layer Relations ---")
    print(f"  {', '.join(STATISTICS['cross_layer_relations'])}")
    print(f"\n--- Cyber-Physical Relations ---")
    print(f"  {', '.join(STATISTICS['cyber_physical_relations'])}")
    print(f"\n--- Supported Material Types ---")
    for mt, info in PROMPT_REGISTRY.items():
        print(f"  {mt}: {info['material_type']} (粒度={info['granularity']}, 关系精度={info['relation_explicitness']})")
    print(f"\n--- Pipeline Modules ---")
    print(f"  config/ontology_v2.py — 本体定义")
    print(f"  config/extraction_prompts.py — 抽取提示词")
    print(f"  extractor/entity_extractor.py — 实体抽取器")
    print(f"  extractor/relation_extractor.py — 关系抽取器")
    print(f"  extractor/schema_validator.py — Schema校验器")
    print(f"  graph_builder/cypher_generator.py — Cypher生成器")
    print(f"  graph_builder/neo4j_importer.py — Neo4j导入器")
    print(f"  graph_builder/neo4j_schema_v2.cypher — Schema脚本")


def main():
    parser = argparse.ArgumentParser(description='Water-Power CPS KG Pipeline v2.0')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # extract
    p_extract = subparsers.add_parser('extract', help='Extract knowledge from materials')
    p_extract.add_argument('--material_type', default='M1_academic_paper', choices=list_material_types())
    p_extract.add_argument('--input_dir', required=True)
    p_extract.add_argument('--output_dir', default='./extracted')
    p_extract.add_argument('--api_url', default='YOUR_API_URL')
    p_extract.add_argument('--model', default='S1-Base-Ultra')
    p_extract.add_argument('--api_key', default='YOUR_API_KEY')

    # validate
    p_validate = subparsers.add_parser('validate', help='Validate extraction results')
    p_validate.add_argument('--input_dir', required=True)

    # generate_cypher
    p_cypher = subparsers.add_parser('generate_cypher', help='Generate Cypher import script')
    p_cypher.add_argument('--input_dir', required=True)
    p_cypher.add_argument('--output_file', default='./import.cypher')

    # import_neo4j
    p_import = subparsers.add_parser('import_neo4j', help='Import to Neo4j')
    p_import.add_argument('--input_dir', required=True)
    p_import.add_argument('--uri', default='bolt://localhost:7687')
    p_import.add_argument('--user', default='neo4j')
    p_import.add_argument('--password', default='YOUR_PASSWORD')
    p_import.add_argument('--database', default='neo4j')

    # info
    subparsers.add_parser('info', help='Show pipeline info')

    args = parser.parse_args()

    if args.command == 'extract':
        cmd_extract(args)
    elif args.command == 'validate':
        cmd_validate(args)
    elif args.command == 'generate_cypher':
        cmd_generate_cypher(args)
    elif args.command == 'import_neo4j':
        cmd_import_neo4j(args)
    elif args.command == 'info':
        cmd_info(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
