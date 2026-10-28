# reviews — отчёты гейта по разделу `formalized-theory`

Отчёты трёх ролей гейта ([`ai/agents/README.md`](../../../ai/agents/README.md)) по разделу. Единица проверки — раздел целиком: один отчёт на роль, `formalized-theory-<роль>-<дата>.md`, с commit и sha256 каждого из трёх документов в шапке (правило 7 гейта). Отчёты по отдельным файлам — только для изолированной правки.

В корне папки лежат только отчёты по **текущей** редакции документов. После внесения правок по отчёту редакция меняется, гейт проходится заново с math-verifier, а отчёты по прежней редакции переносятся в [`archive/`](archive/) с пометкой «Устарел» в первой строке: по ним следующие роли сверяют, что прошлые находки внесены. Отчёты по редакциям до `39700c3` были удалены по прежнему правилу; их история — в git: `git log -- research/formalized-theory/reviews/`.

Отчёты — рабочие материалы: на сайте не показываются.

## Текущая редакция

Редакция от 2026-10-28 (sha256: `axioms.md` `950e72f5…1174`, `definitions.md` `e8baf081…1027`, `formalism.md` `fbb1e403…d170e`). В неё внесены все находки девяти отчётов по редакции `39700c3` (по каждому документу: math-verifier, falsifier, peer-reviewer; суммарно 7 MAJOR и 41 MINOR, CRITICAL не было). **Гейт по текущей редакции не проходился: отчётов нет.** Следующий круг — по разделу целиком, начиная с math-verifier; его входы — три документа и девять архивных отчётов.

## Архив

[`archive/`](archive/) — девять отчётов по редакции `39700c3` (2026-10-25), по одному на роль и документ; все помечены «Устарел», находки внесены 2026-10-28:

| Документ | math-verifier | falsifier | peer-reviewer |
|----------|---------------|-----------|---------------|
| `axioms.md` | [VERIFIED WITH REMARKS](archive/axioms-math-verification-2026-10-25.md) (4 MINOR) | [ВЫДЕРЖИВАЕТ С ПРАВКАМИ](archive/axioms-falsification-2026-10-25.md) (3 MAJOR, 7 MINOR) | [MAJOR REVISION](archive/axioms-peer-review-2026-10-25.md) (6 MINOR собственных) |
| `definitions.md` | [VERIFIED WITH REMARKS](archive/definitions-math-verification-2026-10-25.md) (7 MINOR) | [ВЫДЕРЖИВАЕТ С ПРАВКАМИ](archive/definitions-falsification-2026-10-25.md) (2 MAJOR, 4 MINOR) | [MAJOR REVISION](archive/definitions-peer-review-2026-10-25.md) (4 MINOR собственных) |
| `formalism.md` | [VERIFIED WITH REMARKS](archive/formalism-math-verification-2026-10-25.md) (1 MAJOR, 3 MINOR) | [ВЫДЕРЖИВАЕТ С ПРАВКАМИ](archive/formalism-falsification-2026-10-25.md) (1 MAJOR, 3 MINOR) | [MAJOR REVISION](archive/formalism-peer-review-2026-10-25.md) (3 MINOR собственных) |

Отчёты по `formalism.md` были перенесены в архив раньше остальных: после них в документ добавили контекст отзыва по п. 1.8 (редакция `33d2f0a2…a811`), и только затем, 2026-10-28, внесены сами находки.
