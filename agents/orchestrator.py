import asyncio
from agent_framework.orchestrations import SequentialBuilder
from azure.ai.projects import AIProjectClient

from agents.auditor import create_auditor_agent
from agents.compliance import create_compliance_agent
from agents.architect import create_architect_agent

class StitchWorkflow:
    def __init__(self, chat_client, project_client: AIProjectClient):
        self.chat_client = chat_client
        self.project_client = project_client
        self.auditor = None
        self.compliance = None
        self.architect = None

    async def initialize_agents(self):
        print("Initializing Stitch Team...")
        
        # Bypassing the broken Azure Agent SDK entirely. 
        # We are using the stable chat_client for everyone.
        self.auditor = create_auditor_agent(self.chat_client)
        self.compliance = create_compliance_agent(self.chat_client)
        self.architect = create_architect_agent(self.chat_client)
        
        print("Team Ready.")

    async def run(self, target_file: str):
        if not self.compliance:
            await self.initialize_agents()

        workflow = SequentialBuilder(
            participants=[self.auditor, self.compliance, self.architect]
        ).build()
        
        print(f"[Stitch] Commencing Security Lifecycle for: {target_file}")
        
        # 🚀 THE HACKATHON SHORTCUT: Read the file here and force-feed it to the AI
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                code_content = f.read()
        except Exception as e:
            return f"Error reading file locally: {e}"

        initial_msg = (
            f"Security Audit Request: I need you to analyze the following code from '{target_file}':\n\n"
            f"```python\n{code_content}\n```\n\n"
            "Identify vulnerabilities, evaluate POPIA compliance risks, "
            "and propose a secure remediation patch."
        )
        
        response = await workflow.run(initial_msg)
        
        return response