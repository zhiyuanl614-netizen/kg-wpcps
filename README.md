# KG-WPCPS

**城市供水–电力信息物理耦合系统韧性知识图谱**

本项目按 01→06 六个阶段，将 Web of Science 文献转换为可查询、可溯源的 Neo4j 知识图谱，并提供 KG-RAG 问答。

> Neo4j Server 固定使用 **5.26.28**。当前管线使用内置 vector index，不依赖 APOC 或 GDS。

---

## 1. 管线顺序

| 阶段 | 功能 | 主要输出 |
|---|---|---|
| 01 | WoS 解析、去重、筛选、纳入 | `01data_puring/included/` |
| 02 | 文本切分、语义重排、任务生成 | `02text_split/passages/`、`tasks.jsonl` |
| 03 | LLM 实体、关系、级联、测量抽取 | `03llm_extract/triples/` |
| 04 | 实体消歧、关系对齐、单位归一 | `04fusion_align/merged_kg/` |
| 05 | Neo4j 建图、统计、SVG 导出 | Neo4j、`05_kg_build/reports/` |
| 06 | 实体向量索引和 KG-RAG 问答 | `06_kg_rag_qa/cache/` |

必须按顺序运行：

```text
01 → 02 → 03/A_NER → 03/B_RE → 03/C_Cascade → 03/D_Measurement → 04 → 05 → 06
```

---

## 2. 环境要求

- Windows 10/11、Linux、macOS 或 WSL2；
- Python 3.11 或 3.12；
- 内存至少 8 GB，推荐 16 GB；
- 可用磁盘至少 5 GB；
- Docker Desktop / Docker Engine + Compose v2；
- Neo4j Community 5.26.28；
- 新生成、未公开并设置额度的 CSTCloud 或 OpenAI API Key。

下文以 **Windows PowerShell** 为主，所有命令均在项目根目录执行：

```text
D:\HydroPower_Coupling\kg-wpcps
```

Linux/macOS 将 `\` 换成 `/` 即可。

---

## 3. 创建虚拟环境

### Windows PowerShell

```powershell
py -3.11 -m venv myenv
.\myenv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
```

如果 PowerShell 禁止激活：

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\myenv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv myenv
source myenv/bin/activate
python -m pip install --upgrade pip setuptools wheel
```

---

## 4. 安装依赖

建议先安装 CPU 版 PyTorch：

```powershell
python -m pip install --index-url https://download.pytorch.org/whl/cpu torch
python -m pip install -r .\requirements.txt
python -m spacy download en_core_web_sm
```

检查：

```powershell
python -c "import torch, spacy, openai, neo4j, sentence_transformers; print('dependencies OK')"
```

---

## 5. 配置 `runtime.env`

创建配置文件：

```powershell
Copy-Item .\runtime.env.template .\runtime.env -Force
notepad.exe .\runtime.env
```

Windows 不需要执行 `chmod`。确认文件名是 `runtime.env`，不是 `runtime.env.txt`。

### CSTCloud + Neo4j 示例

```dotenv
CSTCLOUD_API_KEY=<填写新生成的Key>
CSTCLOUD_BASE_URL=https://uni-api.cstcloud.cn/v1
CSTCLOUD_CHAT_MODEL=S1-Base-Ultra
CSTCLOUD_EMBEDDING_MODEL=qwen3-embedding:8b
CSTCLOUD_TIMEOUT=300
CSTCLOUD_RPS=2
LLM_SERVICE_CHAT_PROVIDER=cstcloud
LLM_SERVICE_EMBED_PROVIDER=cstcloud

KG_RAG_CHAT_PROVIDER=cstcloud
KG_RAG_EMBED_PROVIDER=cstcloud
KG_RAG_BACKEND=neo4j
KG_EMBEDDING_DIMENSIONS=4096

NEO4J_URI=bolt://127.0.0.1:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=<填写强密码>

HF_HOME=~/.hf
```

注意：

- 不要使用曾经公开过的旧 Key；
- URL 必须直接写成 `https://...`，不能写成 Markdown 链接；
- `runtime.env` 会自动加载，无需执行 `source`；
- 不要提交或发送 `runtime.env`。

---

## 6. 启动 Neo4j 5.26.28

拉取并启动：

```powershell
docker compose --env-file .\runtime.env -f .\05_kg_build\docker-compose.yml pull
docker compose --env-file .\runtime.env -f .\05_kg_build\docker-compose.yml up -d --force-recreate
```

查看状态：

```powershell
docker compose --env-file .\runtime.env -f .\05_kg_build\docker-compose.yml ps -a
```

等待状态变为 `healthy`。

检查版本：

```powershell
docker inspect kguwpcps-neo4j --format '{{.Config.Image}}'
docker exec kguwpcps-neo4j neo4j version
```

必须输出：

```text
neo4j:5.26.28
neo4j 5.26.28
```

查看日志：

```powershell
docker compose --env-file .\runtime.env -f .\05_kg_build\docker-compose.yml logs --tail 100 neo4j
```

浏览器：

```text
http://127.0.0.1:7474
```

