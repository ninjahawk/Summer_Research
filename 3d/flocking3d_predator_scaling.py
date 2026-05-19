# flocking3d_predator_scaling.py -- 3D predator-count scaling (Finding 44, PLANNED)
#
# Question.  Finding 43 showed that 3D encirclement at n_pred = 6 leaves Phi ~ 0.95,
# far above the 2D floor of ~0.67.  The proposed mechanism is geometric: 6 predators
# on a sphere cover ~2*pi steradians out of 4*pi (half-coverage), so the flock escapes
# through the uncovered solid angle.  Prediction: closing off the 3D sphere requires
# n_pred ~ 6x larger than 2D, because the angular-coverage requirement scales as
# solid angle (4*pi sr) rather than arc length (2*pi rad).
#
# Specifically: in 2D, 6 predators at 60-degree spacing leave a per-predator angular
# gap of ~60 deg ~ 1 rad.  In 3D, achieving the same per-predator solid-angle gap
# (~1 sr) requires n_pred ~ 4*pi/1 ~ 13.  Matching the 2D Phi floor (~0.67) may
# require even more.  This script sweeps n_pred = 1, 3, 6, 10, 20, 50 and measures
# the disruption floor in 3D.
#
# Expected results:
#   n_pred =  1  Phi ~ 1.0   (single predator never disrupts in 3D either)
#   n_pred =  6  Phi ~ 0.95  (reproduces F43)
#   n_pred = 13  Phi ~ 0.85  (geometric prediction crossover)
#   n_pred = 20  Phi ~ 0.75  (approaching 2D-equivalent coverage)
#   n_pred = 50  Phi ~ 0.65  (matches/exceeds 2D floor)
#
# Runtime estimate: ~6 n_pred * 5 seeds * 5000 steps * N=350 in 3D.  Roughly 30-60
# minutes on a modern laptop.  Run with:  python 3d/flocking3d_predator_scaling.py

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
import os
import time

os.makedirs('figures', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

# ---------------------------------------------------------------------------
# Simulation parameters (matched to flocking3d_predator.py for direct comparison)
# ---------------------------------------------------------------------------
N          = 350
N_SEEDS    = 5
N_ITER     = 5000
N_WARMUP   = 3000

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

NPRED_VALS   = [1, 3, 6, 10, 20, 50]
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


def run_3d(n_pred, enc_radius, seed):
    np.random.seed(seed)
    pos = np.random.uniform(0., 1., (3, N))
    raw = np.random.randn(3, N)
    raw /= np.sqrt((raw**2).sum(axis=0))
    vel = V0_PRY * raw

    directions = fibonacci_sphere(n_pred)
    preds = [Pred3D(directions[k], enc_radius, seed*100 + k) for k in range(n_pred)]

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
        for pred in preds:
            fp = pred.force_on_prey(pos)
            fx += fp[0]; fy += fp[1]; fz += fp[2]

        vel[0] += fx * 0.01; vel[1] += fy * 0.01; vel[2] += fz * 0.01
        pos = (pos + vel * 0.01) % 1.0

        for pred in preds:
            pred.step(c, 0.01)

        if step >= N_WARMUP:
            phi_vals.append(order_param3d(vel))
            rg_vals.append(rg3d(pos, c))

    return float(np.mean(phi_vals)), float(np.mean(rg_vals))


# ---------------------------------------------------------------------------
# Predator-count scaling sweep
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    print('Finding 44 -- 3D predator-count scaling')
    print('  N=%d  seeds=%d  iter=%d  warmup=%d  R_enc=%.2f' % (
          N, N_SEEDS, N_ITER, N_WARMUP, RENC_DEFAULT))
    print('  n_pred values:', NPRED_VALS)
    print()

    results = {}
    t0 = time.time()
    for np_ in NPRED_VALS:
        phi_list, rg_list = [], []
        ts = time.time()
        for s in range(N_SEEDS):
            phi, rg = run_3d(np_, RENC_DEFAULT, s)
            phi_list.append(phi); rg_list.append(rg)
        results[np_] = (np.mean(phi_list), np.std(phi_list),
                        np.mean(rg_list), np.std(rg_list))
        print('  n_pred=%2d  Phi=%.3f+/-%.3f  Rg=%.3f+/-%.3f  [%.0fs]' % (
              np_, *results[np_], time.time() - ts))

    print('\nTotal runtime: %.1f min' % ((time.time() - t0)/60.0))

    # Save figure
    nps = np.array(NPRED_VALS, dtype=float)
    phi_mean = np.array([results[n][0] for n in NPRED_VALS])
    phi_std  = np.array([results[n][1] for n in NPRED_VALS])

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.errorbar(nps, phi_mean, yerr=phi_std, marker='o', capsize=3,
                color='C0', label='3D, R_enc = %.2f' % RENC_DEFAULT)
    ax.axhline(0.67, color='C1', ls='--', label='2D floor (Phi ~ 0.67)')
    ax.set_xscale('log')
    ax.set_xlabel('Predator count n_pred')
    ax.set_ylabel('Steady-state Phi')
    ax.set_title('3D encirclement scaling (Finding 44)')
    ax.set_ylim(0.0, 1.05)
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig('figures/finding44_3d_predator_scaling.png', dpi=140)
    print('  -> figures/finding44_3d_predator_scaling.png')

    # Save raw data
    with open('outputs/finding44_3d_predator_scaling.txt', 'w') as f:
        f.write('Finding 44 -- 3D predator-count scaling\n')
        f.write('N=%d seeds=%d iter=%d R_enc=%.2f\n\n' % (
                N, N_SEEDS, N_ITER, RENC_DEFAULT))
        f.write('n_pred  Phi_mean  Phi_std  Rg_mean  Rg_std\n')
        for n in NPRED_VALS:
            f.write('%6d  %.4f    %.4f   %.4f   %.4f\n' % (n, *results[n]))
    print('  -> outputs/finding44_3d_predator_scaling.txt')
