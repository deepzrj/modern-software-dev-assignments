import asyncio
import json
from mcp.server import Server
from mcp.types import Tool, TextContent, EmbeddedResource
from mcp.server.stdio import stdio_server

from week3.server.tools import get_current_weather, get_weather_forecast

server = Server("weather-mcp-server")

@server.list_tools()
async def list_tools():
    """List available weather tools."""
    return [
        Tool(
            name="get_current_weather",
            description="Get current weather for a city (temperature and sky conditions).",
            input_schema={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city name, e.g., London, UK"}
                },
                "required": ["city"]
            }
        ),
        Tool(
            name="get_weather_forecast",
            description="Get a 5-step weather forecast for a city.",
            input_schema={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "The city name"}
                },
                "required": ["city"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool execution requests."""
    if name == "get_current_weather":
        result = get_current_weather(arguments["city"])
    elif name == "get_weather_forecast":
        result = get_weather_forecast(arguments["city"])
    else:
        raise ValueError(f"Unknown tool: {name}")

    return [
        TextContent(
            type="text",
            text=json.dumps(result, indent=2)
        )
    ]

async def main():
    # Use the stdio transport for local integration (e.g., Claude Desktop)
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