---

## 7. 运行预检

```powershell
python .\preflight.py --require-local-nlp --online --neo4j
```

通过时应显示：

```text
[PASS] 在线 chat: valid JSON response
[PASS] 在线 embed: n=1, dim=4096
[PASS] Neo4j 在线连接: version=5.26.28, required=5.26.28
PRECHECK: PASS
```

首次运行时以下警告是正常的，因为 01/02 尚未生成：

```text
[WARN] 01/02 上游产物: {"included": 0, "passages": 0, "tasks": 0}
```

---

# 分步运行 01–06

## 01：文献数据清洗

运行：

```powershell
python .\01data_puring\src\run_all.py
```

流程：

```text
parse → dedup → screen → include → plots
```

主要输出：

```text
01data_puring/parsed/records.jsonl
01data_puring/dedup/records_dedup.jsonl
01data_puring/screened/records_scored.jsonl
01data_puring/included/UWP_*.json
01data_puring/included/manifest.csv
01data_puring/included/prisma_flow.md
01data_puring/reports/
```

预期：约 620 篇纳入文献。

确认：

```powershell
(Get-ChildItem .\01data_puring\included\UWP_*.json).Count
```

---

## 02：文本切分与任务生成

运行：

```powershell
python .\02text_split\src\run_all.py
```

流程：

```text
build_passages → rerank → difficulty → tasks → report
```

主要输出：

```text
02text_split/passages/UWP_*.json
02text_split/tasks.jsonl
02text_split/rerank_scores.csv
02text_split/difficulty_stats.csv
02text_split/reports/
```

预期：

```text
约 620 passages
约 2,226 tasks
约 1,977 个非跳过任务
```

确认上游已经准备好：

```powershell
python .\preflight.py --require-local-nlp --require-upstream --online --neo4j
```

---

## 03：LLM 结构化抽取

03 必须分四步运行。不要直接使用并发 5。

### 03-A：实体识别 A_NER

先测试 5 个任务：

```powershell
python .\03llm_extract\src\bulk_run.py --stages A_NER --workers 1 --batch-size 5 --limit 5
```

查看状态：

```powershell
python .\03llm_extract\src\pipeline.py stats
```

如果 5 个全部成功，再运行全部 A_NER：

```powershell
python .\03llm_extract\src\bulk_run.py --stages A_NER --workers 1 --batch-size 5
```

输出：

```text
03llm_extract/triples/A_NER/
```

### 03-B：受控关系抽取 B_RE

B_RE 依赖 A_NER，必须等待 A_NER 完成：

```powershell
python .\03llm_extract\src\bulk_run.py --stages B_RE --workers 1 --batch-size 5
```

输出：

```text
03llm_extract/triples/B_RE/
```

### 03-C：级联路径抽取 C_Cascade

```powershell
python .\03llm_extract\src\bulk_run.py --stages C_Cascade --workers 2 --batch-size 10
```

输出：

```text
03llm_extract/triples/C_Cascade/
```

### 03-D：数值测量抽取 D_Measurement

```powershell
python .\03llm_extract\src\bulk_run.py --stages D_Measurement --workers 2 --batch-size 10
```

输出：

```text
03llm_extract/triples/D_Measurement/
```

### 查看 03 最终状态

```powershell
python .\03llm_extract\src\pipeline.py commit
python .\03llm_extract\src\pipeline.py stats
```

确认：

```text
exhausted_tasks = 0
A_NER、B_RE、C_Cascade、D_Measurement 均有完成记录
```

`C_Cascade` 或 `D_Measurement` 输出 0 条不一定是错误，可能是原文没有相应内容。

---

## 04：融合与对齐

使用 CSTCloud embedding：

```powershell
python .\04fusion_align\src\run_all.py --embed cstcloud
```

如果不使用向量融合，仅运行规则层：

```powershell
python .\04fusion_align\src\run_all.py --embed none
```

主要输出：

```text
04fusion_align/merged_kg/entities.jsonl
04fusion_align/merged_kg/relations.jsonl
04fusion_align/merged_kg/cascades.jsonl
04fusion_align/merged_kg/measurements.jsonl
04fusion_align/merged_kg/papers.jsonl
04fusion_align/merged_kg/alias_dict.yaml
04fusion_align/reports/
```

确认：

```powershell
Get-ChildItem .\04fusion_align\merged_kg
```

---

## 05：Neo4j 建图

确认 Neo4j healthy：

```powershell
docker compose --env-file .\runtime.env -f .\05_kg_build\docker-compose.yml ps -a
```

建图：

```powershell
python .\05_kg_build\src\run_all.py
```

流程：

```text
schema → papers → entities → relations → cascades → measurements → stats → SVG
```

主要输出：

```text
Neo4j 节点和关系
05_kg_build/reports/graph_stats.md
05_kg_build/viz/subgraph_*.svg
```

浏览器查看：

```text
http://127.0.0.1:7474
```

默认不会清空数据库。只有以下命令会删除目标 database 的全部节点：

```powershell
python .\05_kg_build\src\run_all.py --reset
```

