# mixing_dimension.py -- Direct 2D vs 3D kinematic-mixing rate (Finding 52)
#
# Across Findings 46-51 a theme emerged: the third spatial dimension acts as a
# "mixing aid." The vaccination null results transfer to 3D unchanged (F46), and
# alpha-contrast segregation is DILUTED in 3D relative to 2D (F51). The report's
# Section 4.33 and Conclusion 24 state this as an established theme.
#
# But the theme rests on an inference, not a direct measurement. F47 measured the
# 2D contact-graph mixing rate (Jaccard turnover ~0.037 per 2 time units); the 3D
# mixing rate has never been measured directly. F51's segregation dilution could
# in principle be a geometric packing effect rather than faster mixing. This
# experiment closes that gap: it measures the contact-graph mixing rate directly
# in 2D and in 3D, under matched conditions, so the "mixing aid" claim is verified
# (or falsified) rather than assumed.
#
# Method. Pure flocks (no predators, no contagion), 2D and 3D, at the parameters
# of the respective vaccination experiments (2D: rf=0.10, r0=0.005; 3D: rf=0.20,
# r0=0.02; both N=350, v0=0.02). The contact radius is calibrated separately in
# each dimension so the mean contact degree matches (~8, as in F46/F47). Mixing is
# the mean Jaccard dissimilarity of each agent's contact-neighbor set between
# snapshots two time units apart. The noise amplitude (ramp) is swept so the
# comparison is not a single-point coincidence.
#
# If 3D mixing exceeds 2D mixing at matched degree, the "mixing aid" theme is
# confirmed. If not, the report's Section 4.33 / Conclusion 24 wording must soften.
#
# Run with:  python contagion/mixing_dimension.py

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

import numpy as np
import matplotlib.pyplot as plt
import os
import time

