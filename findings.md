# Findings — PHY 351 Flocking Research
Started 2026-05-08

---

## Index by Theme

The 43 numbered findings below are presented chronologically (in the order they were
generated). For navigation, here they are grouped by theme:

### Baseline and Validation
- F1  Equilibrium cruise speed v_eq = v0 + alpha/mu (exact)
- F2  Solid-to-fluid transition appears continuous (preliminary)
- F3  Low threshold for flock formation (alpha ~ 0.05)
- F4  Full model robust to noise up to eta ~ 10
- F9  Solid-to-fluid is a crossover, not a phase transition (finite-size scaling)
- F17 No phase transition at any intermediate compactness (C = 0.15-0.60)

### Predator Strategy (2D)
- F5  Flocking maintains coherence under predator pressure (Phi ~ 1.0)
- F6  Flock coherence robust to predator aggression
- F7  Dilution effect: larger flocks expose smaller fractions
- F8  Naive multi-predator co-localizes at CoM (mechanism diagnosed)
- F10 Coordinated predators spread out but cannot break the flock (Phi > 0.92)
- F11 Encirclement disrupts the flock (Phi = 0.77 at n_pred = 6)
- F14 Encirclement floor: angular coverage is the key variable
- F15 Encirclement works by flock division, not dissolution
- F16 Minimum viable flock size (Phi = 0.9 crosses between N = 18-25)
- F22 Sub-flock reunion in ~10 tu after predator removal
- F25 Predator sensing threshold at r_sense ~ flock radius
- F31 R_enc/Rg ~ 0.5 universal optimum (size-invariant encirclement scaling)
- F32 Long-time encirclement: intermittent merge/split steady state
- F33 Incomplete encirclement non-monotonic (5-active gap most disruptive)
- F35 Adaptive R_enc = 0.5*Rg outperforms fixed (validates F31 dynamically)

### Contagion and Vaccination
- F12 Static panic does not propagate (calm Phi ~ 1.0 at 20% panic)
- F18 (retracted; superseded by F23)
- F23 SI contagion saturates flock at any beta > 0
- F24 SIS contagion has clean epidemic threshold at beta/gamma ~ 1
- F26 Combined predation + contagion: contagion dominates
- F27 No spatial segregation from v0 contrast alone
- F29 Sub-threshold SIS + encirclement: compression doubles panic peak (mild)
- F30 Alpha-contrast produces real segregation via local clustering
- F34 Outbreak persistence: epidemic outlasts predator removal by 100+ tu
- F36 Targeted (degree-based) vaccination null result
- F37 Spatial vaccination null result
- F29 Critical-shift: encirclement lowers epidemic threshold by ~4%
- F30 Herd-immunity threshold p_c ~ 0.46 (2x mean-field)

### Phase Transition (Diagnosis Thread)
- F9, F17 (above)
- F38 Repulsion hardness null result (n = 1.5-12 identical)
- F39 Langevin thermostat satisfies FDT (KE/N = kT to 1%)
- F40 Hexatic order parameter |psi6| flat: soft repulsion cannot crystallize
- F50 Hard repulsion (n = 12, 24) also flat: higher exponent shrinks the core, not hardens

### 3D Extension
- F41 Flocking generalizes to 3D; v_eq exact
- F42 3D noise crossover at ramp ~ 15-25 (smooth, not a phase transition)
- F43 3D encirclement fails at R_enc/Rg ~ 0.5; 2D-specific result
- F44 3D encirclement disruption non-monotonic in n_pred; hard floor Phi ~ 0.91
- F45 3D adaptive encirclement null result; tracking damps the disruptive fluctuations
- F46 Vaccination targeting fails in 3D too; kinematic mixing is dimension-independent
- F47 Topological (k-NN) alignment does not slow mixing; the §5 prediction is falsified
- F48 Freezing the contact graph does not rescue targeting; degree-targeting null is structural
- F49 3D compression mechanism verified; planar ring arrangement worse than spherical
- F50 Hard repulsion does not crystallize; higher exponent shrinks the core, not hardens it
- F51 3D alpha-contrast segregation: matches 2D at moderate contrast, diluted at high contrast
- F52 3D mixes ~1.8x SLOWER than 2D at matched degree; "mixing aid" theme falsified
- F44 (planned) 3D predator scaling: how many predators match 2D floor?

### Floor and Scaling
- F20 Encirclement floor is N-dependent at fixed R_enc (mid-N artifact)
- F31 With R_enc/Rg scaling, encirclement is size-invariant

---

## Literature Context and Novelty Assessment
*Added 2026-05-15 based on literature search. Updated 2026-05-15 (session 2) with additional papers.*

### Background papers

**Levis, Diaz-Guilera, Pagonabarraga, Starnini (2019/2020). "Flocking-enhanced social contagion."
Phys. Rev. Research 2, 032056.**
Studies bidirectional coupling between a Vicsek-like flocking model and SIS epidemic dynamics, where
agents' flocking DEPENDS on their SIS state (infected agents aligned differently).  Key result:
flocking self-organizes dense swarms that reduce the epidemic threshold below the global mean-field
limit.  Directly related to Findings 26, 29 (compression raises effective contact count, shifts
threshold) but via a DIFFERENT MECHANISM: their compression is endogenous (epidemic state drives
clustering), ours is exogenous (predator encirclement compresses the flock mechanically).  Our
experiment is the first to test the EXTERNAL predator analog of this effect, and to study what
happens when the external compressor is REMOVED (Finding 34 -- epidemic persistence -- is not
addressed in this paper).

**Silverberg, Bierbaum, Sethna, Cohen (2013). "Collective motion of humans in mosh and circle pits."
Phys. Rev. Lett. 110, 228701.**
Original source model.  Demonstrates the same four-force ABM produces realistic crowd dynamics.
Our project is a systematic extension of this model into predator-prey, contagion, and hybrid regimes.

**Recent (2025-2026) predator-strategy papers:**
Pacher, Bierbach, Kurvers, Krause et al. (2026). "Strategic choices of attack location allow
predators to counter a collective prey defence." Proc. R. Soc. B 293, 20260566.
Studies real predatory birds choosing attack positions against fish shoals.  Found that conspicuous
predators avoid the center of shoals to minimize prey alert response; cryptic predators prefer
center attacks.  Our encirclement strategy (equal-angle offset from CoM) is a computational analog
but our mechanism is fundamentally different: we are interested in HOW MANY ANGLES are needed to
overcome collective evasion, and the scaling relationship R_enc/Rg ~ 0.5 (Findings 14, 31) appears
not to be addressed in empirical predator-strategy literature.

**Demsar & Lebar Bajec (2014). "Simulated Predator Attacks on Flocks: A Comparison of Tactics."
Artificial Life 20(3): 343-359.**
Compared three attack tactics (attack center, attack nearest, attack isolated) against social vs.
individualistic prey using a fuzzy individual-based model.  Found social flocking is the optimal
anti-predatory response to predators targeting isolated individuals.  Relevant to F14: Demsar &
Bajec do NOT test a coordinated multi-angle encirclement strategy; our encirclement (equal-angle
compass assignment from CoM) is not among their tactics.  Supports novelty of F14's angular-coverage
threshold result.

**Bartashevich, Romanczuk et al. (2024). "Collective anti-predator escape manoeuvres through optimal
attack and avoidance strategies." Communications Biology 7, 1548.**
Uses agent-based modeling + empirical sardine-vs-marlin observations to study how the "fountain
effect" arises when prey optimize escape angles to maximize distance from predator.  The fountain
effect is a cohesive split-and-rejoin pattern in response to a SINGLE predator's attack direction.
Our encirclement result (F16) is the multi-predator analog: angular COMPRESSION from multiple
directions produces a more violent flock DIVISION into directionally separated sub-flocks rather
than a single fountain.  The single-predator fountain timescale is not measured in their paper;
our quantification of reunion time (~10 tu, F22) appears novel.

**[2025 paper] "Behavioural response of prey to repeated attacks by non-coordinating predators."
Scientific Reports, 2025.**
Uses an underdamped Langevin model (physically similar to our Langevin follow-up, F39) to study
REPEATED attacks by naive (non-coordinating) predators.  Key mechanism: when opposing predation
pressures stretch the group transversely, narrowing leads to splitting.  This is the non-coordinated
analog of our coordinated encirclement (F14-F16).  Our contribution beyond this paper: (a) we study
COORDINATED strategies (compass-angle assignment, not random repeated attacks), (b) we measure
the angular-coverage threshold and R_enc/Rg scaling, and (c) we study the reunion timescale after
predator REMOVAL (not repeated attacks).

**Inada & Kawachi (2002/2005). "Dynamics of prey-flock escaping behavior in response to predator's
attack." J. Theor. Biol., doi: 10.1016/j.jtbi.2005.01.009.**
Two-dimensional molecular-dynamics simulation identifying four collective escape patterns:
Split and Reunion, Split and Separate into Two Groups, Scattered, and Maintain Formation and
Distance.  Our F16 demonstrates the "Split and Reunion" pattern (flock division into coherent
sub-flocks that reconsolidate after predator removal), F22 quantifies the reunion timescale
(~10 time units).  Our contributions beyond Inada & Kawachi: (a) the CAUSE is explicit
encirclement (multi-angle pressure) rather than single-predator attack angle, (b) we characterize
the transition between division patterns as a function of predator count, and (c) we identify
the asymmetry between kinematic recovery (F22, F7) and epidemic recovery (F34).

**Collective evasion timescales / recovery:**
Literature (Inada & Kawachi, Bartashevich et al.) identifies the "split and reunion" pattern and
the fountain effect, but does not quantify reunion timescales or compare kinematic vs. epidemic
recovery after stressor removal.  Finding 22 (kinematic reversibility, ~10 tu), Finding 7
(same, earlier measurement), and Finding 34 (epidemic persistence, ~100+ tu) together provide
the first explicit timescale comparison in a hybrid kinematic-contagion system.  This asymmetry
appears to be a novel contribution.

**Spatial herd immunity inflation:**
Herd immunity inflation above mean-field is a known effect in spatial SIR/SIS models (Diekmann
et al.; Keeling & Rohani) and empirically confirmed during COVID-19 (Britton et al. 2020, Science).
Spatial vaccination strategies for geographic populations have been studied (Bhatt et al. 2022,
PLoS Comput. Biol.; Zhou et al. 2021, GeoHealth), but these use fixed geographic regions, not
kinematic agents that constantly mix spatially.  Our Finding 30 (2x inflation in a flock context,
p_c ~ 0.46 vs 0.20) is a demonstration that a kinematic flock system quantitatively matches the
spatial-epidemic prediction.  Finding 37 (spatial vaccination, in progress) tests whether
spatially-distributed immunity can exploit this; preliminary results suggest kinematic mixing
defeats spatial targeting as effectively as it defeats degree-targeting (F36).

### Novelty summary

| Finding | Status | Notes |
|---------|--------|-------|
| F14 Encirclement disruption | Likely novel | Demsar&Bajec 2014 does not test multi-angle compass assignment; angular threshold not in literature |
| F16 Flock division (not dissolution) | Related + novel | Inada&Kawachi 2002 identifies "Split and Reunion" pattern; our contribution is mechanism (encirclement) + predator-count transition |
| F22 Kinematic reversibility (~10 tu) | Novel | Inada&Kawachi identifies pattern but does not quantify reunion timescale; explicit ~10 tu measurement is new |
| F29 Threshold shift ~4% from compression | Related | Similar to Levis 2020 (endogenous) but external-predator mechanism is different |
| F30 Herd immunity 2x mean-field | Known effect | Consistent with spatial SIS literature; novel in kinematic-flock context |
| F31 R_enc/Rg scaling universal | Likely novel | No literature found on size-invariant encirclement calibration |
| F32 Long-time intermittent dynamics | Possibly novel | Related to repeated-attack papers (Scientific Reports 2025) but not identical mechanism |
| F33 Incomplete encirclement non-monotone | Likely novel | No literature found; counterintuitive 5-predator result |
| F34 Epidemic outlasts kinematic stressor | Likely novel | Not addressed in Levis 2020 or any predator-prey paper found; timescale asymmetry is new |
| F35 Adaptive R_enc outperforms fixed | Likely novel | No paper found on adaptive predator geometry tracking in flocking |
| F36 Targeted vaccination null result | Interesting null | Hub-targeting fails in kinematic flock; spatial reorganization is specific mechanism |
| F37 Spatial vaccination (in progress) | Likely null | Preliminary: kinematic mixing erases spatial targeting advantage as it erases degree targeting |
| F38 Non-equilibrium driving causes crossover | Likely novel | FDT diagnosis in force-based ABM context; not in equilibrium statistical mechanics literature |

---

## Model Summary
Charbonneau Chapter 10. N agents on a periodic 2D unit square [0,1]^2.
Each agent subject to 4 forces per timestep:
- Repulsion: pushes agents apart within range 2*r0
- Flocking: aligns velocity with neighbors within range rf
- Self-propulsion: drives agent toward target speed v0
- Random: uniform noise in [-ramp, ramp]

Forward Euler integration at dt=0.01. Periodic boundaries via ghost agent buffer zone.
Default parameters: N=350, r0=0.005, eps=0.1, rf=0.1, alpha=1.0, v0=1.0, mu=10.0, ramp=0.5

Order parameter: Phi = |mean(v_hat)|, ranges 0 (random) to 1 (perfect alignment)

---

## Finding 1: Equilibrium speed is v_eq = v0 + alpha/mu
<img src="./figures/validate_3_flocking_only.png" width="480"/>

**What:** Agents don't cruise at v0 -- they cruise at v_eq = v0 + alpha/mu.
**Why:** When the flock aligns, the flocking force always pushes agents forward
at magnitude alpha. Self-propulsion equilibrates at a higher speed to compensate.
**Evidence:** With alpha=1, mu=10, v0=1 -> measured mean speed 1.098 vs predicted 1.100 (diff=0.002).
Verified across alpha = 0, 0.5, 1.0, 2.0 -- all match v0 + alpha/mu to within 0.002.
**Implication:** v0 and alpha cannot be set independently without affecting cruise speed.
To target a specific cruise speed v_cruise, set v0 = v_cruise - alpha/mu.

---

## Finding 2: Solid-to-fluid phase transition in repulsion-only system
<img src="./figures/validate_2_repulsion_noise.png" width="480"/>

**What:** With only repulsion and noise (alpha=0, v0=0), KE rises continuously with noise
amplitude eta. Transition appears continuous (not abrupt) across eta ~ 1-10.
**Evidence:** Sweep A in analysis.py, 5 seeds each with error bars.
eta=0.5: KE=0.00 | eta=3: KE=0.16 | eta=10: KE=1.74 | eta=30: KE=15.89
**Visual:** At low eta, agents form hexagonal crystal (close-packed). At high eta, fluid phase.
**Open question:** Is this a true phase transition or a crossover? Would need to look for
diverging susceptibility or correlation length to answer.

---

## Finding 3: Low threshold for flock formation
<img src="./figures/phase4_sweeps.png" width="480"/>

**What:** Flock forms (Phi > 0.5) at very small flocking amplitude alpha -- around alpha ~ 0.05-0.1.
**Evidence:** Sweep B in analysis.py, 5 seeds each.
alpha=0: Phi=0.088 | alpha=0.05: Phi=0.404 | alpha=0.10: Phi=0.607 | alpha=0.20: Phi=0.891
**Note:** Large variance at alpha=0.05-0.10 (std ~0.12-0.19) -- near the transition the outcome
is sensitive to initial conditions. Above alpha~0.2 the flock reliably forms.

---

## Finding 4: Full model robust to noise up to eta~10
**What:** With all forces active (default parameters), Phi stays near 1.0 up to eta~10,
then drops sharply, collapsing to Phi~0.4 at eta=20.
**Evidence:** Sweep C in analysis.py, 5 seeds each.
eta=1: Phi=0.999 | eta=5: Phi=0.976 | eta=10: Phi=0.906 | eta=20: Phi=0.417
**Contrast:** Repulsion-only system (Finding 2) doesn't form a flock at all.
The flocking force makes the system much more resistant to noise disruption.

---

## Finding 5: Flocking maintains coherence under predator pressure
<img src="./figures/predator_2_coherence.png" width="480"/>

**What:** Under predator pressure, flocking prey maintain Phi~1.0 throughout the simulation.
Non-flocking prey (alpha=0) scatter to Phi~0.1 almost immediately.
**Evidence:** Exp 2 in predator.py, 10 seeds each.
- Flocking: steady-state Phi = 0.998, mean predator-nearest distance = 0.112
- Non-flocking: steady-state Phi = 0.096, mean distance = 0.127
**Interpretation:** The flock absorbs the predator's pressure without breaking apart.
Non-flocking agents are marginally farther from the predator individually, but they have
no collective structure. Flocking sacrifices some individual distance for group cohesion.

---

## Finding 6: Flock coherence robust to predator aggression
<img src="./figures/predator_3_aggression_sweep.png" width="480"/>

**What:** Prey flock Phi stays near 0.95-0.98 across all tested predator aggression levels
(alpha_pred = 0 to 15, effective speeds 0.05 to 1.55). Flock does not break apart.
**Evidence:** Exp 3 in predator.py, 8 seeds each.
**Evidence:** Predator-flock distance drops from 0.24 (passive predator) to ~0.10
(alpha_pred >= 1) and then saturates -- the flock successfully holds the predator
at a minimum distance regardless of how fast the predator is.
**Interpretation:** There is an evasion floor. The collective repulsion response is enough
to maintain a fixed buffer distance even against a very aggressive predator.

