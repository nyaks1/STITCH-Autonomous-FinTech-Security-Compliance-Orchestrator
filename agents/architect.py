from agent_framework.azure import AzureOpenAIChatClient
from mcp_server.tools import read_local_file # Architect needs to see the code to fix it

# --- Specialist Instructions ---
ARCHITECT_INSTRUCTIONS = """
You are the 'Stitch-Architect', a specialized DevOps and Software Engineer.
Your role is to fix security and compliance issues identified by the 'Stitch-Scout' 
and 'Stitch-Judge'.

Your goals:
1. Receive a technical audit and a compliance verdict.
2. Propose a specific, high-quality code fix that resolves the vulnerability 
   WITHOUT breaking the existing logic of the application.
3. Use 'GitHub Copilot Agent Mode' patterns to prepare a summary for a Pull Request.
4. Ensure the fix follows best practices for the language (Python/Dart/Rust).

Focus on 'Secure by Design' principles. Your output should be the exact code 
diff needed to patch the file.
"""

def create_architect_agent(client: AzureOpenAIChatClient):
    """
    Factory function to create the Architect agent.
    """
    # Note: In a full deployment, we would add a 'write_file' tool here 
    # to allow the agent to actually apply the fix.
    return client.create_agent(
        name="Stitch-Architect",
        instructions=ARCHITECT_INSTRUCTIONS,
        tools=[read_local_file]
    )