import shutil
import os

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp import types

server_params = StdioServerParameters(
    command = str(shutil.which("npx")), 
    args = ["-y", "@modelcontextprotocol/server-everything"],
    env=os.environ.copy()
)

async def handle_sampling_message(message: types.CreateMessageRequestParams) -> types.CreateMessageResult:
    print(message)
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text="Hello, world! from model",
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )

async def run():
    print("Starting server")
    async with stdio_client(server_params) as (read, write):
        print("Connected")
        async with ClientSession(read, write, sampling_callback=handle_sampling_message) as session:
            print("Session created")
            # Initialize the connection
            await session.initialize()
            print("Initialized")

            # Create a sampling request
            resp = await session.call_tool(
                name="sampleLLM",
                arguments={
                    "prompt": "Hello, world!",
                    "max_tokens": 10,
                }
            )

            assert resp.content[0].type == "text"
            print(f"{resp.content[0].text=}") 
            print("Done")
            exit(0)

if __name__ == "__main__":
    import asyncio
    asyncio.run(run())