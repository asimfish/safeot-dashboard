#!/bin/bash
# Collect SafeOT dashboard snapshots (30109 + aliyun) and push to the `data` branch.
# Usage: update_dashboard.sh [--no-server]
set -u
DATA=~/Code/safeot-dashboard-data
TOOLS=~/Code/safeot-dashboard
SRC=/Users/liyufeng/Desktop/research/safeot/goal34_prep_20260811
R1=tianyiyun-30109; RLOGS=/home/dataset-local/liyufeng/goal34_prep/logs
R2=ali_ppu
R3=volc-a100
LOG=$TOOLS/update.log
ts() { date "+%m-%d %H:%M:%S"; }
cd "$DATA" || exit 1
LOCK="$DATA/.update.lock.d"
if ! mkdir "$LOCK" 2>/dev/null; then
  if [ -n "$(find "$LOCK" -maxdepth 0 -mmin +20 2>/dev/null)" ]; then rmdir "$LOCK" 2>/dev/null; mkdir "$LOCK" 2>/dev/null || exit 0; else echo "$(ts) another update running, skip" >> "$LOG"; exit 0; fi
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT
git pull -q --rebase origin data >/dev/null 2>&1 || git rebase --abort >/dev/null 2>&1
if [ "${1:-}" != "--no-server" ]; then
  if timeout 120 ssh -o BatchMode=yes -o ConnectTimeout=20 $R1 "cd /home/dataset-local/liyufeng/goal34_prep/sota_h2h && python3 collect_dashboard.py" >/dev/null 2>&1; then
    timeout 60 scp -q $R1:$RLOGS/dash_runs.json runs.json 2>/dev/null
    timeout 60 scp -q $R1:$RLOGS/dash_frontier.json frontier_pooled.json 2>/dev/null
    timeout 60 scp -q $R1:$RLOGS/frontier_arms.csv frontier_arms.csv 2>/dev/null
    echo "$(ts) 30109 snapshot ok" >> "$LOG"
  else
    echo "$(ts) 30109 unreachable, keeping old runs.json" >> "$LOG"
  fi
  if timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=20 $R2 "python3 /mnt/data/safeot_vla_m1/collect_gpu.py" > aliyun_gpu.json.tmp 2>/dev/null && [ -s aliyun_gpu.json.tmp ]; then
    mv aliyun_gpu.json.tmp aliyun_gpu.json; echo "$(ts) aliyun snapshot ok" >> "$LOG"
  else
    rm -f aliyun_gpu.json.tmp; echo "$(ts) aliyun unreachable" >> "$LOG"
  fi
  if timeout 120 ssh -o BatchMode=yes -o ConnectTimeout=20 $R3 "cd /home/dataset-local/liyufeng/goal34_prep/sota_h2h && python3 collect_dashboard.py" >/dev/null 2>&1; then
    timeout 60 scp -q $R3:/home/dataset-local/liyufeng/goal34_prep/logs/dash_runs.json volc_runs.json 2>/dev/null && echo "$(ts) volc runs ok" >> "$LOG"
    timeout 90 ssh -o BatchMode=yes -o ConnectTimeout=20 $R3 "cd /home/dataset-local/liyufeng/goal34_prep/sota_h2h && python3 make_frontier_csv.py" >/dev/null 2>&1
    timeout 60 scp -q $R3:/home/dataset-local/liyufeng/goal34_prep/logs/frontier_arms.csv volc_arms.csv 2>/dev/null
  fi
  if timeout 60 ssh -o BatchMode=yes -o ConnectTimeout=20 $R3 "python3 ~/research_storage/safeot/tools/collect_gpu.py" > volc_gpu.json.tmp 2>/dev/null && [ -s volc_gpu.json.tmp ]; then
    mv volc_gpu.json.tmp volc_gpu.json; echo "$(ts) volc snapshot ok" >> "$LOG"
  else
    rm -f volc_gpu.json.tmp; echo "$(ts) volc unreachable" >> "$LOG"
  fi
  python3 - <<'PY'
