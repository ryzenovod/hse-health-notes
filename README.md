# HSE Health Notes

Студенческая база знаний магистратуры НИУ ВШЭ «Управление и экономика здравоохранения».

Сайт: <https://ryzenovod.github.io/hse-health-notes/>

## Что внутри

- конспекты занятий по организации, управлению и экономике здравоохранения;
- карты дисциплин первого курса по темам и преподавателям из LMS;
- структура дисциплин по официальному учебному плану;
- полнотекстовый поиск, светлая и тёмная темы, мобильная навигация.

## Локальный запуск

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/mkdocs serve
```

Строгая проверка сборки:

```bash
.venv/bin/mkdocs build --strict
```

## Публикация

Отправка изменений в ветку `main` запускает GitHub Actions и публикует содержимое каталога `site/` в GitHub Pages. Сборка в CI устанавливает зависимости из `requirements.lock` с проверкой хешей.

Названия дисциплин сверены с [учебным планом](https://www.hse.ru/dbs/education/sp_UnitedLearnPlan_28117.pdf).