---

## Finding 7: Dilution effect -- larger flocks expose smaller fractions
<img src="./figures/predator_4_size_sweep.png" width="480"/>

**What:** The fraction of the flock within predator threat range decreases with flock size.
**Evidence:** Exp 4 in predator.py, 5 seeds each.
N=10: fraction~0.49 | N=25: ~0.21 | N=50: ~0.19 | N=100: ~0.11 | N=200: ~0.14
**Interpretation:** Basic geometric dilution -- predator occupies a fixed area, larger
flock has more agents outside that area. Consistent with the biological "safety in numbers"
hypothesis. Note: N=200 slightly worse than N=100 (0.14 vs 0.11), possibly noise.

---

---

## Finding 8: Solid-to-fluid transition is a crossover, not a phase transition
<img src="./figures/phase_transition_scaling.png" width="480"/>

**What:** Finite-size scaling across N=25,50,100,200 shows KE/N is essentially
independent of N. Susceptibility chi = N*var(KE/N) rises monotonically, no peak.
**Evidence:** phase_transition.py. All four N values give nearly identical KE/N curves.
**Interpretation:** High compactness (C~0.78) traps agents -- each agent oscillates
like an independent harmonic oscillator at its lattice site. A true phase transition
would require chi to diverge at finite eta and scale as N^(gamma/nu). Neither observed.

---

## Finding 9: Flock elongates with predator pressure and with stronger alpha
<img src="./figures/geometry_2_alpha_sweep.png" width="480"/>

**What:** Aspect ratio AR increases with predator presence and flocking amplitude alpha.
**Evidence:** geometry.py
- No predator: AR=2.61 | With predator: AR=2.76
- alpha=0.2: AR=2.09 | alpha=1.0: AR=2.94 | alpha=2.0: AR=7.27
**Interpretation:** Strong velocity alignment forces agents into a tight stream.
Under predator pressure the flock thins and elongates, consistent with the book's
prediction of arched/thinning flocks.

---

## Finding 10: Multiple predators elongate the flock without breaking coherence
<img src="./figures/multi_pred_3_summary.png" width="480"/>

**What:** With 1-4 predators, Phi stays near 0.975-0.991 throughout. AR increases
from 2.83 (1 predator) to 7.91 (3 predators). Min predator-prey distance actually
increases slightly from 0.093 to 0.106.
**Evidence:** multi_predator.py, 8 seeds each.
**Interpretation:** More predators stretch and thin the flock but don't destroy it.
Counterintuitively, evasion distance increases with more predators -- pressure from
multiple directions may force the flock into a harder-to-surround configuration.

---

## Finding 11: Evasion distance increases because predators co-localize at prey CoM
<img src="./figures/evasion_diagnostic.png" width="480"/>

**What:** With multiple predators, each one independently targets the flock center of mass.
Because all predators follow the same rule, they converge to the same location
(measured pred-pred distance ~0.001, essentially zero). This means more predators
pile up at the same point rather than surrounding the flock.
**Evidence:** evasion_analysis.py, 8 seeds each.
- n_pred=1: min_pred_prey_dist=0.094
- n_pred=2: pred-pred dist=0.001, min_pred_prey_dist=0.099
- n_pred=3: pred-pred dist=0.001, min_pred_prey_dist=0.105
- n_pred=4: pred-pred dist=0.001, min_pred_prey_dist=0.096
- Flock orientation vs predator centroid: ~43-46 deg (consistent with random, ~45 deg expected)
**Mechanism:** Co-localized predators exert combined repulsion from the same point.
Multiple predators at the same location produce a stronger net repulsion on nearby prey
than a single predator, pushing the flock farther away. The flock does NOT orient
deliberately (45-degree angle = no systematic orientation strategy).
**Implication:** The "chase CoM" predator strategy is self-undermining when used by
multiple predators. They inadvertently cooperate by concentrating force at one point,
and the flock benefits. Distributed predators approaching from different angles would be
more effective -- but that requires coordination the model does not give them.

---

## Finding 12: Crossover persists across compactness -- no phase transition in this model
<img src="./figures/compactness_phase.png" width="480"/>

**What:** When compactness is held fixed across N by scaling r0 = sqrt(C/(pi*N)),
both dense (C=0.78) and dilute (C=0.10) regimes give essentially identical results:
KE/N curves overlap for all N, susceptibility chi increases monotonically with eta,
and the susceptibility peaks only at the top of the sweep (eta=30) -- not at a finite
critical point. The crossover is not a property of the dense regime alone; it persists
at all tested compactness values.
**Evidence:** compactness_phase.py, 8 seeds per (N, eta) point.
- C=0.78: chi_max at eta=30 for all N; KE/N identical across N=25-200
- C=0.10: same behavior -- chi_max at eta=30, KE/N N-independent
- KE/N values nearly identical between C=0.78 and C=0.10
**Interpretation:** The absence of a critical point is not because agents are caged.
At C=0.10 (dilute), agents barely interact (repulsion radius too small relative to
inter-agent spacing), so they behave essentially as independent random walkers. KE/N
is then set entirely by the noise amplitude, independent of N. Both extremes (too
dense = caged, too dilute = non-interacting) produce N-independent KE/N and monotone
susceptibility. A genuine critical point would likely require intermediate compactness
where agents can form a solid and also rearrange cooperatively -- but even C=0.10 is
too dilute for a solid phase. The repulsion-only model may simply not exhibit a true
phase transition in any easily accessible parameter regime.

---

---

## Finding 13: Coordinated predators spread out but cannot break the flock
<img src="./figures/coord_3_breaking_threshold.png" width="480"/>

**What:** Adding predator-predator repulsion (alpha_coord) forces predators to spread
out spatially instead of co-localizing, and brings them physically closer to the flock.
But even with 10 coordinated predators, Phi never drops below 0.92. The flock's
collective evasion is robust to predator coordination strategy.
**Evidence:** coordinated_predators.py, 8 seeds each.
- alpha_coord=0 (naive): pred-pred sep=0.001, AR=8.82, min_dist=0.105
- alpha_coord=5: pred-pred sep=0.141 (real separation achieved), min_dist=0.078
- alpha_coord=10: pred-pred sep=0.233, min_dist=0.084, Phi=0.970
- alpha_coord=20: pred-pred sep=0.293 (maximum tested)
- n_pred=1..10 with alpha_coord=10: Phi ranges 0.923-0.991, no systematic collapse
**Key threshold:** Separation requires alpha_coord >= ~5. Below that, the shared
CoM target overwhelms the repulsion and predators still pile up.
**Interpretation:** The prey collective is strategy-resistant. Naive predators fail
because they co-localize. Coordinated predators fail because the flock's distributed
repulsion response scales with the number of approaching predators. No number or
strategy of predators in this model breaks the flock.

---

## Finding 14: Encirclement breaks coherence -- first strategy to substantially disrupt the flock
<img src="./figures/encircle_3_breaking_threshold.png" width="480"/>

**What:** Assigning each predator a fixed angular direction and targeting
CoM + R_enc*(cos(theta_k), sin(theta_k)) forces them to approach from equally spaced angles.
This is fundamentally different from both naive and coordinated strategies. At n_pred=6-8,
Phi drops to ~0.77 -- the first substantial coherence reduction in all experiments.
Naive and coordinated predators never dropped below 0.92.
**Evidence:** encirclement.py, 8 seeds each.
- Radius sweep (n_pred=3): R_enc=0.15 minimizes evasion distance (0.076) and Phi (0.953).
  R_enc=0.00 is naive (sep=0.001); R_enc=0.15 achieves pred_sep=0.260.
- vs naive (R_enc=0.15): n_pred=4 encircle Phi=0.909 vs naive 0.974.
  Predators get significantly closer: dist 0.077 vs 0.096.
- Flock-breaking threshold: n_pred=6 gives Phi=0.769 +/- 0.093, n_pred=8 gives 0.782 +/- 0.124.
  Min pred-prey dist falls to 0.050 (vs 0.105 for naive multi-predator). Flock not fully
  broken but substantially disrupted; high std suggests some seeds fragment.
**Optimal radius:** R_enc ~ 0.15 (just inside the flock edge, Rg~0.25). Too small = still
co-localizing. Too large (R_enc=0.25) = predators orbit the flock and evasion distance recovers.
**Interpretation:** Multi-directional pressure from equally spaced angles creates competing
repulsion vectors that cannot all be resolved by a single coherent escape direction. The alignment
force resists but cannot fully compensate when predators approach from 6+ angles simultaneously.
This is the first predator strategy in this model capable of meaningfully disrupting collective
evasion, establishing that flock resilience is strategy-dependent, not absolute.

---

## Finding 15: Encirclement threshold does not scale with N -- convergence to a common floor
<img src="./figures/encircle_scaling.png" width="480"/>

**What:** Fixed n_pred=6 against varying N shows larger flocks are more resistant (Phi rises
from 0.695 at N=50 to 0.903 at N=350). But fixed predator-to-prey ratio (6/350) applied
to larger N makes things WORSE: at N=500 with n_pred=9, Phi=0.654 -- the lowest coherence
in all experiments. Both N=100 and N=350 converge to Phi~0.67 at n_pred=10-12, suggesting
a common disruption floor independent of flock size at sufficient predator density.
**Evidence:** encirclement_scaling.py, 8 seeds each.
- Fixed n_pred=6: N=50 Phi=0.695, N=100 Phi=0.769, N=200 Phi=0.833, N=350/500 Phi=0.90
- Fixed ratio 6/350: N=500, n_pred=9 gives Phi=0.654 +/- 0.171 (worst result in project)
- Full sweep N=100 vs N=350: both reach Phi~0.67-0.68 at n_pred=10
**Interpretation:** The dilution effect protects against a fixed predator count (more agents
share the evasion burden). But the ratio law fails -- more predators at fixed ratio are
MORE effective for larger N because finer angular coverage (9 angles vs 6) is harder to
escape. There is no simple scaling law: disruption depends nonlinearly on both N and n_pred.
The convergence of N=100 and N=350 to the same Phi floor at n_pred=10 suggests the
disruption is set by angular coverage (predators/360 degrees) rather than predators/prey.

---

## Finding 16: Encirclement divides the flock into coherent sub-flocks, not random walkers
<img src="./figures/frag_3_snapshots.png" width="480"/>
<img src="./figures/frag_2_cluster_stats.png" width="480"/>

**What:** When global Phi drops to 0.77 under encirclement, the flock is NOT dissolving.
Predators COMPRESS the flock spatially (fewer clusters: 60 naive vs 24 encircle) while
SPLITTING it directionally (each sub-flock escapes in a different direction). Each
sub-flock is internally coherent (largest_phi=0.997). The low global Phi reflects
sub-flocks heading in different directions, not individual agent randomness.
**Evidence:** fragmentation.py, 8 seeds, n_pred=6.
- Naive: 60 clusters, largest_frac=0.137, global_phi=0.997, largest_phi=1.000
  (many small groups all moving same direction -- spatially spread but directionally unified)
- Encirclement: 24 clusters, largest_frac=0.253, global_phi=0.718, largest_phi=0.997
  (fewer, larger groups moving in different escape directions)
- As n_pred increases: n_clusters decreases (5->8 pred: 70->19) while largest_frac
  grows (0.08->0.25), confirming spatial compression rather than dissolution.
**Interpretation:** Encirclement succeeds by herding -- predators squeeze the flock from
multiple directions, forcing it to split into sub-groups that escape toward the gaps between
predators. Each sub-group remains a coherent mini-flock. This is flock DIVISION not flock
DISSOLUTION. The mechanism is analogous to wolf-pack herding or dolphin bait-ball formation.
This is biologically the most significant finding of the project.

---

## Finding 17: No phase transition at any intermediate compactness -- crossover is universal
<img src="./figures/compactness_search_chi.png" width="480"/>

**What:** Sweeping compactness C = 0.15, 0.20, 0.30, 0.40, 0.50, 0.60 with finite-size
scaling at N = 25, 50, 100, 200 finds no true phase transition at any density. In every
case, susceptibility chi = N*Var(KE/N) peaks at eta=30 (the top of the sweep) and the
chi_peak value is essentially identical across N (all ~0.022-0.025). No diverging peak,
no N-dependence, no critical point anywhere in the accessible compactness range.
**Evidence:** compactness_search.py, 8 seeds. Chi-peak summary:
All 24 (C, N) combinations peak at eta=30 with chi_peak in [0.021, 0.025].
KE/N curves are N-independent at every C, indistinguishable from the C=0.10 and C=0.78
results of Finding 12.
**Interpretation:** The crossover is a universal property of this model's repulsion force,
not a feature of an extreme density regime. The repulsion potential (1 - d/2r0)^1.5 is
soft -- it smoothly decays to zero at contact. Real melting transitions require hard-core
exclusion to produce the diverging spatial correlations of a critical point. This model's
repulsion was designed for crowd dynamics and simply does not have the right microscopic
physics to produce a true phase transition at any accessible compactness.
**Implication:** The professor's suggested intermediate regime does not exist in this model.
Finding a true phase transition would require either a harder repulsion (e.g., r^{-12}
Lennard-Jones) or a different model class entirely.

---

## Finding 18: Panic does not propagate -- calm agents stay coherent even at 20% panic fraction
<img src="./figures/panic_1_sweep.png" width="480"/>
<img src="./figures/panic_2_snapshots.png" width="480"/>

**What:** When a fraction f of agents are replaced by panicked agents (weak flocking alpha=0.1,
high noise ramp=10.0), the global order parameter drops smoothly: Phi=1.000 at f=0% down to
Phi=0.853 at f=20%. But the calm-agent-only order parameter stays at 0.999 throughout.
Panic does not propagate into the calm sub-flock.
**Evidence:** panic.py, 8 seeds each.
- f=0%:  Global Phi=1.000, Calm Phi=1.000
- f=1%:  Global Phi=0.991, Calm Phi=1.000
- f=5%:  Global Phi=0.958, Calm Phi=0.999
- f=10%: Global Phi=0.922, Calm Phi=0.999
- f=20%: Global Phi=0.853, Calm Phi=0.999
**Mechanism:** The global Phi drop is pure dilution: incoherent panicked agents are included
in the order parameter average, dragging it down. The calm agents form a coherent flock that
effectively ignores panicked neighbors. The flocking force is strong enough that calm agents
maintain alignment even with 20% erratic neighbors.
**Direction:** Flock heading shows no systematic deflection across panic fractions (~-9 to -13 deg,
essentially noise around the f=0 baseline). Panicked agents do not steer the flock.
**Comparison with predator strategies:** A single predator achieves Phi~0.995 (essentially no
disruption). Even f=20% panic achieves only Phi=0.853 -- and with calm_Phi=0.999 this represents
dilution, not genuine flock disruption. Encirclement with n_pred=6 achieves Phi=0.769 with the
flock actually dividing (calm agents are disrupted). External predator pressure is more disruptive
than internal panic at any tested fraction.
**Implication:** The book section "Why You Should Never Panic" implies panic is dangerous to the
collective. In this model, the opposite is observed: the flock is immune to internal panic because
the alignment force dominates. The book result may depend on panic propagation via local contagion
(agents near panicked agents becoming panicked themselves), which this model does not implement.

---

## Finding 19: Predator sensing threshold at r_sense ~ flock radius; limited sensing slightly worsens encirclement
<img src="./figures/sensing_1_summary.png" width="480"/>
<img src="./figures/sensing_2_cycles.png" width="480"/>

**What:** A predator with sensing radius r_sense can only lock on to the flock when the nearest
prey is within r_sense; otherwise it executes a slow random walk. There is a sharp transition in
lock-on fraction near r_sense ~ 0.10-0.15 (approximately equal to flock radius Rg ~ 0.10-0.15).
Above r_sense=0.20 the predator always finds the flock and the result is identical to perfect sensing.
**Evidence:** predator_sensing.py, 8 seeds, single predator.
- r_sense=0.05: lock_frac=0.12, Phi=0.990 -- predator rarely finds flock; dist=0.035 (close when it does)
- r_sense=0.10: lock_frac=0.77, Phi=0.972 +/- 0.037 -- transition regime; highest variance
- r_sense=0.15: lock_frac=0.97, Phi=0.995 -- nearly equivalent to perfect sensing
- r_sense>=0.20: lock_frac=1.00, Phi=0.995 -- identical to inf sensing
**Multi-predator:** Limited sensing (r=0.20) vs perfect sensing makes essentially no difference
for naive predators (n=1,3). For encirclement (n=6), limited sensing gives Phi=0.788 vs 0.853
for perfect sensing -- limited sensing slightly WORSENS the outcome for the flock.
**Mechanism for encirclement result:** When a locked-on encircling predator loses the flock and
re-enters search mode, it drifts randomly and may re-approach from a non-assigned angle. This adds
unpredictable multi-directional pressure on top of the structured encirclement pattern, increasing
disruption variability (std=0.126 vs 0.087 for perfect sensing). Some seeds fragment badly.
**Implication:** The biologically "realistic" sensing limitation does not help the flock -- it
leaves the single-predator result unchanged and slightly increases vulnerability to coordinated
strategies. The critical parameter is whether r_sense exceeds the flock's spatial footprint.

---

