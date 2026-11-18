#!/usr/bin/env python3
"""T-1, отклонение света вблизи массы: несущие числа агрегата и проверка по объявленным критериям.

Запуск: python3 check_aggregate.py  (только стандартная библиотека; пишет _check_aggregate.json рядом).
Критерии К-1, К-2 — секция «Критерии проверки» файла ../aggregate.md. Числа наблюдений — именованные
константы со ссылкой на карточку факта (../../../facts/OBS-N-*.md) и её строку.
"""
import json
import math
import os


def sig(x, n=9):
    """Округление до n значащих цифр (для записи в сводку)."""
    return float(f"{x:.{n}g}")

# --- постоянные ---------------------------------------------------------------------------------
C = 299_792_458.0            # м/с, точное значение (определение метра)
GM_SUN = 1.3271244e20        # м^3/с^2, номинальное значение, резолюция B3 МАС 2015 (A-1, source.md, L-9)
R_SUN = 6.957e8              # м, номинальный радиус Солнца, там же
RAD_TO_ARCSEC = 180.0 / math.pi * 3600.0
PE_TO_SIGMA = 1.0 / 0.6745   # вероятная ошибка -> стандартное отклонение

# --- критерии (объявление — ../aggregate.md) ------------------------------------------------------
K1_SIGMA = 3.0               # К-1: формулировка сходится с фактом при |z| <= 3
K2_SIGMA = 5.0               # К-2: формулировка отвергнута при |z| > 5 хотя бы по одному факту

# --- из формулировки (Ag-6) -----------------------------------------------------------------------
theta_full = 4.0 * GM_SUN / (C**2 * R_SUN) * RAD_TO_ARCSEC   # у края Солнца, угл. сек.
theta_half = theta_full / 2.0                                # прочтение (б) канона, I-9

# --- наблюдения: отношение к опорному 4GM/(c^2 b), то есть (1 + gamma)/2 ---------------------------
# (gamma, sigma_gamma, карточка и строка)
GAMMA = {
    "OBS-2 R-1": (0.99983, 0.00045),      # РСДБ, геодезические сеансы
    "OBS-2 R-4": (0.99992, 0.00012),      # РСДБ, позднейшая обработка
    "OBS-3": (0.997, 0.003),              # Hipparcos
    "OBS-4": (1.0 + 2.1e-5, 2.3e-5),      # Cassini, длительность прохождения
    "OBS-10": (0.97, 0.09),               # масса галактики двумя способами
}
# OBS-1, затмение 1919 г.: смещение у края диска, угл. сек., вероятные ошибки
ECLIPSE_1919 = {"OBS-1 Собрал": (1.98, 0.12), "OBS-1 Принсипи": (1.61, 0.30)}

facts = {}
for key, (g, sg) in GAMMA.items():
    ratio, sigma = (1.0 + g) / 2.0, sg / 2.0
    facts[key] = {"ratio": ratio, "sigma": sigma,
                  "z_full": (ratio - 1.0) / sigma,      # формулировка агрегата: 1
                  "z_half": (ratio - 0.5) / sigma}      # половина (I-9)
for key, (val, pe) in ECLIPSE_1919.items():
    sigma = pe * PE_TO_SIGMA
    facts[key] = {"arcsec": val, "sigma_arcsec": sigma,
                  "z_full": (val - theta_full) / sigma,
                  "z_half": (val - theta_half) / sigma}

max_abs_z_full = max(abs(f["z_full"]) for f in facts.values())
max_abs_z_half = max(abs(f["z_half"]) for f in facts.values())

result = {
    "theme": "T-1",
    "constants": {"c_m_s": C, "GM_sun_m3_s2": GM_SUN, "R_sun_m": R_SUN},
    "criteria": {"K1_sigma": K1_SIGMA, "K2_sigma": K2_SIGMA, "free_parameters": 0},
    "theta_full_arcsec": round(theta_full, 4),
    "theta_half_arcsec": round(theta_half, 4),
    "facts": {k: {kk: (sig(vv) if isinstance(vv, float) else vv) for kk, vv in v.items()}
              for k, v in facts.items()},
    "K1_aggregate": {"max_abs_z": round(max_abs_z_full, 3),
                     "verdict": "PASS" if max_abs_z_full <= K1_SIGMA else "FAIL"},
    "K2_half_deflection": {"max_abs_z": round(max_abs_z_half, 1),
                           "verdict": "REJECTED" if max_abs_z_half > K2_SIGMA else "NOT REJECTED"},
    "note": "OBS-11 в проверку не входит: карта массы построена по самому закону Ag-6.",
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_check_aggregate.json")
with open(out, "w", encoding="utf-8") as fh:
    json.dump(result, fh, ensure_ascii=False, indent=2)
    fh.write("\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
