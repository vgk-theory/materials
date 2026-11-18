#!/usr/bin/env python3
"""T-2, гравитационное красное смещение: несущие числа агрегата и проверка по объявленным критериям.

Запуск: python3 check_aggregate.py  (только стандартная библиотека; пишет _check_aggregate.json рядом).
Критерии К-1, К-2 — секция «Критерии проверки» файла ../aggregate.md. Числа наблюдений — именованные
константы со ссылкой на карточку факта (../../../facts/OBS-N-*.md).
"""
import json
import math
import os


def sig(x, n=9):
    """Округление до n значащих цифр (для записи в сводку)."""
    return float(f"{x:.{n}g}")

# --- постоянные ---------------------------------------------------------------------------------
C = 299_792_458.0            # м/с, точное значение
G_STD = 9.80665              # м/с^2, стандартное ускорение свободного падения
H_TOWER = 22.5               # м, высота в опыте OBS-5

# --- критерии (объявление — ../aggregate.md) ------------------------------------------------------
K1_SIGMA = 3.0
K2_SIGMA = 5.0

# --- из формулировки (Ag-7) -----------------------------------------------------------------------
shift_per_metre = G_STD / C**2                 # gh/c^2 на метр
shift_tower = shift_per_metre * H_TOWER        # опорный сдвиг OBS-5

# --- наблюдения: отклонение измеренного сдвига от опорного, в долях опорного ------------------------
# (отклонение, sigma, карточка)
DEVIATION = {
    "OBS-7": (0.19e-5, 2.48e-5),               # спутники на вытянутой орбите
    "OBS-8": (1.4e-5, 9.1e-5),                 # оптические часы, 450 м
    "OBS-14": (2.2e-7, 2.5e-7),                # часы разного устройства, годовое изменение U
}
# OBS-5: отношение к опорному, статистическая погрешность и предел систематической
OBS5_RATIO, OBS5_STAT, OBS5_SYST = 0.9990, 0.0076, 0.010
# OBS-9: наблюдение и расчёт (нс): перелёты на восток и на запад; расчёт = высотная + скоростная часть
OBS9 = {
    "east": {"obs": (-59.0, 10.0), "height": (144.0, 14.0), "velocity": (-184.0, 18.0)},
    "west": {"obs": (273.0, 7.0), "height": (179.0, 18.0), "velocity": (96.0, 10.0)},
}
# коэффициенты законов: alpha (OBS-7), полусумма (alpha + beta)/2 (OBS-2, строка R-4)
ALPHA, S_ALPHA = 1.0 + 0.19e-5, 2.48e-5
HALF_SUM, S_HALF_SUM = 0.99996, 0.00006

facts = {k: {"deviation": d, "sigma": s, "z": d / s} for k, (d, s) in DEVIATION.items()}
s5 = math.hypot(OBS5_STAT, OBS5_SYST)
facts["OBS-5"] = {"ratio": OBS5_RATIO, "sigma": s5, "z": (OBS5_RATIO - 1.0) / s5}

obs9 = {}
for leg, d in OBS9.items():
    pred = d["height"][0] + d["velocity"][0]
    s_pred = math.hypot(d["height"][1], d["velocity"][1])
    obs, s_obs = d["obs"]
    obs9[leg] = {
        "predicted_ns": pred, "sigma_predicted_ns": round(s_pred, 1),
        "z_aggregate": (obs - pred) / math.hypot(s_obs, s_pred),                       # Ag-4 + Ag-8
        "z_no_height_part": (obs - d["velocity"][0]) / math.hypot(s_obs, d["velocity"][1]),
        "z_equal_clock_rate": obs / s_obs,                                             # I-11: разность 0
    }
    facts[f"OBS-9 {leg}"] = {"z": obs9[leg]["z_aggregate"]}

# удвоенный сдвиг (оба механизма вместе) против OBS-5
doubled_linear = (2.0 - 1.0) / (OBS5_STAT + OBS5_SYST)
doubled_quadrature = (2.0 - 1.0) / s5

beta = 2.0 * HALF_SUM - ALPHA
s_beta = math.sqrt(4.0 * S_HALF_SUM**2 + S_ALPHA**2)

max_abs_z = max(abs(f["z"]) for f in facts.values())
z_i11 = min(abs(v["z_equal_clock_rate"]) for v in obs9.values())

def r(x, n=3):
    return round(x, n)

result = {
    "theme": "T-2",
    "constants": {"c_m_s": C, "g_m_s2": G_STD, "h_tower_m": H_TOWER},
    "criteria": {"K1_sigma": K1_SIGMA, "K2_sigma": K2_SIGMA, "free_parameters": 0},
    "shift_per_metre": float(f"{shift_per_metre:.4e}"),
    "shift_tower": float(f"{shift_tower:.4e}"),
    "facts": {k: {kk: (sig(vv) if isinstance(vv, float) else vv) for kk, vv in v.items()} for k, v in facts.items()},
    "OBS-9": {leg: {k: (r(v, 2) if isinstance(v, float) else v) for k, v in d.items()} for leg, d in obs9.items()},
    "K1_aggregate": {"max_abs_z": r(max_abs_z), "verdict": "PASS" if max_abs_z <= K1_SIGMA else "FAIL"},
    "K2_doubled_shift_vs_OBS-5": {"z_linear": r(doubled_linear, 1), "z_quadrature": r(doubled_quadrature, 1),
                                  "verdict": "REJECTED" if doubled_linear > K2_SIGMA else "NOT REJECTED"},
    "K2_equal_clock_rate_vs_OBS-9": {"min_abs_z": r(z_i11, 1),
                                     "verdict": "REJECTED" if z_i11 > K2_SIGMA else "NOT REJECTED"},
    "coefficients": {"alpha": ALPHA, "sigma_alpha": S_ALPHA, "beta": r(beta, 6), "sigma_beta": r(s_beta, 6)},
    "note": "OBS-6 (граница 7e-5), OBS-12, OBS-29 — границы; OBS-15 — условное согласие; OBS-13 Ag-4 "
            "независимо не проверяет: в счёт К-1 не входят.",
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_check_aggregate.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(result, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
