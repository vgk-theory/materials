---
source: ../../sources/monograph/gravitatsionnoe-vzaimodeystvie-osnovy-kosmologii.pdf
source_type: monograph
document: adaptations-index
authors: участники сообщества (имена не указаны) при участии AI
processed_by: Claude (Anthropic)
processed_date: 2026-11-18
reviewed_by_human: false
---

# Индекс раздела `adaptations`

Точка входа. Читать раздел в таком порядке, останавливаясь, как только ответ найден:

1. Нужный индекс ниже — одна строка на единицу (идентификатор, статус, путь).
2. Шапка (front matter) основного файла единицы: `status`, `imports`, `relates`, `verdict` —
   действующее состояние без чтения тела файла.
3. Нужная секция файла по заголовку.
4. Правила раздела — [`README.md`](README.md), только если они нужны для записи.

| Что | Индекс | Единиц | Где состояние единицы |
|---|---|---|---|
| Темы, покрытие «тема × модель», реестр импортов, бэклог тем | [`themes/index.md`](themes/index.md) | 7 (2 с агрегатом, 5 открыты) + бэклог 23 | шапка `themes/T-N-<slug>/T-N.md` |
| Модели (реестр) | [`models/registry.md`](models/registry.md) | 13, записано 11 | шапка `models/A-N-<slug>/adaptation.md` |
| Факты | [`facts/index.md`](facts/index.md) | 29 | шапка `facts/OBS-N-<slug>.md` |

Поля шапки: `id`; `status` (шкалы — `README.md`, «Статусы»); `imports` — счётчик импортов (модель, тема);
`relates` — связанные единицы; `verdict` — действующее состояние, перезаписывается целиком, история — в git.
Индексы и шапка обновляются в том же изменении, что и сама единица.
