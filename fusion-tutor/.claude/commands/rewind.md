---
description: Откатить модель Fusion к прошлой версии (как /rewind в Claude Code)
argument-hint: [номер версии или "last" для отмены последнего шага]
---

Откат активного документа Fusion. Аргумент: $ARGUMENTS

1. Если аргумент `last` — один вызов `fusion_mcp_update` `undo`, покажи
   скриншот и закончи.
2. Иначе покажи список версий (read-only скрипт, `readOnly: true`):

   ```python
   import adsk.core, datetime
   def run(_context: str):
       doc = adsk.core.Application.get().activeDocument
       print(doc.name, "| несохранённые правки:", doc.isModified)
       for v in doc.dataFile.versions:
           t = datetime.datetime.fromtimestamp(v.dateCreated).strftime("%d.%m %H:%M:%S")
           print(f"v{v.versionNumber}  {t}  {v.description}")
   ```
   Добавь к каждой версии из `log/fusion-actions.jsonl` / журнала занятия,
   что учитель менял после неё. Если номер не дан — спроси, к какой версии
   вернуться.
3. Откат к версии N — один вызов `fusion_mcp_execute` script (без readOnly;
   хук перед этим сам сохранит текущее состояние, так что откат тоже можно
   отменить):

   ```python
   import adsk.core, adsk.fusion
   def run(_context: str):
       app = adsk.core.Application.get()
       doc = app.activeDocument
       df = doc.dataFile
       target = [v for v in df.versions if v.versionNumber == N][0]
       if not target.promote():          # версия N становится новой последней
           raise RuntimeError("promote() failed")
       doc.close(False)                  # текущее состояние уже в чекпоинте
       newdoc = app.documents.open(df.latestVersion)
       d = adsk.fusion.Design.cast(app.activeProduct)
       print("opened", newdoc.name, "v", newdoc.dataFile.versionNumber,
             [b.name for b in d.rootComponent.bRepBodies])
   ```
   (Проверено 03.10 на `_tutor-sandbox`: v1→v8 и обратно v7→v9.)
4. Проверь результат (`inspect_model.py` + скриншот) и скажи студенту, к
   чему вернулись. Запиши откат в журнал занятия.
