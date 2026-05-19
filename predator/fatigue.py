# fatigue.py -- Does prey fatigue make encirclement damage irreversible? (Finding 53)
#
# Finding 22 established that encirclement damage is fully reversible: when the
# predators are removed, the divided sub-flocks reunite within ~10 time units and
# Phi returns to ~1. Finding 26 reinforced this -- kinematic damage reverses fast,
# only contagion (which writes a persistent internal panic flag) outlasts the
# stressor. But both rest on an assumption: that prey agents have NO internal
# state. A real animal under sustained predator pressure fatigues.
#
# This experiment adds a fatigue variable Q_i in [0,1] to each prey agent:
#   - Q rises at rate r_fat while the agent is "stressed" (within a predator's
#     repulsion range), and recovers at a fixed rate r_rec otherwise.
#   - Fatigue impairs one faculty, and the experiment tests TWO modes:
#       'speed': effective cruise speed v0_eff = v0 * (1 - Q)   -- the agent
#                tires and cannot thrust.
#       'align': effective alignment alpha_eff = alpha * (1 - Q) -- the agent
#                disengages and stops tracking its neighbors.
#
# The two modes are predicted to differ sharply, on the basis of earlier findings.
# Finding 24 showed that a v0 contrast does NOT segregate the flock -- the
# alignment force homogenises group speed, carrying slow agents along. So fatigue
# in 'speed' mode should be harmless: the flock carries its tired members and
# Finding 22 reversibility survives. Finding 27, by contrast, showed that an alpha
# contrast DOES segregate the flock via local clustering. So fatigue in 'align'
# mode should be able to make encirclement damage irreversible -- disengaged
# agents segregate out and fail to rejoin.
#
# Protocol: warmup -> encirclement (predators present) -> predators removed ->
# recovery observation. The fatigue accumulation rate r_fat is swept for each
# mode. At r_fat = 0 both modes reduce to F22 (full recovery expected). The
# deliverable is the recovery-Phi vs r_fat curve for each mode.
#
# Run with:  python predator/fatigue.py

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
import os
import time