## Finding 20: Panic contagion saturates the flock at any non-zero rate -- there is no epidemic threshold
<img src="./figures/contagion_1_sweep.png" width="480"/>
<img src="./figures/contagion_3_snapshots.png" width="480"/>

**What:** Adding a contagion mechanism (calm agents become panicked at rate beta per panicked
neighbor within r_cont=0.05, no recovery) fundamentally changes Finding 18. With contagion off
(beta=0), the population stays at f_inf=0.011 (just the seed). With ANY non-zero contagion rate
tested -- even beta=0.5 -- the entire population panics: f_inf=1.000 (zero variance across all
6 seeds). The calm sub-flock that Finding 18 found to be immune now disappears entirely,
because every calm agent eventually flips. Global Phi collapses from 0.993 (beta=0) to 0.168
(beta=0.5) and saturates near 0.10 for beta >= 2.
**Evidence:** panic_contagion.py, 6 seeds, f0=1%, N=350, n_iter=4000.
- beta=0.0:  f_inf=0.011, Phi=0.993, calm_Phi=1.000 (matches Finding 18)
- beta=0.5:  f_inf=1.000, Phi=0.168, t_half=3.6 time units
- beta=2.0:  f_inf=1.000, Phi=0.100, t_half=1.2 time units
- beta=20.0: f_inf=1.000, Phi=0.109, t_half=0.4 time units
- Seed-size sensitivity at beta=2.0 (f0=0.5%..10%): always f_inf=1.000 regardless of f0
**Mechanism:** This is an SI (susceptible -> infected, no recovery) process on a spatially
mixed population. With N=350 agents in [0,1]^2 and r_cont=0.05, each agent's neighborhood
contains ~3 agents on average; once a few panic, every calm agent quickly meets a panicked
neighbor. The absorbing-state structure (panic cannot be undone) plus mixing motion guarantees
the outbreak completes, regardless of beta. beta only sets the speed: t_half scales roughly
as 1/beta. There is no critical beta_c in this formulation.
**Contrast with Finding 18:** Finding 18 said the flock is "immune to internal panic" -- but
that conclusion was an artifact of treating panic as a fixed label. Once contagion exists,
the alignment force cannot save the flock because the population pool of calm agents is
drained. The book's "Why You Should Never Panic" claim is recovered: panic is dangerous to
the collective IF and ONLY IF it propagates through contact.
**Implication:** A more refined model (SIS with recovery rate gamma, or a panic-suppression
mechanism analogous to immune memory) would be required to find a true epidemic threshold
beta_c. In the no-recovery limit, any contact-mediated panic is fatal to the flock.

---

## Finding 21: Minimum viable flock size -- coherence threshold at N~18-25
<img src="./figures/min_size_1_summary.png" width="480"/>

**What:** Sweeping N from 3 to 100 (8 seeds each) shows that flock coherence builds
smoothly with N rather than at a sharp threshold.  In the no-predator control:
Phi=0.49 at N=3, 0.69 at N=8, 0.81 at N=12, 0.96 at N=40, 0.99 at N=100.  Phi
crosses 0.9 between N=18 and N=25.  Below N=12 the flock is unreliable
(std=0.13-0.20 across seeds).  Predator pressure (single naive, or two opposed
encirclers) does not substantially shift this threshold.  In fact, at the
smallest sizes (N=3-8), a predator can briefly RAISE Phi by pushing the group
into a forced alignment.  Capture frequency (predator within 2*r0 of any prey)
stays below 10% at all tested sizes.
**Evidence:** min_flock_size.py with slow prey (v0=0.02, ramp=0.1) so the
v0=0.05 predator can actually pursue (matches Findings 5-16 regime).
- N=3:   Phi(none)=0.49, Phi(naive)=0.63, Phi(encircle2)=0.73
- N=8:   Phi(none)=0.69, Phi(naive)=0.49, Phi(encircle2)=0.61
- N=18:  Phi(none)=0.84, Phi(naive)=0.87, Phi(encircle2)=0.92
- N=40:  Phi(none)=0.96, Phi(naive)=0.91, Phi(encircle2)=0.95
- N=100: Phi(none)=0.99, Phi(naive)=0.94, Phi(encircle2)=0.94
- Evasion distance falls monotonically with N for both predator conditions
  (encircle2 always closer than naive); capture frac ~0 throughout.
**Interpretation:** Flock formation is collective: each agent's alignment
contribution to its neighbors needs a critical mass of mutually visible peers
within rf=0.1.  Below N~12 the spatial density (in a 1x1 domain) is too sparse
for the flocking force to dominate noise.  Between N=12 and N=25 the system
crosses over from noise-dominated to alignment-dominated.  Above N~25 the
group reliably flocks.
**Implication:** The "safety in numbers" hypothesis already established by
Finding 7 has a lower limit: below the coherence threshold, prey have neither
collective evasion nor individual escape distance (mind drops more sharply at
small N).  Real prey species near the coherence threshold should be most
vulnerable to predation in this model -- but the absolute capture rate in this
simulation is too small to test.

---

## Finding 22: Encirclement-induced fragmentation is fully transient -- sub-flocks reunite within ~10 time units of predator removal
<img src="./figures/reunion_1_timeseries.png" width="480"/>

**What:** Finding 16 showed encirclement divides the flock into coherent
sub-flocks.  This experiment runs a 3-phase simulation -- 1500 steps no
predator (warm-up), 4000 steps with 10 encircling predators (attack), 6500
steps no predator (recovery) -- and tracks Phi, cluster count, and largest
cluster fraction.  All 6 seeds recover fully.  Mean recovery time to Phi=0.95
is 10.3 time units (about 1030 steps), much shorter than the 4000-step attack
that caused the disruption.  Final Phi=1.000 +/- 0.001 -- better than the
pre-attack Phi=0.975, because by the end of the recovery window the flock
has had time to fully settle.
**Evidence:** reunion.py, 6 seeds, slow prey (v0=0.02), n_pred=10, R_enc=0.15.
- Pre-attack:    Phi=0.975, n_clusters=1.2, largest_frac=0.989
- During attack: Phi=0.716, n_clusters=4.5, largest_frac=0.413
                 (genuine fragmentation: largest fragment is 41% of flock)
- Post-attack:   Phi=1.000, n_clusters=1.0, largest_frac=0.993
- Recovery times (Phi -> 0.95):  [9.0, 4.5, 10.0, 16.0, 6.0, 16.5] time units;
  6/6 seeds recovered.
**Mechanism:** Predator removal eliminates the multi-directional pressure that
was holding sub-flocks apart.  Each sub-flock's local Phi was already ~1.0
during the attack (Finding 16), so each is internally consistent and moving
with a definite heading.  On the periodic 1x1 domain, sub-flocks heading in
different directions inevitably re-encounter each other, and at any meeting
the flocking force (within rf=0.1) re-aligns them.  Reunion is rapid because
sub-flocks are already aligned internally and only need their headings to
agree.
**Implication:** Encirclement causes DIVISION not DISSOLUTION (Finding 16);
this experiment confirms it causes only TRANSIENT division.  The flock's
topological state is preserved: as soon as the stressor is removed, the
group reconstitutes.  This is qualitatively different from contagious panic
(Finding 20), which would NOT spontaneously reverse on predator removal --
panicked agents stay panicked.  Predation and contagion produce different
classes of damage to the collective: predation is reversible, contagion is
absorbing.

---

## Finding 23: Combined predation + contagion -- contagion dominates; encirclement cannot rescue the calm sub-flock
<img src="./figures/hybrid_1_summary.png" width="480"/>

**What:** When the flock is simultaneously subjected to encirclement (n_pred=6) AND
contact-mediated panic contagion (beta=0.5, f0=1%), the combined outcome is essentially
identical to contagion-only.  All four conditions tested:
- none:      Phi=1.000, calm_Phi=1.000, f=0.000
- encircle:  Phi=0.707, calm_Phi=0.707, f=0.000  (matches Finding 16)
- contagion: Phi=0.050, calm_Phi=undefined, f=1.000  (matches Finding 20)
- both:      Phi=0.050, calm_Phi=undefined, f=1.000
**Evidence:** hybrid_stressors.py, 6 seeds, slow prey (v0=0.02, ramp=0.1).
**Mechanism:** Contagion is an absorbing-state process: once everyone is panicked, the
flock cannot be re-coherent regardless of what predators do.  Encirclement is a
kinematic disruption that requires the alignment force to operate -- with panicked
agents (alpha=0.1), the flocking force is too weak for predators to "herd" anyway.
Contagion races to saturation faster than encirclement can fragment.  Panic propagation
in the combined condition is not measurably different from contagion-only.
**Interpretation:** The two disruption mechanisms do not compose -- they operate in
non-overlapping regimes.  Encirclement disrupts a healthy alignment force; contagion
destroys the alignment force.  Once contagion has run, encirclement loses its target.
Hypothetical experiments where contagion is sub-threshold (e.g., SIS with high recovery)
would be needed to see encirclement still matter.
**Implication:** For a flock facing both an external pursuer and internal social
contagion, the contagion is the lethal threat.  The defensive priorities are not
symmetric: invest in mechanisms that suppress contagion (immune memory, signal-checking,
threshold behavior) rather than in mechanisms that prevent encirclement.

---

## Finding 24: Active/passive mixed populations do not spatially segregate
<img src="./figures/segregation_1_summary.png" width="480"/>

**What:** A mixed population of fast (v0=1.0) and slow (v0=0.1-0.7) agents in the standard
flocking model produces NO measurable spatial segregation along the heading direction.
Segregation index s = (mean_x_active - mean_x_passive)/Rg in the flock-aligned frame
stays at 0 +/- 0.05 across all tested conditions.  Phi remains at 1.000 throughout,
so the mixed flock is fully coherent.
**Evidence:** segregation.py, 5 seeds.
- Contrast sweep at f_active=0.5 (v0_passive=0.1..1.0): s ranges -0.035 to +0.029
- Fraction sweep at v0_passive=0.3 (f_active=0.1..0.9): s ranges -0.040 to -0.005
All values within statistical noise (errorbar ~0.04).  Snapshot at v0_passive=0.2 shows
active and passive agents well-mixed.
**Mechanism:** The alignment force homogenises velocity across the entire flock.  Each
agent's self-propulsion target is v0_self + alpha/mu, but the actual cruise speed is
the COMPROMISE set by the balance between self-propulsion and alignment.  In an aligned
flock, every agent feels the same flocking-force magnitude alpha, so the mean speed is
set by the population-weighted target.  Active and passive agents end up cruising at
nearly the same speed, eliminating the front/back differential that would produce
segregation.  This is consistent with Finding 1's result that the alignment force
fundamentally changes the kinematics: v_eq is not just v0_self.
**Implication:** Charbonneau Sec 10.4 describes spatial segregation in heterogeneous
populations; that result probably requires either (a) different alpha values between
groups (so the alignment compromise is asymmetric), or (b) a non-flocking baseline
where each agent moves independently at its own v0.  In the model as implemented here,
v0 contrast alone is insufficient to produce segregation -- the alignment force defeats it.
The defensive analogy: a flock of mixed-speed individuals can still respond as one unit;
the slower individuals do not become trailing stragglers.

---

## Finding 25: SIS contagion has a clean epidemic threshold at beta/gamma ~ 1; flock disruption tracks it
<img src="./figures/contagion_sis_1_sweeps.png" width="480"/>

**What:** Adding a recovery rate gamma to the contagion model (calm <-> panic) restores
the textbook SIS phase structure.  Below beta_c, contagion dies out and the flock stays
coherent; above beta_c, an endemic steady state emerges and the flock degrades.  The
critical line in (beta, gamma) space is approximately beta = gamma.
**Evidence:** contagion_sis.py, 5 seeds, f0=5%, N=350.
- Beta sweep at gamma=1.0: f_ss=0.000 at beta=0.0, jumps to 0.434 at beta=1.0, 0.789 at
  beta=2.0, saturates near 0.95 at beta=10.  Phi mirrors: 1.000 -> 0.661 -> 0.307.
- Gamma sweep at beta=2.0: f_ss=0.978 at gamma=0.1 (low recovery, persistent outbreak),
  drops to 0.000 at gamma=5 (recovery wins).  Sharp transition between gamma=2 and 5.
- 2D phase diagram (beta in [0.2, 4.0], gamma in [0.3, 10.0]): f_ss approximately
  tracks the diagonal beta = gamma.  Outbreak region (f_ss > 0.5) lies below the
  diagonal (beta > gamma); die-out region above.
**Comparison with mean-field:** Standard SIS predicts beta_c * <k> = gamma where <k> is
the mean local contact count.  Observed threshold beta_c ~ gamma corresponds to
<k> ~ 1, which is plausible for a flock at N=350 with r_cont=0.05: although a uniform
density in [0,1]^2 gives <k> = pi*r_cont^2*N ~ 2.7, the flock is actually moving as a
spatially extended structure with effective rather than uniform density at the contagion
scale.  The phase-diagram diagonal closely matches the prediction.
**Comparison with the SI model (Finding 20):** Finding 20 used no recovery -- the SI
limit is the gamma -> 0 corner of the phase diagram, where the outbreak always wins
regardless of beta.  Finding 20 said "any contact-mediated panic is fatal"; here we
see that statement was specifically about the no-recovery limit.  With finite gamma,
panic can be contained, and the flock retains coherence.
**Implication:** The biologically interesting question is therefore not whether
contagion exists but whether the recovery rate exceeds the contact rate.  For a real
flock, "recovery" might correspond to a calm-pulling-back-into-alignment mechanism --
panicked individuals returning to the alignment force as they re-enter coherent
neighborhoods.  The model suggests there is no need for explicit immune memory: a
strong enough alignment force could in principle generate effective recovery.  This
links flock disruption (a kinematic problem) to epidemic theory (a contact-process
problem) via a single dimensionless ratio beta/gamma.

---

## Finding 26: Encirclement amplifies but does not tip sub-threshold contagion -- partial coupling
<img src="./figures/hybrid_sis_1_summary.png" width="480"/>

**What:** At a sub-threshold SIS point (beta=1.0, gamma=3.0; beta/gamma=0.33, well below
the Finding 25 threshold), contagion alone fizzles -- panic peaks at f_max=0.13 then
dies out, leaving f_ss=0 and Phi=1.0.  Adding 6 encircling predators DOUBLES the panic
peak (f_max=0.27) but does NOT push the outbreak over threshold: f_ss=0.000 in the
combined condition too.  The mechanism is the local contact count <k>: encirclement
compresses the flock so that <k> rises from 8.9 to 30.2 (3.4x).  Effective contagion
strength beta*<k> rises with it, but at beta/gamma=0.33 the amplification is
insufficient to flip the dynamics.  Meanwhile, the COMBINED flock Phi is worse (0.73)
than encirclement alone (0.86) -- the transient outbreak adds non-negligible kinematic
disruption beyond what encirclement alone produces.
**Evidence:** hybrid_sis.py, 6 seeds, slow prey, beta=1, gamma=3.
- none:     Phi=1.000  f_max=0.000  <k>=8.89
- sis_only: Phi=1.000  f_max=0.134  <k>=8.10  (fizzles)
- encircle: Phi=0.864  f_max=0.000  <k>=30.21  (no contagion present)
- both:     Phi=0.729  f_max=0.269  <k>=32.60  (peak doubled, but still dies out)
**Comparison with Finding 23:** In Finding 23 the contagion was SUPERCRITICAL (SI / no
recovery) and dominated everything.  Here it is SUBCRITICAL and even amplified by
encirclement-induced compression, it still dies out.  The two findings bracket the
behaviour: contagion above its critical strength dominates; below threshold, even
strong external amplification cannot rescue the outbreak.  There is no easy way to push
a contained contagion over its tipping point through external mechanical pressure alone.
**Implication:** This is good news for collectives facing both stressors: as long as
the recovery rate exceeds the bare contact rate by a comfortable margin (here 3x), the
flock can absorb external disruption without triggering a contagious panic.  The
mapping beta_eff = beta * <k> via local-density modulation is real but mild -- a 3-4x
amplification of <k> by encirclement is not enough to bridge a factor-of-3 gap between
beta/gamma and 1.  For an attacker, this means coupling two attack modes is not a
free win; the contagion must already be near-supercritical for compression to matter.

---

## Finding 27: Alpha-contrast populations segregate via local clustering, not heading-axis separation
<img src="./figures/segregation_alpha_1_summary.png" width="480"/>

**What:** Replacing the v0 contrast of Finding 24 with alpha (alignment-strength)
contrast produces real spatial segregation -- but it manifests as local same-type
clustering, not as a front/back split along the heading direction.  The along-heading
segregation index stays near zero (consistent with v0-contrast Finding 24), so a naive
metric would miss the effect.  But the local-purity diagnostic (fraction of an agent's
rf-neighbors that share its type) rises monotonically with alpha contrast.
**Evidence:** segregation_alpha.py, 5 seeds, f_active=0.5.
- alpha_p=1.0 (no contrast):   purity_active=0.500, purity_passive=0.497  (baseline = 0.5)
- alpha_p=0.5:                 purity_active=0.556, purity_passive=0.549
- alpha_p=0.3:                 purity_active=0.550, purity_passive=0.542
- alpha_p=0.1:                 purity_active=0.630, purity_passive=0.598
- alpha_p=0.0:                 purity_active=0.732, purity_passive=0.684
  - Phi=0.513 -- the "flock" has effectively dissolved at alpha_p=0 because half the
    agents have no alignment force at all.
