from pathlib import Path
import duckdb
import json

FRAGMENTS = Path("C:/real_memory_system/fragments")
AGENT_LOG = FRAGMENTS / "answers.jsonl"
AGENT_QUEUE = Path("C:/real_memory_system/tools/tasks/agent_queue.json")
OCR_DIR = FRAGMENTS / "media/ocr"


def query_sources(query, source_type):
    if source_type == "sql":
        return query_sql_memory(query)
    elif source_type == "unstructured":
        return query_unstructured_chunks(query)
    elif source_type == "agent":
        return query_agent_outputs(query)
    elif source_type == "log":
        return query_logs(query)
    elif source_type == "ocr":
        return query_ocr_fragments(query)
    return []


def query_sql_memory(query):
    conn = duckdb.connect(str(FRAGMENTS / "cat_memory.duckdb"))
    conn.execute("SET memory_limit='4GB'")
    rows = conn.execute("SELECT content FROM fragments WHERE content ILIKE ? LIMIT 10", ('%' + query + '%',)).fetchall()
    return [r[0] for r in rows]


def query_unstructured_chunks(query):
    results = []
    for file in (FRAGMENTS / "text").glob("*.txt"):
        if query.lower() in file.read_text(encoding="utf-8").lower():
            results.append(file.read_text(encoding="utf-8"))
    return results


def query_agent_outputs(query):
    if AGENT_QUEUE.exists():
        data = json.loads(AGENT_QUEUE.read_text())
        return [json.dumps(entry) for entry in data if query.lower() in json.dumps(entry).lower()]
    return []


def query_logs(query):
    results = []
    if AGENT_LOG.exists():
        with AGENT_LOG.open("r", encoding="utf-8") as f:
            for line in f:
                if query.lower() in line.lower():
                    results.append(line.strip())
    return results


def query_ocr_fragments(query):
    results = []
    for file in OCR_DIR.glob("*.txt"):
        if query.lower() in file.read_text(encoding="utf-8").lower():
            results.append(file.read_text(encoding="utf-8"))
    return results
