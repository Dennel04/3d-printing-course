# Fusion MCP и API — грабли и обходы

Собрано 2026-10-04 по проблемам, на которые наткнулись при работе учителя
через Fusion MCP, и по поиску (форумы Autodesk, справка Autodesk MCP).

## Что мешало и почему

| Симптом | Причина | Решение |
|---|---|---|
| Хук: «Cannot perform 'script' while a command dialog is open» | В Fusion активна команда: `ConstrainedOrbitCommand` (вращение), `FusionDeleteCommand` (случайный Delete) | Студент жмёт Esc. Смотреть заранее: `fusion_mcp_read` → `activeCommand`. Простой = `SelectCommand` |
| Модель крутится за мышью и не останавливается | Известный баг Fusion (FUS-82525): отпустил кнопку орбиты над деревом браузера → орбита осталась активной | Потянуть ViewCube за угол к центру экрана (принятое решение на форуме Autodesk). Вращать через Shift+колесо, а не кнопкой Orbit на нижней панели |
| Fusion не отвечает даже на read-only запросы, хук «timed out» | Открыто модальное окно в Fusion; все вызовы API ждут, пока его закроют. 2026-10-04 это был вопрос «сохранить / не сохранять `_tutor-sandbox`», всплывший, когда учитель создал новый документ. Песочница с несохранёнными правками висела в фоне, хотя `activeDocument` был пуст | Студент закрывает окно. В начале занятия смотреть **все** открытые документы (`fusion_mcp_read` → `document`/`open`), а не только активный; несохранённые — сохранить или закрыть до создания новых. Чтобы не ждать 90 с — сначала быстрый ping |
| Сохранение/чекпоинт долго висит | Версия грузится в облако; по справке Autodesk — антивирус/файрвол/медленный интернет/большие файлы | Не делать лишних версий; большие сборки (робот) вставлять ссылкой (XREF), а не копией |

## API: проверенные обходы

- **f3z** не импортируется через `importManager.createFusionArchiveImportOptions`
  (только f3d) → `DataFolder.uploadFile(path)` в проект, потом открыть.
- **Вырез «сквозь всё» в обе стороны**: `setAllExtent(SymmetricExtentDirection)` /
  `setOneSideExtent(ThroughAll, Symmetric)` режет **только в одну сторону**
  (подтверждено у нас и на форуме «API Extrude 2 sides Through All»).
  Работает: `setTwoSidesExtent(ThroughAll, ThroughAll)`; при правке готовой
  фичи нужны и углы: `setTwoSidesExtent(a, b, V('0 deg'), V('0 deg'))`.
- **Правка готовой фичи** → сначала `feature.timelineObject.rollTo(True)`,
  потом `design.timeline.moveToEnd()`, иначе «Didn't roll editing feature back».
- `unitsManager.evaluateExpression(expr, 'mm')` возвращает **см** (внутренние
  единицы), а не мм.
- **Эскиз на смещённой конструктивной плоскости**: размеры от `originPoint`
  не дали «полностью определён». Обход: эскиз на базовой плоскости + у
  выдавливания `OffsetStartDefinition` с тем же выражением.
- Эскиз на XZ-плоскости: sketch x = мир X, sketch y = **−**мир Z → точки
  ставить через `sketch.modelToSketchSpace(Point3D)`.
- **Скрипт упал — откатился целиком** (одна транзакция): частичных фич не
  остаётся, можно чинить и запускать заново.
- `app.data.activeProject` падает (InternalValidationError), когда не открыт
  ни один документ → искать проект в `app.data.dataProjects` по имени.
- Покупное изделие (STEP) — в новый компонент с матрицей
  (`addNewComponent(matrix)` + `importToTarget2(..., comp)`), тогда не нужен
  snapshot позиции.
- Чужую большую сборку — `occurrences.addByInsert(dataFile, matrix, True)`
  (XREF): лёгкая, обновляется, для Interference годится.
- Read-only скрипт может: двигать камеру вида, читать `ui.activeCommand`,
  вызвать `ui.terminateActiveCommand()` (проверено, когда активна
  `SelectCommand`).

## Правило для учителя

После каждого построения проверять **геометрию** (сколько отверстий и где,
размеры), а не только Interference. Ошибку с отверстиями на одной стенке
заметил студент, а не проверка.
