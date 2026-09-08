"""Paper-facing frontier figures + LaTeX tables from frontier_arms.csv (final mode only).

Pooled per (task, method, margin): return = mean over seeds (error bar = seed std),
violation rate = pooled episodes (error bar = Wilson 95% CI). Hollow marker = soft
channel above the 25/episode budget (Level-2 only). Typed arms within budget are joined by
their Pareto frontier (upper-left hull).

usage: make_paper_fig.py [frontier_arms.csv] [--suite paper|l2|l1|circle|velocity|all] [--outdir DIR]
  paper  -> fig_frontier_paper.{pdf,png}, tab_frontier.tex          (4 hetero tasks, legacy names)
  other  -> fig_frontier_<suite>.{pdf,png}, tab_frontier_<suite>.tex
Panels of tasks without verified arms are drawn empty ("pending") so the layout is stable.
"""
import argparse
import csv
import math
import os
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SOFT_BUDGET = 25.0
SUITES = {
    "paper": [("pg2", "PointGoal2"), ("cg2", "CarGoal2"), ("pp2", "PointPush2"), ("cp2", "CarPush2")],
    "l2": [("pg2", "PointGoal2"), ("cg2", "CarGoal2"), ("pp2", "PointPush2"), ("cp2", "CarPush2"), ("pb2", "PointButton2"), ("cb2", "CarButton2")],
    "l1": [("pg1", "PointGoal1"), ("cg1", "CarGoal1"), ("pp1", "PointPush1"), ("cp1", "CarPush1"), ("pb1", "PointButton1"), ("cb1", "CarButton1")],
    "circle": [("pc1", "PointCircle1"), ("pc2", "PointCircle2"), ("cc1", "CarCircle1"), ("cc2", "CarCircle2")],
    "velocity": [("hcv", "HalfCheetahVelocity"), ("hov", "HopperVelocity"), ("swv", "SwimmerVelocity"), ("wav", "Walker2dVelocity"), ("anv", "AntVelocity"), ("huv", "HumanoidVelocity")],
}
XLABEL = {"paper": "hard-constraint violation rate (% episodes, 95% Wilson CI)",
          "l2": "hard-constraint violation rate (% episodes, 95% Wilson CI)",
          "l1": "episodes with any hazard cost (%, 95% Wilson CI)",
          "circle": "episodes leaving the safe region (%, 95% Wilson CI)",
          "velocity": "episodes exceeding the velocity limit (%, 95% Wilson CI)"}
KNOB_LABEL = {"none": r"$\delta$=0", "0.90": r"$\delta$=.9", "0.80": r"$\delta$=.8", "0.75": r"$\delta$=.75",
              "0.70": r"$\delta$=.7", "0.80g": ".8g", "0.75g": ".75g", "0.70g": ".7g",
              "0.75g/c.05": ".75g,c.05", "0.75g/c.10": ".75g,c.10", "0.80g/c.10": ".8g,c.10", "0.85": r"$\delta$=.85", "0.90g": ".9g", "0.65g": ".65g", "0.70g/c.10": ".7g,c.10",
              "geo.35/.50g": "geo.35", "geo.45/.60g": "geo.45", "state-margin": "sm", "state-margin gated": "smg",
              "coef1": "c=1", "coef5": "c=5", "coef20": "c=20", "lagr": "lim=.1", "lim.02": "lim=.02", "lim.50": "lim=.5", "n/a": "pf=.1", "pf.02": "pf=.02", "pf.50": "pf=.5"}
STYLE = {"SafeOT-typed": dict(marker="o", color="#1f77b4", label="SafeOT-typed (ours)"),
         "FDPI": dict(marker="s", color="#d62728", label="FDPI (constraint-based)"),
         "SAC-Lag": dict(marker="D", color="#c51b8a", label="SAC-Lagrangian (penalty-based)"),
         "SAC-Pen": dict(marker="^", color="#6a51a3", label="SAC + fixed penalty (penalty-based)"),
         "SDAC": dict(marker="v", color="#2ca02c", label="SDAC (multi-constraint SOTA)"),
         "SRCPO": dict(marker="P", color="#17becf", label="SRCPO (multi-constraint SOTA)")}
NAME = {m: m for m in STYLE}


