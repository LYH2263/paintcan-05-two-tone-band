import json, sqlite3
from datetime import datetime, timezone
def insert(conn, kind, payload, result, room_id=None):
    now = datetime.now(timezone.utc).isoformat()
    cur = conn.execute("INSERT INTO calc_runs(kind,room_id,input_json,result_json,created_at) VALUES (?,?,?,?,?)",
        (kind, room_id, json.dumps(payload, ensure_ascii=False), json.dumps(result, ensure_ascii=False), now))
    conn.commit(); return int(cur.lastrowid)
def list_recent(conn, limit=50):
    rows = [dict(r) for r in conn.execute("SELECT * FROM calc_runs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()]
    for r in rows:
        # 钉选快照：历史展示只读库存 JSON，旧条不随后续参数修改变化
        r["input"] = json.loads(r["input_json"]) if r.get("input_json") else None
        r["result"] = json.loads(r["result_json"]) if r.get("result_json") else None
    return rows
