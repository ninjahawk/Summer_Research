# langevin_hexatic_hard.py -- Langevin + hexatic with HARD repulsion (Finding 50)
#
# Finding 40 measured the hexatic order parameter |psi6| under a Langevin thermostat
# and found that the n = 1.5 soft repulsion cannot crystallize at any temperature:
# |psi6| stayed flat at ~0.4 across the entire kT range, with no solid-phase value
# near 1 and no N-dependent susceptibility peak. F40 closed with an explicit
# recommendation: "Demonstrating the KTHNY transition in this model family requires
# a near-hard-core Langevin simulation (n >= 12)."
#
# This experiment runs exactly that. It repeats the F40 Langevin + hexatic
# finite-size-scaling protocol with hard repulsion exponents n = 12 and n = 24, at
# two dense packing fractions (C = 0.70 and C = 0.85). The question is whether a
# harder contact potential -- one that resists core overlap far more steeply than
# n = 1.5 -- finally produces a crystalline solid at low kT and a KTHNY-type
# melting signature.
#
# KTHNY signatures to look for:
#   - |psi6| -> ~1 at low kT (hexagonal solid) and -> ~0 at high kT (fluid),
#     instead of the flat ~0.4 of the soft potential;
#   - chi_psi6 = N * Var(|psi6|) peaking at a finite kT_c;
#   - the peak growing with N (and kT_c drifting) -- finite-size scaling of a
#     genuine transition rather than a smooth crossover.
#
# If even n = 24 at C = 0.85 stays flat, the result is definitive: this force-based
# model family cannot crystallize, and the phase-transition thread closes negatively.
#
# Run with:  python phase/langevin_hexatic_hard.py

import os
import numpy as np
import matplotlib.pyplot as plt
import time

