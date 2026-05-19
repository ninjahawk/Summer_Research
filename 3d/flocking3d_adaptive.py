# flocking3d_adaptive.py -- 3D adaptive encirclement (Finding 45)
#
# Question.  In 2D, Finding 35 showed adaptive R_enc = 0.5*live_Rg outperforms a
# fixed R_enc=0.15, because it tracks the optimal R_enc/Rg ~ 0.5 ratio through the
# merge/split cycle.  Finding 43 then showed the 2D optimum (R_enc/Rg ~ 0.5) does
# NOT transfer to 3D: in 3D the disruption minimum sits at R_enc=0.15 (R_enc/Rg ~
# 0.38), and at R_enc/Rg = 0.50 the flock is essentially untouched (Phi ~ 0.997).
#
# So the 3D adaptive question is two-sided:
#   (a) Does adaptive tracking help at all in 3D?
#   (b) Which target ratio matters -- the 2D-inherited 0.50, or the 3D-empirical
#       0.38 (the ratio that fixed R_enc=0.15 happens to realize)?
#
# Prediction.  Because the 3D disruption-vs-R_enc curve is much shallower than 2D
# (Phi only dips to ~0.95 at the optimum vs ~0.75 in 2D), adaptive tracking should
# give a SMALLER benefit than the 2D -8% mean-Phi improvement.  Adaptive at ratio
# 0.50 should be near-useless (sits at the no-disruption end of the curve).
# Adaptive at 0.38 should roughly match fixed R_enc=0.15, with possibly a slight
# edge by holding the optimum through Rg fluctuations.
#
# Design.  N=350, n_pred=10, 15000 steps (long run, captures merge/split cycle).
#   Fixed:        R_enc = 0.15
#   Adaptive-38:  R_enc = 0.38 * live_Rg, updated every step
#   Adaptive-50:  R_enc = 0.50 * live_Rg, updated every step
# Metrics: mean Phi, temporal std Phi, mean Rg, fraction of time Phi > 0.85.
#
# Run with:  python 3d/flocking3d_adaptive.py

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
import os
import time