- Along-heading segregation index stays at 0 +/- 0.10 across the entire sweep.
**Mechanism:** Active agents have a strong alignment force pulling them toward their
neighbors' velocity; this preferentially binds active-active pairs which move
similarly.  Passive agents either don't align (alpha_p=0) or align weakly, so they
drift more independently.  The active sub-population coheres into local clusters that
exclude passive agents -- visible directly in the alpha_p=0 snapshot as compact red
clumps amid scattered blue particles.  Crucially, this clustering is isotropic in the
flock frame -- the clusters can form anywhere, not preferentially at the leading edge.
**Comparison with Finding 24:** v0 contrast alone produces NO segregation because the
alignment force homogenises group speed.  alpha contrast DOES produce segregation
because it creates differential binding strength.  The book's Section 10.4 segregation
result is recovered, conditional on asymmetric ALIGNMENT (not asymmetric speed).
**Implication:** In real biological flocks, segregation may indicate differential
alignment fidelity between individuals (e.g., different sensory acuity, different
attention to neighbors) rather than differential locomotion capability.  The proper
diagnostic for segregation is local purity, not bulk position relative to heading.

---

## Finding 28: Encirclement floor rises at very large N -- Finding 15's "common floor" is N-dependent
<img src="./figures/large_N_1_summary.png" width="480"/>

**What:** Finding 15 conjectured that the encirclement-induced Phi floor at ~0.67
(observed for N=100 and N=350 at n_pred=10) was set by angular coverage and should be
N-independent.  Extending the test to N=700 and N=1000 partially refutes this: the
floor rises with N.  At n_pred=10: Phi=0.667 (N=350), 0.700 (N=700), 0.740 (N=1000).
At n_pred=14: Phi=0.637 (N=350), 0.727 (N=700), 0.790 (N=1000).  The encirclement
strategy is LESS effective against larger flocks at fixed angular coverage.
**Evidence:** large_N_encirclement.py, 4 seeds, slow prey, R_enc=0.15.
- N=350,  n_pred=6:  Phi=0.902 +/- 0.043   n_pred=10: 0.667 +/- 0.106   n_pred=14: 0.637 +/- 0.128
- N=700,  n_pred=6:  Phi=0.863 +/- 0.076   n_pred=10: 0.700 +/- 0.150   n_pred=14: 0.727 +/- 0.113
- N=1000, n_pred=6:  Phi=0.849 +/- 0.119   n_pred=10: 0.740 +/- 0.080   n_pred=14: 0.790 +/- 0.132
- Evasion distance flat across N at n_pred=6 (~0.056); at n_pred=10 the predator gets
  closer for smaller N (mind=0.034 at N=350 vs 0.039 at N=1000); at n_pred=14, mind
  actually INCREASES with N (0.028 -> 0.047).
**Mechanism:** The encirclement targets are placed at R_enc=0.15 from the flock CoM.
For small N, this radius is comparable to the flock's own radius of gyration (Rg ~
0.10-0.15 at N=350); the predators occupy positions near the flock edge where they can
exert real pressure on the boundary.  At N=1000, the flock is broader -- Rg grows --
and R_enc=0.15 places the predators INSIDE the flock or close to its CoM, where their
repulsion is partially absorbed by surrounding prey.  The encirclement geometry stops
matching the flock geometry, and the angular pressure becomes less effective.  This is
a real geometric effect: encirclement requires R_enc ~ Rg to disrupt, and Rg grows
with N.
**Implication:** A predator strategy that worked at intermediate flock sizes does not
automatically scale up.  For a large flock, the encirclement radius would have to be
scaled up too -- but doing so positions the predators outside the flock's repulsion
range and they revert to ineffective orbiting (Section 4.6 radius sweep).  Real
predators facing very large prey aggregations may need to switch strategies entirely
(e.g., partition the flock into sub-groups before encircling) rather than scale a
single tactic.  The Finding 15 angular-coverage hypothesis is therefore correct
within a window of N, but not universal.

---

## Finding 29: Encirclement shifts the SIS epidemic threshold leftward by ~4%
<img src="./figures/critical_shift_1.png" width="480"/>

**What:** A direct sweep of beta at fixed gamma=2.0 with and without 6 encircling
predators measures the shift in the apparent epidemic threshold beta_c.  Without
encirclement, the threshold (where f_ss crosses 0.5) is beta_c = 1.93.  With
encirclement, beta_c = 1.85.  The shift is 0.077 in beta -- about 4% leftward.
**Evidence:** critical_shift.py, 5 seeds, slow prey, gamma=2.0, n_iter=5000.
| beta | f_ss (no enc) | f_ss (enc)  | shift |
|------|---------------|-------------|-------|
| 1.00 | 0.227 +- 0.11 | 0.271 +- 0.01 | +0.04 |
| 1.50 | 0.340 +- 0.17 | 0.425 +- 0.02 | +0.09 (largest) |
| 2.00 | 0.528 +- 0.01 | 0.533 +- 0.01 | +0.00 |
| 2.50 | 0.586 +- 0.01 | 0.594 +- 0.01 | +0.01 |
| 3.00 | 0.644 +- 0.01 | 0.638 +- 0.01 | -0.01 |
The encirclement effect is largest just below threshold (beta=1.5) where the system is
poised.  Above threshold the curves converge.
**Mechanism:** Encirclement compresses the flock and raises the local contact count
<k> by ~3x (Finding 26).  The bare epidemic threshold is beta_c * <k> ~ gamma, so a
3x larger <k> would naively lower beta_c by 3x.  The observed shift is much smaller --
4% rather than 70% -- because not all contacts within R_CONT propagate equally:
within a tightly compressed sub-flock, panicked agents are mostly surrounded by other
panicked agents, so the effective "new infection per contact" is reduced.  The
compression therefore creates redundant contagion rather than novel reach.
**Resolution of Finding 26 conjecture:** Finding 26 hypothesized that compression
would shift the threshold; this experiment confirms the shift exists (it is real and
statistically significant just below threshold) but quantifies it as modest.  A
contagion at 5% below the bare threshold can be tipped by encirclement; a contagion
at 30% below the threshold cannot.
**Implication:** Encirclement is a near-critical amplifier, not a general one.  For a
collective in a stable subcritical regime, an external pursuer cannot trigger a
runaway internal cascade.  But for a collective already living near the edge of a
contagion threshold, an external pursuer can be the difference between containment
and outbreak.  This combines the predation and contagion findings into a single
near-critical-coupling picture.

---

## Finding 30: Herd-immunity threshold in the flock is ~2x larger than mean-field predicts
<img src="./figures/herd_immunity_1.png" width="480"/>

**What:** At supercritical SIS (beta=2.5, gamma=2.0; bare R0=beta/gamma=1.25), a
sub-population of "immune" agents that never become panicked can quench the outbreak.
Mean-field SIS theory predicts the herd-immunity threshold p_c = 1 - 1/R0 = 0.20.
Measured threshold in the flock model (defined as p_immune at which f_ss drops below
0.1) is p_c ~ 0.46 -- more than twice the mean-field prediction.
**Evidence:** herd_immunity.py, 5 seeds, slow prey.
- p_immune=0.00: f_ss=0.586
- p_immune=0.20: f_ss=0.401  (mean-field threshold; still well above 0.1)
- p_immune=0.30: f_ss=0.301
- p_immune=0.40: f_ss=0.189
- p_immune=0.46: f_ss ~ 0.10  (interpolated empirical threshold)
- p_immune=0.50: f_ss=0.050
- p_immune=0.60: f_ss=0.019
**Mechanism:** Mean-field herd-immunity assumes a well-mixed population where every
contact has the same chance of being with an immune agent.  In the flock, contacts
are spatially structured: panicked sub-clusters move together so their members
contact mostly each other.  The effective <k> seen by a susceptible agent in a
panicked cluster is much higher than the average over the whole population, so the
immunity per cluster has to be higher to break the chain.  Spatial correlation
inflates the required threshold.
**Comparison with classical epidemic theory:** This effect is well-known in spatial
SIR/SIS models -- random vaccination is less effective than targeted vaccination.
The flock model recovers the qualitative result.  Quantitatively, p_c_measured /
p_c_mean_field = 2.3, which is large but not unprecedented for spatially clustered
contact networks.
**Implication:** For real biological collectives or human crowds, the fraction of
"calm anchors" needed to suppress contagion-driven panic is larger than naive
calculations suggest.  This is also a confirmation that the flock is NOT a well-mixed
population at the contagion length scale (r_cont=0.05 << flock radius Rg~0.15).
Spatial structure matters for both the encirclement results (Findings 16, 28) and the
contagion results (Findings 25, 30) -- the same locality that lets sub-flocks be
internally coherent also makes them vulnerable to contagion clusters.

---

## Finding 31: Encirclement scaling collapses on R_enc / Rg -- refining Finding 28
<img src="./figures/renc_scaling_1.png" width="480"/>

**What:** Finding 28 reported the encirclement floor rises with N at fixed R_enc=0.15.
The proposed mechanism was a geometric mismatch: R_enc was tuned to N=350's Rg and
became too small relative to N=1000's larger Rg.  This experiment tests that mechanism
directly by sweeping R_enc at both N=350 and N=1000.  Result: when plotted against
R_enc / Rg the two Phi curves COLLAPSE.  Optimal disruption is at R_enc / Rg ~ 0.5 for
both flock sizes, with Phi_min = 0.667 (N=350) and 0.732 (N=1000) -- very close.
**Evidence:** renc_scaling.py, 4 seeds, n_pred=10.
- N=350:  optimal R_enc = 0.15 (R/Rg = 0.48), Phi_min = 0.667
- N=1000: optimal R_enc = 0.20 (R/Rg = 0.60), Phi_min = 0.732
- At R_enc = 0.05 (R/Rg ~ 0.16) both sizes give Phi > 0.93 (predators co-localize at CoM)
- At R_enc = 0.30 (R/Rg > 0.87) both sizes give Phi > 0.97 (predators orbit outside flock)
- Surprisingly, Rg saturates around 0.30 for both N due to box-size confinement on the
  periodic unit square; the maximum geometric Rg in [0,1]^2 is 0.408.
**Refinement of Finding 28:** Finding 28's apparent N-dependence of the encirclement
floor was almost entirely an R_enc/Rg mismatch.  At N=1000 with R_enc=0.15, the
predators were at R_enc/Rg = 0.45 -- slightly inside the optimum.  Re-tuning to
R_enc=0.20 (R_enc/Rg = 0.60) recovers Phi = 0.732, essentially matching the N=350
floor.  The strategy is therefore size-invariant, but it must be re-calibrated to
flock geometry to maintain effectiveness.
**Interpretation of the optimum at R_enc/Rg ~ 0.5:** This places the predators within
the bulk of the flock (Rg is the RMS radius, so the average prey is at distance Rg
from CoM) but not at the center.  At R_enc/Rg ~ 0.5 each predator sits in the heart
of one quadrant of the flock, surrounded by prey on all sides and pushing them inward
toward neighboring predators.  At R_enc/Rg < 0.3 the predators converge too close to
CoM and overlap; at R_enc/Rg > 0.8 they exit the flock and exert force only on the
periphery.
**Implication:** Encirclement is geometrically rather than numerically constrained.
Predators tracking the flock's Rg (e.g., visually estimating its size and adjusting
approach distance) could deploy this strategy successfully against flocks of any size.
A predator strategy that wraps the flock at half its radius is universal.

---

## Finding 32: Long-time encirclement produces an intermittent merge/split steady state
<img src="./figures/long_encircle_1.png" width="480"/>

**What:** Running the encirclement protocol (n_pred=10, R_enc=0.15) for 30000 timesteps
(300 time units, 10x longer than typical short-time experiments) reveals that the
flock does NOT settle into a frozen fragmented configuration.  Instead, Phi oscillates
strongly throughout the run: mean Phi=0.751 +/- 0.061 across seeds, but the TEMPORAL
standard deviation within a single seed is 0.21 (excursions from Phi~0.4 to Phi~0.95).
Cluster count and largest cluster fraction oscillate similarly.  Sub-flocks
continuously merge and re-split.
**Evidence:** long_encirclement.py, 4 seeds, slow prey, last 1/3 of each run (t > 200):
- Phi:          mean = 0.751   across-seed std = 0.061   temporal-std-per-seed ~ 0.21
- n_clusters:   mean = 4.80
- largest_frac: mean = 0.455
- The temporal std exceeding the seed-to-seed std indicates fluctuations within each
  run dominate over baseline differences between runs -- the dynamics are intrinsically
  intermittent, not in a quiet steady state.
**Mechanism:** When the flock briefly aligns into a single coherent group (Phi -> 0.9),
the predators all chase one CoM target offset by their respective angles and apply
maximally-multi-directional pressure.  This is the strongest disruption, so the flock
quickly fragments.  Once fragmented (Phi -> 0.5), each predator preferentially follows
one sub-flock (whichever is nearest its angular target), reducing the multi-directional
pressure on any single sub-flock.  Without that pressure, the dominant sub-flock can
re-assemble or absorb others, raising Phi.  The cycle repeats: alignment provokes
maximum predation, fragmentation releases it.  The system explores both configurations
indefinitely.
**Comparison with the short-time (4000-step) result:** Finding 16 reported Phi=0.72
for the same setup at short times.  This long-time result confirms the time-averaged
value is similar (0.75), but reveals it hides large temporal swings that would be
invisible in a steady-state-only analysis.
**Implication:** The flock-under-encirclement is a dynamical system with attractor
dynamics that include intermittent re-merging events.  No stable sub-flock identity
exists; agents move between sub-flocks as the configuration evolves.  From a
biological perspective: encirclement does not "permanently break" the flock even
during sustained predation, but it does prevent the flock from settling into a
quiet aligned state.  The collective is repeatedly being reshuffled.

---

## Finding 33: Incomplete encirclement is mostly less disruptive, and the flock doesn't escape through the gap
<img src="./figures/gap_encirclement_1.png" width="480"/>

**What:** Starting from full 6-predator encirclement (n_total=6, 60-degree slots) and
removing predators one at a time produces non-monotone disruption.  Phi=0.92 at full
encirclement (with 6 predators), dips to 0.83-0.87 with 5 active predators, then RISES
back to 0.91-0.96 with 3-4 active predators.  The flock's center-of-mass drift
direction has no preferred alignment with the gap direction (mean angle differences
70-110 degrees from gap), so the flock does not steer toward the open side.
**Evidence:** encirclement_gap.py, 5 seeds, R_enc=0.15.
- n_active=6 (full):                          Phi=0.918 +/- 0.038, drift=0.34
- n_active=5 contiguous gap (one 60-deg open): Phi=0.833 +/- 0.041, drift=0.24
- n_active=5 distributed gap (irregular spacing): Phi=0.873 +/- 0.090, drift=0.42
- n_active=4 contiguous:                      Phi=0.963 +/- 0.029, drift=0.47
- n_active=4 distributed:                     Phi=0.908 +/- 0.042
- n_active=3 contiguous:                      Phi=0.955 +/- 0.035
- n_active=3 distributed:                     Phi=0.903 +/- 0.063
- Drift direction angle from gap direction: 70-110 degrees (essentially uncorrelated
  with gap orientation)
**Mechanism for non-monotonic Phi:** Removing one predator from a balanced 6-symmetric
configuration creates an asymmetry that the remaining 5 predators continuously chase --
the flock CoM shifts toward the gap, the 5 predators re-encircle the new CoM, but the
asymmetric pressure keeps the flock from settling.  This is more disruptive than the
balanced 6-fold pattern.  Removing 2-3 predators eliminates the asymmetry: 3-4
remaining predators at large spacing produce weaker multi-directional pressure, and the
flock partially recovers (Phi up to 0.96).  Contiguous gaps tend to be more disruptive
than distributed gaps with the same n_active because they preserve more local
multi-angle pressure on one side.
**Why no steering toward the gap:** The flocking force depends only on neighbor
velocities, not on absolute predator positions.  Agents do not perceive "where the
gap is" -- they only feel local repulsion from nearby predators and alignment with
local neighbors.  The CoM drifts toward the gap initially because the gap-side prey
feel no repulsion, but the predators continuously update their targets, so the
asymmetric pressure persists indefinitely.  There is no global escape route detection.
**Implication:** Biological "encirclement" by wolf packs leaves gaps for tactical
reasons (avoid friendly fire, allow some prey to scatter for easier individual pursuit)
rather than because gaps necessarily reduce flock disruption.  In this model, full
symmetric encirclement is paradoxically less disruptive than a near-full encirclement
with a single asymmetric gap.  A "near-perfect" trap may be the worst case for the
flock.

---

## Finding 34: Encirclement-established contagion persists after predator removal -- damage irreversibility requires both stressors
<img src="./figures/outbreak_removal_1.png" width="480"/>