os.makedirs('figures', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

N_VALS    = [50, 100, 200]
KT_VALS   = [0.002, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0]
EXP_VALS  = [12.0, 24.0]
C_VALS    = [0.70, 0.85]
N_SEEDS   = 6
N_ITER    = 12000          # equilibration; measure last quarter
DT        = 0.01
MU        = 10.0
EPS0      = 0.1


def run_langevin_hex(N, kT, seed, C, exp_n):
    """Langevin dynamics with hard repulsion. Return (mean KE/N, mean|psi6|, std|psi6|)."""
    np.random.seed(seed)
    r0 = np.sqrt(C / (np.pi * N))
    rb = 2.0 * r0
    r_nbr = 3.0 * r0

    noise_std = np.sqrt(2.0 * MU * kT * DT)

    x = np.zeros(2 * N)
    x[:N] = np.random.uniform(0., 1., N)
    x[N:] = np.random.uniform(0., 1., N)
    v_init = np.sqrt(kT) if kT > 0 else 0.0
    vx = v_init * np.random.randn(N)
    vy = v_init * np.random.randn(N)

    psi6_series, ke_series = [], []
    measure_start = (3 * N_ITER) // 4

    for step in range(N_ITER):
        nx = x[:N]; ny = x[N:]
        real_dx = nx[np.newaxis, :] - nx[:, np.newaxis]
        real_dy = ny[np.newaxis, :] - ny[:, np.newaxis]
        real_dx -= np.round(real_dx); real_dy -= np.round(real_dy)
        d2 = real_dx**2 + real_dy**2
        not_self = ~np.eye(N, dtype=bool)

        rep_mask = (d2 <= rb**2) & not_self & (d2 > 0)
        d_safe   = np.where(rep_mask, np.sqrt(d2), 1.0)
        base_r   = np.maximum(np.where(rep_mask, 1.0 - d_safe / rb, 0.0), 0.0)
        strength = np.where(rep_mask, EPS0 * (base_r ** exp_n) / d_safe, 0.0)
        repx = (-strength * real_dx).sum(axis=1)
        repy = (-strength * real_dy).sum(axis=1)

        damp_x = -MU * vx; damp_y = -MU * vy
        frandx = noise_std * np.random.randn(N) / DT
        frandy = noise_std * np.random.randn(N) / DT

        vx += (repx + damp_x + frandx) * DT
        vy += (repy + damp_y + frandy) * DT
        x[:N] = (x[:N] + vx * DT) % 1.0
        x[N:] = (x[N:] + vy * DT) % 1.0

        if step >= measure_start:
            ke_series.append(0.5 * (vx**2 + vy**2).mean())
            nbr_mask = (d2 <= r_nbr**2) & not_self
            angles = np.where(nbr_mask, np.arctan2(real_dy, real_dx), 0.0)
            cos6 = np.where(nbr_mask, np.cos(6.0 * angles), 0.0).sum(axis=1)
            sin6 = np.where(nbr_mask, np.sin(6.0 * angles), 0.0).sum(axis=1)
            k_j  = nbr_mask.sum(axis=1).clip(min=1)
            psi6_abs = np.sqrt((cos6 / k_j)**2 + (sin6 / k_j)**2)
            psi6_series.append(psi6_abs.mean())

    return np.mean(ke_series), np.mean(psi6_series), np.std(psi6_series)


if __name__ == '__main__':
    print('Finding 50 -- Langevin + hexatic with HARD repulsion (n=12, 24)')
    print('  C_vals=%s  exponents=%s  mu=%.1f' % (C_VALS, EXP_VALS, MU))
    print('  N=%s  kT=%s  seeds=%d' % (N_VALS, KT_VALS, N_SEEDS))
    print()
    t0 = time.time()

    # results[(exp,C,N,kT)] = (ke_mean, ke_std, psi6_mean, psi6_std)
    results = {}
    for exp_n in EXP_VALS:
        for C in C_VALS:
            for N in N_VALS:
                tc = time.time()
                for kT in KT_VALS:
                    ke_v, psi6_v = [], []
                    for s in range(N_SEEDS):
                        ke, pm, ps = run_langevin_hex(N, kT, s, C, exp_n)
                        ke_v.append(ke); psi6_v.append(pm)
                    results[(exp_n, C, N, kT)] = (np.mean(ke_v), np.std(ke_v),
                                                  np.mean(psi6_v), np.std(psi6_v))
                print('  n=%2d C=%.2f N=%3d done [%.0fs]' % (
                      exp_n, C, N, time.time() - tc), flush=True)

    print('\nTotal runtime: %.1f min' % ((time.time() - t0)/60.0))
    print()
    print('=== Summary: mean|psi6| at low/high kT and chi_psi6 peak ===')
    print('  KTHNY signature: psi6(low kT)~1, psi6(high kT)~0, chi_psi6 peak grows with N')
    print()
    for exp_n in EXP_VALS:
        for C in C_VALS:
            print('n=%d  C=%.2f:' % (exp_n, C))
            for N in N_VALS:
                psi6_means = np.array([results[(exp_n,C,N,kT)][2] for kT in KT_VALS])
                psi6_stds  = np.array([results[(exp_n,C,N,kT)][3] for kT in KT_VALS])
                chi = N * psi6_stds**2
                pk = int(np.argmax(chi))
                print('  N=%3d: psi6(kT=%.3f)=%.3f  psi6(kT=%.1f)=%.3f  '
                      'chi_peak=%.4f at kT=%.3f' % (
                      N, KT_VALS[0], psi6_means[0], KT_VALS[-1], psi6_means[-1],
                      chi[pk], KT_VALS[pk]))
            print()

    # --- Figure: rows = (exp,C) combos, cols = (mean psi6, chi_psi6) ---
    combos = [(e, c) for e in EXP_VALS for c in C_VALS]
    fig, axes = plt.subplots(len(combos), 2, figsize=(11, 4.2*len(combos)))
    colors = {50: 'seagreen', 100: 'darkorange', 200: 'crimson'}
    kT_arr = np.array(KT_VALS)

    for row, (exp_n, C) in enumerate(combos):
        ax_psi, ax_chi = axes[row, 0], axes[row, 1]
        for N in N_VALS:
            pm = np.array([results[(exp_n,C,N,kT)][2] for kT in KT_VALS])
            ps = np.array([results[(exp_n,C,N,kT)][3] for kT in KT_VALS])
            chi = N * ps**2
            ax_psi.errorbar(kT_arr, pm, yerr=ps/np.sqrt(N_SEEDS), marker='o',
                            color=colors[N], ms=4, capsize=3, label='N=%d' % N)
            ax_chi.plot(kT_arr, chi, marker='o', color=colors[N], ms=5,
                        label='N=%d' % N)
        ax_psi.set_xscale('log'); ax_psi.set_ylim(0, 1.05)
        ax_psi.set_xlabel('Temperature kT'); ax_psi.set_ylabel('mean |psi6|')
        ax_psi.set_title('n=%d C=%.2f: hexatic order (1=solid,0=fluid)' % (exp_n, C))
        ax_psi.legend(fontsize=8); ax_psi.grid(alpha=0.3)
        ax_chi.set_xscale('log')
        ax_chi.set_xlabel('Temperature kT'); ax_chi.set_ylabel('chi_psi6 = N*Var(psi6)')
        ax_chi.set_title('n=%d C=%.2f: hexatic susceptibility' % (exp_n, C))
        ax_chi.legend(fontsize=8); ax_chi.grid(alpha=0.3)

    fig.suptitle('Finding 50 -- Langevin + hexatic with hard repulsion (n=12, 24)\n'
                 'Does a near-hard-core potential produce KTHNY crystallization?',
                 fontsize=11)
    fig.tight_layout()
    fig.savefig('figures/finding50_langevin_hexatic_hard.png', dpi=130)
    print('  -> figures/finding50_langevin_hexatic_hard.png')

    with open('outputs/finding50_langevin_hexatic_hard.txt', 'w') as f:
        f.write('Finding 50 -- Langevin + hexatic with hard repulsion\n')
        f.write('exponents=%s C=%s N=%s seeds=%d iter=%d\n\n' % (
                EXP_VALS, C_VALS, N_VALS, N_SEEDS, N_ITER))
        for exp_n in EXP_VALS:
            for C in C_VALS:
                f.write('n=%d C=%.2f:\n' % (exp_n, C))
                f.write('  N    psi6(loT)  psi6(hiT)  chi_peak  kT_peak\n')
                for N in N_VALS:
                    pm = np.array([results[(exp_n,C,N,kT)][2] for kT in KT_VALS])
                    ps = np.array([results[(exp_n,C,N,kT)][3] for kT in KT_VALS])
                    chi = N * ps**2
                    pk = int(np.argmax(chi))
                    f.write('  %3d  %.4f     %.4f     %.4f    %.3f\n' % (
                            N, pm[0], pm[-1], chi[pk], KT_VALS[pk]))
                f.write('\n')
    print('  -> outputs/finding50_langevin_hexatic_hard.txt')
