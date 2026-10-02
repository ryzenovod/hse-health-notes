# HSE Health Notes

Студенческая база знаний магистратуры НИУ ВШЭ «Управление и экономика здравоохранения».

Сайт: <https://ryzenovod.github.io/hse-health-notes/>

## Что внутри

- каталог конспектов по предметам и темам;
- карты дисциплин первого курса по темам и преподавателям из LMS;
- структура дисциплин по официальному учебному плану;
- полнотекстовый поиск, светлая и тёмная темы, мобильная навигация.
- локальные SVG-схемы и формулы: MathJax 3.2.2 загружается асинхронно только в статьях с математикой, без внешнего CDN.

## Локальный запуск

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes -r requirements.lock
.venv/bin/mkdocs serve
```

Строгая проверка сборки:

```bash
.venv/bin/mkdocs build --strict
.venv/bin/python scripts/check_site.py site
.venv/bin/python -m unittest discover -s tests
```

## Публикация

Отправка изменений в ветку `main` запускает GitHub Actions и публикует содержимое каталога `site/` в GitHub Pages. Pull request запускает сборку и проверки без публикации. CI устанавливает зависимости из `requirements.lock` с проверкой хешей, проверяет внутренние ссылки, якоря и метаданные схем.

## Схемы занятий

`scripts/generate_course_figures.py` строит локальные SVG для налогового семинара, лекции ЭОС 1 октября, диагностики и управленческих кейсов. Координаты рассчитаны из указанных в конспектах моделей. Пересборка:

```bash
.venv/bin/python scripts/generate_course_figures.py
```

Названия дисциплин сверены с [учебным планом](https://www.hse.ru/dbs/education/sp_UnitedLearnPlan_28117.pdf).
