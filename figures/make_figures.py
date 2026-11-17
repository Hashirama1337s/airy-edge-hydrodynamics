"""Draw the README figures of airy-edge-hydrodynamics from the data the repository ships.

Usage:  python figures/make_figures.py <repo root>
Needs Python 3.11, matplotlib 3.11 and mpmath. Writes figures/*.svg next to this script.

Every plotted number is read from shipped files:
  data/c0down/up_h24.jsonl      tracked critical point c0, d = 3 .. 4
  data/DYN1/track_c0.jsonl      tracked c0, d = 4 .. 4096 (blind seat of BAR-DYN1)
  data/DYN1b/track_c0b.jsonl    tracked c0, d = 4096 .. 32768 (blind seat of BAR-DYN1b)
  data/DYN1b/refine_B.jsonl     c0 refined at 150 bits, d = 256 .. 32768 (values of paper Table 4)
  data/c0down/refine_B.jsonl    c0 refined at 150 bits, d = 3 and 3.5
  data/theory/PRED-THEORY.json  sealed Airy constants U1, A (the script recomputes A from U1 and checks it)
  data/RC/RESULT.json           monodromy certificate: inner radius R_in and outer radius R_out at d = 512, 1024, 8192
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
from matplotlib.lines import Line2D
import mpmath as mp

# ---------------------------------------------------------------- brand style (figures/STYLE.md)
BG, BORDER, GRID, AXC, TXT, ACC = "#1c2026", "#2f353d", "#22272e", "#9aa4ae", "#e8edf2", "#39ff14"
CAT = ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#0ca30c", "#9085e9", "#e66767"]
W_IN = 12.5  # 900 pt viewBox width

plt.rcParams.update({
    "svg.fonttype": "none", "svg.hashsalt": "moki-julio",
    "font.family": "sans-serif", "font.sans-serif": ["Segoe UI", "Helvetica", "Arial", "DejaVu Sans"],
    "font.size": 16, "axes.labelsize": 17, "xtick.labelsize": 15, "ytick.labelsize": 15,
    "axes.facecolor": BG, "figure.facecolor": "none", "savefig.facecolor": "none",
    "axes.edgecolor": AXC, "axes.labelcolor": TXT, "xtick.color": AXC, "ytick.color": AXC,
    "text.color": TXT, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 1.0,
    "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
    "legend.fontsize": 14, "lines.linewidth": 2.0, "axes.axisbelow": True,
})


def new_fig(h_in):
    fig = plt.figure(figsize=(W_IN, h_in))
    fig.patches.append(FancyBboxPatch((0.004, 0.006), 0.992, 0.988, boxstyle="round,pad=0,rounding_size=0.015",
                                      transform=fig.transFigure, facecolor=BG, edgecolor=BORDER, linewidth=1.5,
                                      zorder=-10))
    return fig


def title(fig, main, sub):
    h = fig.get_figheight()
    fig.text(0.035, 1 - 0.33 / h, main, fontsize=21, fontweight="bold", color=TXT, va="top")
    fig.text(0.035, 1 - 0.78 / h, sub, fontsize=15, color=AXC, va="top")


def save(fig, out, name):
    fig.savefig(os.path.join(out, name), format="svg", metadata={"Date": None, "Creator": None})
    plt.close(fig)
    print("wrote figures/" + name)


def jl(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def jload(root, rel):
    with open(os.path.join(root, rel), encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------- data
def track(root):
    """One continuous track d = 3 .. 32768 of c0 = qfr^2 (complex), sorted by d, duplicates at d = 4, 4096 dropped."""
    pts = {}
    for rel in ("data/c0down/up_h24.jsonl", "data/DYN1/track_c0.jsonl", "data/DYN1b/track_c0b.jsonl"):
        for r in jl(root, rel):
            pts.setdefault(float(r["d"]), complex(float(r["q2"][0]), float(r["q2"][1])))
    return sorted(pts.items())


def refined(root):
    out = {}
    for rel in ("data/c0down/refine_B.jsonl", "data/DYN1b/refine_B.jsonl"):
        for r in jl(root, rel):
            out[float(r["d"])] = mp.mpc(mp.mpf(r["q2"][0]), mp.mpf(r["q2"][1]))
    return out


def airy_A(root):
    mp.mp.dps = 30
    pred = jload(root, "data/theory/PRED-THEORY.json")["derived_law"]
    seed = mp.mpc(*[mp.mpf(x) for x in pred["U1"]])
    W = lambda U: mp.airyai(U, 1) ** 2 - U * mp.airyai(U) ** 2
    U1 = mp.findroot(W, seed)
    T1 = mp.airyai(U1, 1) / mp.airyai(U1)
    A = -4 * T1 * mp.mpf(2) ** (-mp.mpf(1) / 3)
    A_sealed = mp.mpc(*[mp.mpf(x) for x in pred["A (coef of d^-1/3 in qfr^2+2)"]])
    assert abs(A - A_sealed) < mp.mpf(10) ** -15, (A, A_sealed)
    return complex(A)


# ---------------------------------------------------------------- figure 1: the track in the complex plane
def fig_track(root, out, tr, ref, A):
    fig = new_fig(8.4)
    title(fig, "The trouble spot c0, followed from d = 3 to d = 32768",
          "The collision point that limits the fluid series where this was checked; plane of complex wavenumber squared")
    ax = fig.add_axes([0.09, 0.1, 0.88, 0.74])
    xs = [z.real for _, z in tr]
    ys = [z.imag for _, z in tr]
    ax.plot(xs, ys, color=ACC, lw=2, zorder=3, label="computed track of c0 (line joins computed points)")
    ax.plot(-2, 0, marker="o", ms=14, mfc="none", mec=TXT, mew=2, ls="", zorder=4, label="fixed spot qfr² = -2")

    def mark(axx, d, dx, dy, ha="left"):
        z = ref[d] if d in ref else dict(tr)[d]
        x, y = float(mp.re(z)), float(mp.im(z))
        axx.plot(x, y, marker="o", ms=9, color=ACC, mec=BG, mew=1.5, zorder=5)
        axx.annotate("d = %s" % format(int(d), ","), (x, y), xytext=(dx, dy), textcoords="offset points",
                     fontsize=14, ha=ha, va="center")

    mark(ax, 3.0, 14, -16)
    mark(ax, 4.0, 14, 0)
    ax.axhline(0, color=AXC, lw=1, zorder=1)
    ax.axvline(0, color=AXC, lw=1, zorder=1)
    ax.set_xlim(-2.45, 2.45)
    ax.set_ylim(-0.12, 2.85)
    ax.set_aspect("equal")
    ax.set_xlabel("real part of qfr²   (qfr = wavenumber in units of 2π × temperature)")
    ax.set_ylabel("imaginary part of qfr²")
    ax.legend(loc="upper left", handlelength=2.6)

    # zoom on the end of the track, with the leading Airy law
    ins = ax.inset_axes([-1.05, 0.2, 2.25, 1.62], transform=ax.transData)
    ins.set_facecolor(BG)
    for s in ins.spines.values():
        s.set_visible(True)
        s.set_color(AXC)
    end = [(d, z) for d, z in tr if d >= 256]         # all inside the zoom window (no reliance on clipping)
    ins.plot([z.real for _, z in end], [z.imag for _, z in end], color=ACC, lw=2, zorder=3)
    law_d = [d for d, _ in tr if d >= 256]
    law = [complex(-2 + A * d ** (-1.0 / 3)) for d in law_d]
    ins.plot([z.real for z in law], [z.imag for z in law], color=CAT[0], lw=2, ls=(0, (4, 3)), zorder=4,
             label="leading Airy law\n-2 + A d^(-1/3), d ≥ 256")
    ins.plot(-2, 0, marker="o", ms=14, mfc="none", mec=TXT, mew=2, zorder=4)
    for d, dy in ((256.0, 0), (1024.0, 0), (4096.0, 0), (32768.0, 0)):
        mark(ins, d, 12, dy)
    ins.set_xlim(-2.06, -1.68)
    ins.set_ylim(-0.06, 1.0)
    ins.tick_params(labelsize=12)
    ins.set_title("zoom on the end of the track (axes stretched)", fontsize=13, color=AXC, pad=6)
    ins.legend(loc="lower right", bbox_to_anchor=(1.0, 0.07), fontsize=13, handlelength=2.2)
    ax.indicate_inset_zoom(ins, edgecolor=AXC, alpha=1.0)
    save(fig, out, "c0-track.svg")


# ---------------------------------------------------------------- figure 2: distance to the fixed spot, log-log
def fig_rate(root, out, tr, A):
    fig = new_fig(6.8)
    title(fig, "Creeping towards the fixed spot as one over the cube root of d",
          "Distance of c0 from qfr² = -2: computed track against the Airy law (no fitted numbers)")
    ax = fig.add_axes([0.1, 0.14, 0.86, 0.64])
    ax.set_xscale("log")
    ax.set_yscale("log")
    ds = [d for d, _ in tr]
    dist = [abs(z + 2) for _, z in tr]
    ax.plot(ds, dist, color=ACC, lw=2, zorder=3, label="computed track of c0 (line joins computed points)")
    law_d = [d for d in ds if d >= 256]
    ax.plot(law_d, [abs(A) * d ** (-1.0 / 3) for d in law_d], color=CAT[0], lw=2, ls=(0, (5, 4)), zorder=4,
            label="leading Airy law |A| d^(-1/3), |A| = %.4f, drawn for d ≥ 256" % abs(A))
    d0 = 32768.0
    z0 = dict(tr)[d0]
    ax.annotate("d = 32,768: distance %.4f\n(law alone: %.4f)" % (abs(z0 + 2), abs(A) * d0 ** (-1.0 / 3)),
                (d0, abs(z0 + 2)), xytext=(6000, 0.6), textcoords="data", ha="center", fontsize=14,
                arrowprops=dict(arrowstyle="-", color=AXC, lw=1, shrinkB=6))
    ax.set_xlim(2.5, 5e4)
    ax.set_ylim(0.1, 6)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: format(int(v), ",")))
    ax.yaxis.set_major_locator(matplotlib.ticker.FixedLocator([0.1, 0.2, 0.5, 1, 2, 5]))
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: ("%g" % v)))
    ax.set_xlabel("number of dimensions d of the plasma (log scale)")
    ax.set_ylabel("distance |qfr² + 2| (log scale)")
    ax.legend(loc="lower left")
    save(fig, out, "c0-approach-rate.svg")


# ---------------------------------------------------------------- figure 3: circle of trust at d = 8192
def fig_circle(root, out, ref):
    rc = jload(root, "data/RC/RESULT.json")["8192"]
    r_in, r_out = mp.mpf(rc["R_in"]), mp.mpf(rc["R_out"])
    c0 = ref[8192.0]
    R = abs(c0)
    assert abs((r_in + r_out) / 2 - R) < mp.mpf(10) ** -12      # the census used |c0| -+ dr
    R, x0, y0 = float(R), float(mp.re(c0)), float(mp.im(c0))

    fig = new_fig(8.0)
    title(fig, "The circle of trust at d = 8192",
          "The fluid series in qfr² works inside a circle around zero; its edge is the trouble spot c0")
    ax = fig.add_axes([0.06, 0.1, 0.6, 0.74])
    fill = "#203b24"  # the accent at 12 % over the background, as a solid colour
    ax.add_patch(Circle((0, 0), R, facecolor=fill, edgecolor="none", zorder=1))
    ax.add_patch(Circle((0, 0), R, facecolor="none", edgecolor=ACC, lw=2, zorder=2))
    ax.axhline(0, color=AXC, lw=1, zorder=1)
    ax.axvline(0, color=AXC, lw=1, zorder=1)
    ax.plot([0, R], [0, 0], color=CAT[0], lw=5, solid_capstyle="butt", zorder=3)
    for s in (1, -1):
        ax.plot(x0, s * y0, marker="X", ms=15, color=CAT[1], mec=BG, mew=1.5, zorder=5)
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.5, 2.5)
    ax.set_aspect("equal")
    ax.set_xlabel("real part of qfr²")
    ax.set_ylabel("imaginary part of qfr²")
    ax.annotate("c0 and its mirror image:\ntwo ripples collide here", (x0, y0), xytext=(-1.2, 2.0),
                textcoords="data", fontsize=14, ha="center", va="center",
                arrowprops=dict(arrowstyle="-", color=AXC, lw=1, shrinkB=9))
    fig.text(0.68, 0.74, "The fluid series works inside a\ncircle around zero, out to the\nnearest trouble spot.", fontsize=15, va="top")
    fig.text(0.68, 0.58, "Green circle: radius |c0| = %.4f.\nA numerical census places the\nradius between %.4f and %.4f\n"
                         "(barring a pole or a cancelling\npair of trouble spots inside one\nsector)."
             % (R, float(r_in), R), fontsize=15, va="top", color=TXT)
    fig.text(0.68, 0.29, "Blue: real wavenumbers, where\nqfr² is a positive real number.\nThe series covers "
                         "them out to\nthe radius (at least %.4f), although\nthe trouble spot is not on that line." % float(r_in),
             fontsize=15, va="top", color=TXT)
    save(fig, out, "circle-of-trust-d8192.svg")
    return R, float(r_in)


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python make_figures.py <repo root>")
    root = sys.argv[1]
    here = os.path.dirname(os.path.abspath(__file__))
    out = here if os.path.basename(here) == "figures" else os.path.join(here, "figures")
    os.makedirs(out, exist_ok=True)
    tr, ref, A = track(root), refined(root), airy_A(root)
    for d in (3.0, 4096.0, 32768.0):                     # track and refinement agree where both exist
        if d in ref:
            assert abs(complex(ref[d]) - dict(tr)[d]) < 1e-10, d
    fig_track(root, out, tr, ref, A)
    fig_rate(root, out, tr, A)
    R, r_in = fig_circle(root, out, ref)
    print("track points:", len(tr), "d from", tr[0][0], "to", tr[-1][0])
    print("A =", A, "|A| =", abs(A))
    print("highest Im c0 on track:", max(z.imag for _, z in tr))
    z = dict(tr)[32768.0]
    print("d = 32768: |c0 + 2| =", abs(z + 2), " law:", abs(A) * 32768 ** (-1 / 3))
    print("d = 8192: |c0| =", R, " R_in =", r_in)


if __name__ == "__main__":
    main()