不要对共享或生产数据库使用 `--reset`。

---

## 06：KG-RAG 索引与问答

### 06-A：生成并写入实体向量

Neo4j 后端：

```powershell
python .\06_kg_rag_qa\src\s1_index_entities.py --backend neo4j
```

本地后端：

```powershell
python .\06_kg_rag_qa\src\s1_index_entities.py --backend local
```

输出：

```text
06_kg_rag_qa/cache/embeddings.jsonl
06_kg_rag_qa/cache/index_meta.json
```

### 06-B：只检索上下文

```powershell
python .\06_kg_rag_qa\src\cli.py --context-only "地震如何影响水电耦合系统？"
```

### 06-C：生成完整答案

```powershell
python .\06_kg_rag_qa\src\cli.py --once "地震如何影响水电耦合系统？"
```

### 06-D：交互式问答

```powershell
python .\06_kg_rag_qa\src\cli.py
```

输入 `:q` 退出。

---

## 8. 03 超时恢复

如果 A_NER 出现大量：

```text
Request timed out
```

先按 `Ctrl+C` 停止。成功 cache 已保存，不会丢失。

在 `runtime.env` 中调整：

```dotenv
CSTCLOUD_TIMEOUT=300
CSTCLOUD_RPS=2
```

单并发仍超时时可改为：

```dotenv
CSTCLOUD_TIMEOUT=600
CSTCLOUD_RPS=1
```

提交已有 cache：

```powershell
python .\03llm_extract\src\pipeline.py commit
python .\03llm_extract\src\pipeline.py stats
```

只清除网络超时错误记录：

```powershell
$errDir = ".\03llm_extract\cache\_errors"

if (Test-Path $errDir) {
  Get-ChildItem "$errDir\*.json" | ForEach-Object {
    $record = Get-Content $_.FullName -Raw | ConvertFrom-Json
    if ($record.error -match "timed out|Connection error") {
      Remove-Item $_.FullName
    }
  }
}
```

然后重新执行对应阶段。不要删除：

```text
03llm_extract/cache/_committed.txt
03llm_extract/cache/T_*.json
```

新版会在单批失败率达到 35% 时自动停止，避免连续数小时无效请求。

---

## 9. 断点续跑

每个阶段都可直接重新执行：

- 01/02 会重新生成对应产物；
- 03 会跳过已有成功 cache；
- 04 会重新生成 merged_kg；
- 05 使用 `MERGE` 幂等写入；
- 06 会校验 embedding 维度并更新索引。

如果 03 已完成，可从 04 继续：

```powershell
python .\04fusion_align\src\run_all.py --embed cstcloud
python .\05_kg_build\src\run_all.py
python .\06_kg_rag_qa\src\s1_index_entities.py --backend neo4j
python .\06_kg_rag_qa\src\cli.py --once "地震如何影响水电耦合系统？"
```

---

## 10. 常见问题

### `nano` / `chmod` 无法识别

它们是 Linux 命令。PowerShell 使用：

```powershell
notepad.exe .\runtime.env
```

### Docker `ps` 为空

```powershell
docker version
docker compose --env-file .\runtime.env -f .\05_kg_build\docker-compose.yml up -d --force-recreate
docker compose --env-file .\runtime.env -f .\05_kg_build\docker-compose.yml ps -a
```

### 日志出现 APOC / GDS 错误

说明仍在使用旧版 Compose。当前文件不安装插件。更新后执行：

```powershell
docker compose --env-file .\runtime.env -f .\05_kg_build\docker-compose.yml down
docker compose --env-file .\runtime.env -f .\05_kg_build\docker-compose.yml pull
docker compose --env-file .\runtime.env -f .\05_kg_build\docker-compose.yml up -d --force-recreate
```

### Neo4j 版本不正确

```powershell
docker exec kguwpcps-neo4j neo4j version
```

必须是：

```text
neo4j 5.26.28
```

### API 返回 401 / 403

- Key 已失效、权限不足或额度不足；
- 使用了公开过的旧 Key；
- `runtime.env` 未保存或被写成 `runtime.env.txt`。

### embedding 维度不一致

- local_st：384；
- qwen3-embedding:8b：4096；
- OpenAI text-embedding-3-small：1536。

修改 `KG_EMBEDDING_DIMENSIONS` 后重新运行 06-A。

---

## 11. 停止 Neo4j

停止但保留容器：

```powershell
docker compose --env-file .\runtime.env -f .\05_kg_build\docker-compose.yml stop
```

重新启动：

```powershell
docker compose --env-file .\runtime.env -f .\05_kg_build\docker-compose.yml start
```

删除容器但保留绑定目录数据：

```powershell
docker compose --env-file .\runtime.env -f .\05_kg_build\docker-compose.yml down
```

不要使用 `down -v`，不要随意删除 `05_kg_build/neo4j/data`。

---

## 12. 安全检查

扫描源码是否残留 API Key：

```powershell
python .\llm_service\audit_key_leaks.py .
```

应显示：

```text
未发现 API Key 残留
```

请始终使用新生成、限额、未公开的 API Key。
