from mcp.server.fastmcp import FastMCP
import os

# Initialize the MCP Server
mcp = FastMCP("Stitch-Core-Tools")

@mcp.tool()
async def read_local_file(file_path: str) -> str:
    """
    Reads a file from the local repository. 
    Used by agents to audit code for security risks.
    """
    try:
        # Security Guardrail: Prevent directory traversal
        base_path = os.getcwd()
        full_path = os.path.normpath(os.path.join(base_path, file_path))
        
        if not full_path.startswith(base_path):
            return "Error: Access denied. Path is outside of project scope."
            
        if not os.path.exists(full_path):
            return f"Error: File '{file_path}' not found."

        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

# You can add more tools here later, like 'scan_directory' or 'check_env_vars'

if __name__ == "__main__":
    mcp.run()