os.makedirs('figures', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

# ---------------------------------------------------------------------------
# Simulation parameters (matched to flocking3d_predator.py)
# ---------------------------------------------------------------------------
N        = 350
N_SEEDS  = 5
N_ITER   = 15000
N_WARMUP = 3000

R0_3D  = 0.02
RF_3D  = 0.20
ALPHA  = 1.0
V0_PRY = 0.02
MU     = 10.0
RAMP   = 0.1
EPS    = 0.1
EXP_N  = 1.5
RB_3D  = 2.0 * R0_3D

V0_PRD  = 0.05
ALPHA_P = 5.0
MU_P    = 10.0
R0_P    = 0.10
EPS_P   = 2.0
RAMP_P  = 1.0

N_PRED      = 10
FIXED_RENC  = 0.15
ADAPT_RATIOS = [0.38, 0.50]


# ---------------------------------------------------------------------------
# 3D geometry helpers
# ---------------------------------------------------------------------------
def com3d(pos):
    cx = np.arctan2(np.sin(2*np.pi*pos[0]).mean(),
                    np.cos(2*np.pi*pos[0]).mean()) / (2*np.pi) % 1.0
    cy = np.arctan2(np.sin(2*np.pi*pos[1]).mean(),
                    np.cos(2*np.pi*pos[1]).mean()) / (2*np.pi) % 1.0
    cz = np.arctan2(np.sin(2*np.pi*pos[2]).mean(),
                    np.cos(2*np.pi*pos[2]).mean()) / (2*np.pi) % 1.0
    return np.array([cx, cy, cz])


def rg3d(pos, c):
    d = pos - c[:, np.newaxis]
    d -= np.round(d)
    return float(np.sqrt((d**2).sum(axis=0).mean()))


def order_param3d(vel):
    spd = np.maximum(np.sqrt((vel**2).sum(axis=0)), 1e-10)
    vhat = vel / spd[np.newaxis, :]
    return float(np.sqrt((vhat.mean(axis=1)**2).sum()))


def fibonacci_sphere(n):
    if n == 1:
        return np.array([[0.0, 0.0, 1.0]])
    golden = (1.0 + np.sqrt(5.0)) / 2.0
    idx = np.arange(n)
    theta = np.arccos(1.0 - 2.0*(idx + 0.5)/n)
    phi   = 2.0 * np.pi * idx / golden
    return np.column_stack([np.sin(theta)*np.cos(phi),
                            np.sin(theta)*np.sin(phi),
                            np.cos(theta)])


class Pred3D:
    """Encircling predator. If adapt_ratio is set, enc_radius is updated live."""
    def __init__(self, direction, enc_radius, seed):
        rng = np.random.default_rng(seed)
        self.pos = rng.uniform(0., 1., 3)
        raw = rng.standard_normal(3)
        self.vel = V0_PRD * raw / np.linalg.norm(raw)
        self.direction  = np.asarray(direction, dtype=float)
        self.enc_radius = enc_radius

    def target(self, c):
        return (c + self.enc_radius * self.direction) % 1.0

    def step(self, c, dt):
        disp = self.target(c) - self.pos
        disp -= np.round(disp)
        dist = np.linalg.norm(disp)
        spd = np.linalg.norm(self.vel) + 1e-12
        drive = (ALPHA_P * disp / (dist + 1e-12)
                 + MU_P * (V0_PRD - spd) * self.vel / spd
                 + RAMP_P * np.random.uniform(-1., 1., 3))
        self.vel += drive * dt
        self.pos = (self.pos + self.vel * dt) % 1.0

    def force_on_prey(self, pos):
        d = pos - self.pos[:, np.newaxis]
        d -= np.round(d)
        dist = np.sqrt((d**2).sum(axis=0))
        in_range = (dist > 0) & (dist <= R0_P)
        base = np.maximum(1.0 - dist / R0_P, 0.0)
        strength = np.where(in_range, EPS_P * base**1.5 / (dist + 1e-12), 0.0)
        return strength[np.newaxis, :] * d   # push prey away (d = prey - pred)


def run_3d(mode, adapt_ratio, seed):
    """mode: 'fixed' uses FIXED_RENC; 'adaptive' uses adapt_ratio*live_Rg."""
    np.random.seed(seed)
    pos = np.random.uniform(0., 1., (3, N))
    raw = np.random.randn(3, N)
    raw /= np.sqrt((raw**2).sum(axis=0))
    vel = V0_PRY * raw

    directions = fibonacci_sphere(N_PRED)
    init_renc = FIXED_RENC if mode == 'fixed' else adapt_ratio * 0.40
    preds = [Pred3D(directions[k], init_renc, seed*100 + k) for k in range(N_PRED)]

    phi_vals, rg_vals = [], []

    for step in range(N_ITER):
        dx = pos[0, np.newaxis, :] - pos[0, :, np.newaxis]
        dy = pos[1, np.newaxis, :] - pos[1, :, np.newaxis]
        dz = pos[2, np.newaxis, :] - pos[2, :, np.newaxis]
        dx -= np.round(dx); dy -= np.round(dy); dz -= np.round(dz)
        d2 = dx**2 + dy**2 + dz**2
        not_self = ~np.eye(N, dtype=bool)

        rep_mask = (d2 <= RB_3D**2) & not_self & (d2 > 0)
        d_safe   = np.where(rep_mask, np.sqrt(d2), 1.0)
        base_r   = np.maximum(np.where(rep_mask, 1.0 - d_safe/RB_3D, 0.0), 0.0)
        strength = np.where(rep_mask, EPS * base_r**EXP_N / d_safe, 0.0)
        fx = (-strength * dx).sum(axis=1)
        fy = (-strength * dy).sum(axis=1)
        fz = (-strength * dz).sum(axis=1)

        flock_mask = (d2 <= RF_3D**2) & not_self
        svx = (vel[0] * flock_mask).sum(axis=1)
        svy = (vel[1] * flock_mask).sum(axis=1)
        svz = (vel[2] * flock_mask).sum(axis=1)
        vbar = np.sqrt(svx**2 + svy**2 + svz**2)
        has = (flock_mask.sum(axis=1) > 0)
        safe = np.where(has, vbar, 1.0)
        fx += np.where(has, ALPHA * svx / safe, 0.0)
        fy += np.where(has, ALPHA * svy / safe, 0.0)
        fz += np.where(has, ALPHA * svz / safe, 0.0)

        spd = np.maximum(np.sqrt(vel[0]**2 + vel[1]**2 + vel[2]**2), 1e-10)
        prop = MU * (V0_PRY - spd) / spd
        fx += prop * vel[0]; fy += prop * vel[1]; fz += prop * vel[2]

        fx += RAMP * np.random.uniform(-1., 1., N)
        fy += RAMP * np.random.uniform(-1., 1., N)
        fz += RAMP * np.random.uniform(-1., 1., N)

        c = com3d(pos)
        rg_now = rg3d(pos, c)

        if mode == 'adaptive':
            renc_live = adapt_ratio * rg_now
            for pred in preds:
                pred.enc_radius = renc_live

        for pred in preds:
            fp = pred.force_on_prey(pos)
            fx += fp[0]; fy += fp[1]; fz += fp[2]

        vel[0] += fx * 0.01; vel[1] += fy * 0.01; vel[2] += fz * 0.01
        pos = (pos + vel * 0.01) % 1.0

        for pred in preds:
            pred.step(c, 0.01)

        if step >= N_WARMUP:
            phi_vals.append(order_param3d(vel))
            rg_vals.append(rg_now)

    phi_arr = np.array(phi_vals)
    rg_arr  = np.array(rg_vals)
    return (float(phi_arr.mean()), float(phi_arr.std()),
            float(rg_arr.mean()), float((phi_arr > 0.85).mean()))


# ---------------------------------------------------------------------------
# Fixed vs adaptive comparison
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    print('Finding 45 -- 3D adaptive encirclement')
    print('  N=%d  seeds=%d  iter=%d  warmup=%d  n_pred=%d' % (
          N, N_SEEDS, N_ITER, N_WARMUP, N_PRED))
    print()

    configs = [('fixed', None, 'fixed R_enc=%.2f' % FIXED_RENC)]
    for r in ADAPT_RATIOS:
        configs.append(('adaptive', r, 'adaptive R_enc=%.2f*Rg' % r))

    results = {}
    t0 = time.time()
    for mode, ratio, label in configs:
        phi_m, phi_s, rg_m, frac = [], [], [], []
        ts = time.time()
        for s in range(N_SEEDS):
            pm, ps, rm, fr = run_3d(mode, ratio, s)
            phi_m.append(pm); phi_s.append(ps); rg_m.append(rm); frac.append(fr)
        key = label
        results[key] = (np.mean(phi_m), np.std(phi_m), np.mean(phi_s),
                        np.mean(rg_m), np.mean(frac))
        print('  %-26s Phi=%.3f+/-%.3f  tstd=%.3f  Rg=%.3f  f(Phi>0.85)=%.3f  [%.0fs]' % (
              label, results[key][0], results[key][1], results[key][2],
              results[key][3], results[key][4], time.time() - ts))

    print('\nTotal runtime: %.1f min' % ((time.time() - t0)/60.0))

    labels   = list(results.keys())
    phi_mean = [results[k][0] for k in labels]
    phi_err  = [results[k][1] for k in labels]

    fig, ax = plt.subplots(figsize=(6.5, 4))
    xpos = np.arange(len(labels))
    ax.bar(xpos, phi_mean, yerr=phi_err, capsize=4,
           color=['C0', 'C1', 'C2'])
    ax.axhline(0.953, color='gray', ls='--', label='F43 3D enc n=10 (Phi~0.94)')
    ax.set_xticks(xpos)
    ax.set_xticklabels(labels, rotation=15, ha='right')
    ax.set_ylabel('Steady-state Phi')
    ax.set_title('3D adaptive vs fixed encirclement (Finding 45)')
    ax.set_ylim(0.0, 1.05)
    ax.legend()
    ax.grid(alpha=0.3, axis='y')
    fig.tight_layout()
    fig.savefig('figures/finding45_3d_adaptive.png', dpi=140)
    print('  -> figures/finding45_3d_adaptive.png')

    with open('outputs/finding45_3d_adaptive.txt', 'w') as f:
        f.write('Finding 45 -- 3D adaptive encirclement\n')
        f.write('N=%d seeds=%d iter=%d n_pred=%d\n\n' % (N, N_SEEDS, N_ITER, N_PRED))
        f.write('config                      Phi_mean  Phi_std  t_std  Rg     f(Phi>0.85)\n')
        for k in labels:
            f.write('%-26s  %.4f    %.4f   %.4f  %.4f  %.4f\n' % (k, *results[k]))
    print('  -> outputs/finding45_3d_adaptive.txt')
