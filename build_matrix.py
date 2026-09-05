"""Merge plan.json (planned grid) + runs.json (server snapshot) -> matrix.json for the dashboard.
Row = (task, method, knob). Status: planned / training k/n / awaiting-verify / verifying / done(+result) / negative.
"""
import json, sys, time

DATA = sys.argv[1] if len(sys.argv) > 1 else "."
plan = json.load(open(f"{DATA}/plan.json", encoding="utf-8"))
runs = json.load(open(f"{DATA}/runs.json", encoding="utf-8"))["runs"]
by = {}
for r in runs:
    by.setdefault((r["task"], r["variant"]), []).append(r)

rows = []
for p in plan["rows"]:
    rs = []
    for v in p["variants"]:
        rs += by.get((p["task"], v), [])
    seen = {}
    for r in rs:  # one record per seed (v1a/v1b duplicates: keep latest)
        k = r["seed"]
        if k not in seen or r["mtime"] > seen[k]["mtime"]:
            seen[k] = r
    rs = list(seen.values())
    n_plan = p["seeds"]
    n_train = len(rs); n_done = sum(1 for r in rs if r["done"]); n_run = sum(1 for r in rs if r["running"])
    verified = [r for r in rs if r["blocks"] >= 3]
    eps = sum(r["eps"] for r in verified); hvv = sum(r["hv"] for r in verified)
    ret = (sum(r["ret"] for r in verified) / len(verified)) if verified else None
    soft = (sum(r["soft"] for r in verified if r["soft"] is not None) / max(1, sum(1 for r in verified if r["soft"] is not None))) if verified else None
    if n_train == 0:
        status, detail = "planned", "未开始"
    elif n_run > 0:
        status, detail = "training", "训练中 %d 路 (%d/%d 完成)" % (n_run, n_done, n_plan)
    elif n_done < n_plan and len(verified) == n_done:
        status, detail = ("verified_partial", "已验证 %d/%d 种子(缺 %d)" % (len(verified), n_plan, n_plan - len(verified)))
    elif len(verified) < n_done:
        status, detail = "verifying", "终档验证 %d/%d" % (len(verified), n_done)
    else:
        status, detail = "done", "完成 %d 种子 · %d 集" % (len(verified), eps)
    if p.get("negative"):
        status = "negative"
    rows.append({"goal": p["goal"], "task": p["task"], "method": p["method"], "knob": p["knob"], "family": p["family"],
                 "seeds_plan": n_plan, "seeds_done": n_done, "seeds_verified": len(verified), "eps": eps,
                 "rate": (100.0 * hvv / eps) if eps else None, "ret": ret, "soft": soft,
                 "status": status, "detail": detail, "owner": p.get("owner", "agent-A"), "note": p.get("note", ""),
                 "runs": sorted(r["name"] for r in rs)})
out = {"updated": time.strftime("%Y-%m-%dT%H:%M:%S"), "rows": rows,
       "summary": {"total": len(rows), "done": sum(1 for r in rows if r["status"] == "done"),
                   "training": sum(1 for r in rows if r["status"] == "training"), "planned": sum(1 for r in rows if r["status"] == "planned")}}
json.dump(out, open(f"{DATA}/matrix.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("matrix rows=%d done=%d training=%d planned=%d" % (len(rows), out["summary"]["done"], out["summary"]["training"], out["summary"]["planned"]))
