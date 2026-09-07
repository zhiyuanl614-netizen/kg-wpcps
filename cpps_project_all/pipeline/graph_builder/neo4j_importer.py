# -*- coding: utf-8 -*-
"""
v2.0 Neo4j导入器
- 支持v2.0本体标签和关系类型
- 支持从抽取结果JSON直接导入
- 支持Cypher脚本文件执行
- 支持批量导入+进度追踪
- 支持Schema初始化
"""

import json, os, logging, time
from typing import Dict, List, Optional, Tuple
from pathlib import Path

import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.ontology_v2 import ENTITY_DEFINITIONS, RELATION_DEFINITIONS
from graph_builder.cypher_generator import CypherGenerator

logger = logging.getLogger(__name__)


class Neo4jImporter:
    """v2.0 Neo4j导入器"""

    def __init__(self,
                 uri: str = 'bolt://localhost:7687',
                 user: str = 'neo4j',
                 password: str = 'YOUR_PASSWORD',
                 database: str = 'neo4j'):
        try:
            from neo4j import GraphDatabase
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
            self.database = database
            self._connected = True
            logger.info(f"Connected to Neo4j at {uri}")
        except ImportError:
            logger.warning("neo4j driver not installed. Install with: pip install neo4j")
            self.driver = None
            self._connected = False
        except Exception as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            self.driver = None
            self._connected = False

        self.cypher_gen = CypherGenerator(use_merge=True, add_source_material=True)

    def close(self):
        if self.driver:
            self.driver.close()

    def is_connected(self) -> bool:
        return self._connected

    # ============================================================
    # Schema初始化
    # ============================================================
    def init_schema(self, cypher_file: Optional[str] = None) -> bool:
        """初始化Neo4j Schema（约束+索引）"""
        if not self._connected:
            logger.error("Not connected to Neo4j")
            return False

        if cypher_file is None:
            # 使用默认v2.0 Schema
            cypher_file = os.path.join(os.path.dirname(__file__), 'neo4j_schema_v2.cypher')

        if not os.path.exists(cypher_file):
            logger.error(f"Schema file not found: {cypher_file}")
            return False

        return self.run_cypher_file(cypher_file, skip_data=True)

    # ============================================================
    # 从JSON目录导入
    # ============================================================
    def import_extracted(self, json_dir: str, batch_size: int = 100) -> Tuple[int, int]:
        """
        从抽取结果JSON目录批量导入到Neo4j

        Returns:
            (total_entities, total_relations)
        """
        if not self._connected:
            logger.error("Not connected to Neo4j")
            return 0, 0

        files = sorted(Path(json_dir).glob('extracted_*.json'))
        total_entities = 0
        total_rels = 0

        for f in files:
            logger.info(f"Importing: {f.name}")
            with open(f, 'r', encoding='utf-8') as fh:
                data = json.load(fh)

            material_type = data.get("_meta", {}).get("material_type", "unknown")

            # 导入实体
            entities = data.get('entities', [])
            e_count = self._import_entities(entities, material_type, batch_size)
            total_entities += e_count

            # 导入关系
            rels = data.get('relations', [])
            r_count = self._import_relations(rels, batch_size)
            total_rels += r_count

            # 导入级联关系
            cascade_rels = self.cypher_gen._extract_cascade_relations(data)
            if cascade_rels:
                c_count = self._import_relations(cascade_rels, batch_size)
                total_rels += c_count

            logger.info(f"  Imported: {e_count} entities, {r_count + len(cascade_rels)} relations")

        logger.info(f"Import complete: {total_entities} entities, {total_rels} relationships from {len(files)} files")
        return total_entities, total_rels

    def _import_entities(self, entities: List[Dict], material_type: str, batch_size: int = 100) -> int:
        """批量导入实体"""
        count = 0
        with self.driver.session(database=self.database) as session:
            for i in range(0, len(entities), batch_size):
                batch = entities[i:i + batch_size]
                cypher_batch = []
                for e in batch:
                    c = self.cypher_gen.entity_to_cypher(e, material_type)
                    if c:
                        cypher_batch.append(c)

                if cypher_batch:
                    query = "\n".join(cypher_batch)
                    try:
                        session.run(query)
                        count += len(cypher_batch)
                    except Exception as ex:
                        logger.error(f"Entity batch import failed: {ex}")
                        # 逐条重试
                        for c in cypher_batch:
                            try:
                                session.run(c)
                                count += 1
                            except Exception as ex2:
                                logger.error(f"Single entity import failed: {ex2}")

        return count

    def _import_relations(self, relations: List[Dict], batch_size: int = 50) -> int:
        """批量导入关系"""
        count = 0
        with self.driver.session(database=self.database) as session:
            for i in range(0, len(relations), batch_size):
                batch = relations[i:i + batch_size]
                for r in batch:
                    cypher = self.cypher_gen.relation_to_cypher(r)
                    if cypher:
                        try:
                            session.run(cypher)
                            count += 1
                        except Exception as ex:
                            logger.error(f"Relation import failed: {ex}\n  Cypher: {cypher[:200]}")

        return count

    # ============================================================
    # Cypher脚本执行
    # ============================================================
    def run_cypher_file(self, cypher_path: str, skip_data: bool = False) -> bool:
        """
        执行Cypher脚本文件

        Args:
            cypher_path: Cypher文件路径
            skip_data: 是否跳过数据创建语句（仅执行Schema定义）
        """
        if not self._connected:
            logger.error("Not connected to Neo4j")
            return False

        with open(cypher_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 按分号分割语句
        statements = []
        for stmt in content.split(';'):
            stmt = stmt.strip()
            if not stmt or stmt.startswith('//'):
                continue
            # 跳过数据创建（以CREATE (开头的非约束语句）
            if skip_data and stmt.startswith('CREATE (') and 'CONSTRAINT' not in stmt:
                continue
            statements.append(stmt)

        success = 0
        failed = 0
        with self.driver.session(database=self.database) as session:
            for stmt in statements:
                try:
                    session.run(stmt)
                    success += 1
                except Exception as e:
                    failed += 1
                    logger.warning(f"Cypher execution failed: {stmt[:100]}... Error: {e}")

        logger.info(f"Cypher file executed: {success} success, {failed} failed")
        return failed == 0

    # ============================================================
    # 查询辅助
    # ============================================================
    def count_nodes(self) -> Dict[str, int]:
        """统计各标签节点数"""
        if not self._connected:
            return {}

        result = {}
        with self.driver.session(database=self.database) as session:
            for label in ENTITY_DEFINITIONS:
                try:
                    count = session.run(f"MATCH (n:{label}) RETURN count(n) AS cnt").single()["cnt"]
                    result[label] = count
                except Exception:
                    result[label] = 0

        return result

    def count_relationships(self) -> Dict[str, int]:
        """统计各关系类型数"""
        if not self._connected:
            return {}

        result = {}
        with self.driver.session(database=self.database) as session:
            for rtype in RELATION_DEFINITIONS:
                try:
                    count = session.run(
                        f"MATCH ()-[r:{rtype}]->() RETURN count(r) AS cnt"
                    ).single()["cnt"]
                    result[rtype] = count
                except Exception:
                    result[rtype] = 0

        return result

    def verify_schema(self) -> Dict:
        """验证Schema是否正确创建"""
        if not self._connected:
            return {"connected": False}

        with self.driver.session(database=self.database) as session:
            constraints = list(session.run("SHOW CONSTRAINTS"))
            indexes = list(session.run("SHOW INDEXES"))

        return {
            "connected": True,
            "constraint_count": len(constraints),
            "index_count": len(indexes),
            "constraints": [dict(c) for c in constraints],
        }


if __name__ == "__main__":
    importer = Neo4jImporter(
        uri='bolt://localhost:7687',
        user='neo4j',
        password='YOUR_PASSWORD'
    )
    print("=== Neo4jImporter v2.0 ===")
    print(f"Connected: {importer.is_connected()}")
    print(f"Cypher Generator: {type(importer.cypher_gen).__name__}")
    print(f"Entity types: {len(ENTITY_DEFINITIONS)}")
    print(f"Relation types: {len(RELATION_DEFINITIONS)}")

    if importer.is_connected():
        print(f"\nNode counts: {importer.count_nodes()}")
        print(f"Relationship counts: {importer.count_relationships()}")
    else:
        print("\n(Not connected to Neo4j - skipping live queries)")
