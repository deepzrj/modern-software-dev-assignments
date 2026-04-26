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

Intended to get forecast data for a city.

Input:

```json
{
  "city": "London, UK"
}
```

Current implementation note: `week3/server/main.py` registers this tool, but `week3/server/tools.py` still contains stubbed forecast logic. Complete the function by calling OpenWeather's `/forecast` endpoint before relying on this tool for grading or demos.

## Example Client Requests

Natural-language prompts that should trigger the tools:

```text
What is the current weather in London, UK?
```

```text
Give me the weather forecast for San Francisco.
```

## Error Handling

The current weather tool handles the main API failure modes:

- Missing `OPENWEATHER_API_KEY` returns a configuration error.
- HTTP `429` returns a rate-limit message.
- Other non-200 OpenWeather responses return the upstream status code.
- Request timeouts return a timeout message.
- Unexpected exceptions are logged to stderr and returned as error JSON.

## Files

- `server/main.py`: MCP server entrypoint, tool registration, and STDIO transport.
- `server/tools.py`: OpenWeather API wrapper functions and error handling.
- `server/config.py`: `.env` loading and API configuration.
