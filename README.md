# Lab
Learning Purpose

Basic Python examples for log parsing, automation scripts, and diagnostic tasks.
No external dependencies — standard library only.

## Layout

- `log_parsing/` — parse timestamped log files and summarize by level
  - `python3 -m log_parsing.cli path/to/file.log [--level ERROR] [--since "YYYY-MM-DD HH:MM:SS"] [--until "YYYY-MM-DD HH:MM:SS"]`
- `automation/` — small automation scripts
  - `python3 -m automation.file_organizer <directory> [--dry-run]` — sort files into subfolders by extension
  - `python3 -m automation.backup <source_dir> <dest_dir>` — create a timestamped zip backup
- `diagnostics/` — basic system diagnostics
  - `python3 -m diagnostics.system_check [--path /] [--host 8.8.8.8] [--port 53]` — checks disk space, memory, network, and CPU count
- `tests/` — unittest suite for the above

## Running tests

```
python3 -m unittest discover -s tests -v
```
