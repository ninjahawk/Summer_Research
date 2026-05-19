# flocking3d_predator.py -- 3D predator strategies: does encirclement work in 3D?
#
# Finding 43.  Extends the 3D flocking model (Finding 41/42) with predator pressure.
#
# Key questions:
#   (1) Does the encirclement strategy disrupt a 3D flock?
#   (2) Is R_enc/Rg ~ 0.5 still the universal optimal ratio in 3D?
#   (3) How does the 3D Phi floor compare to the 2D floor at the same n_pred?
#
# Slow-prey regime (v0=0.02, ramp=0.1) so predators can catch up -- same regime
# used in all 2D predator experiments (legacy PREY_DEFAULT in predator.py).
# 3D neighbor-count matching: rf=0.20, r0=0.02 (from Finding 41).
#
# Experiments:
#   A. Strategy comparison: naive vs encirclement at n_pred=1,3,6,10 (fixed R_enc=0.15)
#   B. R_enc sweep at n_pred=6: find optimal R_enc/Rg in 3D, compare to 2D result
#   C. 2D comparison: encirclement at same n_pred values (via model.py Flock/Predator)

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
import os

from model import Flock, Predator

os.makedirs('figures', exist_ok=True)

# ---------------------------------------------------------------------------
# Simulation parameters
# ---------------------------------------------------------------------------
N          = 350
N_SEEDS    = 5
N_ITER     = 5000
N_WARMUP   = 3000   # steps before recording

# 3D prey physics
R0_3D  = 0.02
RF_3D  = 0.20
ALPHA  = 1.0
V0_PRY = 0.02     # slow prey so predators can catch up
MU     = 10.0
RAMP   = 0.1
EPS    = 0.1
EXP_N  = 1.5
RB_3D  = 2.0 * R0_3D

# Predator parameters (same as 2D legacy PRED_DEFAULT from predator.py)
V0_PRD  = 0.05
ALPHA_P = 5.0
MU_P    = 10.0
R0_P    = 0.10    # repulsion range predator -> prey
EPS_P   = 2.0
RAMP_P  = 1.0

NPRED_VALS = [1, 3, 6, 10]
RENC_DEFAULT = 0.15
RENC_SWEEP   = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35]


# ---------------------------------------------------------------------------
# 3D geometry helpers
# ---------------------------------------------------------------------------

def com3d(pos):
    """Periodic center of mass on [0,1]^3 torus. pos is (3,N)."""
    cx = np.arctan2(np.sin(2*np.pi*pos[0]).mean(),
                    np.cos(2*np.pi*pos[0]).mean()) / (2*np.pi) % 1.0
    cy = np.arctan2(np.sin(2*np.pi*pos[1]).mean(),
                    np.cos(2*np.pi*pos[1]).mean()) / (2*np.pi) % 1.0
    cz = np.arctan2(np.sin(2*np.pi*pos[2]).mean(),
                    np.cos(2*np.pi*pos[2]).mean()) / (2*np.pi) % 1.0
    return np.array([cx, cy, cz])


def rg3d(pos, c):
    """Radius of gyration on 3D torus. pos is (3,N), c is (3,)."""
    d = pos - c[:, np.newaxis]
    d -= np.round(d)
    return float(np.sqrt((d**2).sum(axis=0).mean()))


def order_param3d(vel):
    """Order parameter Phi = |mean unit velocity|. vel is (3,N)."""
    spd = np.sqrt((vel**2).sum(axis=0))
    spd = np.maximum(spd, 1e-10)
    vhat = vel / spd[np.newaxis, :]
    return float(np.sqrt((vhat.mean(axis=1)**2).sum()))


def fibonacci_sphere(n):
    """Approximately uniform distribution of n directions on the unit sphere."""
    if n == 1:
        return np.array([[0.0, 0.0, 1.0]])
    golden = (1.0 + np.sqrt(5.0)) / 2.0
    idx = np.arange(n)
    theta = np.arccos(1.0 - 2.0*(idx + 0.5)/n)
    phi   = 2.0 * np.pi * idx / golden
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)
    return np.column_stack([x, y, z])


