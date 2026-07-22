# Lab Repository Organization

## Overview

This repository contains learning utilities organized into three main modules:
- **log_parsing**: Parse and analyze application logs
- **automation**: Utilities for file organization and backups
- **diagnostics**: System health checks

## Directory Structure

```
Lab/
├── automation/              Python module for automation tasks
│   ├── __init__.py         Package marker
│   ├── cli.py              Unified CLI entry point
│   ├── backup.py           Create timestamped zip backups
│   └── file_organizer.py   Sort files by extension
├── diagnostics/            Python module for system diagnostics
│   ├── __init__.py         Package marker
│   ├── cli.py              Unified CLI entry point
│   └── system_check.py     Check disk, memory, network, CPU
├── log_parsing/            Python module for log analysis
│   ├── __init__.py         Package marker
│   ├── parser.py           Parse plain-text timestamped logs
│   ├── json_parser.py      Parse JSON logs for ERROR entries
│   ├── json_parser_advanced.py  Advanced JSON parsing with field filtering
│   └── cli.py              CLI for structured log parsing
├── tests/                  Unit tests
│   ├── test_automation.py
│   ├── test_diagnostics.py
│   └── test_log_parser.py
├── README.md               Project overview
├── .gitignore              Git exclusions
└── docs/
    └── ORGANIZATION.md     This file
```

## Usage

### Log Parsing

**Structured log parsing (timestamped plain text):**
```bash
python3 -m log_parsing.cli path/to/file.log [--level ERROR] [--since "YYYY-MM-DD HH:MM:SS"] [--until "YYYY-MM-DD HH:MM:SS"]
```

**JSON log parsing:**
```bash
python3 -m log_parsing.json_parser path/to/file.json
```

**Advanced JSON parsing with field filtering and export:**
```bash
python3 -m log_parsing.json_parser_advanced path/to/file.json [output_file.json]
```

### Automation

**Organize files by extension:**
```bash
python3 -m automation.cli organize /path/to/directory [--dry-run]
```

**Create timestamped backup:**
```bash
python3 -m automation.cli backup /source/dir /dest/dir
```

### Diagnostics

**Run all system checks:**
```bash
python3 -m diagnostics.cli system-check [--path /] [--host 8.8.8.8] [--port 53]
```

## Running Tests

```bash
python3 -m unittest discover -s tests -v
```

## Notes

- All modules use Python's standard library only — no external dependencies
- Each module is designed to be run standalone via `python3 -m <module>.cli`
- Tests use Python's built-in `unittest` framework