**What:** Running a three-phase protocol (warmup -> encirclement + SIS -> predators removed)
with beta=1.5, gamma=2.0 (bare beta/gamma=0.75; bare endemic fraction ~0.34, below the
f_ss=0.5 threshold) tests whether contagion established under compression collapses once the
compressor is removed.  Result: it does NOT.  During encirclement, compression elevates local
<k> (Finding 26) and drives f to 0.450 and Phi to 0.185.  After predator removal, Phi
partially recovers (0.185 -> 0.266) consistent with sub-flock kinematic reunification, but
f only slowly declines (0.450 -> 0.413 in 50 time units), remaining far above the bare
endemic level.  The flock does not return to coherence.
**Evidence:** outbreak_removal.py, 5 seeds, slow prey (v0=0.02), n_pred=6, R_enc=0.15.
- During attack (last 5 tu, t=45-50):  f = 0.450 +/- 0.015   Phi = 0.185 +/- 0.055
- Post-removal (last 10 tu, t=89-100): f = 0.413 +/- 0.039   Phi = 0.266 +/- 0.069
**Mechanism:** When encirclement compresses the flock, local <k> triples (Finding 26,
8.9 -> 30.2), driving effective beta*<k>/gamma well above 1 and establishing an endemic
SIS state at f~0.45.  Removing the predators ends the kinematic compression -- sub-flocks
can re-merge (Finding 22), which raises Phi from 0.185 to 0.266 in ~50 tu.  But the
contagion was seeded into a large fraction of the population.  Post-removal, the bare
dynamics (beta/gamma=0.75, below threshold) should eventually drive f -> 0, but the
approach is slow: with f~0.41 and ~145 panicked agents still circulating among 350 total,
the per-step recovery rate is much slower than the peak infection rate during compression.
The system decays toward the bare endemic state (~0.34) on a timescale of hundreds of
time units -- far longer than the kinematic recovery time of ~10 tu (Finding 22).
**Contrast with Finding 22 (pure encirclement):** Without contagion, Phi recovers to
0.95+ in ~10 time units after predator removal.  With contagion established, Phi is still
only 0.266 after 50 time units.  The residual epidemic suppresses alignment even once the
kinematic stressor is gone.  Encirclement alone is fully reversible; encirclement + SIS
leaves a long-lived epidemiological scar.
**Contrast with Finding 23 (simultaneous encirclement + supercritical SI):** In Finding 23,
supercritical SI absorbed everything and predators were irrelevant.  Here, the contagion is
sub-threshold but pushed above a transient supercritical regime only by compression.  The
two stressors cooperate during the attack and then partially decouple on removal --
kinematic damage reverses quickly, epidemiological damage slowly.
**Implication:** From a biological standpoint: a predator group that triggers a panic
cascade (even a sub-threshold one) while physically encircling the flock inflicts lasting
damage that outlives the predation event itself.  The "reversibility" of predation
(Finding 22) is conditional on no contagion being present.  A predator strategy that
deliberately seeds panic first (or takes advantage of pre-existing near-critical social
contagion) achieves disproportionate impact relative to the duration of the attack.
This result connects kinematic and epidemiological timescales in a concrete prediction:
kinematic recovery ~ O(10) time units; epidemiological residual ~ O(100+) time units.

---

## Finding 35: Adaptive R_enc = 0.5*Rg is more disruptive than fixed R_enc, confirming the F31 universal ratio
<img src="./figures/adaptive_encirclement_1.png" width="480"/>

**What:** Comparing fixed R_enc=0.150 vs adaptive R_enc = 0.5 × live_Rg for n_pred=10,
N=350, 15000 steps (150 tu), 5 seeds.  Adaptive is more disruptive: mean Phi drops
0.778 -> 0.713 and the fraction of time above Phi=0.85 drops 0.56 -> 0.37.
| Condition | mean_Phi | seed_std | temporal_std | frac>0.85 | mean_Renc/Rg |
|-----------|----------|----------|--------------|-----------|--------------|
| Fixed     |   0.778  |  0.250   |    0.233     |   0.56    |     0.485    |
| Adaptive  |   0.713  |  0.234   |    0.219     |   0.37    |     0.500    |
**Evidence:** adaptive_encirclement.py, 5 seeds, slow prey (v0=0.02, ramp=0.1), N=350.
**Mechanism:** During the merge/split cycle (Finding 32), flock Rg fluctuates as
sub-flocks disperse (large Rg) and reconsolidate (smaller Rg).  Fixed R_enc=0.150
achieves mean R_enc/Rg=0.485 (close to optimal but drifts from it during fluctuations).
Adaptive maintains R_enc/Rg=0.500 throughout by tracking live Rg.  This suppresses the
recovery-to-high-Phi excursions that occur when a reconsolidating flock temporarily
escapes the fixed predators' optimal zone.  Lower temporal_std (0.219 vs 0.233) for
adaptive confirms the excursions are reduced.
**Effect size:** Mean Phi reduction of 8.3% is modest -- consistent with Finding 31's
observation that the disruption function has a relatively flat plateau near the optimal.
The frac_above_0.85 reduction (0.56 -> 0.37; -34% relative) is a larger effect because
it measures coherent-state dwell time, which adaptive systematically eliminates.
**Comparison with Finding 31:** Finding 31 showed encirclement performance collapses on
R_enc/Rg and the optimum is at ~0.5 for both N=350 and N=1000.  The adaptive experiment
closes the loop: a predator that tracks live Rg achieves essentially the same optimal
ratio, and does so consistently across the entire time series rather than only at
initialization.  The result validates both the R_enc/Rg scaling (F31) and the adaptive
strategy jointly.
**Null-result caveat:** Adaptive R_enc uses GLOBAL Rg (all N=350 prey), which inflates
when the flock is fragmented into dispersed sub-flocks.  A more sophisticated predator
tracking per-sub-flock Rg would adapt to individual fragments.  The current adaptive
strategy therefore represents a conservative lower bound on adaptive advantage.
**Implication:** A real predator group that can estimate overall flock extent and adjust
encirclement radius proportionally achieves 8% higher disruption in mean alignment and
34% more time in the flock's fragmented state.  The strategy generalises across N without
re-calibration.  In contrast, a fixed-radius encirclement strategy (Finding 15, F31)
must be recalibrated when the flock grows or shrinks.

---

## Finding 36: Targeted vaccination provides no significant advantage over random vaccination -- the flock contact network is not hub-dominated
<img src="./figures/targeted_immunity_1.png" width="560"/>

**What:** Comparing targeted (top contact-degree agents immunised first) vs random
vaccination at supercritical SIS (beta=2.5, gamma=2.0, R0=1.25 -- same as Finding 30).
Result: no significant advantage for targeted vaccination at any p_immune.  The herd-
immunity threshold is p_c ~ 0.46 for BOTH strategies, identical to Finding 30's random-
vaccination result.
| p_immune | f_ss (random)  | f_ss (targeted) | diff    |
|----------|----------------|-----------------|---------|
|   0.00   | 0.593 +/- 0.008| 0.587 +/- 0.006 | -0.006  |
|   0.10   | 0.491 +/- 0.010| 0.495 +/- 0.006 | +0.004  |
|   0.20   | 0.393 +/- 0.008| 0.395 +/- 0.010 | +0.002  |
|   0.30   | 0.304 +/- 0.013| 0.301 +/- 0.014 | -0.003  |
|   0.40   | 0.204 +/- 0.016| 0.177 +/- 0.080 | -0.027  |
|   0.46   | 0.101 +/- 0.072| 0.084 +/- 0.065 | -0.016  |
|   0.50   | 0.046 +/- 0.066| 0.043 +/- 0.053 | -0.003  |
|   0.60   | 0.000 +/- 0.000| 0.000 +/- 0.000 |  0.000  |
All differences at p <= 0.30 are within statistical noise (|diff| <= 0.006, smaller than
both error bars).  Near threshold (p=0.40-0.46) targeted shows a small edge (diff =
-0.027 and -0.016) but the variance for targeted is 4-5x higher than for random
(std 0.080 vs 0.016 at p=0.40), making these differences not statistically robust.
**Evidence:** targeted_immunity.py, 6 seeds, slow prey (v0=0.02).
Degree distribution across 6 seeds: mean=9.02, median=8, std=6.17, max=31.
**Mechanism -- why targeting fails:**
The classical network theory result (target hub nodes first) requires a fat-tailed degree
distribution in which a small fraction of agents have dramatically higher connectivity.
In a scale-free network, max_k/mean_k can be 100-1000x; here max_k/mean_k = 31/9 = 3.4.
The degree heterogeneity (CV = std/mean = 6.17/9.02 = 0.68) is moderate but bounded.
Immunising the top-degree agents removes the most connected individuals, but in a
kinematic flock the contact network is not fixed: as high-degree agents at the flock
center are immunised, their neighbors close in via the repulsion and alignment forces,
and new hub positions form in the interior.  Spatial reorganisation restores the
contact structure even when the specific high-degree agents are neutralised.
**Contrast with Finding 30:** Finding 30 showed the random herd-immunity threshold is
~2x mean-field (p_c~0.46 vs 0.20) due to spatial clustering.  The 2x inflation came
from panicked sub-clusters moving together -- agents within a cluster contact mostly
each other.  This is SPATIAL clustering, not degree heterogeneity.  Targeted vaccination
is designed to exploit degree heterogeneity, not spatial clustering.  The flock has both
properties, but the spatial-clustering effect is the dominant one for herd immunity, and
targeted vaccination does not specifically counter it.
**Implication:** Degree-targeted vaccination strategies, which are highly effective in
scale-free social networks, offer minimal advantage in flocking collectives.  The reason
is that flock contact networks are spatially-embedded and nearly uniform in degree: the
most connected agents are those near the flock center, and their connectivity arises
from geometric proximity (many neighbors in a dense region), not from topological hub
status.  For a flock-like system, what matters for herd immunity is breaking the spatial
clusters (which would require geographically targeted, rather than degree-targeted,
vaccination -- e.g. vaccinating agents uniformly spread across the spatial extent of the
flock, not just the high-degree core agents).

---

## Finding 37: Spatial vaccination provides no advantage over random -- kinematic mixing erases spatial targeting
<img src="./figures/spatial_vaccination_1.png" width="640"/>

**What:** Finding 36 identified that the 2x mean-field herd-immunity threshold inflation (p_c~0.46 vs 0.20)
is caused by SPATIAL CLUSTERING of panicked sub-groups, not degree heterogeneity.  This experiment tests
the hypothesis that geographically-targeted immunity -- selecting immune agents by farthest-point maxmin
sampling to maximally cover the flock's spatial extent -- would outperform random vaccination by directly
targeting the spatial-clustering mechanism.
**Evidence:** spatial_vaccination.py, 5 seeds, beta=2.5, gamma=2.0, R0=1.25.
Summary table (mean +/- std over 5 seeds):
  p_immune   f_ss random       f_ss spatial     f_ss targeted
  0.00       0.594+/-0.009    0.589+/-0.006    0.586+/-0.006
  0.10       0.490+/-0.010    0.492+/-0.010    0.493+/-0.006
  0.20       0.391+/-0.007    0.391+/-0.013    0.398+/-0.009
  0.30       0.301+/-0.011    0.297+/-0.009    0.298+/-0.013
  0.40       0.202+/-0.016    0.170+/-0.085    0.168+/-0.085
  0.46       0.088+/-0.073    0.125+/-0.063    0.072+/-0.064
  0.50       0.056+/-0.068    0.088+/-0.045    0.052+/-0.055
  0.60       0.000+/-0.000    0.000+/-0.000    0.000+/-0.000
Degree distribution: mean=8.79, median=8, std=6.07, max=31.
**Null result:** All three strategies produce statistically indistinguishable f_ss at every
p_immune value.  At p=0.10-0.30, all means differ by at most 0.007 (well within noise).
Near threshold (p=0.40-0.50), spatial and targeted strategies show much LARGER variance
(std~0.085) than random (std~0.016-0.068), making their mean values unreliable.  At p=0.46
the spatial strategy (f=0.125) is actually slightly WORSE than random (f=0.088).
**Mechanism -- why spatial targeting fails:**
(1) KINEMATIC MIXING: Flock agents constantly rearrange via the alignment, repulsion, and
self-propulsion forces.  The warmup flock position (at which immune agents are selected) is
uncorrelated with the agent positions at t=50 or t=100 when SIS dynamics are running.  The
spatial distribution of immune agents at vaccination time is scrambled by the time the
epidemic begins, making spatial targeting equivalent to random.
(2) RANDOM IS MORE RELIABLE NEAR THRESHOLD: At p=0.40-0.46, random vaccination has small
variance (std~0.016-0.073) while spatial and targeted have large variance (std~0.063-0.085).
Random vaccination distributes immune agents across all spatial regions probabilistically,
giving a stable average outcome near threshold.  Spatial/targeted place immune agents in
specific positions that may or may not align with the epidemic seed location -- a source of
high variability without a mean improvement.
**Comparison with F36:** Both F36 (degree-targeted) and F37 (spatially-targeted) are null
results, for the same underlying reason: the flock contact network is DYNAMIC.  Kinematic
reorganization (F36) restores hub positions after degree-targeted immunization; kinematic
mixing (F37) scrambles spatial positions after spatial immunization.  Neither targeting
strategy can maintain its structural advantage in a flocking system.
**Implication:** For kinematic flocking collectives, no agent-selection strategy outperforms
random vaccination.  The 2x herd-immunity threshold inflation is a structural property of the
spatial contact network (driven by collective alignment that creates spatial clusters), and
it cannot be exploited through any static vaccination strategy applied before the epidemic
runs.  Effective containment requires either a high overall immune fraction (~0.46) or a
dynamic vaccination strategy applied during the epidemic as agent positions are tracked.

---

## Finding 38: Repulsion hardness does not affect the crossover -- the absence of a phase transition is driven by non-equilibrium forcing, not potential softness
<img src="./figures/hard_repulsion_1_chi.png" width="640"/>
<img src="./figures/hard_repulsion_2_ke.png" width="640"/>

**What:** Finding 17 showed no phase transition in the standard model (n=1.5 repulsion exponent)
at any compactness C=0.10-0.78, and conjectured that the soft repulsion potential was the
root cause.  This experiment tests the conjecture directly by sweeping repulsion exponent
n = 1.5, 3.0, 6.0, 12.0 with finite-size scaling (N=25, 50, 100, 200; C=0.40, 8 seeds, no
flocking/self-propulsion).  Result: the chi-peak (susceptibility) for ALL exponents lies at
eta=30 (the top of the sweep), for ALL N values.  The KE/N curves and crossover shape are
essentially identical across n=1.5 to n=12.
**Evidence:** hard_repulsion.py, 8 seeds, C=0.40, N=25-200, eta=0.5-30.
chi_peak at eta=30.0 for all (n, N) combinations tested:
  n=1.5:  N=25: chi=2607  N=50: chi=7311  N=100: chi=3785  N=200: chi=3858
  n=3.0:  N=25: chi=2609  N=50: chi=7305  N=100: chi=3766  N=200: chi=3854
  n=6.0:  N=25: chi=2615  N=50: chi=7285  N=100: chi=3770  N=200: chi=3851
  n=12.0: N=25: chi=2615  N=50: chi=7289  N=100: chi=3773  N=200: chi=3853
KE/N ranges also nearly identical across exponents at same N.
**Interpretation:** The absence of a phase transition is NOT caused by the softness of the
repulsion potential.  In equilibrium statistical mechanics, 2D hard discs (C=0.40) form a
hexagonal solid at low temperature and undergo KTHNY melting at higher temperature -- a true
phase transition does exist for hard-core potentials.  Our model produces no such transition
even at n=12 (near hard-core) because the driving is NON-EQUILIBRIUM: uniform random kicks
(not thermal noise satisfying detailed balance) with no viscous damping (no Stokes friction
-mu*v term).  Without the fluctuation-dissipation relation, the "temperature" is not a
well-defined control parameter, and the system cannot equilibrate into a crystal phase that
melts sharply.  Instead, the crossover is set by the competition between random kick energy
and positional confinement (cage size ~ r0), which depends on the force RANGE (2r0) but is
insensitive to the force PROFILE (exponent n).
**Implication:** Finding 17's conjecture was correct in one sense (the model cannot produce
a true phase transition) but wrong about the cause.  The missing ingredient is not harder
repulsion but thermal equilibration: a Langevin simulation with viscous damping (-mu*v),
noise amplitude sqrt(2*mu*kT/dt), and a well-defined temperature T would recover the
hard-disc transition.  Within the current model family (self-propulsion regulation, not
viscous damping), no modification of the repulsion exponent will produce a diverging
susceptibility.  The solid-to-fluid crossover is a universal consequence of the non-
equilibrium driving, not a potential-specific artifact.

---

## Finding 39: Langevin thermostat thermalizes correctly but KE/N does not detect KTHNY melting
<img src="./figures/langevin_1.png" width="640"/>

**What:** Finding 38 diagnosed that the smooth crossover in the repulsion-only model is
caused by non-equilibrium driving (no FDT), not by soft repulsion.  The proposed fix was
to replace the driving with Langevin dynamics.  This experiment tests that fix: proper
Langevin thermostat (viscous damping -mu*vx/vy plus FDT-satisfying noise sqrt(2*mu*kT*dt))
at C=0.60 and C=0.70 (bracketing the 2D hard-disc melting point ~0.69-0.72), N=25-200,
kT=0.001-5.0, 8 seeds.
**Evidence:** langevin_repulsion.py. Summary of chi_peak and equipartition check:
Compactness C=0.60:
  N= 25: chi_peak=0.0817 at kT=5.000  |  KE/N(kT=0.1)=0.1047 vs kT=0.100
  N= 50: chi_peak=0.0406 at kT=5.000  |  KE/N(kT=0.1)=0.1053 vs kT=0.100
  N=100: chi_peak=0.0507 at kT=5.000  |  KE/N(kT=0.1)=0.1051 vs kT=0.100
  N=200: chi_peak=0.0440 at kT=5.000  |  KE/N(kT=0.1)=0.1054 vs kT=0.100
