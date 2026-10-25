# reviews — отчёты гейта по разделу `formalized-theory`

Отчёты трёх ролей гейта ([`ai/agents/README.md`](../../../ai/agents/README.md)) по разделу. Единица проверки — раздел целиком: один отчёт на роль, `formalized-theory-<роль>-<дата>.md`, с commit и sha256 каждого из трёх документов в шапке (правило 7 гейта). Отчёты по отдельным файлам — только для изолированной правки; лежащие здесь пофайловые отчёты от 2026-10-25 сделаны до введения этого правила.

В корне папки лежат только отчёты по **текущей** редакции документов. После внесения правок по отчёту редакция меняется, гейт проходится заново с math-verifier, а отчёты по прежней редакции переносятся в [`archive/`](archive/) с пометкой «Устарел» в первой строке: по ним следующие роли сверяют, что прошлые находки внесены. Отчёты по редакциям до `39700c3` были удалены по прежнему правилу; их история — в git: `git log -- research/formalized-theory/reviews/`.

Отчёты — рабочие материалы: на сайте не показываются.

## Текущая редакция

Редакция `39700c3` (2026-10-25). Все три роли по всем трём документам выполнены; CRITICAL-находок нет; вердикт peer-reviewer по каждому документу — MAJOR REVISION. Итоговый статус и сводка — в [`../README.md`](../README.md).

| Документ | math-verifier | falsifier | peer-reviewer |
|----------|---------------|-----------|---------------|
| `axioms.md` | [VERIFIED WITH REMARKS](axioms-math-verification-2026-10-25.md) | [ВЫДЕРЖИВАЕТ С ПРАВКАМИ](axioms-falsification-2026-10-25.md) | [MAJOR REVISION](axioms-peer-review-2026-10-25.md) |
| `definitions.md` | [VERIFIED WITH REMARKS](definitions-math-verification-2026-10-25.md) | [ВЫДЕРЖИВАЕТ С ПРАВКАМИ](definitions-falsification-2026-10-25.md) | [MAJOR REVISION](definitions-peer-review-2026-10-25.md) |
| `formalism.md` | не проходился для текущей редакции; по `39700c3` — [VERIFIED WITH REMARKS](archive/formalism-math-verification-2026-10-25.md) (архив) | по `39700c3` — [ВЫДЕРЖИВАЕТ С ПРАВКАМИ](archive/formalism-falsification-2026-10-25.md) (архив) | по `39700c3` — [MAJOR REVISION](archive/formalism-peer-review-2026-10-25.md) (архив) |

`formalism.md` изменён после гейта (добавлен контекст отзыва по п. 1.8), поэтому его отчёты перенесены в [`archive/`](archive/) с пометкой «Устарел»; находки из них не внесены и остаются текущими для следующего круга.