os.makedirs('figures', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

# ---------------------------------------------------------------------------
# Parameters (2D slow-prey encirclement regime)
# ---------------------------------------------------------------------------
N        = 350
N_SEEDS  = 5
DT       = 0.01

R0     = 0.005
RF     = 0.10
ALPHA  = 1.0
V0     = 0.02
MU     = 10.0
RAMP   = 0.1
EPS    = 0.1
RB     = 2.0 * R0

V0_PRD  = 0.05
ALPHA_P = 5.0
MU_P    = 10.0
R0_P    = 0.10
EPS_P   = 2.0
RAMP_P  = 1.0

N_PRED   = 10
RENC_RATIO = 0.5         # R_enc set to RENC_RATIO * (measured flock Rg) -- the
                         # F23 universal disruption optimum -- so encirclement
                         # always engages regardless of the settled flock size
BLOB_SIGMA = 0.05        # compact-blob initialisation: prey start clustered, not
                         # spread uniformly (the model has no cohesion force)

N_WARMUP = 3000
N_ENC    = 6000          # 60 time units of encirclement
N_REC    = 6000          # 60 time units of recovery after predator removal

R_REC    = 0.01          # fatigue recovery rate (per time unit), fixed --
                         # slow, so accumulated fatigue persists through the
                         # ~120 tu experiment rather than clearing instantly
R_FAT_VALS = [0.0, 0.05, 0.1, 0.2, 0.4, 0.8]   # fatigue accumulation rate sweep


def periodic_com(a):
    a2 = 2*np.pi*a
    return np.arctan2(np.sin(a2).mean(), np.cos(a2).mean()) / (2*np.pi) % 1.0


def order_param(vx, vy):
    sp = np.maximum(np.sqrt(vx**2+vy**2), 1e-12)
    return float(np.sqrt((vx/sp).mean()**2 + (vy/sp).mean()**2))


class EncPred:
    def __init__(self, angle, enc_radius, seed):
        rng = np.random.default_rng(seed)
        self.x, self.y = rng.uniform(0,1), rng.uniform(0,1)
        a = rng.uniform(0, 2*np.pi)
        self.vx, self.vy = V0_PRD*np.cos(a), V0_PRD*np.sin(a)
        self.dirx, self.diry = np.cos(angle), np.sin(angle)
        self.enc_radius = enc_radius

    def target(self, cx, cy):
        return ((cx + self.enc_radius*self.dirx) % 1.0,
                (cy + self.enc_radius*self.diry) % 1.0)

    def step(self, cx, cy):
        tx, ty = self.target(cx, cy)
        dx = tx - self.x; dy = ty - self.y
        dx -= round(dx); dy -= round(dy)
        dist = np.hypot(dx, dy) + 1e-12
        spd = np.hypot(self.vx, self.vy) + 1e-12
        self.vx += (ALPHA_P*dx/dist + MU_P*(V0_PRD-spd)*self.vx/spd
                    + RAMP_P*np.random.uniform(-1,1)) * DT
        self.vy += (ALPHA_P*dy/dist + MU_P*(V0_PRD-spd)*self.vy/spd
                    + RAMP_P*np.random.uniform(-1,1)) * DT
        self.x = (self.x + self.vx*DT) % 1.0
        self.y = (self.y + self.vy*DT) % 1.0

    def force_on_prey(self, x, y):
        dx = x - self.x; dy = y - self.y
        dx -= np.round(dx); dy -= np.round(dy)
        dist = np.sqrt(dx**2 + dy**2)
        in_r = (dist > 0) & (dist <= R0_P)
        base = np.maximum(1.0 - dist/R0_P, 0.0)
        st = np.where(in_r, EPS_P * base**1.5 / (dist+1e-12), 0.0)
        # push prey away from predator (dx,dy = prey - pred)
        return st*dx, st*dy, in_r


def run(r_fat, mode, seed):
    """mode: 'speed' (fatigue cuts v0) or 'align' (fatigue cuts alpha).
    Return (Phi_enc_end, Phi_rec_end, Q_enc_end, Q_rec_end)."""
    np.random.seed(seed)
    # compact-blob initialisation: the model has no cohesion force, so a uniform
    # start would leave the flock spatially diffuse and un-encirclable
    x = (0.5 + np.random.normal(0, BLOB_SIGMA, N)) % 1.0
    y = (0.5 + np.random.normal(0, BLOB_SIGMA, N)) % 1.0
    vx = np.random.uniform(-1,1,N)*V0; vy = np.random.uniform(-1,1,N)*V0
    Q = np.zeros(N)
    not_self = ~np.eye(N, dtype=bool)

    angles = 2*np.pi*np.arange(N_PRED)/N_PRED
    preds = None

    phi_enc = phi_rec = q_enc = q_rec = 0.0
    total = N_WARMUP + N_ENC + N_REC

    for step in range(total):
        if step == N_WARMUP:
            # measure the settled flock Rg, place predators at R_enc = 0.5*Rg
            cx0, cy0 = periodic_com(x), periodic_com(y)
            rx = x - cx0; ry = y - cy0
            rx -= np.round(rx); ry -= np.round(ry)
            rg0 = np.sqrt((rx**2 + ry**2).mean())
            renc = RENC_RATIO * rg0
            preds = [EncPred(angles[k], renc, seed*100+k) for k in range(N_PRED)]
        if step == N_WARMUP + N_ENC:
            preds = None   # predators removed

        dx = x[np.newaxis,:]-x[:,np.newaxis]; dy = y[np.newaxis,:]-y[:,np.newaxis]
        dx -= np.round(dx); dy -= np.round(dy)
        d2 = dx**2 + dy**2

        rep = (d2 <= RB**2) & not_self & (d2 > 0)
        ds = np.where(rep, np.sqrt(d2), 1.0)
        br = np.maximum(np.where(rep, 1.0-ds/RB, 0.0), 0.0)
        st = np.where(rep, EPS*br**1.5/ds, 0.0)
        fx = (-st*dx).sum(1); fy = (-st*dy).sum(1)

        # fatigue impairs either alignment (alpha) or speed (v0), per mode
        alpha_eff = ALPHA * (1.0 - Q) if mode == 'align' else np.full(N, ALPHA)
        v0_eff    = V0 * (1.0 - Q)    if mode == 'speed' else np.full(N, V0)

        fm = (d2 <= RF**2) & not_self
        svx = (vx[np.newaxis,:]*fm).sum(1); svy = (vy[np.newaxis,:]*fm).sum(1)
        nrm = np.sqrt(svx**2+svy**2); has = fm.sum(1) > 0
        safe = np.where(has, nrm, 1.0)
        fx += np.where(has, alpha_eff*svx/safe, 0.0)
        fy += np.where(has, alpha_eff*svy/safe, 0.0)

        # self-propulsion (cruise speed reduced by fatigue in 'speed' mode)
        spd = np.maximum(np.sqrt(vx**2+vy**2), 1e-12)
        prop = MU*(v0_eff - spd)/spd
        fx += prop*vx; fy += prop*vy

        fx += RAMP*np.random.uniform(-1,1,N)
        fy += RAMP*np.random.uniform(-1,1,N)

        stressed = np.zeros(N, dtype=bool)
        if preds is not None:
            cx, cy = periodic_com(x), periodic_com(y)
            for p in preds:
                pfx, pfy, in_r = p.force_on_prey(x, y)
                fx += pfx; fy += pfy
                stressed |= in_r
            for p in preds:
                p.step(cx, cy)

        # fatigue update
        dQ = np.where(stressed, r_fat, -R_REC) * DT
        Q = np.clip(Q + dQ, 0.0, 1.0)

        vx += fx*DT; vy += fy*DT
        x = (x + vx*DT) % 1.0; y = (y + vy*DT) % 1.0

        if step == N_WARMUP + N_ENC - 1:
            phi_enc = order_param(vx, vy); q_enc = float(Q.mean())
        if step == total - 1:
            phi_rec = order_param(vx, vy); q_rec = float(Q.mean())

    return phi_enc, phi_rec, q_enc, q_rec


if __name__ == '__main__':
    print('Finding 53 -- prey fatigue and the reversibility of encirclement')
    print('  N=%d  n_pred=%d  R_enc=%.2f  seeds=%d' % (N, N_PRED, R_ENC, N_SEEDS))
    print('  encirclement %d steps, recovery %d steps; r_rec=%.2f' % (
          N_ENC, N_REC, R_REC))
    print('  r_fat sweep: %s   modes: speed, align' % R_FAT_VALS)
    print()
    t0 = time.time()

    results = {}   # (mode, r_fat) -> (Phi_enc, Phi_rec, Phi_rec_std, Q_enc, Q_rec)
    for mode in ('speed', 'align'):
        for rf in R_FAT_VALS:
            pe, pr, qe, qr = [], [], [], []
            ts = time.time()
            for s in range(N_SEEDS):
                a, b, c, d = run(rf, mode, s)
                pe.append(a); pr.append(b); qe.append(c); qr.append(d)
            results[(mode, rf)] = (np.mean(pe), np.mean(pr), np.std(pr),
                                   np.mean(qe), np.mean(qr))
            print('  %-6s r_fat=%.2f  Phi_enc=%.3f  Phi_recovered=%.3f+/-%.3f  '
                  'Q_enc=%.3f  Q_rec=%.3f  [%.0fs]' % (
                  mode, rf, results[(mode,rf)][0], results[(mode,rf)][1],
                  results[(mode,rf)][2], results[(mode,rf)][3],
                  results[(mode,rf)][4], time.time()-ts), flush=True)
        print()

    print('Total runtime: %.1f min' % ((time.time()-t0)/60.0))

    rfs = np.array(R_FAT_VALS)
    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    for mode, col in (('speed', 'steelblue'), ('align', 'crimson')):
        pr = np.array([results[(mode,r)][1] for r in R_FAT_VALS])
        pe = np.array([results[(mode,r)][2] for r in R_FAT_VALS])
        ax.errorbar(rfs, pr, yerr=pe, marker='o', capsize=4, color=col,
                    label='%s-mode: Phi recovered' % mode)
    ax.axhline(0.95, ls=':', color='gray', label='full-recovery level')
    ax.set_xlabel('Fatigue accumulation rate r_fat (per time unit)')
    ax.set_ylabel('Phi recovered (60 tu after predator removal)')
    ax.set_title('Finding 53 -- prey fatigue vs encirclement reversibility\n'
                 'speed-fatigue vs alignment-fatigue')
    ax.set_ylim(0, 1.05)
    ax.legend(fontsize=9); ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig('figures/finding53_fatigue.png', dpi=140)
    print('  -> figures/finding53_fatigue.png')

    with open('outputs/finding53_fatigue.txt', 'w') as f:
        f.write('Finding 53 -- prey fatigue and encirclement reversibility\n')
        f.write('N=%d n_pred=%d R_enc=%.2f seeds=%d r_rec=%.2f\n\n' % (
                N, N_PRED, R_ENC, N_SEEDS, R_REC))
        for mode in ('speed', 'align'):
            f.write('mode=%s:\n' % mode)
            f.write('  r_fat  Phi_enc  Phi_recovered  Q_enc  Q_rec\n')
            for r in R_FAT_VALS:
                v = results[(mode, r)]
                f.write('  %.2f   %.4f   %.4f         %.4f  %.4f\n' % (
                        r, v[0], v[1], v[3], v[4]))
            f.write('\n')
    print('  -> outputs/finding53_fatigue.txt')