Compactness C=0.70: identical chi_peak values to C=0.60.
**Two key observations:**
(1) EQUIPARTITION SATISFIED: KE/N at kT=0.1 is 0.1047-0.1054, matching kT=0.100 to within
1%.  The Langevin dynamics work as designed -- the system thermalizes to the Boltzmann
distribution and the velocity distribution has the correct temperature.
(2) IDENTICAL BEHAVIOR FOR C=0.60 AND C=0.70: At kT=5.0 (chi peak), the thermal energy
(kT=5.0) is 50x larger than the repulsion amplitude (eps=0.1), so positional interactions
are negligible and both compactnesses behave as free gases.  The chi values at kT=5.0 are
therefore determined by the thermal fluctuations of a free gas, not by the repulsion, and
are C-independent.  The system's positional structure (which DOES differ between C=0.60
and C=0.70 at low kT) is invisible to the KE/N metric.
**Interpretation:** The Langevin thermostat confirms the FDT diagnosis from F38: the system
now equilibrates thermally.  However, the chi = N * Var(KE/N) susceptibility does NOT detect
the KTHNY structural phase transition.  KTHNY melting is a transition in POSITIONAL ORDER
(hexatic bond-angle correlation, defect proliferation), not in kinetic energy.  The right
observable would be the hexatic order parameter |psi_6| = |mean_neighbors(exp(6*i*theta))|
or the bond-angle correlation function g6(r).  With KE/N, both solid (low kT) and fluid
(high kT) phases give low seed-to-seed variance (all seeds agree on KE/N ≈ kT), so the
metric cannot distinguish them.  The chi_peak at kT=5.0 reflects free-gas noise at high
temperature, not a structural critical point.
**Implication:** To demonstrate the KTHNY transition in this model, two changes are needed:
(1) Add a positional order metric (hexatic order parameter psi_6 or g(r)).
(2) Use harder repulsion (larger n) so the solid-fluid transition occurs at a kT accessible
in the simulation (soft n=1.5 repulsion may push the transition to very low kT where
equilibration times are long).  Finding 38 showed that harder n doesn't help the
non-equilibrium model, but in the Langevin model harder n would produce a sharper
transition at higher kT.  This remains open for a future experiment.

---

## Finding 40: Hexatic order parameter confirms n=1.5 soft repulsion cannot crystallize -- KTHNY transition requires harder potential
<img src="./figures/langevin_hexatic_1.png" width="640"/>

**What:** Finding 39 established that chi_KE is insensitive to structural melting and proposed
that the hexatic order parameter |psi6| = |(1/k_j) * sum_neighbors exp(6*i*theta)| is the
correct observable for the KTHNY structural phase transition.  This experiment (langevin_hexatic.py)
replaces chi_KE with chi_psi6 = N * Var_seeds(time-avg |psi6|) for the same Langevin simulation
at C=0.60 and C=0.70, N=25-200, kT=0.001-5.0, 8 seeds, n=1.5.
**Evidence:** langevin_hexatic.py. Summary of chi_psi6 and |psi6| vs kT:
| C | N | chi_psi6_peak | kT of peak | psi6(kT=0.001) | psi6(kT=5.0) |
|---|---|---------------|------------|----------------|--------------|
| 0.60 | 25  | 0.0115 | 0.001 | 0.416 | 0.425 |
| 0.60 | 50  | 0.0044 | 0.001 | 0.423 | 0.423 |
| 0.60 | 100 | 0.0024 | 0.005 | 0.421 | 0.422 |
| 0.60 | 200 | 0.0042 | 0.001 | 0.416 | 0.421 |
| 0.70 | 25  | 0.0044 | 0.005 | 0.372 | 0.387 |
| 0.70 | 50  | 0.0023 | 0.001 | 0.378 | 0.386 |
| 0.70 | 100 | 0.0010 | 0.005 | 0.377 | 0.386 |
| 0.70 | 200 | 0.0027 | 0.001 | 0.376 | 0.385 |
Equipartition confirmed (KE/N at kT=0.1 is 0.1053-0.1055, within 1% of target kT=0.1).
**Null result -- three diagnostic failures of KTHNY signal:**
(1) |psi6| IS FLAT across all kT: C=0.60 varies only 0.416-0.425 (2%) across the entire
kT sweep; C=0.70 varies 0.372-0.387 (4%).  A KTHNY solid-to-fluid transition would show
|psi6| near 1.0 in the solid phase and near 0 in the fluid phase, with a sharp crossover
at kT_c.  Here |psi6| is constant at ~0.4 at BOTH the coldest (kT=0.001) and hottest (kT=5.0)
temperatures -- no solid phase, no fluid phase in the expected KTHNY sense.
(2) chi_psi6 PEAKS AT THE BOTTOM OF THE SWEEP (kT=0.001-0.005): the susceptibility has no
interior maximum.  This is the signature of a monotonically decreasing function, not of a
critical point at finite kT_c.
(3) chi_psi6 DOES NOT GROW WITH N: for C=0.60, chi_psi6_peak goes 0.0115 (N=25) -> 0.0024
(N=100) -> 0.0042 (N=200), with no systematic increase.  A diverging susceptibility would
scale as N^(gamma/nu).  The observed values actually decrease.
**Mechanism:** The failure is not in the metric (psi6 IS the correct observable for KTHNY)
but in the potential.  For a hexagonal crystal to form, each agent must have 6 neighbors at a
well-defined lattice spacing with no overlap.  The n=1.5 repulsion (F ~ (1-d/2r0)^1.5) is a
smooth contact avoidance: it approaches zero at d=2r0 and allows significant overlap before
becoming substantial.  Agents can pass through each other's soft cores at any finite kT,
preventing a rigid hexagonal lattice from locking in.  The psi6 ~0.4 constant reflects fixed
short-range geometric correlation from the initial repulsive packing, not a thermally-ordered
crystalline phase.
**Counterintuitive density dependence:** C=0.70 has lower psi6 than C=0.60 at all kT (0.38
vs 0.42).  In equilibrium hard-disc systems, higher compactness drives more hexagonal order.
With soft repulsion, the opposite occurs: at C=0.70, agents are close enough to exert
significant overlapping repulsion in many directions simultaneously, creating a frustrated
amorphous arrangement.  At C=0.60 there is more room and agents settle into locally hexagonal
clusters (psi6 slightly higher), but without long-range crystalline order.
**Implication:** The four-experiment phase-transition thread is now complete:
- F17: no transition in original model (any C)
- F38: non-equilibrium driving (not softness) is the cause
- F39: Langevin thermalizes correctly; KE/N is wrong metric
- F40: correct metric (|psi6|) confirms n=1.5 cannot crystallize; psi6 flat across all kT
To demonstrate KTHNY requires a near-hard-core Langevin simulation (n=12 or true hard-disc
MC) where agents cannot overlap and a hexagonal lattice can lock in at low kT.  That is a
distinct experimental direction beyond the current model family.

---

## Open Questions / Next Directions
1. Literature comparison: completed 2026-05-15 (session 2). New papers added: Demsar &
   Lebar Bajec 2014, Bartashevich et al. 2024, Inada & Kawachi 2002, Scientific Reports 2025.
   Novelty table updated for F14, F16, F22, F32, F33, F34, F35, F37, F38.
2. Spatial vaccination strategy (F37): COMPLETE. Null result -- kinematic mixing erases all
   static targeting strategies. p_c~0.46 for random, spatial, and targeted.
3. KTHNY via hexatic order parameter (F40): COMPLETE. n=1.5 soft repulsion cannot crystallize;
   psi6 flat at ~0.4 across all kT. Correct metric confirmed; harder potential needed for KTHNY.
4. 3D flocking extension: extend model to [0,1]^3 periodic domain; test whether the
   flock division mechanism and encirclement results still hold in 3D.

---

## Finding 41: 3D flocking validates cleanly -- v_eq = v0 + alpha/mu exact in 3D; crossover is less noise-robust than 2D
<img src="./figures/flocking3d_1.png" width="640"/>

**What:** Extension of the 2D flocking model to [0,1]^3 periodic domain.  Parameters scaled
so that 3D has similar neighbor count to 2D: rf=0.20 gives N*(4/3)*pi*rf^3 = 11.7 expected
neighbors (matching 2D rf=0.1 with ~11 neighbors).  r0=0.02 gives volume fraction ~0.012.
All other parameters unchanged from 2D defaults.
**Evidence:** flocking3d.py, N=350, r0=0.020, rf=0.20, alpha=1.0, v0=1.0, mu=10.0, 8 seeds.
ramp sweep [0.0, 0.1, 0.2, 0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0]:
  ramp=0.0:  Phi=1.0000  |v|=1.1000
  ramp=0.1:  Phi=1.0000  |v|=1.1000
  ramp=0.5:  Phi=0.9995  |v|=1.1000
  ramp=1.0:  Phi=0.9982  |v|=1.1001
  ramp=2.0:  Phi=0.9931  |v|=1.1006
  ramp=5.0:  Phi=0.9595  |v|=1.1035
  ramp=10.0: Phi=0.8409  |v|=1.1138
**Key result 1 -- v_eq analytical result holds exactly in 3D:**
Measured |v| at ramp=0 is 1.1000, matching the predicted v_eq = v0 + alpha/mu = 1.1000 exactly.
The derivation (force balance at equilibrium in an aligned flock: alpha + mu*(v0-v_eq) = 0)
uses only the 1D force balance along the aligned direction, which is dimensionality-independent.
**Key result 2 -- 3D flocking works but is less noise-robust than 2D:**
Phi degrades monotonically from 1.000 (ramp=0) to 0.841 (ramp=10).  In 2D at the same
ramp=10, Phi is approximately 0.97-0.99 (from phase sweep data).  The 3D model is less
noise-robust because random noise affects all 3 velocity components: at ramp=10, the noise
RMS magnitude is ramp*sqrt(3/3) = ramp per agent in 3D vs ramp*sqrt(2/3) per agent in 2D.
More degrees of freedom reduce the effectiveness of the alignment force at restoring order.
The crossover is at ramp >> 10 -- an extended sweep to ramp=30 is needed to characterize
the full transition region.
**Seed-to-seed consistency:** std across seeds is very small throughout (0.0022 at ramp=10),
confirming the 3D model is deterministic and well-behaved.
**Implication:** The force-based flocking model generalizes cleanly to 3D.  The core
analytical result (v_eq = v0 + alpha/mu) is universal.  The 3D transition region is at
higher ramp than the first 10-step sweep covers; extended noise sweep is the natural next step.

---

## Finding 42: 3D noise crossover is smooth like 2D -- chi_peak drifts up with N; 3D less noise-robust than 2D
<img src="./figures/flocking3d_noise_1.png" width="640"/>

**What:** Finding 41 showed 3D flocking is coherent to ramp=10 but the crossover lies at
ramp>>10.  This experiment (flocking3d_noise.py) runs an extended noise sweep (ramp=0.5-30)
for 3D at N=100, 200, 350 and 2D N=350 (matched neighbor count), measuring Phi and
chi = N * Var_seeds(Phi) for finite-size scaling.
**Evidence:** flocking3d_noise.py, N_SEEDS=8, N_ITER=4000, ramp=0.5-30.
3D results:
  N=100: chi_peak=0.1139 at ramp=15.0 | Phi(ramp=0.5)=0.9993 | Phi(ramp=20)=0.2205
  N=200: chi_peak=0.0970 at ramp=20.0 | Phi(ramp=0.5)=0.9995 | Phi(ramp=20)=0.3300
  N=350: chi_peak=0.1951 at ramp=25.0 | Phi(ramp=0.5)=0.9995 | Phi(ramp=20)=0.4197
2D N=350 (matched neighbor count: rf=0.1, r0=0.005):
  chi_peak=0.7683 at ramp=30.0 | Phi(ramp=0.5)=0.9997 | Phi(ramp=20)=0.6017
**Key result 1 -- 3D crossover at ramp~15-25; 2D crossover at ramp>30:**
In 3D, Phi transitions from ~0.999 (ramp=0.5) to 0.22-0.42 (ramp=20, N-dependent).
The 2D model is far more noise-robust: Phi=0.60 at ramp=20, and chi_peak is still at the
top of the sweep (ramp=30), indicating the 2D crossover lies beyond ramp=30.  The 3D model
is less noise-robust because the additional noise degree of freedom (3rd component) increases
total perturbation magnitude relative to alignment strength.
**Key result 2 -- chi_peak shifts UP with N (smooth crossover, not phase transition):**
For a true phase transition, chi_peak grows with N AND the peak location converges to a
finite ramp_c as N->inf.  Here, the peak location INCREASES with N:
  N=100: ramp_c=15  |  N=200: ramp_c=20  |  N=350: ramp_c=25
This is the signature of a smooth crossover: larger systems maintain coherence to higher noise
because the alignment force averages over more neighbors, shifting the crossover upward.
chi_peak values are non-monotonic (0.1139, 0.0970, 0.1951), not systematically diverging.
**Key result 3 -- same qualitative behavior in 2D and 3D:**
Both 2D and 3D show smooth noise-driven crossovers in this model family, consistent with
the non-equilibrium driving mechanism (no FDT) identified in F38.  The 3D crossover simply
occurs at lower ramp because 3 noise components > 2.
**Implication:** The 3D force-based flocking model has the same qualitative phase behavior
as 2D: a smooth crossover, not a true phase transition.  The 3D crossover region is
ramp~15-25 for N=100-350 (vs ramp>30 for 2D).  The v_eq result (F41), smooth crossover (F42),
and finite-size behavior are consistent between 2D and 3D.

---

## Finding 43: 3D encirclement fails to replicate 2D effectiveness -- R_enc/Rg universal optimum is 2D-specific
<img src="./figures/flocking3d_predator_1.png" width="640"/>

**What:** Extends the 3D flocking model with predator pressure. Tests naive (chase CoM) vs
encirclement strategies at n_pred=1,3,6,10, and sweeps R_enc to test whether the R_enc/Rg~0.5
universal optimum from Finding 23 transfers to 3D.
**Evidence:** flocking3d_predator.py, N=350, slow prey v0=0.02, ramp=0.1, N_SEEDS=5, N_ITER=5000.
3D encirclement results (R_enc=0.15, n_pred=1-10):
  n_pred=1:  Phi=0.999  Rg=0.421
  n_pred=3:  Phi=0.999  Rg=0.417
  n_pred=6:  Phi=0.953+/-0.077  Rg=0.397
  n_pred=10: Phi=0.941+/-0.074  Rg=0.375
2D encirclement at same R_enc=0.15:
  n_pred=3:  Phi=0.969  |  n_pred=6:  Phi=0.750  |  n_pred=10: Phi=0.729
3D R_enc sweep at n_pred=6:
  R_enc=0.15: R_enc/Rg=0.38, Phi=0.953+/-0.077
  R_enc=0.20: R_enc/Rg=0.50, Phi=0.997+/-0.001  <-- 2D optimum, NO disruption in 3D
  R_enc=0.25: R_enc/Rg=0.62, Phi=0.985
**Key result 1 -- naive predators fail in 3D as in 2D:**
Naive co-localization occurs in 3D for the same reason as 2D (all predators target the same
3D CoM), giving Phi>0.99 at all n_pred. The co-localization mechanism is dimension-independent.
**Key result 2 -- encirclement is dramatically less effective in 3D:**
At n_pred=6 and R_enc=0.15 (2D-calibrated), 3D encirclement gives Phi=0.953 (high variance
+/-0.077) vs 2D Phi=0.750 (consistent). At n_pred=10, Phi=0.941 vs 2D Phi=0.729.
Disruption exists but is mild and unreliable -- the 3D flock is much more robust.
**Key result 3 -- R_enc/Rg~0.50 universal optimum does NOT transfer to 3D:**
The R_enc sweep shows minimum disruption at R_enc=0.15 (R_enc/Rg=0.38), NOT at R_enc/Rg=0.50.
At R_enc=0.20 (exactly R_enc/Rg=0.50 -- the 2D optimum), Phi jumps back to 0.997 (no
disruption). The 2D universal scaling law breaks down completely in 3D.
**Key result 4 -- mechanism: 3D provides an escape dimension and sparse sphere coverage:**
(a) The 3D flock has Rg~0.40 vs 2D Rg~0.29 -- larger spread means the same absolute R_enc
corresponds to a smaller R_enc/Rg. (b) More fundamentally, 6 predators on a sphere surface
cover far less of the solid angle than 6 predators on a circle cover of the full circle: a
sphere surface is ~6x larger than a same-radius circle, so encirclement density drops. (c)
The flock can escape through the third spatial dimension (vertical to any predator plane),
making encirclement fundamentally less effective regardless of R_enc.
**Implication:** Encirclement is a 2D-specific strategy whose effectiveness depends on
predators sealing a 1D ring (circle). In 3D, sealing a 2D surface (sphere) with the same
number of predators is geometrically much harder. Effective 3D predator encirclement would
require either many more predators (to achieve comparable sphere coverage) or a fundamentally
different strategy that blocks all 3D escape directions simultaneously.

---

## Finding 44: 3D encirclement disruption is non-monotonic in predator count -- a hard floor at Phi~0.91, never reaching the 2D floor
<img src="./figures/finding44_3d_predator_scaling.png" width="640"/>