def knob_label(m, mg):
    if mg == "n/a":
        return "pf=.1" if m == "FDPI" else ""
    if mg.startswith("geo"):
        return "geo" + mg[3:].split("/")[0]
    return KNOB_LABEL.get(mg, mg)


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def load_pool(src):
    rows = [r for r in csv.DictReader(open(src)) if r["mode"] == "final" and int(r["ver_eps"]) > 0]
    pool = defaultdict(lambda: {"eps": 0, "hv": 0, "rets": [], "soft": [], "jc": [], "csr": []})
    for r in rows:
        p = pool[(r["task"], r["method"], r["margin"])]
        p["eps"] += int(r["ver_eps"]); p["hv"] += int(r["ver_hv"])
        p["rets"].append(float(r["ver_ret"])); p["soft"].append(float(r["ver_soft"]))
        p["jc"].append(float(r.get("jc") or 0.0)); p["csr"].append(float(r.get("csr25") or 0.0))
    return pool


def stats(p):
    n = len(p["rets"])
    ret = sum(p["rets"]) / n
    sd = math.sqrt(sum((x - ret) ** 2 for x in p["rets"]) / (n - 1)) if n > 1 else 0.0
    rate = p["hv"] / p["eps"]
    lo, hi = wilson(p["hv"], p["eps"])
    soft = sum(p["soft"]) / n
    jc = sum(p["jc"]) / n
    csr = sum(p["csr"]) / n
    return dict(n=n, eps=p["eps"], hv=p["hv"], ret=ret, sd=sd, rate=rate, lo=lo, hi=hi, soft=soft, jc=jc, csr=csr)


def pareto(points):
    """points: list of (rate, ret, key); return upper-left hull sorted by rate."""
    pts = sorted(points, key=lambda t: (t[0], -t[1]))
    hull, best = [], -1e9
    for rate, ret, key in pts:
        if ret > best:
            hull.append((rate, ret, key)); best = ret
    return hull


def draw_panel(ax, task, title, arms, suite, legend_anchor, tex):
    typed_ok = []
    for (t, m, mg), s in sorted(arms.items(), key=lambda kv: kv[1]["rate"]):
        st = STYLE[m]
        x = 100 * s["rate"]; xerr = [[x - 100 * s["lo"]], [100 * s["hi"] - x]]
        over = suite in ("paper", "l2") and s["soft"] > SOFT_BUDGET
        ax.errorbar(x, s["ret"], xerr=xerr, yerr=s["sd"], fmt="none", ecolor=st["color"], elinewidth=0.8, alpha=0.5, capsize=2, zorder=2)
        ax.scatter(x, s["ret"], marker=st["marker"], s=95 if m == "SafeOT-typed" else 80,
                   facecolor="none" if over else st["color"], edgecolor=st["color"] if over else "k",
                   linewidth=1.5 if over else 0.8, zorder=3,
                   label=st["label"] if st["label"] not in ax.get_legend_handles_labels()[1] else None)
        lbl = knob_label(m, mg)
        if lbl:
            ax.annotate(lbl, (x, s["ret"]), textcoords="offset points", xytext=(5, 4), fontsize=7,
                        color="#333333" if not over else "#888888")
        if m == "SafeOT-typed" and not over:
            typed_ok.append((x, s["ret"], mg))
        tex.append((task, m, mg, s))
    hull = pareto(typed_ok)
    if len(hull) > 1:
        ax.plot([h[0] for h in hull], [h[1] for h in hull], "-", color="#1f77b4", lw=1.6, alpha=0.8, zorder=1,
                label="typed Pareto frontier" + (" (soft $\\leq$ 25)" if suite in ("paper", "l2") else "") if legend_anchor else None)
    for meth, ls, lbl in (("SAC-Pen", ":", "SAC-Pen coefficient sweep"), ("FDPI", "--", "FDPI $p_f$ sweep"),
                          ("SAC-Lag", "--", "SAC-Lag cost-limit sweep")):
        pts = sorted([(100 * s["rate"], s["ret"]) for (t, m, mg), s in arms.items() if m == meth])
        if len(pts) > 1:
            ax.plot([p[0] for p in pts], [p[1] for p in pts], ls, color=STYLE[meth]["color"], lw=1.2, alpha=0.8,
                    zorder=1, label=lbl if legend_anchor else None)
    if not arms:
        ax.text(0.5, 0.5, "pending\n(no verified final checkpoints yet)", ha="center", va="center", transform=ax.transAxes, color="#888888", fontsize=9)
    ax.set_xscale("symlog", linthresh=0.3)
    ax.set_xlim(-0.05, 100 if suite in ("l1", "circle", "velocity") else 60)
    ax.set_xlabel(XLABEL[suite], fontsize=8)
    ax.set_ylabel("return")
    ax.set_title(title)
    ax.axvline(0, color="k", lw=0.5, ls=":")
    ax.grid(alpha=0.25, which="both")


