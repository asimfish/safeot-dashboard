"""Intent mock for Figure 1 (teaser, candidate B): v16 three-column diagram, sharpened, plus a real-data payoff strip.
Writes teaser_mock.tex (standalone TikZ/pgfplots, same preamble/palette as the drawing agent's v16 Figure1.tex).
Data: W2's figure3c_alltask_aggregate.csv (median across tasks of seed-mean cost/B; SafePO 10 tasks, Bullet 6)."""
import csv, os

HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, "figure3c_alltask_aggregate.csv"))))


def series(suite, method):
    pts = [(float(r["progress_pct"]), float(r["cost_over_budget_median"])) for r in rows
           if r["suite"] == suite and r["method"] == method]
    return sorted(pts)


def coords(pts):
    return " ".join(f"({x:g},{y:.3f})" for x, y in pts)


def area_above_one(pts):
    # polygon between max(y,1) and 1, so only the budget excess is shaded
    top = [(x, max(y, 1.0)) for x, y in pts]
    return coords(top + [(pts[-1][0], 1.0), (pts[0][0], 1.0)])


def strip_axis(suite, x0, title, ymax, ytick, note):
    s = series(suite, "SafeOT-Dual")
    t = series(suite, "TRPO-Lag")
    return rf"""
\begin{{axis}}[at={{({x0}bp,-201bp)}},anchor=south west,width=128bp,height=44bp,scale only axis,
  xmin=0,xmax=100,ymin=0,ymax={ymax},xtick={{0,50,100}},ytick={{{ytick}}},
  axis lines=left,axis line style={{ink!70,line width=.5bp}},tick style={{ink!70,line width=.4bp}},
  tick label style={{font=\ticks}},label style={{font=\ticks}},
  xticklabels={{0,,100\,\%}},
  clip=true]
\addplot[draw=none,fill=lag,fill opacity=.22] coordinates {{{area_above_one(t)}}} -- cycle;
\addplot[draw=none,fill=ours,fill opacity=.30] coordinates {{{area_above_one(s)}}} -- cycle;
\addplot[ink!60,dashed,line width=.5bp] coordinates {{(0,1) (100,1)}};
\addplot[lag,line width=.9bp,densely dotted] coordinates {{{coords(t)}}};
\addplot[ours,line width=1.1bp] coordinates {{{coords(s)}}};
\end{{axis}}
\node[anchor=north west,font=\bodyfont\bfseries] at ({x0 + 18}bp,{-201 + 44 + 1}bp) {{{title}}};

\node[anchor=west,align=left,font=\bodyfont] at ({x0 + 134}bp,{-201 + 24}bp) {{{note}}};
"""


