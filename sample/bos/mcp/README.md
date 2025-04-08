# Sample BOS Model Context Protocol Server

An MCP server implementation for retrieving  data such as PDF's from BOS.

## Features
### Resources
Expose BOS Data through **Resources**. (think of these sort of like GET endpoints; they are used to load information into the LLM's context). Currently only **string** documents supported and limited to **1000** objects.


### Tools
- **ListBuckets**
  - Returns a list of all buckets owned by the authenticated sender of the request
- **ListObjects**
  - Returns some or all (up to 1,000) of the objects in a bucket with each request
- **GetObject**
  - Retrieves an object from BOS In the GetObject request, specify the full key name for the object. General purpose buckets - Both the virtual-hosted-style requests and the path-style requests are supported

## Configuration
you can set configurations in `mcp_conf.py` file.


## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).


You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
npx @modelcontextprotocol/inspector uv --directory /Users/your path/mcp/src/bos_mcp_server run bos-mcp-server
```


Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.
