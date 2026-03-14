from agent_framework.azure import AzureOpenAIChatClient
from mcp_server.tools import read_local_file, check_azure_security_groups

# --- Specialist Instructions ---
AUDITOR_INSTRUCTIONS = """
You are the 'Stitch-Scout', a specialized Red Team Security Auditor.
You perform 'Static Analysis' on local code AND 'Live Analysis' on Azure infrastructure.

Your workflow:
1. Scan local code (e.g., main.py) using 'read_local_file' to find vulnerabilities.
2. If the code interacts with Azure, use 'check_azure_security_groups' to see if 
   the live infrastructure is exposed to the public internet.

Report code flaws and cloud misconfigurations together as a single 'Threat Intelligence' report.
Focus on South African PII leaks and common OWASP risks.
"""

def create_auditor_agent(client: AzureOpenAIChatClient):
    """
    Factory function to create the Auditor agent with dual tools:
    - read_local_file: For static code scanning.
    - check_azure_security_groups: For live infrastructure auditing.
    """
    return client.create_agent(
        name="Stitch-Auditor",
        instructions=AUDITOR_INSTRUCTIONS,
        tools=[read_local_file, check_azure_security_groups]
    )