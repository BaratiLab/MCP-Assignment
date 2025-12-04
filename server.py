from mcp.server.fastmcp import FastMCP

from tools import load_tools 

# Initialize FastMCP server
mcp_server = FastMCP("mcp-assignment")

def main():
    # Initialize and run the server
    load_tools(mcp_server)
    mcp_server.run(transport='stdio')

if __name__ == "__main__":
    main()

