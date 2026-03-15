from agent_framework import Agent

COMPLIANCE_INSTRUCTIONS = """
You are the 'Stitch-Judge', a specialized Compliance and Governance Agent.
Your expertise is in South African POPIA and international GDPR standards.

Your role:
1. Receive security reports from the 'Stitch-Auditor'.
2. Cite the relevant principles (e.g., Accountability, Section 19: Security Safeguards).
3. Assign a 'Risk Level' (Low, Medium, High, Critical).
"""

def create_compliance_agent(chat_client):
    return Agent(
        name="Stitch-Judge",
        client=chat_client,  # <-- CHANGED TO 'client'
        instructions=COMPLIANCE_INSTRUCTIONS,
        tools=[] 
    )