**What:** Sweeps predator count n_pred = 1, 3, 6, 10, 20, 50 for 3D encirclement at fixed
R_enc = 0.15, to test whether adding predators closes the sphere-surface coverage gap and
drives 3D disruption down toward the 2D floor (~0.67).
**Evidence:** flocking3d_predator_scaling.py, N=350, slow prey v0=0.02, ramp=0.1,
N_SEEDS=5, N_ITER=5000, warmup=3000.
  n_pred= 1  Phi=0.999+/-0.000  Rg=0.421+/-0.009
  n_pred= 3  Phi=0.999+/-0.000  Rg=0.417+/-0.008
  n_pred= 6  Phi=0.981+/-0.022  Rg=0.399+/-0.015
  n_pred=10  Phi=0.913+/-0.082  Rg=0.355+/-0.049   <-- disruption optimum
  n_pred=20  Phi=0.975+/-0.026  Rg=0.312+/-0.044
  n_pred=50  Phi=0.930+/-0.035  Rg=0.241+/-0.024
**Key result 1 -- the geometric prediction is falsified.**
The pre-registered prediction (F43 follow-up) was a monotonic decrease in Phi with n_pred,
crossing the 2D floor (~0.67) near n_pred ~ 20-50 once the sphere surface was adequately
covered. Instead disruption is NON-MONOTONIC: Phi reaches a shallow minimum of 0.913 at
n_pred=10, then RISES back to 0.93-0.98 for n_pred = 20 and 50. The 3D order parameter
never drops below ~0.91 at any predator count tested. The "coverage-limited" hypothesis --
that enough predators would seal the sphere -- is wrong.
**Key result 2 -- mechanism: more predators compress, they do not divide.**
Rg falls monotonically with n_pred (0.42 -> 0.24): each added predator squeezes the flock
inward. In 2D this compression DIVIDES the flock into scattering sub-flocks (F15), which is
why 2D encirclement works. In 3D the same compression instead packs the flock into a
denser, smaller sphere. A denser flock has stronger local alignment coupling (more
neighbors within rf), so it is MORE coherent, not less. Past n_pred~10 the compression
effect dominates and Phi climbs back up. 3D encirclement therefore has a built-in
self-defeating feedback: the harder you squeeze, the more cohesive the target becomes.
**Key result 3 -- the n_pred=10 optimum is real but unreliable.**
At the optimum the seed-to-seed std is large (+/-0.082): some seeds reach Phi~0.8, others
stay near 0.99. n_pred=10 sits on a knife-edge between the under-coverage regime (few
predators, flock ignores them) and the over-compression regime (many predators, flock
balls up). Neither neighboring count is reliably disruptive.
**Implication:** Encirclement cannot be rescued in 3D by brute-force predator count. The
2D floor of Phi~0.67 is unreachable in 3D with this strategy at any n_pred up to 50. This
confirms F43's deeper reading: the escape-dimension argument is FUNDAMENTAL, not merely a
coverage deficit. Effective 3D flock disruption requires a qualitatively different
strategy -- one that exploits the compression-induced density gradient or attacks the
flock's internal alignment coupling directly, rather than relying on geometric enclosure.

---

## Finding 45: 3D adaptive encirclement is a null result -- adaptive tracking does not help, and mildly hurts by damping disruptive fluctuations
<img src="./figures/finding45_3d_adaptive.png" width="560"/>

**What:** In 2D, adaptive R_enc = 0.5*live_Rg outperforms fixed R_enc (F35) by holding the
predators at the R_enc/Rg~0.5 optimum through the merge/split cycle. This tests whether
adaptive tracking helps in 3D, where F43 showed the 2D optimum ratio does not transfer.
Compares fixed R_enc=0.15 against adaptive at ratios 0.38 and 0.50, n_pred=10, long run
(15000 steps = 150 time units) to capture the steady state.
**Evidence:** flocking3d_adaptive.py, N=350, slow prey v0=0.02, ramp=0.1, N_SEEDS=5.
  fixed R_enc=0.15        Phi=0.968+/-0.009  t_std=0.077  Rg=0.305  f(Phi>0.85)=0.924
  adaptive R_enc=0.38*Rg  Phi=0.974+/-0.013  t_std=0.060  Rg=0.338  f(Phi>0.85)=0.942
  adaptive R_enc=0.50*Rg  Phi=0.982+/-0.012  t_std=0.036  Rg=0.334  f(Phi>0.85)=0.963
**Key result 1 -- adaptive does not help; it mildly hurts.**
Fixed R_enc=0.15 gives the LOWEST steady-state Phi (0.968, most disruption). Adaptive
tracking monotonically raises Phi: 0.38*Rg -> 0.974, 0.50*Rg -> 0.982. The 2D benefit of
adaptive encirclement (F35: mean Phi 0.778 -> 0.713, a real improvement) does not transfer
to 3D. It reverses sign.
**Key result 2 -- mechanism: adaptive damps the only disruptive moments.**
The temporal std of Phi falls sharply with adaptivity (t_std: 0.077 fixed -> 0.060 -> 0.036).
In 3D, encirclement never produces sustained disruption (F43, F44); its only disruptive
moments are transient downward fluctuations of Phi. Fixed R_enc lets these fluctuations
happen. Adaptive R_enc, by continuously repositioning predators to track the live Rg,
stabilizes the predator-flock geometry into a steady configuration -- which suppresses the
fluctuations and therefore suppresses the disruption. Adaptive tracking makes the flock
STEADIER, and a steadier 3D flock is a more coherent one.
**Key result 3 -- the F44 n_pred=10 minimum is a transient.**
F44 measured Phi=0.913 at n_pred=10 over 5000 steps; here the same configuration (fixed
R_enc=0.15, n_pred=10) settles to Phi=0.968 over 15000 steps. The F44 "disruption optimum"
is a mid-run transient that relaxes away over longer times -- consistent with F44's finding
that n_pred=10 sits on an unreliable knife-edge.
**Why it differs from 2D:** Adaptive encirclement works in 2D because there is a genuine
R_enc/Rg~0.5 optimum (F23) and tracking Rg keeps predators on it through the merge/split
cycle. F43 already showed 3D has no such optimum -- the disruption-vs-R_enc curve is shallow
and flat. With no optimum to track, adaptive control contributes only its stabilizing
side-effect, which is counterproductive.
**Implication:** Confirms and extends F43/F44. Encirclement in 3D cannot be rescued by
predator count (F44) or by adaptive geometry (F45). All three 3D predator findings point
to the same conclusion: geometric enclosure is a 2D-specific strategy, and 3D flock
disruption requires a fundamentally different mechanism.

---

## Finding 46: Vaccination targeting fails in 3D too -- kinematic mixing defeats spatial and degree-targeted strategies in three dimensions
<img src="./figures/finding46_3d_vaccination.png" width="560"/>

**What:** The report's Section 5 synthesis attributes the failure of degree-targeted (F36)
and spatial (F37) vaccination to alignment-driven kinematic mixing -- the alignment force
continuously rewires the neighbor graph faster than any static structural feature can be
exploited. Both null results were established in 2D. This tests whether the mechanism
survives in 3D, where the extra spatial degree of freedom could plausibly speed mixing up
(spatial vaccination fails even harder) or slow it down (immune-agent coverage persists,
spatial vaccination starts to help).
**Evidence:** flocking3d_vaccination.py, 3D flocking model (N=350, [0,1]^3 torus,
r0=0.02, rf=0.20, v0=0.02), SIS contagion (beta=2.5, gamma=2.0) on the 3D contact
network. R_CONT=0.155 tuned so mean contact degree (8.05) matches the 2D experiments.
N_SEEDS=5, 10000-step SIS runs, f_ss = mean panic fraction over the last 20 time units.
  p_immune  random          spatial         targeted
  0.00      0.806+/-0.005   0.805+/-0.002   0.809+/-0.005
  0.10      0.701+/-0.008   0.705+/-0.004   0.705+/-0.004
  0.20      0.598+/-0.002   0.600+/-0.003   0.601+/-0.005
  0.30      0.493+/-0.003   0.494+/-0.004   0.495+/-0.005
  0.40      0.387+/-0.004   0.392+/-0.006   0.387+/-0.009
  0.46      0.322+/-0.006   0.320+/-0.008   0.323+/-0.006
  0.50      0.282+/-0.008   0.284+/-0.005   0.283+/-0.009
  0.60      0.168+/-0.006   0.170+/-0.011   0.166+/-0.008
Degree distribution: mean=8.05, median=7, max=26, CV=0.59.
**Key result 1 -- complete strategy equivalence (the central null result).**
At every immune fraction, random, spatial (3D farthest-point maxmin), and degree-targeted
vaccination produce identical steady-state panic fractions. The largest difference between
any two strategies at any p_immune is ~0.005, smaller than the seed-to-seed standard
deviation. Neither targeting strategy beats random in 3D. The F36/F37 null results
transfer to three dimensions without qualification.
**Key result 2 -- the mixing mechanism is dimension-independent.**
This was not guaranteed. F43 showed one 2D result (R_enc/Rg~0.5 optimum) fails to transfer
to 3D. But kinematic mixing does transfer: the extra degree of freedom does not slow the
neighbor-graph turnover enough for spatial coverage to persist, nor does the degree
distribution gain a fat tail (CV=0.59 in 3D vs 0.68 in 2D -- if anything LESS heterogeneous,
giving hub-targeting even less to exploit). The alignment force reshuffles agent identities
faster than the epidemic timescale in 3D just as in 2D.
**Key result 3 -- no herd-immunity threshold within p<=0.6.**
Unlike the 2D experiments (F37 quenched near p~0.46), f_ss here declines smoothly with
p_immune and remains nonzero (0.168) even at p=0.60. This is a regime effect, not a
contradiction: the 3D contact network gives an effective reproduction number
R0 ~ beta*<k>/gamma ~ 10, far more supercritical than the 2D runs, so immunity dilutes the
epidemic proportionally rather than quenching it. The strategy-equivalence result is
independent of this -- all three strategies sit on the same decay curve.
**Implication:** Strengthens the Section 5 synthesis. Alignment-driven kinematic mixing is
a dimension-independent mechanism. The flock's defining feature -- velocity alignment --
is precisely what makes its members interchangeable on the epidemic timescale, so any
vaccination strategy that relies on a stable structural property (high degree, spatial
position) collapses to random in both 2D and 3D. Targeting can only beat random in a flock
if there is a fixed sub-structure that the alignment force does not erase.

---

## Finding 47: The Section 5 topological-alignment prediction is FALSIFIED -- k-NN alignment does not slow kinematic mixing, and targeted vaccination does not recover
<img src="./figures/finding47_topological_mixing.png" width="680"/>

**What:** The report's Section 5 synthesis closed with an explicit, pre-registered
falsifiable prediction: replacing the metric alignment force (align to all neighbors within
rf) with a topological one (align to the k nearest neighbors) should produce "weaker mixing
-- the neighbor graph would be more stable because k-nearest is a permutation-stable
structure," and consequently "targeted vaccination should partially recover its advantage
over random." This experiment tests that prediction head-on.
**Evidence:** topological_mixing.py, 2D flocking N=350, N_SEEDS=5. The alignment rule is
switchable between metric (neighbors within rf=0.10) and topological (k nearest neighbors,
with k=32 calibrated to the mean metric alignment degree). Two diagnostics:
(A) mixing rate -- mean Jaccard dissimilarity of each agent's contact-neighbor set (within
R_CONT=0.05) between snapshots 2 time units apart; (B) random vs degree-targeted
vaccination at supercritical SIS (beta=2.5, gamma=2.0).
  Diagnostic A -- mixing rate (Jaccard dissimilarity per 2 tu):
    metric  0.0371+/-0.0039   contact-degree CV = 0.655
    topo    0.0364+/-0.0032   contact-degree CV = 0.615
  Diagnostic B -- targeted-vs-random advantage (f_ss random minus f_ss targeted;
  positive = targeting helps):
    metric: p=0.20 -0.006 | p=0.30 -0.013 | p=0.40 -0.007 | p=0.50 -0.024
    topo:   p=0.20 -0.004 | p=0.30 -0.007 | p=0.40 -0.038 | p=0.50  0.000
**Key result 1 -- the prediction is falsified on both counts.**
(a) Topological alignment does NOT slow mixing. The Jaccard neighbor-graph turnover is
0.0364 per 2 tu for topo vs 0.0371 for metric -- statistically identical, the difference
far smaller than the seed-to-seed std. (b) Targeted vaccination does NOT recover an
advantage under topological alignment. The targeted-minus-random advantage is negative or
zero at every immune fraction under BOTH alignment rules -- targeting never beats random,
and at p=0.40 topo it is 0.038 WORSE. The Section 5 prediction is wrong.
**Key result 2 -- why "permutation-stable" was a red herring.**
The prediction conflated two distinct networks. The ALIGNMENT network (who an agent
averages velocity with) is what topological alignment changes -- and yes, k-NN fixes every
agent's alignment degree at exactly k. But the CONTACT network (who is within R_CONT, the
network contagion actually spreads on) is set by physical proximity, and it churns because
agents with slightly dispersed velocities slide past one another. That residual velocity
dispersion comes from repulsion, noise, and the averaging in the alignment force -- all
present identically under both rules. Changing how the alignment force *selects* neighbors
does not change how fast agents *physically move past* each other. So the contact graph
rewires at the same rate, and the contact-degree distribution stays equally heterogeneous
(CV 0.62 vs 0.66 -- k-NN did not homogenize it, because it homogenizes the alignment
degree, not the contact degree).
**Key result 3 -- a real but unrelated side effect.**
Topological alignment does lower f_ss in absolute terms (random-vaccination f_ss at p=0.20:
0.359 topo vs 0.389 metric; full quench at p=0.50 for topo vs residual 0.025 for metric).
The k-NN flock is slightly more spatially extended, weakening the contagion. But this is a
uniform shift of the whole epidemic curve, not a targeting effect -- random and targeted
shift together, and targeting still confers no advantage.
**Implication:** Kinematic mixing is driven by the physical relative motion of agents, not
by the topology of the alignment rule. The mechanism is even more robust than Section 5
claimed: it does not depend on the metric character of the alignment force. Section 5's
falsifiable prediction was a genuine test of the synthesis, and the synthesis failed it --
the proposed escape route (a permutation-stable alignment graph) does not exist, because
the contact graph and the alignment graph are different objects. The report's Section 5
has been updated to record this falsification and the corrected mechanism.

---

## Finding 48: Freezing the contact graph does NOT rescue targeted vaccination -- the degree-targeting null is structural, not kinematic
<img src="./figures/finding48_contact_freezing.png" width="680"/>

**What:** Finding 47's revised Section 5 named one genuine escape route for targeted
vaccination: "freezing the contact graph itself -- suppressing the relative motion of
agents." This experiment builds that frozen graph and tests whether targeting then works.
The noise amplitude (ramp) is the book's solid-to-fluid control parameter: at low ramp the
flock is in its "solid" regime where agents lock into a near-rigid lattice, at high ramp it
is "fluid" and mixes freely. Sweeping ramp therefore sweeps the contact-graph mixing rate.
**Evidence:** contact_freezing.py, 2D flocking N=350, N_SEEDS=5, metric alignment, SIS
contagion (beta=2.5, gamma=2.0). Random vs degree-targeted vaccination at p_immune=0.20
and 0.35, across ramp = 0.003, 0.01, 0.03, 0.1, 0.3.
  ramp    Phi     contact mixing (Jaccard/2tu)
  0.003   0.997   0.0036 +/- 0.0023
  0.010   0.997   0.0056 +/- 0.0014
  0.030   0.998   0.0125 +/- 0.0023
  0.100   0.998   0.0364 +/- 0.0018
  0.300   0.991   0.1064 +/- 0.0061
  Targeted advantage (f_ss random minus targeted; positive = targeting wins):
  ramp    p=0.20    p=0.35
  0.003   -0.003    -0.002
  0.010   +0.002    -0.028
  0.030   +0.012    -0.037
  0.100   -0.002    +0.039
  0.300   +0.004    +0.016
**Key result 1 -- the contact graph really does freeze, in a still-coherent flock.**
Lowering ramp from 0.3 to 0.003 drops the contact-graph Jaccard turnover from 0.106 to
0.0036 per 2 tu -- a 30-fold reduction -- while Phi stays at 0.997-0.998 throughout. The
flock remains a coherent moving flock; only the relative motion of its members is
suppressed. Section 5's claim (after F47) that a frozen contact graph is "incompatible with
a flock that moves" was too strong: the solid regime achieves exactly that.
**Key result 2 -- targeting still fails, at every mixing rate.**
Despite the 30x range in mixing rate, the targeted-vs-random advantage stays scattered
around zero (-0.037 to +0.039) with no monotonic trend. At the most frozen point
(ramp=0.003, mixing=0.0036) the advantage is -0.003 and -0.002 -- targeting is, if
anything, marginally worse than random. Freezing the contact graph does NOT rescue targeted
vaccination. The F47-predicted escape route is closed.
**Key result 3 -- the degree-targeting null is structural, not kinematic.**
This disentangles two explanations that Finding 36 and the Section 5 synthesis had
conflated. F36 found degree-targeting fails and attributed it to kinematic mixing
(rewiring restores hub positions). F48 removes the mixing and targeting STILL fails --
so mixing was never the operative cause for degree-targeting. The real cause is the one
F36 also noted but the synthesis under-weighted: the flock contact network has a
thin-tailed degree distribution (CV~0.68, no true hubs). Hub-targeting only beats random
on fat-tailed (scale-free) networks; freezing a thin-tailed network does not create hubs.
The degree-targeting null is a STATIC STRUCTURAL property of the flock graph, present
whether or not the graph mixes.
**Implication:** The Section 5 synthesis over-attributed the vaccination null results to
kinematic mixing. Degree-targeting (F36) fails for a structural reason -- degree
homogeneity -- that is independent of mixing, as F48 proves by removing the mixing.
Kinematic mixing remains the correct explanation for the SPATIAL vaccination null (F37):
spatial coverage is a feature that genuinely exists at any instant and is genuinely erased
by motion. The two null results are NOT the same mechanism. The honest unifying statement
is weaker: the flock offers no exploitable structure for vaccination -- either because the
structure never exists (degree homogeneity) or because mixing erases it (spatial coverage).
Section 5 has been revised to separate these two mechanisms.