def make_suite(suite, pool, outdir):
    tasks = SUITES[suite]
    n = len(tasks)
    ncols = n if n <= 4 else 3
    nrows = math.ceil(n / ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4.4 * nrows), squeeze=False)
    flat = [ax for row in axes for ax in row]
    tex = []
    for i, (ax, (task, title)) in enumerate(zip(flat, tasks)):
        arms = {k: stats(p) for k, p in pool.items() if k[0] == task}
        draw_panel(ax, task, title, arms, suite, legend_anchor=(i == 0), tex=tex)
    for ax in flat[n:]:
        ax.axis("off")
    handles, labels = [], []
    for ax_ in flat[:n]:
        h2, l2 = ax_.get_legend_handles_labels()
        for h, l in zip(h2, l2):
            if l not in labels:
                handles.append(h); labels.append(l)
    fig.legend(handles, labels, loc="lower center", ncol=3, fontsize=8, frameon=False, bbox_to_anchor=(0.5, 0.0))
    sub = "hollow = soft cost > 25/episode" if suite in ("paper", "l2") else "single cost channel; violation = any cost in the episode"
    fig.suptitle("Return vs. violation rate (final checkpoint, 312 episodes/seed; %s)" % sub, fontsize=9.5)
    fig.tight_layout(rect=(0, 0.13 if nrows == 1 else 0.08, 1, 0.95))
    stem = "fig_frontier_paper" if suite == "paper" else "fig_frontier_%s" % suite
    fig.savefig(os.path.join(outdir, stem + ".pdf"))
    fig.savefig(os.path.join(outdir, stem + ".png"), dpi=200)
    plt.close(fig)

    hetero = suite in ("paper", "l2")
    # hetero: episode-level hard violation + soft budget; single-channel: violation + standard J_c and CSR@25
    lines = [r"\begin{tabular}{llrrrrr%s}" % ("c" if hetero else "r"), r"\toprule",
             r"Task & Method (knob) & $n$ & Episodes & Viol.\ (\%) & Return $J_r$" + (r" & Soft cost/ep & Budget \\" if hetero else r" & Cost $J_c$ & CSR@25 \\"), r"\midrule"]
    for task, title in tasks:
        sub_rows = sorted([t for t in tex if t[0] == task], key=lambda t: -t[3]["ret"])
        if not sub_rows:
            lines.append(r"%s & \multicolumn{7}{l}{pending} \\" % title)
        for i, (t, m, mg, s) in enumerate(sub_rows):
            knob = knob_label(m, mg)
            knob = (" (" + knob + ")") if knob else ""
            row = r"%s & %s%s & %d & %d & %.2f [%.2f, %.2f] & %.2f $\pm$ %.2f" % (
                title if i == 0 else "", NAME[m], knob, s["n"], s["eps"], 100 * s["rate"], 100 * s["lo"], 100 * s["hi"], s["ret"], s["sd"])
            if hetero:
                row += r" & %.1f & %s \\" % (s["soft"], r"\checkmark" if s["soft"] <= SOFT_BUDGET else r"$\times$")
            else:
                row += r" & %.2f & %.3f \\" % (s["jc"], s["csr"])
            lines.append(row)
        lines.append(r"\midrule")
    lines[-1] = r"\bottomrule"
    lines.append(r"\end{tabular}")
    tab = "tab_frontier.tex" if suite == "paper" else "tab_frontier_%s.tex" % suite
    open(os.path.join(outdir, tab), "w").write("\n".join(lines) + "\n")
    print("wrote %s.pdf/.png and %s (%d arms)" % (stem, tab, len(tex)))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src", nargs="?", default="frontier_arms.csv")
    ap.add_argument("--suite", default="paper", choices=list(SUITES) + ["all"])
    ap.add_argument("--outdir", default=".")
    a = ap.parse_args()
    pool = load_pool(a.src)
    for s in (list(SUITES) if a.suite == "all" else [a.suite]):
        make_suite(s, pool, a.outdir)