# ---------------------------------------------------------------------------
# 3D simulation: prey + predators
# ---------------------------------------------------------------------------

class Pred3D:
    """Minimal 3D predator: naive (chase CoM) or encircle (fixed direction offset)."""

    def __init__(self, direction=None, enc_radius=RENC_DEFAULT, strategy='encircle', seed=None):
        rng = np.random.default_rng(seed)
        self.pos = rng.uniform(0.0, 1.0, 3)
        raw = rng.standard_normal(3)
        self.vel = V0_PRD * raw / np.linalg.norm(raw)
        self.direction  = np.asarray(direction, dtype=float) if direction is not None else np.array([0.,0.,1.])
        self.enc_radius = enc_radius
        self.strategy   = strategy

    def target(self, c):
        if self.strategy == 'encircle':
            t = c + self.enc_radius * self.direction
            return t % 1.0
        return c.copy()

    def step(self, c, dt):
        t = self.target(c)
        disp = t - self.pos
        disp -= np.round(disp)
        dist = np.linalg.norm(disp)
        drive = (ALPHA_P * disp / (dist + 1e-12)
                 + MU_P * (V0_PRD - np.linalg.norm(self.vel))
                   * self.vel / (np.linalg.norm(self.vel) + 1e-12))
        drive += RAMP_P * np.random.uniform(-1., 1., 3)
        self.vel += drive * dt
        self.pos = (self.pos + self.vel * dt) % 1.0

    def force_on_prey(self, pos):
        """Repulsion from predator onto all N prey. pos is (3,N). Returns (3,N)."""
        d = pos - self.pos[:, np.newaxis]
        d -= np.round(d)
        dist = np.sqrt((d**2).sum(axis=0))   # (N,)
        in_range = (dist > 0) & (dist <= R0_P)
        base = np.maximum(1.0 - dist / R0_P, 0.0)
        strength = np.where(in_range, EPS_P * base**1.5 / (dist + 1e-12), 0.0)
        return strength[np.newaxis, :] * d   # push prey away (d = prey - pred)


def run_3d(n_pred, strategy, enc_radius, seed):
    """Single 3D simulation run. Returns (mean_Phi, mean_Rg)."""
    np.random.seed(seed)

    pos = np.random.uniform(0., 1., (3, N))
    raw = np.random.randn(3, N)
    raw /= np.sqrt((raw**2).sum(axis=0))
    vel = V0_PRY * raw

    directions = fibonacci_sphere(n_pred)
    preds = [Pred3D(direction=directions[k], enc_radius=enc_radius,
                    strategy=strategy, seed=seed*100+k)
             for k in range(n_pred)]

    phi_vals = []
    rg_vals  = []

    for step in range(N_ITER):
        # Pairwise prey displacement on 3D torus
        dx = pos[0, np.newaxis, :] - pos[0, :, np.newaxis]
        dy = pos[1, np.newaxis, :] - pos[1, :, np.newaxis]
        dz = pos[2, np.newaxis, :] - pos[2, :, np.newaxis]
        dx -= np.round(dx); dy -= np.round(dy); dz -= np.round(dz)
        d2 = dx**2 + dy**2 + dz**2
        not_self = ~np.eye(N, dtype=bool)

        # Repulsion
        rep_mask = (d2 <= RB_3D**2) & not_self & (d2 > 0)
        d_safe   = np.where(rep_mask, np.sqrt(d2), 1.0)
        base_r   = np.maximum(np.where(rep_mask, 1.0 - d_safe/RB_3D, 0.0), 0.0)
        strength = np.where(rep_mask, EPS * base_r**EXP_N / d_safe, 0.0)
        fx = (-strength * dx).sum(axis=1)
        fy = (-strength * dy).sum(axis=1)
        fz = (-strength * dz).sum(axis=1)

        # Alignment
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

        # Self-propulsion
        spd = np.maximum(np.sqrt(vel[0]**2 + vel[1]**2 + vel[2]**2), 1e-10)
        prop = MU * (V0_PRY - spd) / spd
        fx += prop * vel[0]; fy += prop * vel[1]; fz += prop * vel[2]

        # Noise
        fx += RAMP * np.random.uniform(-1., 1., N)
        fy += RAMP * np.random.uniform(-1., 1., N)
        fz += RAMP * np.random.uniform(-1., 1., N)

        # Predator forces on prey
        c = com3d(pos)
        for pred in preds:
            fp = pred.force_on_prey(pos)
            fx += fp[0]; fy += fp[1]; fz += fp[2]

        # Integrate prey
        vel[0] += fx * 0.01; vel[1] += fy * 0.01; vel[2] += fz * 0.01
        pos = (pos + vel * 0.01) % 1.0

        # Step predators
        for pred in preds:
            pred.step(c, 0.01)

        if step >= N_WARMUP:
            phi_vals.append(order_param3d(vel))
            rg_vals.append(rg3d(pos, c))

    return float(np.mean(phi_vals)), float(np.mean(rg_vals))


