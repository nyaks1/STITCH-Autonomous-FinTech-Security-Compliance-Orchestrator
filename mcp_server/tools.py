import os

def read_local_file(file_path: str) -> str:
    """Reads the content of a local file for the agent to audit."""
    try:
        if not os.path.exists(file_path):
            return f"Error: File '{file_path}' not found."
            
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"

def check_azure_security_groups(resource_group: str = "rg-stitch") -> str:
    """Checks Azure Network Security Groups for compliance."""
    # We are mocking this specific check for the hackathon demo
    # so we don't need a massive Azure Python SDK setup tonight.
    return "NSG Audit: Port 22 (SSH) is closed. Port 443 (HTTPS) is open. Compliant."