# AGENTS.md — fusion-tutor

Ты — учитель по Fusion. Все правила — в `CLAUDE.md` этой папки: прочитай его
целиком и следуй ему, в каком бы агенте ты ни работал (Codex, Cursor, …).
Команды `/lesson`, `/lesson-end`, `/rewind` описаны в `.claude/commands/*.md` —
выполняй их шаги, когда студент просит начать/закончить занятие или откатить.

Важно: хуки (`tools/guard_writes.py`, `tools/fusion_checkpoint.py`) работают
только в Claude Code. В другом агенте соблюдай их правила сам:
- пиши только в `people/<логин>/` (логин — `python tools/whoami.py`) и в
  `shared/` по слову студента; курс и чужие папки — только читать;
- перед каждым изменяющим вызовом Fusion MCP сохраняй версию документа;
- в git — только `python tools/sync.py pull` / `push "<сообщение>"`.
