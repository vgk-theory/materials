#!/usr/bin/env python
"""PK-1, пункт материализации Д-5: фактор размыкания (1) автора
(«разнос масс (зависимость от телесного угла) … график скругляется», стр. 21)
против согласованности GM⊕ по орбитам разной высоты.

Что считается. Для сферы радиуса R на расстоянии r > R:
  точный телесный угол        Ω(r)     = 2π(1 − √(1 − R²/r²))
  малоугловой (ур. 8 formalism) Ω₀(r)   = πR²/r²
  проекционный               Ω_p(r)   = ∫cosθ dΩ = π sin²θ_max = πR²/r²  (точно при всех r > R)
Относительное отклонение  δ(r) = Ω/Ω₀ − 1 = 2(1 − √(1 − x))/x − 1,  x = (R/r)².
Ряд при r ≫ R: δ ≈ x/4 (выводится, печатается для сравнения, несущим числом не является).

Посылка переноса (п. 3.1 scientific-method.md): если бы результирующая сила масштабировалась
точным телесным углом Ω (а не проекционным Ω_p ≡ Ω₀), то GM⊕, подогнанное по орбитам разной
высоты в модели 1/r², расходилось бы на величину порядка δ(r). Наблюдаемая согласованность
GM⊕ между орбитальными решениями — ε_obs (внешняя константа, см. ниже).

Критерий: PASS ⇔ min_orbits δ(r) / ε_obs ≥ 10², иначе FAIL (одно условие, совпадает с кодом).
Точки переворота (пишутся в JSON): ε_obs* = min δ / 10² (по согласованности) и threshold* = min δ / ε_obs
(по порогу); статус CONTRADICTS прочтения «∝ Ω» от порога не зависит (достаточно δ/ε_obs > 1).
Приведение шкал TT/TDB (L_B = 1.55e-8) меняет GM⊕ на 1.6e-8 относительных — ниже ε_obs, не учитывается.
Честная запись (п. 1.3 scientific-method.md): критерий и ε_obs объявлены в этой шапке до
запуска скрипта (2026-10-30), но значения δ были известны раньше — со второй редакции
карточки (2026-10-24: 0.40 / 0.015 / 6.9e-5). Строгой пред-регистрацией
это не является. Порог 10² обоснован независимо от δ: неопределённость выбора орбиты внутри
класса (≤ ×1.5) покрывается порогом 10² с запасом почти в два порядка; разброс оценок
согласованности GM⊕ между 1e-8 и 1e-7 уже поглощён консервативным выбором ε_obs = 1e-7 и
повторно не учитывается. Точка переворота: ε_obs* = min δ / 10² (пишется в JSON) — PASS
держится, пока согласованность GM⊕ между SLR и ЛЛЛ лучше ε_obs*.

Константы (все внешние):
  R⊕ = 6378.137 км                — GRS80 (Moritz H., J. Geod. 74, 128, 2000); IERS TN 36 табл. 1.1
                                     даёт a_E = 6378.1366 км — меняет δ на 1.25e-7 (Луна) … 2.9e-7 (ИСЗ-700) относительных
  GM⊕ относительная неопределённость 2·10⁻⁹ — там же (8·10⁵ м³/с² на 3.986004418·10¹⁴)
  ε_obs = 1·10⁻⁷                   — верхняя (консервативная) оценка согласованности GM⊕
                                     между SLR (LAGEOS) и орбитами GPS/LEO и ЛЛЛ
                                     (Ries et al., GRL 19, 529, 1992); берётся худшая граница
  Большие полуоси (км), иллюстративные значения орбит:
    ИСЗ h = 700 км → r = R⊕ + 700;  LAGEOS-1 a ≈ 12 270;  GPS a ≈ 26 560;  Луна ā ≈ 384 400
Числа орбит — справочные (ILRS / IS-GPS-200 / IAU); несущее число — не они, а δ, которое
от выбора орбит внутри указанных высот меняется не более чем в 1.5 раза и критерий не задевает.

Вывод: sims/_solid_angle.json
"""

import json
import math
import os

R_EARTH_KM = 6378.137          # GRS80 (Moritz 2000)
GM_REL_UNC = 2.0e-9            # IERS TN 36: 8e5 / 3.986004418e14
EPS_OBS = 1.0e-7               # консервативная согласованность GM⊕ между решениями
THRESHOLD = 1.0e2              # критерий: min δ / ε_obs >= 100

ORBITS = {
    "ISZ_700km": R_EARTH_KM + 700.0,
    "LAGEOS": 12270.0,
    "GPS": 26560.0,
    "Moon": 384400.0,
}


def delta_exact(r_km: float) -> float:
    x = (R_EARTH_KM / r_km) ** 2
    return 2.0 * (1.0 - math.sqrt(1.0 - x)) / x - 1.0


def delta_series(r_km: float) -> float:
    return (R_EARTH_KM / r_km) ** 2 / 4.0


def main() -> None:
    rows = {}
    for name, r in ORBITS.items():
        d = delta_exact(r)
        rows[name] = {
            "r_km": r,
            "x": (R_EARTH_KM / r) ** 2,
            "delta_exact": d,
            "delta_series_x_over_4": delta_series(r),
            "delta_over_eps_obs": d / EPS_OBS,
            "delta_over_gm_unc": d / GM_REL_UNC,
        }
    d_min = min(v["delta_exact"] for v in rows.values())
    d_max = max(v["delta_exact"] for v in rows.values())
    ratio_min = d_min / EPS_OBS
    passed = ratio_min >= THRESHOLD
    out = {
        "constants": {
            "R_earth_km": R_EARTH_KM,
            "GM_rel_uncertainty": GM_REL_UNC,
            "eps_obs": EPS_OBS,
            "threshold": THRESHOLD,
        },
        "orbits": rows,
        "delta_min": d_min,
        "delta_max": d_max,
        "orders_min_vs_eps_obs": math.log10(ratio_min),
        "orders_span_vs_gm_unc": math.log10(d_max / GM_REL_UNC),
        "eps_obs_star_reversal_point": d_min / THRESHOLD,
        "threshold_star_reversal_point": d_min / EPS_OBS,
        "note": "статус CONTRADICTS прочтения (B) не зависит от порога: достаточно delta/eps_obs > 1; порог задаёт запас",
        "criterion": "min_delta / eps_obs >= threshold",
        "PASS": passed,
    }
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "_solid_angle.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
    for name, v in rows.items():
        print(f"{name:10s} r={v['r_km']:9.1f} km  delta={v['delta_exact']:.4g}  "
              f"x/4={v['delta_series_x_over_4']:.4g}  delta/eps_obs={v['delta_over_eps_obs']:.3g}")
    print(f"min delta / eps_obs = {ratio_min:.3g}  (log10 = {out['orders_min_vs_eps_obs']:.2f}); "
          f"PASS={passed}")


if __name__ == "__main__":
    main()
