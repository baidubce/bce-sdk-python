import asyncio
import logging
from typing import List, Optional, Dict
from mcp.server.models import InitializationOptions
from mcp.server import NotificationOptions, Server, McpError
import mcp.server.stdio
from mcp.types import Resource, LoggingLevel, EmptyResult, Tool, TextContent, ImageContent, EmbeddedResource, BlobResourceContents, ReadResourceResult
import mcp_conf as mcp_conf
from baidubce.services.bos.bos_client import BosClient


server = Server("bos_service")
logger = logging.getLogger("mcp_bos_server")

# create a bos client
bos_client = BosClient(mcp_conf.config)

@server.set_logging_level()
async def set_logging_level(level: LoggingLevel) -> EmptyResult:
    logger.setLevel(level.lower())
    await server.request_context.session.send_log_message(
        level="debug",
        data=f"Log level set to {level}",
        logger="mcp_bos_server"
    )
    return EmptyResult()

@server.list_resources()
async def list_resources() -> List[Resource]:
    """
    List S3 buckets and their contents as resources with pagination
    Args:
        start_after: Start listing after this bucket name
    """
    resources = []
    logger.debug("Starting to list resources")

    try:
        # Get limited number of buckets
        # buckets =  bos_client.list_buckets()
        # logger.debug(f"Processing {len(buckets)} buckets )")

        # limit concurrent operations
        bucket_name = mcp_conf.bucket_name
        response = bos_client.list_objects(bucket_name)
        for obj in response.contents:
            object_key = obj.key
            resource = Resource(
                            uri=f"bos://{bucket_name}/{object_key}",
                            name=object_key,
                        )
            resources.append(resource)
            logger.debug(f"Added resource: {resource.uri}")

    except Exception as e:
        logger.error(f"Error listing buckets: {str(e)}")
        raise

    logger.info(f"Returning {len(resources)} resources")
    return resources

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(
            name="ListBuckets", 
            description="Returns a list of all buckets owned by the authenticated sender of the request. ",
            inputSchema={
                "type": "object",
                "properties": {},
                    
                "required": [],
            },
        ),
        Tool(
            name="ListObjects", 
            description="Returns some or all (up to 1,000) of the objects in a bucket with each request. You can use the request parameters as selection criteria to return a subset of the objects in a bucket. To get a list of your buckets, see ListBuckets.",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {"type": "string", "description": "When you use this operation with a directory bucket, you must use virtual-hosted-style , Path-style requests are not supported."},
                    "max_keys": {"type": "integer", "description": "Sets the maximum number of keys returned in the response. By default, the action returns up to 1,000 key names. The response might contain fewer keys but will never contain more."},
                    "prefix": {"type": "string", "description": "Limits the response to keys that begin with the specified prefix."},
                    "marker": {"type": "string", "description": "marker is where you want to start listing from bos. bos starts listing after this specified key. marker can be any key in the bucket."},
                    "delimiter" : {"type": "string", "description": "The delimiter is a forward slash (/). "}
                },
                "required": ["bucket_name"],
            },
        ),
        Tool(
            name="GetObject", 
            description="Retrieves an object from BOS. ",
            inputSchema={
                "type": "object",
                "properties": {
                    "bucket_name": {"type": "string", "description": "Directory buckets"},
                    "key": {"type": "string", "description": "Object of the object to get. Length Constraints: Minimum length of 1."},
                    "range": {"type": "string", "description": "Downloads the specified byte range of an object."},
                    "version_id": {"type": "string", "description": "Version ID used to reference a specific version of the object."},
                },
                "required": ["bucket_name", "key"]
            }
        )
    ]


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[TextContent | ImageContent | EmbeddedResource]:
    try:
        match name:
            case "ListBuckets":
                response = bos_client.list_buckets()
                logger.debug(f"ListBuckets response: {response}")
                buckets = response.buckets
                return [
                    TextContent(
                        type="text",
                        text=str(buckets)
                    )
                ]
            case "ListObjects":
                response = bos_client.list_objects(**arguments)
                objects = []
                for obj in response.contents:
                    objects.append(obj.key)
                return [
                    TextContent(
                        type="text",
                        text=str(objects)
                    )
                ]
            case "GetObject":
                response = bos_client.get_object_as_string(**arguments)
                return [
                    TextContent(
                        type="text",
                        text=str(response)
                    )
                ]
    except Exception as error:
        return [
            TextContent(
                type="text",
                text=f"Error: {str(error)}"
            )
        ]

async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="bos-mcp-server",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())