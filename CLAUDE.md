# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

MCP (Model Context Protocol) server that fetches fitness metrics from Garmin Connect. Exposes a `get_daily_metrics` tool that returns resting heart rate, body battery, and sleep score.

## Commands

```bash
# Run the MCP server
python server.py

# Run all tests
python -m pytest test_server.py -v

# Run a single test
python -m pytest test_server.py::TestParseBodyBatteryWithRealData::test_parses_real_garmin_response -v
```

## Architecture

- **server.py**: FastMCP server with `@mcp.tool()` decorated functions. Parsing logic is extracted into pure functions (`parse_resting_heart_rate`, `parse_sleep_score`, `parse_body_battery`) for testability.

- **garmin_client.py**: Handles Garmin authentication via `garminconnect` library with Garth backend. Caches auth tokens in `.garth/` directory to avoid repeated logins.

- **test_server.py**: Tests use real API response data from `test_fixtures.json` (captured from 2025-12-01) rather than synthetic mocks.

## Garmin API Response Structures

Body battery is a list of day objects:
```python
body_battery[0]['bodyBatteryValuesArray']  # [[timestamp, value], ...]
```

User summary is a flat dict:
```python
stats.get('restingHeartRate')
stats.get('sleepScore')
```

## Environment

Requires `.env` with `GARMIN_EMAIL` and `GARMIN_PASSWORD`.
