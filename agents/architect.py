from agent_framework import Agent

ARCHITECT_INSTRUCTIONS = """
You are the 'Stitch-Architect', a specialized Remediation Agent.
Your job is to receive the vulnerabilities and POPIA verdicts, and write secure code to fix them.
"""

def create_architect_agent(chat_client):
    return Agent(
        name="Stitch-Architect",
        client=chat_client,  # <-- CHANGED TO 'client'
        instructions=ARCHITECT_INSTRUCTIONS,
        tools=[]
    )