# flocking3d_strategy.py -- 3D predator arrangement and the F44 compression mechanism
#                           (Finding 49)
#
# Findings 43-45 established that encirclement fails in 3D and cannot be rescued by
# radius, predator count, or adaptive geometry. Finding 44 proposed a specific
# mechanism: adding predators compresses the flock (Rg falls), but in 3D that
# compression DENSIFIES the flock -- packs more neighbors within each agent's
# alignment radius -- which strengthens the alignment coupling and makes the flock
# MORE coherent rather than dividing it.
#
# That mechanism makes a direct, testable prediction: under 3D encirclement the
# mean alignment-neighbor count <k_align> (agents within r_f) should RISE as
# predators are added, and Phi should track <k_align> rather than Rg. This script
# measures <k_align> alongside Phi and Rg to verify the claim.
#
# It also tests one alternative to the F43 spherical predator arrangement. The
# F43/F44 predators sit on a Fibonacci sphere; the report argues a sphere is
# intrinsically harder to seal than a 2D ring. A "planar" arrangement places all
# predators on a ring in the z = z_com plane -- recreating the 2D encirclement
# geometry inside the 3D flock. If sphere-vs-ring coverage geometry is really the
# bottleneck, planar should disrupt more than spherical at the same n_pred. If
# planar also fails, 3D robustness is deeper than coverage.
#
# Run with:  python 3d/flocking3d_strategy.py

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
import os
import time

os.makedirs('figures', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

# ---------------------------------------------------------------------------
# Parameters (matched to flocking3d_predator_scaling.py, F44)
# ---------------------------------------------------------------------------
N        = 350
N_SEEDS  = 5
N_ITER   = 5000
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

NPRED_VALS   = [6, 10, 20]
RENC_DEFAULT = 0.15


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


def planar_ring(n):
    """n directions evenly spaced on a ring in the z=0 plane."""
    ang = 2.0 * np.pi * np.arange(n) / n
    return np.column_stack([np.cos(ang), np.sin(ang), np.zeros(n)])


class Pred3D:
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


def run_3d(n_pred, mode, seed):
    """mode: 'sphere' (Fibonacci sphere) or 'planar' (ring in z=0 plane)."""
    np.random.seed(seed)
    pos = np.random.uniform(0., 1., (3, N))
    raw = np.random.randn(3, N)
    raw /= np.sqrt((raw**2).sum(axis=0))
    vel = V0_PRY * raw

    dirs = fibonacci_sphere(n_pred) if mode == 'sphere' else planar_ring(n_pred)
    preds = [Pred3D(dirs[k], RENC_DEFAULT, seed*100 + k) for k in range(n_pred)]

    phi_vals, rg_vals, kalign_vals = [], [], []

    for stp in range(N_ITER):
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
        for pred in preds:
            fp = pred.force_on_prey(pos)
            fx += fp[0]; fy += fp[1]; fz += fp[2]

        vel[0] += fx * 0.01; vel[1] += fy * 0.01; vel[2] += fz * 0.01
        pos = (pos + vel * 0.01) % 1.0

        for pred in preds:
            pred.step(c, 0.01)

        if stp >= N_WARMUP:
            phi_vals.append(order_param3d(vel))
            rg_vals.append(rg3d(pos, c))
            kalign_vals.append(float(flock_mask.sum(axis=1).mean()))

    return (float(np.mean(phi_vals)), float(np.mean(rg_vals)),
            float(np.mean(kalign_vals)))


# ---------------------------------------------------------------------------
if __name__ == '__main__':
    print('Finding 49 -- 3D predator arrangement and the compression mechanism')
    print('  N=%d  seeds=%d  iter=%d  R_enc=%.2f' % (
          N, N_SEEDS, N_ITER, RENC_DEFAULT))
    print('  n_pred:', NPRED_VALS, ' modes: sphere, planar')
    print()
    t0 = time.time()

    results = {}
    for mode in ('sphere', 'planar'):
        for npv in NPRED_VALS:
            phis, rgs, ks = [], [], []
            ts = time.time()
            for s in range(N_SEEDS):
                phi, rg, ka = run_3d(npv, mode, s)
                phis.append(phi); rgs.append(rg); ks.append(ka)
            results[(mode, npv)] = (np.mean(phis), np.std(phis),
                                    np.mean(rgs), np.mean(ks))
            print('  %-7s n_pred=%2d  Phi=%.3f+/-%.3f  Rg=%.3f  <k_align>=%.1f  [%.0fs]' % (
                  mode, npv, results[(mode, npv)][0], results[(mode, npv)][1],
                  results[(mode, npv)][2], results[(mode, npv)][3],
                  time.time() - ts), flush=True)

    print()
    print('Total runtime: %.1f min' % ((time.time() - t0)/60.0))

    # --- Figure ---
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    nps = np.array(NPRED_VALS, dtype=float)

    ax = axes[0]
    for mode, col in (('sphere', 'C0'), ('planar', 'C1')):
        ph = [results[(mode, n)][0] for n in NPRED_VALS]
        pe = [results[(mode, n)][1] for n in NPRED_VALS]
        ax.errorbar(nps, ph, yerr=pe, marker='o', capsize=3, color=col,
                    label=mode)
    ax.axhline(0.67, color='gray', ls='--', label='2D floor')
    ax.set_xlabel('Predator count n_pred')
    ax.set_ylabel('Steady-state Phi')
    ax.set_title('Spherical vs planar predator arrangement')
    ax.set_ylim(0.0, 1.05); ax.legend(); ax.grid(alpha=0.3)

    ax2 = axes[1]
    for mode, col in (('sphere', 'C0'), ('planar', 'C1')):
        ka = [results[(mode, n)][3] for n in NPRED_VALS]
        ax2.plot(nps, ka, marker='s', color=col, label='%s <k_align>' % mode)
    ax2.set_xlabel('Predator count n_pred')
    ax2.set_ylabel('Mean alignment-neighbor count <k_align>')
    ax2.set_title('Compression mechanism (F44):\ndensification vs predator count')
    ax2.legend(); ax2.grid(alpha=0.3)

    fig.suptitle('Finding 49 -- 3D predator arrangement and compression')
    fig.tight_layout()
    fig.savefig('figures/finding49_3d_strategy.png', dpi=140)
    print('  -> figures/finding49_3d_strategy.png')

    with open('outputs/finding49_3d_strategy.txt', 'w') as f:
        f.write('Finding 49 -- 3D predator arrangement and compression mechanism\n')
        f.write('N=%d seeds=%d iter=%d R_enc=%.2f\n\n' % (
                N, N_SEEDS, N_ITER, RENC_DEFAULT))
        f.write('mode     n_pred  Phi_mean  Phi_std  Rg     <k_align>\n')
        for mode in ('sphere', 'planar'):
            for n in NPRED_VALS:
                r = results[(mode, n)]
                f.write('%-7s  %4d   %.4f   %.4f  %.4f  %.2f\n' % (
                        mode, n, r[0], r[1], r[2], r[3]))
    print('  -> outputs/finding49_3d_strategy.txt')
