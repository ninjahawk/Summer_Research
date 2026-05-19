# contact_freezing.py -- Does a frozen contact graph let targeted vaccination work?
#                        (Finding 48)
#
# Finding 47 falsified the Section 5 prediction that a topological alignment force
# would rescue targeted vaccination, and in doing so it sharpened the mechanism:
# targeting fails because the CONTACT graph -- the network contagion spreads on --
# continuously rewires through the physical relative motion of agents. F47's
# revised Section 5 states the only genuine escape route explicitly: "freezing the
# contact graph itself -- that is, suppressing the relative motion of agents."
#
# This experiment tests that escape route directly, and in doing so ties the
# contagion thread to the phase-transition thread. The noise amplitude (ramp) is
# the book's solid-to-fluid control parameter. At low ramp the flock is in its
# "solid" regime: agents lock into a near-rigid lattice and relative motion -- and
# therefore contact-graph rewiring -- is suppressed. At high ramp the flock is
# "fluid" and mixes freely.
#
# Prediction. Sweeping ramp from the solid regime to the fluid regime:
#   (a) the contact-graph mixing rate (Jaccard turnover) should rise with ramp;
#   (b) degree-targeted vaccination should beat random in the low-ramp (frozen,
#       solid) regime and collapse to random in the high-ramp (fluid) regime.
# If (b) holds, targeting works exactly where mixing is absent -- confirming the
# F47 mechanism. If targeting fails even in the frozen regime, the mechanism is
# more subtle still (e.g. the panic-induced noise alone suffices to mix).
#
# Run with:  python contagion/contact_freezing.py

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
import os
import time

