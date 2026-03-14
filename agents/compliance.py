import os
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import FileSearchTool, ToolSet

# Specialist Instructions
COMPLIANCE_INSTRUCTIONS = """
You are the 'Stitch-Judge', a specialized Compliance and Governance Agent.
Your expertise is in South African POPIA (Protection of Personal Information Act) 
and international GDPR standards.

Your role:
1. Receive security reports from the 'Stitch-Auditor'.
2. Use the 'file_search' tool to find specific legal clauses in the POPIA/GDPR knowledge base.
3. Cite the relevant principles (e.g., Accountability, Section 19: Security Safeguards).
4. Assign a 'Risk Level' (Low, Medium, High, Critical) based on potential regulatory impact.

Provide the 'Business Reason' for remediation to the 'Stitch-Architect'.
"""

async def create_compliance_agent(project_client: AIProjectClient):
    """
    Creates the 'Stitch-Judge' using the Foundry Agent Service.
    This version includes the FileSearchTool for legal grounding.
    """
    
    # 1. Setup the Knowledge Base (File Search)
    # Ensure FOUNDRY_VECTOR_STORE_ID is in your .env after uploading your laws
    vector_store_id = os.getenv("FOUNDRY_VECTOR_STORE_ID")
    
    if vector_store_id:
        file_search_tool = FileSearchTool(vector_store_ids=[vector_store_id])
        toolset = ToolSet()
        toolset.add(file_search_tool)
    else:
        print("Warning!!: No Vector Store ID found. Judge will rely on general knowledge.")
        toolset = None

    # 2. Create the Agent on the Foundry Service
    return await project_client.agents.create_agent(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        name="Stitch-Judge",
        instructions=COMPLIANCE_INSTRUCTIONS,
        toolset=toolset
    )