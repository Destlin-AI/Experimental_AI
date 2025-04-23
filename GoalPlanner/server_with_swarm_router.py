from flask import Flask, request, jsonify
from swarm_router import route_prompt
import duckdb
import os

app = Flask(__name__)
DB_PATH = os.path.join("C:/real_memory_system", "memory.duckdb")

@app.route("/api/fragments/current")
def current_fragments():
    try:
        con = duckdb.connect(DB_PATH)
        rows = con.execute("""
            SELECT id, claim, sub_category, tags, timestamp, filepath, content
            FROM fragments ORDER BY timestamp DESC LIMIT 30
        """).fetchall()
        con.close()
        return jsonify([{
            "id": r[0], "claim": r[1], "sub_category": r[2], "tags": r[3],
            "timestamp": r[4].isoformat(), "filepath": r[5], "content": r[6] or ""
        } for r in rows])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/chat", methods=["POST"])
def chat():
    prompt = request.json.get("prompt", "")
    response = route_prompt(prompt)
    return {"response": response}