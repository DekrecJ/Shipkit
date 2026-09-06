# Error Recovery

State/project JSON writes use a temporary file, flush + fsync, then atomic replace. Existing files receive `.bak` backups. `shipkit repair` attempts backup recovery; `shipkit migrate` updates compatible legacy metadata. Forced phase transitions produce lifecycle debt instead of fabricating completion evidence.
