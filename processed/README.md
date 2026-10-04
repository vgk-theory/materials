# processed — производные тексты

Материалы, полученные из оригиналов в [`../sources/`](../sources/README.md), в том числе с помощью AI.

- `monograph/<труд>/` — текст труда автора; имя папки совпадает с именем исходного файла в `sources/monograph/`:
  - `README.md` — сведения о труде и об обработке;
  - `pages/` — постраничный текст, `page-NNNNN.txt`; имя файла соответствует странице труда: `page-00038.txt` — страница 38;
  - `chapters/` — текст в md по главам (если есть)
- `transcripts/` — расшифровки видео, один md на видео

Чтобы найти нужное место в труде, не читайте текст целиком: ищите слово по `pages/` (`grep -rn "<слово>" processed/monograph/<труд>/pages/`), затем открывайте только нужные страницы.

Каждый md-файл с производным текстом начинается с front matter (для постраничного текста — в `README.md` папки труда):

```yaml
---
source: ../../sources/monograph/<файл>      # или ссылка на YouTube
source_type: monograph | video
processed_by: <инструмент/модель или человек>
processed_date: YYYY-MM-DD
reviewed_by_human: false
---
```