# ---------------------------------------------------------------------------
# Experiment A: strategy comparison at n_pred = 1, 3, 6, 10
# ---------------------------------------------------------------------------
print('Experiment A: naive vs encirclement, n_pred sweep, R_enc=%.2f' % RENC_DEFAULT)
print('  N=%d  N_SEEDS=%d  N_ITER=%d  V0_prey=%.2f  ramp=%.1f' % (
      N, N_SEEDS, N_ITER, V0_PRY, RAMP))
print()

res_naive = {}
res_enc   = {}

for np_ in NPRED_VALS:
    phi_n = []; phi_e = []; rg_e = []
    for s in range(N_SEEDS):
        phi, rg = run_3d(np_, 'naive',    RENC_DEFAULT, s)
        phi_n.append(phi)
        phi, rg = run_3d(np_, 'encircle', RENC_DEFAULT, s)
        phi_e.append(phi); rg_e.append(rg)
    res_naive[np_] = (np.mean(phi_n), np.std(phi_n))
    res_enc[np_]   = (np.mean(phi_e), np.std(phi_e), np.mean(rg_e))
    print('  n_pred=%2d  naive Phi=%.3f+/-%.3f  enc Phi=%.3f+/-%.3f  Rg=%.3f' % (
          np_, res_naive[np_][0], res_naive[np_][1],
          res_enc[np_][0],   res_enc[np_][1],
          res_enc[np_][2]))

print()

# ---------------------------------------------------------------------------
# Experiment B: R_enc sweep at n_pred=6
# ---------------------------------------------------------------------------
N_PRED_B = 6
print('Experiment B: R_enc sweep, n_pred=%d' % N_PRED_B)

res_sweep = {}
for renc in RENC_SWEEP:
    phi_vals = []; rg_vals = []
    for s in range(N_SEEDS):
        phi, rg = run_3d(N_PRED_B, 'encircle', renc, s)
        phi_vals.append(phi); rg_vals.append(rg)
    mean_phi = np.mean(phi_vals)
    mean_rg  = np.mean(rg_vals)
    ratio    = renc / mean_rg if mean_rg > 0 else float('nan')
    res_sweep[renc] = (mean_phi, np.std(phi_vals), mean_rg, ratio)
    print('  R_enc=%.2f  Phi=%.3f+/-%.3f  Rg=%.3f  R_enc/Rg=%.2f' % (
          renc, mean_phi, np.std(phi_vals), mean_rg, ratio))

print()

# ---------------------------------------------------------------------------
# Experiment C: 2D comparison via model.py Flock/Predator
# ---------------------------------------------------------------------------
print('Experiment C: 2D comparison at same n_pred values (R_enc=%.2f)' % RENC_DEFAULT)

