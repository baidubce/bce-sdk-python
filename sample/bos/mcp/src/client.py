from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import asyncio
import os
import sys

async def main():
    """
    Main function that runs the example code
    """
    # Get the absolute path to the server script
    # Assuming the server script is in the same directory as this client
    server_script = os.path.join(os.path.dirname(__file__), "bos_mcp_server/server.py")

    # Create server parameters for stdio connection using python interpreter
    server_params = StdioServerParameters(
        command=sys.executable,  # Use Python interpreter
        args=[server_script],    # Path to your server script
        env=None                 # Optional environment variables
    )

    async with stdio_client(server_params) as (read, write):
        bucket_name = "liujiang-test"
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available resources
            resources = await session.list_resources(bucket_name)

            # Print or process the resources
            for resource in resources:
                print(f"Resource: {resource.name} ({resource.uri})")

if __name__ == "__main__":
    asyncio.run(main())