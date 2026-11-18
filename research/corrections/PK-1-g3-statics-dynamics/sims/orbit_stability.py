#!/usr/bin/env python
"""PK-1 numeric verification: orbit stability for four force cases.

Программа §6 карточки PK-1.md (программа проверки, 2026-07-26).

Case A: direct attraction            F = -GMm/r^2 r_hat        (Newton)
Case B: complex repulsion            F = (-k1 + k2) mM/r^2 r_hat, k2-k1 = G
        (BGP eq. 15/15a: результирующая разности сил отталкивания направлена
         К телу M; формально та же центростремительная 1/r^2 — проверка
         поточечного тождества траекторий A и B)
Case C: pure repulsion (от центра)   F = +GMm/r^2 r_hat        (same ICs)
Case D: free fall, L = 0            (attraction, body at rest off r0; NOT a
        displacement from an equilibrium — none exists for one source at L = 0;
        illustrates absence of restoring force without L)

Units: G*M = 1, r0 = 1, m = 1  =>  T_orb = 2*pi.
Initial conditions A/B/C: x = (1+eps) r0, eps = 1% radial perturbation,
v = v_circ(r0) tangential. Case D: at rest at x = (1+eps) r0.

PASS criteria (fixed BEFORE the first run, 2026-07-26; пороги с тех пор не менялись —
пометки к A и B от 2026-10-30 поясняют смысл критериев, а не меняют их):
  A: bounded radial oscillation around r0: 0 < (r_max-r_min)/r_mean < 0.05
     over >= 50 orbital periods; no secular drift:
     |amp(last 10 T) - amp(first 10 T)| / amp(first 10 T) < 0.05;
     epicyclic frequency kappa/omega = 1 +- 0.01 (kappa^2 = omega^2 (3+n) at
     n = -2; closedness of the orbit is a consequence, Bertrand's theorem is
     not invoked — 2026-10-30)
  B: identical to A pointwise: max_t |r_A(t) - r_B(t)| / r0 < 1e-9
     — РЕГРЕССИОННАЯ ПРОВЕРКА КОДА: правая часть B тождественна A по построению
     (0.5 - 1.5 = -1), критерий может провалиться только ошибкой реализации и
     физического содержания не несёт (пометка 2026-10-30)
  C: escape, no finite orbit: r monotonically increasing after t > T/4,
     r(t_end) > 20 r0, total energy E = v^2/2 + GM/r > 0
  D: monotonic departure from initial point (radial infall, no restoring
     force without L; not a statement about statics of Г-3′(а)): r(t) strictly decreasing until the
     stop event r < 0.1 r0; no local minimum followed by return

Output: sims/_orbit_stability.json
"""

import json
import os

import numpy as np
from scipy.integrate import solve_ivp
from scipy.signal import argrelextrema

GM = 1.0
R0 = 1.0
EPS = 0.01          # 1% radial perturbation
T_ORB = 2.0 * np.pi
N_PERIODS = 60      # >= 50 required
RTOL, ATOL = 1e-12, 1e-14

# BGP two-component decomposition (formalism 15a): -k1 internal repulsion,
# +k2 external push from the complex; observable resultant k3 = k2 - k1 = G.
K1 = 0.5 * GM
K2 = 1.5 * GM


def rhs_attraction(t, s):
    x, y, vx, vy = s
    r3 = (x * x + y * y) ** 1.5
    a = -GM / r3
    return [vx, vy, a * x, a * y]


def rhs_complex_repulsion(t, s):
    """Resultant of two repulsive components, net centripetal (eq. 15a)."""
    x, y, vx, vy = s
    r3 = (x * x + y * y) ** 1.5
    a = (K1 / r3) - (K2 / r3)   # = -(K2-K1)/r3 = -GM/r3, computed as split
    return [vx, vy, a * x, a * y]


def rhs_pure_repulsion(t, s):
    x, y, vx, vy = s
    r3 = (x * x + y * y) ** 1.5
    a = +GM / r3
    return [vx, vy, a * x, a * y]


def integrate(rhs, s0, t_end, events=None):
    t_eval = np.linspace(0.0, t_end, 20000)
    sol = solve_ivp(rhs, (0.0, t_end), s0, method="DOP853",
                    rtol=RTOL, atol=ATOL, t_eval=t_eval,
                    events=events, dense_output=False)
    return sol


def radial(sol):
    return np.sqrt(sol.y[0] ** 2 + sol.y[1] ** 2)