tex = r"""\documentclass[border=0bp]{standalone}
\usepackage{newtxtext,newtxmath}
\usepackage{tikz,pgfplots}
\pgfplotsset{compat=1.17}
\usetikzlibrary{arrows.meta,calc}
\definecolor{teal}{HTML}{167C80}
\definecolor{orange}{HTML}{D55E00}
\definecolor{ours}{HTML}{0072B2}
\definecolor{blue}{HTML}{0072B2}
\definecolor{lag}{HTML}{A0467E}
\definecolor{gray}{HTML}{59636A}
\definecolor{ink}{HTML}{23343B}
\definecolor{hard}{HTML}{C43C39}
\definecolor{cost}{HTML}{E69F00}
\newcommand{\bodyfont}{\fontsize{7.5}{8.5}\selectfont}
\newcommand{\ticks}{\fontsize{7}{7.5}\selectfont}
\newcommand{\titlefont}{\fontsize{8.8}{9.6}\selectfont\bfseries}
\newcommand{\mathfont}{\fontsize{8.6}{9.6}\selectfont}
\tikzset{
  every node/.style={font=\bodyfont,text=ink,inner sep=0pt,outer sep=0pt},
  module/.style={rounded corners=3bp,line width=.6bp},
  flow/.style={line width=.8bp,-{Stealth[length=3.5bp,width=3bp]}},
  title/.style={font=\titlefont},
  formula/.style={font=\mathfont},
  chip/.style={rounded corners=2bp,inner xsep=3bp,inner ysep=1.6bp}
}
\begin{document}
\begin{tikzpicture}[x=1bp,y=-1bp]
\path[use as bounding box] (0,0) rectangle (396,212);

% ---------------- columns (same scaffold as v16) ----------------
\draw[module,draw=gray!55,fill=gray!3] (3,3) rectangle (107,137);
\draw[module,draw=gray!55,fill=gray!3] (294,3) rectangle (393,137);
\draw[module,draw=teal,fill=teal!4] (114,3) rectangle (287,73);
\draw[module,draw=teal,fill=teal!4] (114,79) rectangle (287,107);
\draw[module,draw=blue,fill=blue!3] (114,113) rectangle (287,137);

% ---------------- center (1): the budgeted flow, drawn as re-routing ----------------
\node[title,text=teal] at (200.5,11) {SafeOT-Dual: one price rule};
\node[anchor=west] at (120,22) {\textcircled{\scriptsize 1} each epoch: route visits to reward, within budgets};
\coordinate (s) at (134,46); \coordinate (a) at (172,34); \coordinate (b) at (212,34);
\coordinate (c) at (172,58); \coordinate (d) at (212,58); \coordinate (g) at (252,46);
% costly edge highlighted
\draw[cost,line width=5bp,line cap=round,opacity=.35] (a) -- (b);
% observed flow F-hat (faint gray underlay): mostly the short costly route
\draw[gray!45,line width=3.2bp,line cap=round] (s) -- (a) -- (b) -- (g);
\draw[gray!45,line width=1bp,line cap=round] (s) -- (c) -- (d) -- (g);
% projected flow F-star: the costly route is thinned, the detour carries the flow
\begin{scope}[teal,-{Stealth[length=3bp,width=2.6bp]},shorten >=3.4bp,shorten <=3.4bp]
\draw[line width=.9bp] (s) -- (a); \draw[line width=.9bp] (a) -- (b); \draw[line width=.9bp] (b) -- (g);
\draw[line width=2.3bp] (s) -- (c); \draw[line width=2.3bp] (c) -- (d); \draw[line width=2.3bp] (d) -- (g);
\end{scope}
\draw[hard,dashed,line width=.7bp,shorten >=3.4bp,shorten <=3.4bp] (a) -- (d);
\node[text=hard,font=\fontsize{9}{9}\selectfont] at (192,46) {$\times$};
\foreach \n in {a,b,c,d} \filldraw[fill=white,draw=teal,line width=.6bp] (\n) circle (3.1bp);
\filldraw[fill=white,draw=ink,line width=.6bp] (s) circle (3.3bp);
\filldraw[fill=teal,draw=teal] (g) circle (3.3bp);
\node[anchor=east] at (129,46) {start};
\node[anchor=west] at (257,46) {goal};
\node[anchor=west,text=cost!80!black,font=\ticks] at (216,30) {costly};
\node[anchor=south,font=\ticks,align=center] at (200.5,72.6) {nodes $=$ state clusters \;$\cdot$\; width $=$ visits \;$\cdot$\; {\color{hard}$\times$} $=$ hard edge};
\node[anchor=south,font=\ticks,text=gray] at (150,31) {observed $\hat F$};
\node[anchor=north west,font=\ticks,text=teal] at (224,57) {target $F^\star$};

% ---------------- center (2): price ----------------
\node[anchor=west] at (120,87) {\textcircled{\scriptsize 2} price};
\node[formula] at (200.5,89) {$\lambda_k \;=\; {\color{teal}\bar\lambda^\star_k} \;+\; {\color{orange}\beta_k}$};
\node[chip,text=teal,fill=teal!10] at (163,101) {solved, clipped at $c$, filtered};
\node[chip,text=orange,fill=orange!8] at (246,101) {feedback on $\bar J_k-B_k$};
\draw[flow,teal] (200.5,107) -- (200.5,113);

% ---------------- center (3): actor ----------------
\node[anchor=west] at (120,125) {\textcircled{\scriptsize 3} actor};
\node[formula] at (208,125) {$\widetilde A=\frac{A_r-\sum_k\lambda_k A_{c_k}}{1+\sum_k\lambda_k}\ \to\ \text{PPO/TRPO}$};

% ---------------- left: penalty view (exact settings) ----------------
\node[title] at (55,13) {Penalty view};
\node at (55,25) {prices weight costs};
\node[formula] at (55,48) {$\lambda_k=\beta_k$};
\node[text=gray] at (55,60) {graph price off ($c=0$)};
\node[chip,fill=white,draw=gray!40] at (55,82) {$\beta$ fixed $\;\to\;$ fixed penalty};
\node[chip,fill=white,draw=gray!40] at (55,100) {$\beta$ adaptive $\;\to\;$ Lagrangian};
\draw[flow,gray] (114,93) -- (107.5,93);
\node[text=gray,font=\ticks,align=center] at (55,123) {exact settings of the\\ same price rule};

% ---------------- right: constraint view (conditional limits) ----------------
\node[title] at (343.5,13) {Constraint view};
\node at (343.5,25) {prices are budget duals};
\fill[teal!10] (306,90) rectangle (348,58);
\draw[teal,line width=.6bp] (306,58) -- (348,58) -- (348,90);
\draw[flow,gray,line width=.6bp] (306,90) -- (388,90);
\draw[flow,gray,line width=.6bp] (306,90) -- (306,36);
\node[anchor=west,font=\ticks] at (309,38) {$\langle C_2,F\rangle$};
\node[anchor=north east,font=\ticks] at (390,93) {$\langle C_1,F\rangle$};
\node[font=\ticks,text=teal] at (322,74) {budgets};
% reward-greedy point outside, projected onto the binding face
\draw[gray,line width=.6bp] (374,70) circle (2.3bp);
\node[anchor=south,font=\ticks,text=gray,align=center] at (374,66) {reward-\\greedy};
\draw[-{Stealth[length=3bp,width=2.6bp]},gray,line width=.6bp,dashed] (371.5,70) -- (351.5,70);
\fill[teal] (348,70) circle (2.2bp);
\node[anchor=east,font=\ticks] at (345,70) {$F^\star$};
\draw[-{Stealth[length=3bp,width=2.6bp]},orange!0!teal,line width=.9bp] (348,78) -- (362,78);
\node[anchor=west,font=\ticks,text=teal] at (351,84) {$\lambda^\star_1>0$};
\node[anchor=south,font=\ticks,text=gray] at (327,57) {$\lambda^\star_2=0$};
\draw[flow,gray] (287,93) -- (293.5,93);
\node[font=\ticks,align=center] at (343.5,111) {$\varepsilon\to0$: LP dual price};
\node[font=\ticks,align=center] at (343.5,121) {saturated clip: active-set price};
\node[font=\ticks,text=gray] at (343.5,131) {limits, under Sec.~4 assumptions};

% ---------------- bottom strip: what the solved price buys (real data) ----------------
\node[anchor=west,font=\bodyfont] at (3,146) {\textbf{Payoff while learning.} Cost$/$budget during training (task median); shaded $=$ violation $V$.};
\node[anchor=east,font=\ticks] at (393,146) {{\color{ours}\rule[1.6bp]{9bp}{1.1bp}}\,SafeOT-Dual\enspace{\color{lag}$\cdot\!\cdot\!\cdot$}\,TRPO-Lag};
""" + strip_axis("SafePO", 22, "SafePO, 10 tasks ($B=25$)", 2.6, "0,1,2",
                 r"$V$: $0.37\times$\\lower on\\10/10 tasks") + \
    strip_axis("Bullet", 222, "Bullet, 6 tasks ($B=10$)", 16, "0,5,10,15",
               r"$V$: $0.22\times$\\lower on\\6/6 tasks") + r"""
\end{tikzpicture}
\end{document}
"""
open(os.path.join(HERE, "teaser_mock.tex"), "w").write(tex)
print("wrote teaser_mock.tex", len(tex))