res_2d = {}
for np_ in NPRED_VALS:
    phi_vals = []; rg_vals = []
    for s in range(N_SEEDS):
        flock = Flock(N=N, seed=s, v0=V0_PRY, ramp=RAMP,
                      r0=0.005, rf=0.1, alpha=ALPHA, mu=MU, eps=EPS)
        preds2d = [Predator(strategy='encircle',
                            angle=k*360.0/np_,
                            enc_radius=RENC_DEFAULT,
                            v0=V0_PRD, alpha=ALPHA_P, mu=MU_P,
                            r0=R0_P, eps=EPS_P, ramp=RAMP_P)
                   for k in range(np_)]
        phi_ts = []
        for i in range(N_ITER):
            flock.evolve(predators=preds2d)
            if i >= N_WARMUP:
                phi_ts.append(flock.phi)
        phi_vals.append(np.mean(phi_ts))
        # 2D Rg: simple mean sqrt((dx^2+dy^2))
        cx = np.arctan2(np.sin(2*np.pi*flock.px).mean(),
                        np.cos(2*np.pi*flock.px).mean()) / (2*np.pi) % 1.0
        cy = np.arctan2(np.sin(2*np.pi*flock.py).mean(),
                        np.cos(2*np.pi*flock.py).mean()) / (2*np.pi) % 1.0
        ddx = flock.px - cx; ddx -= np.round(ddx)
        ddy = flock.py - cy; ddy -= np.round(ddy)
        rg_vals.append(np.sqrt((ddx**2 + ddy**2).mean()))

    res_2d[np_] = (np.mean(phi_vals), np.std(phi_vals), np.mean(rg_vals))
    print('  n_pred=%2d  2D enc Phi=%.3f+/-%.3f  Rg=%.3f' % (
          np_, res_2d[np_][0], res_2d[np_][1], res_2d[np_][2]))

print()

# ---------------------------------------------------------------------------
# Summary table
# ---------------------------------------------------------------------------
print('Summary: 3D naive vs 3D enc vs 2D enc (R_enc=%.2f)' % RENC_DEFAULT)
print('  n_pred   3D naive     3D enc      2D enc      3D Rg    2D Rg')
for np_ in NPRED_VALS:
    print('  %2d       %.3f        %.3f       %.3f       %.3f     %.3f' % (
          np_,
          res_naive[np_][0],
          res_enc[np_][0],
          res_2d[np_][0],
          res_enc[np_][2],
          res_2d[np_][2]))

print()
print('R_enc sweep (n_pred=%d):' % N_PRED_B)
print('  R_enc   Phi      Rg      R_enc/Rg')
for renc in RENC_SWEEP:
    m, s, rg, ratio = res_sweep[renc]
    print('  %.2f    %.3f+/-%.3f  %.3f    %.2f' % (renc, m, s, rg, ratio))

# R_enc/Rg at minimum Phi
best_renc = min(RENC_SWEEP, key=lambda r: res_sweep[r][0])
best_ratio = res_sweep[best_renc][3]
print()
print('Optimal R_enc = %.2f (Phi=%.3f, R_enc/Rg=%.2f)' % (
      best_renc, res_sweep[best_renc][0], best_ratio))
print('Compare: 2D optimal R_enc/Rg ~ 0.50 (Finding 23)')

# ---------------------------------------------------------------------------
# Figures
# ---------------------------------------------------------------------------
np_arr = np.array(NPRED_VALS)

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# --- Panel 1: strategy comparison ---
ax = axes[0]
phi_naive = [res_naive[k][0] for k in NPRED_VALS]
err_naive = [res_naive[k][1] for k in NPRED_VALS]
phi_enc3d = [res_enc[k][0]   for k in NPRED_VALS]
err_enc3d = [res_enc[k][1]   for k in NPRED_VALS]
phi_enc2d = [res_2d[k][0]    for k in NPRED_VALS]
err_enc2d = [res_2d[k][1]    for k in NPRED_VALS]

ax.errorbar(np_arr, phi_naive, yerr=err_naive, marker='o', capsize=4,
            color='gray',      label='3D naive')