def main():
    out = {"meta": {
        "GM": GM, "r0": R0, "perturbation": EPS,
        "n_periods": N_PERIODS, "integrator": "DOP853",
        "rtol": RTOL, "atol": ATOL,
        "k1": K1, "k2": K2, "note_B": "force computed as split k1/k2 terms",
    }, "cases": {}, "pass": {}}

    t_end = N_PERIODS * T_ORB
    v_circ = np.sqrt(GM / R0)
    s0 = [R0 * (1.0 + EPS), 0.0, 0.0, v_circ]

    # ---- Case A: direct attraction ------------------------------------
    solA = integrate(rhs_attraction, s0, t_end)
    rA = radial(solA)
    amp_rel = (rA.max() - rA.min()) / rA.mean()
    n10 = len(rA) // (N_PERIODS // 10)          # samples per 10 periods
    amp_first = rA[:n10].max() - rA[:n10].min()
    amp_last = rA[-n10:].max() - rA[-n10:].min()
    drift = abs(amp_last - amp_first) / amp_first
    # epicyclic frequency from successive perihelion passages (r minima)
    imin = argrelextrema(rA, np.less, order=5)[0]
    t_min = solA.t[imin]
    T_rad = np.mean(np.diff(t_min))
    # ratio: radial period vs orbital period of the actual orbit
    # (semi-major axis a from vis-viva at t=0); mean-radius estimate removed (dead code, 2026-10-30)
    E0 = 0.5 * v_circ ** 2 - GM / (R0 * (1 + EPS))
    a_sm = -GM / (2 * E0)
    T_orb_actual = 2 * np.pi * np.sqrt(a_sm ** 3 / GM)
    kappa_ratio = T_orb_actual / T_rad
    out["cases"]["A"] = {
        "r_min": float(rA.min()), "r_max": float(rA.max()),
        "rel_amplitude": float(amp_rel),
        "amp_first10T": float(amp_first), "amp_last10T": float(amp_last),
        "secular_drift_rel": float(drift),
        "radial_period": float(T_rad),
        "orbital_period_actual": float(T_orb_actual),
        "kappa_over_omega": float(kappa_ratio),
        "n_perihelia": int(len(imin)),
    }
    out["pass"]["A_bounded"] = bool(0.0 < amp_rel < 0.05)
    out["pass"]["A_no_drift"] = bool(drift < 0.05)
    out["pass"]["A_kappa_eq_omega"] = bool(abs(kappa_ratio - 1.0) < 0.01)

    # ---- Case B: complex repulsion (identical resultant) ---------------
    solB = integrate(rhs_complex_repulsion, s0, t_end)
    rB = radial(solB)
    max_dev = float(np.max(np.abs(rA - rB)) / R0)
    max_dev_xy = float(np.max(np.hypot(solA.y[0] - solB.y[0],
                                       solA.y[1] - solB.y[1])) / R0)
    out["cases"]["B"] = {
        "max_rel_deviation_r_AB": max_dev,
        "max_rel_deviation_xy_AB": max_dev_xy,
        "rel_amplitude": float((rB.max() - rB.min()) / rB.mean()),
    }
    out["pass"]["B_identity_AB"] = bool(max_dev_xy < 1e-9)

    # ---- Case C: pure repulsion, same ICs -------------------------------
    solC = integrate(rhs_pure_repulsion, s0, t_end)
    rC = radial(solC)
    i_quarter = np.searchsorted(solC.t, T_ORB / 4.0)
    monotone_C = bool(np.all(np.diff(rC[i_quarter:]) > 0))
    E_C = 0.5 * v_circ ** 2 + GM / (R0 * (1 + EPS))   # U=+GM/r for repulsion
    out["cases"]["C"] = {
        "r_final": float(rC[-1]),
        "monotone_increase_after_quarter_period": monotone_C,
        "total_energy": float(E_C),
    }
    out["pass"]["C_escape"] = bool(monotone_C and rC[-1] > 20 * R0 and E_C > 0)

    # ---- Case D: L = 0, at rest, attraction -----------------------------
    def hit_inner(t, s):
        return np.hypot(s[0], s[1]) - 0.1 * R0
    hit_inner.terminal = True
    hit_inner.direction = -1
    s0D = [R0 * (1.0 + EPS), 0.0, 0.0, 0.0]
    solD = integrate(rhs_attraction, s0D, t_end, events=hit_inner)
    rD = radial(solD)
    monotone_D = bool(np.all(np.diff(rD) < 0))
    # точка события отдельно от последней точки выборки (добавлено 2026-10-30; на критерии не влияет)
    r_event = (float(np.hypot(solD.y_events[0][0][0], solD.y_events[0][0][1]))
               if solD.status == 1 and len(solD.y_events[0]) else None)
    t_event = float(solD.t_events[0][0]) if solD.status == 1 and len(solD.t_events[0]) else None
    out["cases"]["D"] = {
        "r_initial": float(rD[0]),
        "r_last_sample": float(rD[-1]), "t_last_sample": float(solD.t[-1]),
        "r_event": r_event, "t_event": t_event,
        "monotone_decrease": monotone_D,
        "terminated_at_inner_boundary": bool(solD.status == 1),
    }
    out["pass"]["D_monotonic_departure"] = bool(
        monotone_D and solD.status == 1)

    out["verdict"] = "PASS" if all(out["pass"].values()) else "FAIL"

    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "_orbit_stability.json"), "w") as fh:
        json.dump(out, fh, indent=2)

    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