os.makedirs('figures', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

N         = 350
N_SEEDS   = 5
DT        = 0.01
V0        = 0.02
MU        = 10.0
EPS       = 0.1
EXP_N     = 1.5

RF_2D, R0_2D = 0.10, 0.005
RF_3D, R0_3D = 0.20, 0.02
RCONT_2D = 0.05      # gives mean contact degree ~8-9 (F47)
RCONT_3D = 0.155     # calibrated to the same mean degree (F46)

N_WARMUP   = 3000
MIX_STEPS  = 5000
MIX_INT    = 200     # snapshot every 2 time units
RAMP_VALS  = [0.03, 0.1, 0.3, 1.0]


# ---------------------------------------------------------------------------
# 2D flock (minimum-image torus, metric alignment)
# ---------------------------------------------------------------------------
def step2d(x, y, vx, vy, ramp, rng):
    Nn = x.size
    not_self = ~np.eye(Nn, dtype=bool)
    dx = x[np.newaxis,:]-x[:,np.newaxis]; dy = y[np.newaxis,:]-y[:,np.newaxis]
    dx -= np.round(dx); dy -= np.round(dy)
    d2 = dx**2 + dy**2
    rb = 2.0*R0_2D
    rep = (d2 <= rb**2) & not_self & (d2 > 0)
    ds  = np.where(rep, np.sqrt(d2), 1.0)
    br  = np.maximum(np.where(rep, 1.0-ds/rb, 0.0), 0.0)
    st  = np.where(rep, EPS*br**EXP_N/ds, 0.0)
    fx = (-st*dx).sum(1); fy = (-st*dy).sum(1)
    fm = (d2 <= RF_2D**2) & not_self
    svx = (vx[np.newaxis,:]*fm).sum(1); svy = (vy[np.newaxis,:]*fm).sum(1)
    nrm = np.sqrt(svx**2+svy**2); has = fm.sum(1) > 0
    safe = np.where(has, nrm, 1.0)
    fx += np.where(has, svx/safe, 0.0); fy += np.where(has, svy/safe, 0.0)
    spd = np.maximum(np.sqrt(vx**2+vy**2), 1e-12)
    prop = MU*(V0-spd)/spd
    fx += prop*vx; fy += prop*vy
    fx += ramp*rng.uniform(-1.,1.,Nn); fy += ramp*rng.uniform(-1.,1.,Nn)
    vx = vx+fx*DT; vy = vy+fy*DT
    return (x+vx*DT)%1.0, (y+vy*DT)%1.0, vx, vy


def contact_sets_2d(x, y):
    dx = x[np.newaxis,:]-x[:,np.newaxis]; dy = y[np.newaxis,:]-y[:,np.newaxis]
    dx -= np.round(dx); dy -= np.round(dy)
    w = (dx**2+dy**2 <= RCONT_2D**2) & (dx**2+dy**2 > 0)
    return [frozenset(np.where(r)[0]) for r in w], w.sum(1)


def mixing_2d(seed, ramp):
    np.random.seed(seed)
    x = np.random.uniform(0.,1.,N); y = np.random.uniform(0.,1.,N)
    vx = np.random.uniform(-1.,1.,N)*V0; vy = np.random.uniform(-1.,1.,N)*V0
    rng = np.random.default_rng(seed*17+3)
    for _ in range(N_WARMUP):
        x,y,vx,vy = step2d(x,y,vx,vy,ramp,rng)
    prev=None; diss=[]; degs=[]
    for i in range(MIX_STEPS):
        x,y,vx,vy = step2d(x,y,vx,vy,ramp,rng)
        if i % MIX_INT == 0:
            s,d = contact_sets_2d(x,y); degs.append(d.mean())
            if prev is not None:
                v=[]
                for a,b in zip(prev,s):
                    u=len(a|b); v.append(1.0-(len(a&b)/u if u else 1.0))
                diss.append(np.mean(v))
            prev=s
    return float(np.mean(diss)), float(np.mean(degs))


# ---------------------------------------------------------------------------
# 3D flock
# ---------------------------------------------------------------------------
def step3d(pos, vel, ramp, rng):
    Nn = pos.shape[1]
    not_self = ~np.eye(Nn, dtype=bool)
    dx = pos[0,np.newaxis,:]-pos[0,:,np.newaxis]
    dy = pos[1,np.newaxis,:]-pos[1,:,np.newaxis]
    dz = pos[2,np.newaxis,:]-pos[2,:,np.newaxis]
    dx-=np.round(dx); dy-=np.round(dy); dz-=np.round(dz)
    d2 = dx**2+dy**2+dz**2
    rb = 2.0*R0_3D
    rep = (d2 <= rb**2) & not_self & (d2 > 0)
    ds  = np.where(rep, np.sqrt(d2), 1.0)
    br  = np.maximum(np.where(rep, 1.0-ds/rb, 0.0), 0.0)
    st  = np.where(rep, EPS*br**EXP_N/ds, 0.0)
    fx=(-st*dx).sum(1); fy=(-st*dy).sum(1); fz=(-st*dz).sum(1)
    fm = (d2 <= RF_3D**2) & not_self
    svx=(vel[0]*fm).sum(1); svy=(vel[1]*fm).sum(1); svz=(vel[2]*fm).sum(1)
    nrm=np.sqrt(svx**2+svy**2+svz**2); has=fm.sum(1)>0
    safe=np.where(has,nrm,1.0)
    fx+=np.where(has,svx/safe,0.0); fy+=np.where(has,svy/safe,0.0)
    fz+=np.where(has,svz/safe,0.0)
    spd=np.maximum(np.sqrt(vel[0]**2+vel[1]**2+vel[2]**2),1e-12)
    prop=MU*(V0-spd)/spd
    fx+=prop*vel[0]; fy+=prop*vel[1]; fz+=prop*vel[2]
    fx+=ramp*rng.uniform(-1.,1.,Nn); fy+=ramp*rng.uniform(-1.,1.,Nn)
    fz+=ramp*rng.uniform(-1.,1.,Nn)
    vel=vel.copy()
    vel[0]+=fx*DT; vel[1]+=fy*DT; vel[2]+=fz*DT
    return (pos+vel*DT)%1.0, vel


def contact_sets_3d(pos):
    dx=pos[0,np.newaxis,:]-pos[0,:,np.newaxis]
    dy=pos[1,np.newaxis,:]-pos[1,:,np.newaxis]
    dz=pos[2,np.newaxis,:]-pos[2,:,np.newaxis]
    dx-=np.round(dx); dy-=np.round(dy); dz-=np.round(dz)
    rd2=dx**2+dy**2+dz**2
    w=(rd2<=RCONT_3D**2)&(rd2>0)
    return [frozenset(np.where(r)[0]) for r in w], w.sum(1)


def mixing_3d(seed, ramp):
    np.random.seed(seed)
    pos = np.random.uniform(0.,1.,(3,N))
    raw = np.random.randn(3,N); raw/=np.sqrt((raw**2).sum(0))
    vel = V0*raw
    rng = np.random.default_rng(seed*17+3)
    for _ in range(N_WARMUP):
        pos,vel = step3d(pos,vel,ramp,rng)
    prev=None; diss=[]; degs=[]
    for i in range(MIX_STEPS):
        pos,vel = step3d(pos,vel,ramp,rng)
        if i % MIX_INT == 0:
            s,d = contact_sets_3d(pos); degs.append(d.mean())
            if prev is not None:
                v=[]
                for a,b in zip(prev,s):
                    u=len(a|b); v.append(1.0-(len(a&b)/u if u else 1.0))
                diss.append(np.mean(v))
            prev=s
    return float(np.mean(diss)), float(np.mean(degs))


# ---------------------------------------------------------------------------
if __name__ == '__main__':
    print('Finding 52 -- direct 2D vs 3D kinematic-mixing rate')
    print('  N=%d  seeds=%d  ramp sweep: %s' % (N, N_SEEDS, RAMP_VALS))
    print('  contact radii: 2D=%.3f  3D=%.3f (calibrated to matched degree)' % (
          RCONT_2D, RCONT_3D))
    print()
    t0 = time.time()

    res = {}
    for ramp in RAMP_VALS:
        ts = time.time()
        m2, k2, m3, k3 = [], [], [], []
        for s in range(N_SEEDS):
            a, d = mixing_2d(s, ramp); m2.append(a); k2.append(d)
            a, d = mixing_3d(s, ramp); m3.append(a); k3.append(d)
        res[ramp] = (np.mean(m2), np.std(m2), np.mean(k2),
                     np.mean(m3), np.std(m3), np.mean(k3))
        r = res[ramp]
        print('  ramp=%.2f  2D mix=%.4f+/-%.4f (<k>=%.1f)  '
              '3D mix=%.4f+/-%.4f (<k>=%.1f)  ratio 3D/2D=%.2f  [%.0fs]' % (
              ramp, r[0], r[1], r[2], r[3], r[4], r[5], r[3]/max(r[0],1e-9),
              time.time()-ts), flush=True)

    print('\nTotal runtime: %.1f min' % ((time.time()-t0)/60.0))

    ramps = np.array(RAMP_VALS)
    m2 = np.array([res[r][0] for r in RAMP_VALS])
    e2 = np.array([res[r][1] for r in RAMP_VALS])
    m3 = np.array([res[r][3] for r in RAMP_VALS])
    e3 = np.array([res[r][4] for r in RAMP_VALS])

    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.errorbar(ramps, m2, yerr=e2, marker='o', capsize=4, color='steelblue',
                label='2D')
    ax.errorbar(ramps, m3, yerr=e3, marker='s', capsize=4, color='crimson',
                label='3D')
    ax.set_xscale('log')
    ax.set_xlabel('Noise amplitude ramp')
    ax.set_ylabel('Contact-graph mixing (Jaccard / 2tu)')
    ax.set_title('Finding 52 -- direct 2D vs 3D kinematic-mixing rate\n'
                 '(matched mean contact degree)')
    ax.legend(); ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig('figures/finding52_mixing_dimension.png', dpi=140)
    print('  -> figures/finding52_mixing_dimension.png')

    with open('outputs/finding52_mixing_dimension.txt', 'w') as f:
        f.write('Finding 52 -- direct 2D vs 3D kinematic-mixing rate\n')
        f.write('N=%d seeds=%d  R_cont 2D=%.3f 3D=%.3f\n\n' % (
                N, N_SEEDS, RCONT_2D, RCONT_3D))
        f.write('ramp   2D_mix   2D_<k>   3D_mix   3D_<k>   ratio_3D/2D\n')
        for r in RAMP_VALS:
            v = res[r]
            f.write('%.2f   %.4f   %.2f     %.4f   %.2f     %.2f\n' % (
                    r, v[0], v[2], v[3], v[5], v[3]/max(v[0],1e-9)))
    print('  -> outputs/finding52_mixing_dimension.txt')