os.makedirs('figures', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

# ---------------------------------------------------------------------------
# Parameters (2D, matched to the vaccination experiments F36/F37/F47)
# ---------------------------------------------------------------------------
N         = 350
N_SEEDS   = 5
DT        = 0.01

R0_REP = 0.005
RF     = 0.10
ALPHA  = 1.0
V0     = 0.02
MU     = 10.0
EPS    = 0.1
RB_REP = 2.0 * R0_REP

PANIC_ALPHA = 0.1
PANIC_RAMP  = 10.0
R_CONT      = 0.05
BETA        = 2.5
GAMMA       = 2.0
F0_FRAC     = 0.05

N_WARMUP   = 2000
N_ITER     = 10000
P_IMMUNE_LIST = [0.20, 0.35]

# Noise sweep: solid (low ramp) -> fluid (high ramp). Default contagion ramp=0.1.
RAMP_VALS = [0.003, 0.01, 0.03, 0.1, 0.3]

MIX_STEPS    = 5000
MIX_INTERVAL = 200


# ---------------------------------------------------------------------------
# Geometry / dynamics (2D minimum-image torus, metric alignment)
# ---------------------------------------------------------------------------
def pair_d(x, y):
    dx = x[np.newaxis, :] - x[:, np.newaxis]
    dy = y[np.newaxis, :] - y[:, np.newaxis]
    dx -= np.round(dx); dy -= np.round(dy)
    return dx, dy, dx**2 + dy**2


def order_param(vx, vy):
    spd = np.maximum(np.sqrt(vx**2 + vy**2), 1e-12)
    return float(np.sqrt((vx/spd).mean()**2 + (vy/spd).mean()**2))


def step(x, y, vx, vy, rng, alpha_arr, ramp_arr):
    N_ = x.size
    not_self = ~np.eye(N_, dtype=bool)
    dx, dy, d2 = pair_d(x, y)

    rep_mask = (d2 <= RB_REP**2) & not_self & (d2 > 0)
    d_safe   = np.where(rep_mask, np.sqrt(d2), 1.0)
    base_r   = np.maximum(np.where(rep_mask, 1.0 - d_safe/RB_REP, 0.0), 0.0)
    strength = np.where(rep_mask, EPS * base_r**1.5 / d_safe, 0.0)
    fx = (-strength * dx).sum(axis=1)
    fy = (-strength * dy).sum(axis=1)

    mask = (d2 <= RF**2) & not_self
    svx = (vx[np.newaxis, :] * mask).sum(axis=1)
    svy = (vy[np.newaxis, :] * mask).sum(axis=1)
    has = mask.sum(axis=1) > 0
    nrm = np.sqrt(svx**2 + svy**2)
    safe = np.where(nrm > 0, nrm, 1.0)
    fx += np.where(has, alpha_arr * svx/safe, 0.0)
    fy += np.where(has, alpha_arr * svy/safe, 0.0)

    spd = np.maximum(np.sqrt(vx**2 + vy**2), 1e-12)
    prop = MU * (V0 - spd) / spd
    fx += prop * vx; fy += prop * vy

    fx += ramp_arr * rng.uniform(-1., 1., N_)
    fy += ramp_arr * rng.uniform(-1., 1., N_)

    vx = vx + fx * DT; vy = vy + fy * DT
    x = (x + vx * DT) % 1.0
    y = (y + vy * DT) % 1.0
    return x, y, vx, vy


def warmup(seed, ramp):
    np.random.seed(seed)
    x = np.random.uniform(0., 1., N)
    y = np.random.uniform(0., 1., N)
    vx = np.random.uniform(-1., 1., N) * V0
    vy = np.random.uniform(-1., 1., N) * V0
    rng = np.random.default_rng(seed * 17 + 3)
    alpha_arr = np.full(N, ALPHA)
    ramp_arr  = np.full(N, ramp)
    for _ in range(N_WARMUP):
        x, y, vx, vy = step(x, y, vx, vy, rng, alpha_arr, ramp_arr)
    return x, y, vx, vy


def contact_sets(x, y):
    dx = x[np.newaxis, :] - x[:, np.newaxis]
    dy = y[np.newaxis, :] - y[:, np.newaxis]
    dx -= np.round(dx); dy -= np.round(dy)
    rd2 = dx**2 + dy**2
    within = (rd2 <= R_CONT**2) & (rd2 > 0)
    return [frozenset(np.where(row)[0]) for row in within], within.sum(axis=1)


def degree_order(x, y):
    dx = x[np.newaxis, :] - x[:, np.newaxis]
    dy = y[np.newaxis, :] - y[:, np.newaxis]
    dx -= np.round(dx); dy -= np.round(dy)
    rd2 = dx**2 + dy**2
    deg = ((rd2 <= R_CONT**2) & (rd2 > 0)).sum(axis=1)
    return np.argsort(-deg), deg


def measure_mixing(seed, ramp):
    """Jaccard dissimilarity of contact sets per 2 tu, on a pure flock."""
    x, y, vx, vy = warmup(seed, ramp)
    rng = np.random.default_rng(seed * 29 + 7)
    alpha_arr = np.full(N, ALPHA)
    ramp_arr  = np.full(N, ramp)
    prev = None
    diss = []
    for i in range(MIX_STEPS):
        x, y, vx, vy = step(x, y, vx, vy, rng, alpha_arr, ramp_arr)
        if i % MIX_INTERVAL == 0:
            sets, _ = contact_sets(x, y)
            if prev is not None:
                vals = []
                for a, b in zip(prev, sets):
                    u = len(a | b)
                    vals.append(1.0 - (len(a & b)/u if u else 1.0))
                diss.append(np.mean(vals))
            prev = sets
    return float(np.mean(diss))


def run_sis(x0, y0, vx0, vy0, ramp, rng, is_immune):
    x = x0.copy(); y = y0.copy(); vx = vx0.copy(); vy = vy0.copy()
    is_panicked = np.zeros(N, dtype=bool)
    n0 = max(1, round(F0_FRAC * N))
    sus = np.where(~is_immune)[0]
    idx0 = rng.choice(sus, size=n0, replace=False) if sus.size >= n0 else sus
    is_panicked[idx0] = True

    p_recover = 1.0 - np.exp(-GAMMA * DT)
    last_window = N_ITER - int(20.0 / DT)
    f_series = []

    for i in range(N_ITER):
        alpha_arr = np.where(is_panicked, PANIC_ALPHA, ALPHA)
        ramp_arr  = np.where(is_panicked, PANIC_RAMP,  ramp)
        x, y, vx, vy = step(x, y, vx, vy, rng, alpha_arr, ramp_arr)

        if is_panicked.any() and (~is_panicked & ~is_immune).any():
            dx = x[np.newaxis, :] - x[:, np.newaxis]
            dy = y[np.newaxis, :] - y[:, np.newaxis]
            dx -= np.round(dx); dy -= np.round(dy)
            rd2 = dx**2 + dy**2
            within = (rd2 <= R_CONT**2) & (rd2 > 0)
            kcnt = within @ is_panicked.astype(np.int32)
            cs = np.where(~is_panicked & ~is_immune)[0]
            p_trans = 1.0 - np.exp(-BETA * kcnt[cs] * DT)
            flipped = cs[rng.uniform(0., 1., cs.size) < p_trans]
            if flipped.size:
                is_panicked[flipped] = True

        if is_panicked.any():
            pidx = np.where(is_panicked)[0]
            rec = pidx[rng.uniform(0., 1., pidx.size) < p_recover]
            if rec.size:
                is_panicked[rec] = False

        if i >= last_window and i % 50 == 0:
            f_series.append(is_panicked.mean())

    return float(np.mean(f_series)) if f_series else 0.0


# ---------------------------------------------------------------------------
if __name__ == '__main__':
    print('Finding 48 -- contact-graph freezing and targeted vaccination')
    print('  sweeping noise (ramp) from solid regime to fluid regime')
    print('  ramp values:', RAMP_VALS)
    print()
    t0 = time.time()

    mixing = {}
    phi_w  = {}
    # (ramp, p_immune, strategy) -> [f_ss per seed]
    vac = {}
    for r in RAMP_VALS:
        for p in P_IMMUNE_LIST:
            for strat in ('random', 'targeted'):
                vac[(r, p, strat)] = []

    for ramp in RAMP_VALS:
        tr = time.time()
        diss_seeds, phi_seeds = [], []
        for s in range(N_SEEDS):
            diss_seeds.append(measure_mixing(s, ramp))
        mixing[ramp] = (np.mean(diss_seeds), np.std(diss_seeds))

        for s in range(N_SEEDS):
            x0, y0, vx0, vy0 = warmup(s, ramp)
            phi_seeds.append(order_param(vx0, vy0))
            deg_sorted, _ = degree_order(x0, y0)
            for p_im in P_IMMUNE_LIST:
                n_im = int(round(p_im * N))
                rng_r = np.random.default_rng(s*1000 + int(p_im*1000) + int(ramp*1e5))
                im_r = np.zeros(N, dtype=bool)
                im_r[rng_r.choice(N, size=n_im, replace=False)] = True
                im_t = np.zeros(N, dtype=bool)
                im_t[deg_sorted[:n_im]] = True
                f_r = run_sis(x0, y0, vx0, vy0, ramp,
                              np.random.default_rng(s*2000+int(p_im*1000)+int(ramp*1e5)), im_r)
                f_t = run_sis(x0, y0, vx0, vy0, ramp,
                              np.random.default_rng(s*3000+int(p_im*1000)+int(ramp*1e5)), im_t)
                vac[(ramp, p_im, 'random')].append(f_r)
                vac[(ramp, p_im, 'targeted')].append(f_t)
        phi_w[ramp] = (np.mean(phi_seeds), np.std(phi_seeds))
        print('  ramp=%.3f  Phi=%.3f  mixing(Jaccard/2tu)=%.4f+/-%.4f  [%.0fs]' % (
              ramp, phi_w[ramp][0], mixing[ramp][0], mixing[ramp][1],
              time.time() - tr), flush=True)

    print()
    print('=== Vaccination: targeted advantage (f_ss random - targeted) ===')
    print('  positive => targeting beats random')
    summary = {}
    for ramp in RAMP_VALS:
        line = '  ramp=%.3f  mixing=%.4f  ' % (ramp, mixing[ramp][0])
        for p in P_IMMUNE_LIST:
            r = np.array(vac[(ramp, p, 'random')])
            t = np.array(vac[(ramp, p, 'targeted')])
            adv = r.mean() - t.mean()
            summary[(ramp, p)] = (r.mean(), r.std(), t.mean(), t.std(), adv)
            line += 'p=%.2f: rand=%.3f targ=%.3f adv=%+.3f  ' % (
                    p, r.mean(), t.mean(), adv)
        print(line)
    print()
    print('Total runtime: %.1f min' % ((time.time() - t0)/60.0))

    # --- Figure ---
    ramps = np.array(RAMP_VALS)
    mix_arr = np.array([mixing[r][0] for r in RAMP_VALS])
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))

    ax = axes[0]
    ax.errorbar(ramps, mix_arr, yerr=[mixing[r][1] for r in RAMP_VALS],
                marker='o', capsize=4, color='C0')
    ax.set_xscale('log')
    ax.set_xlabel('Noise amplitude ramp')
    ax.set_ylabel('Contact-graph mixing (Jaccard / 2tu)')
    ax.set_title('Contact-graph mixing vs noise\n(solid -> fluid)')
    ax.grid(alpha=0.3)

    ax2 = axes[1]
    for p, mk in zip(P_IMMUNE_LIST, ('o', 's')):
        adv = [summary[(r, p)][4] for r in RAMP_VALS]
        ax2.plot(ramps, adv, marker=mk, label='p_immune=%.2f' % p)
    ax2.axhline(0.0, color='gray', ls='--', lw=1)
    ax2.set_xscale('log')
    ax2.set_xlabel('Noise amplitude ramp')
    ax2.set_ylabel('Targeted advantage (f_ss random - targeted)')
    ax2.set_title('Does targeting beat random?\npositive = yes')
    ax2.legend(fontsize=9); ax2.grid(alpha=0.3)

    fig.suptitle('Finding 48 -- contact-graph freezing and targeted vaccination')
    fig.tight_layout()
    fig.savefig('figures/finding48_contact_freezing.png', dpi=140)
    print('  -> figures/finding48_contact_freezing.png')

    with open('outputs/finding48_contact_freezing.txt', 'w') as f:
        f.write('Finding 48 -- contact-graph freezing and targeted vaccination\n')
        f.write('N=%d seeds=%d  beta=%.2f gamma=%.2f\n\n' % (N, N_SEEDS, BETA, GAMMA))
        f.write('ramp    Phi     mixing(Jaccard/2tu)\n')
        for r in RAMP_VALS:
            f.write('%.3f   %.3f   %.4f +/- %.4f\n' % (
                    r, phi_w[r][0], mixing[r][0], mixing[r][1]))
        f.write('\nVaccination (f_ss): targeted advantage = random - targeted\n')
        for r in RAMP_VALS:
            for p in P_IMMUNE_LIST:
                rm, rs, tm_, ts, adv = summary[(r, p)]
                f.write('  ramp=%.3f p=%.2f  random=%.4f  targeted=%.4f  adv=%+.4f\n' % (
                        r, p, rm, tm_, adv))
    print('  -> outputs/finding48_contact_freezing.txt')