import json, os, time
r = json.load(open("runs.json"))
srv = [s for s in r.get("servers", []) if s.get("name") not in ("aliyun-ppu", "volc-a100")]
if os.path.exists("volc_gpu.json"):
    v = json.load(open("volc_gpu.json"))
    v.update({"name": "volc-a100", "desc": "2x A100-80G, 128 核, 3PB vepfs; SafeRL 第二算力(DP/ACT 训练共用 GPU); 环境部署中",
              "snap_time": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(os.path.getmtime("volc_gpu.json")))})
    srv.append(v)
if os.path.exists("aliyun_gpu.json"):
    a = json.load(open("aliyun_gpu.json"))
    a.update({"name": "aliyun-ppu", "desc": "16x PPU-ZW810E 96G, 184 核; VLA(Safety-CHORES)评测; 共享(act_train 等他人任务)",
              "snap_time": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(os.path.getmtime("aliyun_gpu.json")))})
    srv.append(a)
r["servers"] = srv
# merge volc runs (tag server; dedupe by name, prefer more ckpts)
for x in r.get("runs", []):
    x.setdefault("server", "30109")
if os.path.exists("volc_runs.json"):
    vr = json.load(open("volc_runs.json"))
    have = {x["name"]: x for x in r["runs"]}
    for x in vr.get("runs", []):
        if x["variant"] in ("sdac", "srcpo"):
            continue
        x["server"] = "volc"
        if x["name"] not in have or x["ckpts"] > have[x["name"]]["ckpts"]:
            have[x["name"]] = x
    r["runs"] = list(have.values())
    r["lanes"] = r.get("lanes", []) + ["volc: " + l for l in vr.get("lanes", [])]
json.dump(r, open("runs.json", "w"), ensure_ascii=False, indent=1)
PY
  python3 - <<'PY2'
import csv, os, json
rows = {}
for f in ("frontier_arms.csv", "volc_arms.csv"):
    if not os.path.exists(f): continue
    for r in csv.DictReader(open(f)):
        if f == "volc_arms.csv" and r["method"] in ("FDPI", "SDAC", "SRCPO") and r["task"] != "pp2": continue  # 30109 已有
        k = (r["task"], r["method"], r["margin"], r["seed"], r["mode"])
        if k not in rows or int(r["ver_eps"]) > int(rows[k]["ver_eps"]): rows[k] = r
if rows:
    cols = list(next(iter(rows.values())).keys())
    with open("frontier_arms.csv", "w") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); [w.writerow(r) for r in rows.values()]
    # pooled json for the dashboard table
    pool = {}
    for r in rows.values():
        if r["mode"] != "final" or int(r["ver_eps"]) == 0: continue
        k = (r["task"], r["method"], r["margin"]); p = pool.setdefault(k, {"n": 0, "eps": 0, "hv": 0, "ret": [], "soft": []})
        p["n"] += 1; p["eps"] += int(r["ver_eps"]); p["hv"] += int(r["ver_hv"]); p["ret"].append(float(r["ver_ret"])); p["soft"].append(float(r["ver_soft"]))
    out = [{"task": t, "method": m, "knob": mg, "n": p["n"], "eps": p["eps"], "rate": 100.0 * p["hv"] / p["eps"], "ret": sum(p["ret"]) / p["n"], "soft": sum(p["soft"]) / p["n"]} for (t, m, mg), p in pool.items()]
    out.sort(key=lambda x: (x["task"], -x["ret"]))
    import time; json.dump({"updated": time.strftime("%Y-%m-%dT%H:%M:%S"), "rows": out}, open("frontier_pooled.json", "w"), ensure_ascii=False, indent=1)
PY2
  python3 "$TOOLS/build_matrix.py" "$DATA" >/dev/null 2>&1 || echo "$(ts) build_matrix failed" >> "$LOG"
fi
[ -f "$SRC/fig_frontier_paper.png" ] && cp "$SRC/fig_frontier_paper.png" .
python3 -c "import json;[json.load(open(f)) for f in ('status.json','runs.json','matrix.json','plan.json')]" 2>/dev/null || { echo "$(ts) invalid json, abort" >> "$LOG"; exit 1; }
git add -A >/dev/null 2>&1
if git diff --cached --quiet; then echo "$(ts) no change" >> "$LOG"; exit 0; fi
git commit -q -m "data: $(date '+%Y-%m-%d %H:%M')" && (git push -q origin data 2>>"$LOG" || (git pull -q --rebase origin data && git push -q origin data 2>>"$LOG")) && echo "$(ts) pushed" >> "$LOG"
