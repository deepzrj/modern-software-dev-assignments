# Week 3 - Weather MCP Server

This folder contains a local STDIO Model Context Protocol server that wraps the OpenWeather API. It exposes weather tools that can be connected to an MCP-aware client such as Claude Desktop or an AI IDE.

## External API

Provider: OpenWeather

Base URL:

```text
https://api.openweathermap.org/data/2.5
```

The server is designed around these endpoints:

- `/weather` for current weather by city.
- `/forecast` for forecast data by city.

## Environment Variables

Create or update the repository root `.env` file:

```text
OPENWEATHER_API_KEY=your_openweather_api_key
```

The server loads this value from the repository root using `python-dotenv`.

## Setup

Install the repository dependencies from the repository root:

```bash
poetry install --no-interaction
```

If running without Poetry, make sure these packages are installed in the active Python environment:

```bash
pip install mcp requests python-dotenv
```

## Run Locally

From the repository root:

```bash
poetry run python -m week3.server.main
```

The server uses STDIO transport, so logs are sent to stderr instead of stdout. This avoids corrupting MCP protocol messages.

## Claude Desktop Example Configuration

Add a server entry similar to this in the Claude Desktop MCP config, adjusting paths for your machine:

```json
{
  "mcpServers": {
    "weather": {
      "command": "poetry",
      "args": ["run", "python", "-m", "week3.server.main"],
      "cwd": "C:\\Users\\MCW\\modern-dev-portfolio\\base-repo"
    }
  }
}
```

Restart the MCP client after editing the config.

## Tools

### `get_current_weather`

Gets current weather for a city.

Input:

```json
{
  "city": "London, UK"
}
```

Example output:

```json
{
  "city": "London",
  "temperature": "12.4C",
  "condition": "light rain",
  "humidity": "82%"
}
```

### `get_weather_forecast`

Gets the next five forecast entries for a city from OpenWeather.

Input:

```json
{
  "city": "London, UK"
}
```

Example output:

```json
{
  "city": "London",
  "forecast": [
    {
      "time": "2026-04-26 12:00:00",
      "temperature": "13.2C",
      "condition": "cloudy",
      "humidity": "76%"
    }
  ]
}
```

## Example Client Requests

Natural-language prompts that should trigger the tools:

```text
What is the current weather in London, UK?
```

```text
Give me the weather forecast for San Francisco.
```

## Error Handling

The weather tools handle the main API failure modes:

- Missing `OPENWEATHER_API_KEY` returns a configuration error.
- HTTP `429` returns a rate-limit message.
- Other non-200 OpenWeather responses return the upstream status code.
- Request timeouts return a timeout message.
- Unexpected exceptions are logged to stderr and returned as error JSON.

## Files

- `server/main.py`: MCP server entrypoint, tool registration, and STDIO transport.
- `server/tools.py`: OpenWeather API wrapper functions and error handling.
- `server/config.py`: `.env` loading and API configuration.

## Personal Learnings & Takeaways

Week 3 introduced me to MCP tool design through a small OpenWeather wrapper. The server exposes two typed tools, keeps logs on stderr for STDIO compatibility, and returns structured error JSON for missing API keys, timeouts, rate limits, and upstream failures.

The assignment made the separation of responsibilities clear:
- The **model** decides what action to take
- The **tool** executes that action deterministically against a real API

I also practiced API interaction patterns, including:
- handling missing or invalid inputs
- dealing with network failures
- validating responses before returning them

The main takeaway was that useful MCP servers need ordinary software-engineering discipline: clear schemas, predictable errors, and transport-safe logging.