ax.errorbar(np_arr, phi_enc3d, yerr=err_enc3d, marker='s', capsize=4,
            color='steelblue', label='3D encircle (R_enc=%.2f)' % RENC_DEFAULT)
ax.errorbar(np_arr, phi_enc2d, yerr=err_enc2d, marker='^', capsize=4,
            color='darkorange', label='2D encircle (R_enc=%.2f)' % RENC_DEFAULT)
ax.axhline(1, ls='--', color='gray', lw=0.8)
ax.set_xlabel('Number of predators')
ax.set_ylabel('Order parameter Phi')
ax.set_title('Strategy comparison: 3D vs 2D encirclement\nN=%d  v0=%.2f  R_enc=%.2f' % (
             N, V0_PRY, RENC_DEFAULT))
ax.legend(fontsize=8); ax.set_ylim(0, 1.05); ax.grid(alpha=0.3)

# --- Panel 2: R_enc sweep ---
ax2 = axes[1]
renc_arr  = np.array(RENC_SWEEP)
phi_sw    = np.array([res_sweep[r][0] for r in RENC_SWEEP])
err_sw    = np.array([res_sweep[r][1] for r in RENC_SWEEP])
ratio_arr = np.array([res_sweep[r][3] for r in RENC_SWEEP])

ax2.errorbar(ratio_arr, phi_sw, yerr=err_sw, marker='o', capsize=4,
             color='steelblue', label='3D n_pred=%d' % N_PRED_B)
ax2.axvline(0.5, ls='--', color='darkorange', lw=1.5,
            label='R_enc/Rg=0.5 (2D optimum)')
ax2.axvline(best_ratio, ls=':', color='steelblue', lw=1.5,
            label='3D best R_enc/Rg=%.2f' % best_ratio)
ax2.set_xlabel('R_enc / Rg')
ax2.set_ylabel('Order parameter Phi')
ax2.set_title('R_enc sweep in 3D (n_pred=%d)\nMinimum Phi at R_enc/Rg=%.2f' % (
             N_PRED_B, best_ratio))
ax2.legend(fontsize=8); ax2.grid(alpha=0.3)

# --- Panel 3: 3D vs 2D Phi floor vs n_pred ---
ax3 = axes[2]
ax3.plot(np_arr, phi_enc3d, 'o-', color='steelblue',  label='3D encircle')
ax3.plot(np_arr, phi_enc2d, '^-', color='darkorange',  label='2D encircle')
ax3.fill_between(np_arr,
                 np.array(phi_enc3d) - np.array(err_enc3d),
                 np.array(phi_enc3d) + np.array(err_enc3d),
                 alpha=0.2, color='steelblue')
ax3.fill_between(np_arr,
                 np.array(phi_enc2d) - np.array(err_enc2d),
                 np.array(phi_enc2d) + np.array(err_enc2d),
                 alpha=0.2, color='darkorange')
ax3.axhline(0.67, ls='--', color='black', lw=1,
            label='2D floor ~0.67 (Finding 8)')
ax3.set_xlabel('Number of predators')
ax3.set_ylabel('Order parameter Phi')
ax3.set_title('3D vs 2D encirclement floor\nSame R_enc=%.2f, N=%d, v0=%.2f' % (
             RENC_DEFAULT, N, V0_PRY))
ax3.legend(fontsize=8); ax3.set_ylim(0, 1.05); ax3.grid(alpha=0.3)

fig.suptitle(
    'Finding 43: 3D predator strategies -- encirclement in [0,1]^3\n'
    'N=%d  rf=%.2f  v0_prey=%.2f  ramp=%.1f  N_SEEDS=%d  N_ITER=%d' % (
    N, RF_3D, V0_PRY, RAMP, N_SEEDS, N_ITER),
    fontsize=10)
plt.tight_layout()
plt.savefig('figures/flocking3d_predator_1.png', dpi=120)
plt.close()
print()
print('  --> figures/flocking3d_predator_1.png')
