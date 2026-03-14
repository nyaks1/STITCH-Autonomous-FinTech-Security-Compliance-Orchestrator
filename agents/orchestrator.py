import asyncio
from agent_framework.orchestrations import SequentialBuilder
from azure.ai.projects import AIProjectClient
from azure.identity.aio import DefaultAzureCredential

# Import our specialized agent factories
from agents.auditor import create_auditor_agent
from agents.compliance import create_compliance_agent
from agents.architect import create_architect_agent

class StitchWorkflow:
    def __init__(self, chat_client, project_client: AIProjectClient):
        self.chat_client = chat_client
        self.project_client = project_client
        
        # We define them as None first because Compliance is async
        self.auditor = None
        self.compliance = None
        self.architect = None

    async def initialize_agents(self):
        """Initializes the team. Required because Foundry agents are async."""
        print("🏗️  Initializing Stitch Team...")
        
        # 1. Local Agent (Auditor)
        self.auditor = create_auditor_agent(self.chat_client)
        
        # 2. Foundry Agent (Judge - This is the async one!)
        self.compliance = await create_compliance_agent(self.project_client)
        
        # 3. Local Agent (Architect)
        self.architect = create_architect_agent(self.chat_client)
        print("✅ Team Ready.")

    async def run(self, target_file: str):
        # Ensure agents are initialized
        if not self.compliance:
            await self.initialize_agents()

        # 🧵 Building the 2026 Sequential Workflow
        # This patterns automatically passes the 'Audit Report' to the 'Judge'
        # and the 'Judge's Verdict' to the 'Architect'.
        workflow = (
            SequentialBuilder()
            .add_participant(self.auditor)
            .add_participant(self.compliance)
            .add_participant(self.architect)
            .build()
        )

        # Create a session for state persistence
        session = await workflow.create_session()
        
        print(f"[Stitch] Commencing Security Lifecycle for: {target_file}")
        
        # The initial prompt that kicks off the chain reaction
        initial_msg = (
            f"Security Audit Request: Scan the local file '{target_file}'. "
            "Identify vulnerabilities, evaluate POPIA compliance risks, "
            "and propose a secure remediation patch."
        )
        
        # Execute the workflow
        response = await workflow.run(initial_msg, session=session)
        
        return response