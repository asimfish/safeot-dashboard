"""Per-suite significance table from the merged frontier_arms.csv.

For every task in a suite, two SafeOT-typed arms are compared against FDPI (pf=.1) and SAC-Lag (lim=.1):
  * "safest"  - the typed arm with the lowest episode-level violation rate (ties -> higher return)
  * "top"     - the typed arm with the highest return
Violation rates: one-sided Fisher exact test on pooled episodes (H1: typed rate < baseline rate).
Returns: Welch t-test on per-seed mean returns (n=3 per arm; seed is the replication unit), two-sided p
plus the sign of the difference. Nothing is selected by hand: the two typed arms follow the fixed rule above.

usage: suite_stats.py frontier_arms.csv --suite l1|l2|circle|velocity|paper|all --outdir DIR
writes tab_stats_<suite>.tex and stats_<suite>.json (all arms with >= 312 verified episodes per seed).
"""
import argparse
import json
import math
import os
import sys

from scipy import stats as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_paper_fig import SUITES, knob_label, load_pool  # noqa: E402

BASELINES = (("FDPI", "n/a", "FDPI"), ("SAC-Lag", "lagr", "SAC-Lag"))


def arm_stats(p):
    rets = p["rets"]
    return dict(n=len(rets), eps=p["eps"], hv=p["hv"], rate=100.0 * p["hv"] / p["eps"],
                ret=sum(rets) / len(rets), sd=(st.tstd(rets) if len(rets) > 1 else 0.0), rets=rets)


def fisher_less(a, b):
    return float(st.fisher_exact([[a["hv"], a["eps"] - a["hv"]], [b["hv"], b["eps"] - b["hv"]]], alternative="less").pvalue)


def welch(a, b):
    if len(a["rets"]) < 2 or len(b["rets"]) < 2:
        return float("nan")
    return float(st.ttest_ind(a["rets"], b["rets"], equal_var=False).pvalue)


def fmt_p(p):
    if p != p:
        return "--"
    return "$<$0.001" if p < 0.001 else "%.3f" % p


def suite_table(suite, pool):
    tasks = SUITES[suite]
    lines = [r"\begin{tabular}{llrrrrrr}", r"\toprule",
             r"Task & Typed arm & Viol.\ (\%) & Return & $p$ viol.\ $<$ FDPI & $p$ ret.\ vs FDPI & $p$ viol.\ $<$ Lag & $p$ ret.\ vs Lag \\",
             r"\midrule"]
    report = {}
    for t, name in tasks:
        arms = {(m, mg): arm_stats(p) for (tk, m, mg), p in pool.items() if tk == t}
        typed = {mg: a for (m, mg), a in arms.items() if m == "SafeOT-typed"}
        base = {tag: arms.get((m, mg)) for m, mg, tag in BASELINES}
        if not typed or base["FDPI"] is None:
            lines.append(r"%s & \multicolumn{7}{l}{pending} \\" % name)
            continue
        safest_mg = min(typed, key=lambda mg: (typed[mg]["rate"], -typed[mg]["ret"]))
        top_mg = max(typed, key=lambda mg: typed[mg]["ret"])
        picks = [("safest", safest_mg)] + ([("top", top_mg)] if top_mg != safest_mg else [])
        rep = {}
        first = True
        for tag, mg in picks:
            a = typed[mg]
            row = dict(knob=mg, tag=tag, rate=a["rate"], ret=a["ret"], sd=a["sd"], n=a["n"], eps=a["eps"], hv=a["hv"])
            cells = []
            for btag in ("FDPI", "SAC-Lag"):
                b = base[btag]
                if b is None:
                    row["p_viol_vs_" + btag] = None; row["p_ret_vs_" + btag] = None; cells += ["--", "--"]
                    continue
                pv, pr = fisher_less(a, b), welch(a, b)
                sign = "+" if a["ret"] > b["ret"] else "-"
                row["p_viol_vs_" + btag] = pv; row["p_ret_vs_" + btag] = pr; row["ret_sign_vs_" + btag] = sign
                cells += [fmt_p(pv), (fmt_p(pr) + " (%s)" % sign) if pr == pr else "--"]
            rep[tag] = row
            lines.append(r"%s & %s (%s) & %.2f & %.2f $\pm$ %.2f & %s \\" % (
                name if first else "", knob_label("SafeOT-typed", mg), tag, a["rate"], a["ret"], a["sd"], " & ".join(cells)))
            first = False
        for btag in ("FDPI", "SAC-Lag"):
            b = base[btag]
            if b is not None:
                lines.append(r" & %s & %.2f & %.2f $\pm$ %.2f & \multicolumn{4}{l}{baseline, $n$=%d, %d episodes} \\" % (
                    btag + (" (pf=.1)" if btag == "FDPI" else " (lim=.1)"), b["rate"], b["ret"], b["sd"], b["n"], b["eps"]))
                rep[btag] = dict(rate=b["rate"], ret=b["ret"], sd=b["sd"], n=b["n"], eps=b["eps"], hv=b["hv"])
        report[t] = rep
        lines.append(r"\midrule")
    if lines[-1] == r"\midrule":
        lines[-1] = r"\bottomrule"
    else:
        lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    return "\n".join(lines) + "\n", report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("--suite", default="all")
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--min-eps", type=int, default=312)
    a = ap.parse_args()
    pool = load_pool(a.src, a.min_eps)
    os.makedirs(a.outdir, exist_ok=True)
    suites = list(SUITES) if a.suite == "all" else [a.suite]
    for s in suites:
        tex, rep = suite_table(s, pool)
        open(os.path.join(a.outdir, "tab_stats_%s.tex" % s), "w").write(tex)
        json.dump(rep, open(os.path.join(a.outdir, "stats_%s.json" % s), "w"), indent=1)
        for t, r in rep.items():
            for tag in ("safest", "top"):
                if tag in r:
                    x = r[tag]
                    print("%-8s %-4s %-6s knob=%-14s rate=%6.2f%% ret=%9.2f | vsFDPI p_viol=%s p_ret=%s%s | vsLag p_viol=%s p_ret=%s%s" % (
                        s, t, tag, x["knob"], x["rate"], x["ret"], fmt_p(x["p_viol_vs_FDPI"] if x["p_viol_vs_FDPI"] is not None else float("nan")),
                        fmt_p(x["p_ret_vs_FDPI"] if x["p_ret_vs_FDPI"] is not None else float("nan")), x.get("ret_sign_vs_FDPI", ""),
                        fmt_p(x["p_viol_vs_SAC-Lag"] if x["p_viol_vs_SAC-Lag"] is not None else float("nan")),
                        fmt_p(x["p_ret_vs_SAC-Lag"] if x["p_ret_vs_SAC-Lag"] is not None else float("nan")), x.get("ret_sign_vs_SAC-Lag", "")))
    print("wrote", ", ".join("tab_stats_%s.tex" % s for s in suites), "to", a.outdir)


if __name__ == "__main__":
    main()
