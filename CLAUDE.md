# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**"The Enforcer"** - An AI-driven training coach MCP server that:
- Fetches fitness data from Garmin Connect
- Maintains a 7-day rolling training plan
- Enforces training pillars (Strength, Mobility, Long Effort)
- Provides LLM-driven coaching with daily briefs

**Athlete context:** Running, Cycling, High-intensity games (Ultimate). Injury-prone, needs enforced Mobility + Strength. Multiple target events with A/B/C priority.

## Commands

```bash
# Run the MCP server
python server.py

# Run all tests (36 tests)
python -m pytest test_server.py -v

# Run a single test
python -m pytest test_server.py::TestParseActivity::test_parses_running_activity -v
```

## Current MCP Tools

| Tool | Purpose | Returns |
|------|---------|---------|
| `get_daily_metrics()` | RHR, Body Battery, Sleep Score | Formatted string |
| `get_activities_range(start, end)` | Activity history | JSON array |
| `get_personal_records()` | All PBs | JSON array |
| `get_training_readiness(date)` | Recovery score, HRV, load | JSON object |

## Architecture

```
server.py
├── Parsing functions (pure, testable)
│   ├── parse_resting_heart_rate()
│   ├── parse_sleep_score()
│   ├── parse_body_battery()
│   ├── parse_activity() / parse_activities()
│   ├── parse_personal_records()
│   └── parse_training_readiness()
└── MCP tools (@mcp.tool() decorated)

garmin_client.py
└── get_garmin_client() - Auth with token caching in .garth/

test_server.py
└── Tests using real fixture data from test_fixtures.json
```

## Garmin API Response Structures

**Activities** (`get_activities_by_date`):
```python
activity['activityType']['typeKey']  # "running", "strength_training", etc.
activity['duration']  # seconds
activity['distance']  # meters
activity['averageHR'], activity['maxHR']
```

**Personal Records** (`get_personal_record`):
```python
pr_data['personalRecords'][0]['prTypeLabelKey']  # "pr_running_fastest_5k_time"
pr_data['personalRecords'][0]['value']  # seconds for time-based
```

**Training Readiness** (`get_training_readiness`):
```python
readiness['score']  # 0-100
readiness['level']  # "PRIME", "HIGH", "MODERATE", "LOW"
readiness['hrvStatus'], readiness['acuteLoad']
```

## Implementation Plan (The Enforcer)

See full plan: `.claude/plans/reactive-questing-alpaca.md`

### Sprint 1: Data Foundation ✅ (3/4 complete)
- [x] `get_activities_range()` - Activity history
- [x] `get_personal_records()` - PBs
- [x] `get_training_readiness()` - Recovery metrics
- [ ] `refresh_athlete_profile()` - Generate baseline from 6mo history

### Sprint 2: Rule Engine (pending)
- [ ] `training_config.json` schema (events, blocks, pillars)
- [ ] `check_weekly_compliance()` function
- [ ] `get_compliance_report()` tool

### Sprint 3: LLM Planning (pending)
- [ ] `build_planning_context()` function
- [ ] `generate_weekly_plan()` tool (LLM-driven)
- [ ] Suggestion system (LLM proposes, user approves)

### Sprint 4: Automation (pending)
- [ ] `daily_loop.py` - Morning audit script
- [ ] Task Scheduler setup (05:00 daily)
- [ ] Telegram notifier

## Environment

Requires `.env` with:
```
GARMIN_EMAIL=your@email.com
GARMIN_PASSWORD=yourpassword
ANTHROPIC_API_KEY=sk-ant-xxx  # For LLM integration (Sprint 3+)
```

## Testing Pattern

Tests use real API responses captured in `test_fixtures.json`. When adding new tools:
1. Create parsing function (pure, no I/O)
2. Add MCP tool with `@mcp.tool()` decorator
3. Write tests with sample data matching Garmin structure
4. Run: `python -m pytest test_server.py -v`
