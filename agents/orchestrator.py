import asyncio
from agent_framework.orchestrations import SequentialBuilder
from azure.ai.projects import AIProjectClient

from agents.auditor import create_auditor_agent
from agents.compliance import create_compliance_agent
from agents.architect import create_architect_agent

# ANSI Terminal Colors for the UI
class Colors:
    RED = '\033[91m'       # For the Scout
    YELLOW = '\033[93m'    # For the Judge
    GREEN = '\033[92m'     # For the Architect
    BLUE = '\033[94m'      
    CYAN = '\033[96m'      
    RESET = '\033[0m'
    BOLD = '\033[1m'

class StitchWorkflow:
    def __init__(self, chat_client, project_client: AIProjectClient):
        self.chat_client = chat_client
        self.project_client = project_client
        self.auditor = None
        self.compliance = None
        self.architect = None

    async def initialize_agents(self):
        print(f"{Colors.BLUE}{Colors.BOLD}  Initializing Stitch Team...{Colors.RESET}")
        await asyncio.sleep(0.5) # Dramatic pause for the UI
        
        # Bypassing the broken Azure Agent SDK entirely. 
        # We are using the stable chat_client for everyone.
        self.auditor = create_auditor_agent(self.chat_client)
        self.compliance = create_compliance_agent(self.chat_client)
        self.architect = create_architect_agent(self.chat_client)
        
        print(f"{Colors.GREEN}{Colors.BOLD} Team Ready.{Colors.RESET}\n")
        await asyncio.sleep(0.5)

    async def run(self, target_file: str):
        if not self.compliance:
            await self.initialize_agents()

        workflow = SequentialBuilder(
            participants=[self.auditor, self.compliance, self.architect]
        ).build()
        
        #The "Hollywood" Agent Hand-off UI
        print(f"{Colors.CYAN}{Colors.BOLD}[Stitch] Commencing Security Lifecycle for: {target_file}{Colors.RESET}")
        print("-" * 50)
        await asyncio.sleep(1)
        
        # Scout is RED (Hunting for danger)
        print(f"{Colors.RED}{Colors.BOLD} [Stitch-Scout]{Colors.RESET} Scanning local code for vulnerabilities...")
        await asyncio.sleep(1)
        
        # Judge is YELLOW (Legal caution/Audit)
        print(f"{Colors.YELLOW}{Colors.BOLD}  [Stitch-Judge]{Colors.RESET} Evaluating data flow against POPIA & GDPR standards...")
        await asyncio.sleep(1)
        
        # Architect is GREEN (Secure and fixed)
        print(f"{Colors.GREEN}{Colors.BOLD}  [Stitch-Architect]{Colors.RESET} Drafting secure remediation patch...")
        print("-" * 50)
        
        print(f"{Colors.CYAN} Waiting for AI consensus (this may take a few seconds)...{Colors.RESET}\n")
        
        # THE HACKATHON SHORTCUT: Read the file here and force-feed it to the AI
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