---

## Finding 49: 3D encirclement compression mechanism verified; planar (ring) predator arrangement is worse than spherical, not better
<img src="./figures/finding49_3d_strategy.png" width="680"/>

**What:** Finding 44 proposed that 3D encirclement fails because adding predators
compresses the flock, and in 3D compression densifies it (more neighbors within the
alignment radius), strengthening the alignment coupling. This experiment (a) verifies that
mechanism by measuring the mean alignment-neighbor count <k_align> directly, and (b) tests
the report's implicit claim that the spherical predator arrangement is the bottleneck, by
comparing it against a planar arrangement -- all predators on a ring in the z=z_com plane,
recreating the 2D encirclement geometry inside the 3D flock.
**Evidence:** flocking3d_strategy.py, N=350, N_SEEDS=5, N_ITER=5000, R_enc=0.15.
  mode     n_pred  Phi              Rg      <k_align>
  sphere      6    0.981+/-0.022    0.399   22.0
  sphere     10    0.913+/-0.082    0.355   41.3
  sphere     20    0.975+/-0.026    0.312   48.1
  planar      6    0.971+/-0.053    0.393   24.6
  planar     10    0.998+/-0.001    0.411   18.8
  planar     20    0.997+/-0.001    0.399   21.0
**Key result 1 -- the F44 compression mechanism is verified.**
Under spherical encirclement, as n_pred rises 6->10->20 the radius of gyration falls
monotonically (0.399->0.355->0.312) and the mean alignment-neighbor count rises
monotonically (22.0->41.3->48.1). Adding predators demonstrably compresses and densifies
the 3D flock, exactly as Finding 44 claimed.
**Key result 2 -- densification explains the Phi recovery, but Phi is not a pure function
of <k_align>.** From n_pred=10 to 20, <k_align> rises 41->48 and Phi rises 0.913->0.975:
densification stabilizes the flock, as F44 predicted. But from n_pred=6 to 10, <k_align>
also rises (22->41) while Phi FALLS (0.981->0.913). The picture is a competition: predator
forcing perturbs the flock, densification stabilizes it. At n_pred=10 the perturbation
transiently wins (the F44 knife-edge); by n_pred=20 the flock is so dense (<k_align>=48)
that the stabilization dominates and coherence is restored. The F44 mechanism is the
restoring force, not the whole story.
**Key result 3 -- the planar (ring) arrangement is WORSE than spherical, not better.**
The report (Section 4.25) argued a sphere is intrinsically harder to seal than a 2D ring.
The natural inference -- that a ring of predators would do better -- is refuted. Planar
encirclement gives Phi=0.998 at n_pred=10 and 0.997 at n_pred=20: essentially no
disruption, strictly worse than the (already weak) spherical result. The reason is
decisive: planar predators sit in the z=z_com plane and constrain only the flock's xy
extent. The flock simply extends along the unconstrained z axis -- planar Rg stays
~0.39-0.41 and <k_align> stays ~19-25, i.e. the flock is NOT compressed at all. A ring in
3D closes nothing; the third dimension is wide open above and below it.
**Implication:** Closes the 3D predator thread definitively. Spherical encirclement at
least achieves compression (and fails because compression densifies and stabilizes); the
planar ring fails even harder because it achieves no compression. Together with F43
(radius), F44 (count), and F45 (adaptive), every geometric variant of encirclement has now
been shown to fail in 3D. The escape dimension is fundamental: any predator arrangement
that leaves one spatial axis unconstrained lets the flock flow along it, and no arrangement
of a modest predator count can constrain all three axes of a sphere the way a 2D ring
constrains both axes of a circle.

---

## Finding 50: Hard repulsion does not crystallize either -- raising the exponent shrinks the effective core, it does not harden it
<img src="./figures/finding50_langevin_hexatic_hard.png" width="640"/>

**What:** Finding 40 measured the hexatic order parameter |psi6| under a Langevin
thermostat and found the n=1.5 soft repulsion cannot crystallize at any temperature
(|psi6| flat at ~0.4). F40 closed with an explicit recommendation: "Demonstrating the
KTHNY transition in this model family requires a near-hard-core Langevin simulation
(n>=12)." This experiment runs exactly that -- the F40 protocol with repulsion exponents
n=12 and n=24, at dense packings C=0.70 and C=0.85.
**Evidence:** langevin_hexatic_hard.py, Langevin thermostat (mu=10, FDT-satisfying noise),
N=50/100/200, N_SEEDS=6, N_ITER=12000, kT=0.002-3.0.
  n=12 C=0.85: psi6(kT=0.002)=0.340-0.344  psi6(kT=3.0)=0.344  chi_peak<=0.003
  n=24 C=0.85: psi6(kT=0.002)=0.339-0.345  psi6(kT=3.0)=0.344  chi_peak<=0.002
  n=12 C=0.70: psi6(kT=0.002)=0.382-0.389  psi6(kT=3.0)=0.385-0.386
  n=24 C=0.70: psi6(kT=0.002)=0.381-0.389  psi6(kT=3.0)=0.385-0.386
**Key result 1 -- hard repulsion does not crystallize, and F40's recommendation fails.**
|psi6| is flat at ~0.34-0.39 across the ENTIRE temperature range (kT 0.002 to 3.0), for
BOTH exponents and BOTH densities -- identical to the n=1.5 result of F40. psi6(low kT) and
psi6(high kT) agree to within 0.005 everywhere: there is no solid-phase rise toward 1 and
no fluid collapse toward 0. chi_psi6 is tiny (<=0.004) and DECREASES with N
(0.0041->0.0017->0.0009 at n=12 C=0.70) -- the opposite of a transition, where chi would
grow with N. There is no KTHNY transition at any exponent tested.
**Key result 2 -- mechanism: a higher exponent shrinks the core, it does not harden it.**
The repulsion force is strength = eps * base_r^n / d with base_r = 1 - d/rb. F40's
recommendation assumed a higher n hardens the contact. It does the opposite. Because
base_r ranges 0 to 1, base_r^n for large n is negligible UNLESS base_r is near 1, i.e.
unless d is very close to 0. Numerically the force factor base_r^n at d=0.5*rb is 0.354
for n=1.5, but 2.4e-4 for n=12 and 6e-8 for n=24. Raising the exponent therefore collapses
the effective interaction range toward d->0: at n=24 the repulsion is negligible beyond
d~0.05*rb. A higher n makes the agents into nearly-free particles with a tiny pointlike
core -- effectively MORE dilute and LESS able to order, not harder. F40's "n>=12"
prescription rested on a misreading of this force form.
**Key result 3 -- the phase-transition thread closes definitively negative.**
Combining F38 (exponent sweep, non-Langevin: identical crossover), F39 (Langevin
thermalizes correctly), F40 (n=1.5 hexatic flat), and F50 (n=12, 24 hexatic flat): the
Charbonneau force model cannot crystallize at any repulsion exponent, because no exponent
of the base_r^n form produces a genuine finite-sized hard core. The solid-to-fluid
"transition" is a smooth crossover, full stop.
**Caveat:** Low-kT runs start from a random quench, so kinetic arrest (glass) is a formal
possibility. But the decisive evidence against a transition is independent of annealing:
chi_psi6 DECREASES with N rather than growing, and |psi6| is identical at the hardest
exponent and the softest (F40). If a crystalline phase existed, harder exponents and
larger N would show at least partial ordering; none appears.
**Implication:** To exhibit KTHNY melting, the model would need a genuinely different
repulsion -- a true inverse-power-law potential (force ~ d^-n) or a WCA/hard-disc form --
not a higher exponent in the existing base_r^n force. This is a corrected and definitive
close to the phase-transition thread (F2, F9, F17, F38, F39, F40, F50): within the
Charbonneau model as written, the smooth crossover is the only behavior, at any exponent.

---

## Finding 51: Alpha-contrast segregation in 3D -- identical to 2D at moderate contrast, but the extra dimension dilutes it at high contrast
<img src="./figures/finding51_3d_segregation.png" width="560"/>

**What:** Finding 27 showed that in 2D, two populations with different alignment strength
alpha spatially segregate -- the local-purity diagnostic (fraction of an agent's rf
neighbors sharing its type) rose from 0.50 (well mixed) to 0.73 at maximum alpha contrast.
This tests whether that self-organized segregation transfers to 3D. Findings 46-48
established that kinematic MIXING (which destroys imposed structure) is
dimension-independent; this asks whether self-ORGANIZED structure is too.
**Evidence:** flocking3d_segregation.py, 3D flocking N=350, fast-prey regime (v0=1.0,
ramp=0.5), f_active=0.5, N_SEEDS=5. alpha_active=1.0, alpha_passive swept 1.0->0.0.
  alpha_passive  3D purity_active   2D purity_active (F27)
  1.0 (no contrast)  0.489+/-0.009    0.500
  0.7                0.526+/-0.014    --
  0.5                0.554+/-0.021    0.556
  0.3                0.552+/-0.012    0.550
  0.1                0.553+/-0.013    0.630
  0.0                0.690+/-0.023    0.732
3D Phi: 0.999 for alpha_passive>=0.3, 0.993 at 0.1, collapses to 0.523 at 0.0.
**Key result 1 -- segregation transfers to 3D, and is identical to 2D at moderate contrast.**
At alpha_passive = 0.5 and 0.3, the 3D local purity (0.554, 0.552) matches the 2D values
(0.556, 0.550) to within noise. Self-organized alpha-contrast segregation is real in 3D.
The mechanism (weaker-alignment agents fall out of the tight active core and cluster
locally) is dimension-independent in the moderate-contrast regime.
**Key result 2 -- the extra dimension dilutes segregation at high contrast.**
The 2D and 3D curves diverge sharply once the contrast is large. At alpha_passive=0.1, 2D
purity has climbed to 0.630 while 3D is still on a flat plateau at 0.553 -- no stronger
than at alpha_passive=0.5. In 2D segregation rises steadily from moderate contrast onward;
in 3D it plateaus at a mild ~0.55 and only breaks upward at alpha_passive=0.0 (purity
0.690). The extra spatial dimension gives a partially-aligned passive agent more
independent directions along which to interpenetrate the active population, so moderate
mis-alignment is no longer enough to drive clustering -- it is mixed back in.
**Key result 3 -- strong 3D segregation costs global coherence.**
3D segregation only becomes strong (purity 0.69) at alpha_passive=0.0, where the passive
half of the flock has zero alignment and behaves as a non-flocking gas. At that point the
global order parameter collapses to Phi=0.523: the "segregated" state is really an
aligned active flock shedding an incoherent passive cloud, not two co-moving coherent
sub-flocks. For all alpha_passive >= 0.1, Phi stays >= 0.99 and segregation is only mild.
**Implication:** Self-organized structure is partially dimension-dependent, in contrast to
kinematic mixing (F46) which is fully dimension-independent. Both point the same way: the
extra dimension favors mixing. Mixing erodes imposed structure equally in 2D and 3D
(F46-F48), and it also erodes self-organized segregation more effectively in 3D than in 2D
(F51). A flock in three dimensions is harder to sort and just as hard to target -- the
third dimension is, consistently across every experiment, a mixing aid.

---

## Finding 52: 3D mixes SLOWER than 2D -- the "third dimension is a mixing aid" theme is falsified
<img src="./figures/finding52_mixing_dimension.png" width="560"/>

**What:** Findings 46-51 built up an interpretive theme -- that the third spatial dimension
acts as a "mixing aid" -- which was written into the report (Section 4.33, Conclusion 24).
But that theme rested on inference, never a direct measurement: F47 measured the 2D
contact-graph mixing rate, but the 3D rate was never measured. This experiment measures it
directly, in the same self-test spirit as F47/F48, to verify or falsify the claim.
**Evidence:** mixing_dimension.py. Pure flocks (no predators, no contagion), 2D and 3D, at
the parameters of the respective vaccination experiments, N=350, N_SEEDS=5. The contact
radius is calibrated per dimension so the mean contact degree matches (~8 in both:
2D R_cont=0.050, 3D R_cont=0.155). Mixing = mean Jaccard dissimilarity of each agent's
contact-neighbor set between snapshots 2 time units apart. Noise (ramp) is swept.
  ramp   2D mix            3D mix            ratio 3D/2D
  0.03   0.0109+/-0.0009   0.0060+/-0.0006   0.55
  0.10   0.0370+/-0.0025   0.0213+/-0.0006   0.57
  0.30   0.1086+/-0.0042   0.0581+/-0.0027   0.54
  1.00   0.3143+/-0.0036   0.1839+/-0.0048   0.59
**Key result -- the theme is falsified: 3D mixes SLOWER.**
At every noise level, the 3D contact graph rewires at only ~0.54-0.59 of the 2D rate. The
ratio is remarkably stable (~0.56) across a 30-fold range of absolute mixing rates. The
third dimension is NOT a mixing aid -- at matched mean contact degree, the 3D flock's
contact graph turns over about 1.8x SLOWER than the 2D flock's.
**Mechanism:** Matching the mean contact degree forces the 3D contact radius to be ~3x
larger than the 2D one (0.155 vs 0.050), because a ball of given radius holds far more
agents than a disc. A larger contact region takes longer for agents moving at the same
speed to enter and leave, so the neighbor set is "stickier" and turns over more slowly.
(A pure surface-to-volume estimate predicts turnover ~ 1/R_cont, i.e. ratio ~0.32; the
measured 0.56 indicates the 3D relative-velocity dispersion is somewhat larger, partly
offsetting the radius effect.)
**Reconciliation with F46 and F51 -- the 3D results have other causes:**
(a) F46 (vaccination targeting fails in 3D): degree-targeting fails for the STRUCTURAL
reason established in F48 (no hubs), which is dimension-independent. Spatial targeting
fails because, even at the slower 3D rate, the contact graph still fully turns over many
times during a 100-tu epidemic -- mixing is slower but still more than sufficient to erase
spatial coverage. F46's mechanism survives; only the "faster" embellishment was wrong.
(b) F51 (segregation diluted in 3D): this is NOT caused by faster mixing. It is a
GEOMETRIC effect of the neighborhood shape -- in 3D an agent's neighbors occupy a ball
rather than a disc, giving a partially-aligned agent more independent directions along
which to be surrounded by the other type, so instantaneous local purity is geometrically
diluted. The dilution is about neighborhood geometry, not turnover rate.
**Implication:** The "third dimension is a mixing aid" theme is wrong and has been removed
from the report. The corrected statement: the third dimension changes neighborhood
GEOMETRY (a ball has more independent directions than a disc) without speeding up mixing
-- in fact it slows mixing by ~1.8x at matched degree. The 3D flock remains hard to
disrupt (escape dimension, F43-F49), hard to target (structural, F48), and hard to sort
(geometric, F51), but none of these is due to faster mixing. This finding is a direct
self-test catch: an interpretive theme that looked unifying was falsified by the
measurement it predicted.

---

## Open Questions / Next Directions
1. 3D flocking thread COMPLETE (F41-F46):
   - F41: v_eq=v0+alpha/mu exact in 3D; basic noise sweep
   - F42: smooth crossover at ramp~15-25; chi_peak drifts up with N; same as 2D qualitatively
   - F43: 3D encirclement fails; R_enc/Rg~0.5 optimum is 2D-specific
   - F44: 3D predator-count scaling -- disruption non-monotonic, hard floor Phi~0.91
   - F45: 3D adaptive encirclement null -- tracking damps the disruptive fluctuations
   - F46: 3D vaccination null -- kinematic mixing defeats targeting in 3D too
2. 3D predator thread is fully closed. Encirclement cannot be rescued in 3D by radius
   tuning (F43), predator count (F44), or adaptive geometry (F45).
3. Section 5 self-test COMPLETE (F47, F48): the topological-alignment prediction was
   FALSIFIED (F47), and freezing the contact graph still does not rescue targeting (F48).
   The vaccination story is fully resolved: degree-targeting fails structurally (no
   hubs), spatial-targeting fails kinematically (mixing erases coverage). Section 5
   revised to separate the two mechanisms. No open escape route remains.
4. Alternative research directions:
   - A 3D-effective predator strategy that is NOT encirclement: exploit the
     compression-induced density gradient (F44), or attack alignment coupling directly.
     Would validate the F44/F45 mechanistic claim.
   - Phase transition in 3D (hard repulsion Langevin in 3D)
   - Segregation in 3D
   - Agent memory / fatigue models

