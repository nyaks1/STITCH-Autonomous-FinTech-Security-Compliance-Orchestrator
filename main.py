import asyncio
import os
from dotenv import load_dotenv

# Azure Identity & Foundry SDKs
from azure.identity.aio import DefaultAzureCredential
from azure.ai.projects.aio import AIProjectClient  # Async version
from agent_framework.azure import AzureOpenAIChatClient

# Stitch Orchestrator
from agents.orchestrator import StitchWorkflow

load_dotenv()

# ANSI Terminal Colors for the UI
class Colors:
    HEADER = '\033[95m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

async def main():
    print(f"\n{Colors.CYAN}{Colors.BOLD}..Stitch is waking up...{Colors.RESET}\n")
    
    # 1. Use the unified async credential
    async with DefaultAzureCredential() as credential:
        
        # 2. Local Chat Client (for Auditor & Architect)
        chat_client = AzureOpenAIChatClient(credential=credential)
        
        # 3. Foundry Project Client (for the Judge)
        # Ensure 'PROJECT_CONNECTION_STRING' is in your .env
        project_endpoint = os.getenv("PROJECT_CONNECTION_STRING")
        
        async with AIProjectClient(endpoint=project_endpoint, credential=credential) as project_client:
            
            # 4. Initialize the Stitch Workflow with both clients
            stitch = StitchWorkflow(chat_client, project_client)
            
            # 5. Run the security lifecycle on a target file
            target = "vulnerable_sample.py"
            result = await stitch.run(target)
            
            # The Beautiful Final UI
            print("\n" + f"{Colors.GREEN}{Colors.BOLD}================================================={Colors.RESET}")
            print(f"{Colors.GREEN}{Colors.BOLD}              FINAL STITCH REPORT                {Colors.RESET}")
            print(f"{Colors.GREEN}{Colors.BOLD}================================================={Colors.RESET}")
            print(f"{Colors.HEADER}FILE: {target}{Colors.RESET}")
            print("-" * 50)
            print(f"{Colors.CYAN}{Colors.BOLD}VERDICT & PATCH PLAN:\n{Colors.RESET}")
            
            def hunt_for_text(obj):
                found_texts = []
                if isinstance(obj, list):
                    for item in obj:
                        found_texts.extend(hunt_for_text(item))
                elif hasattr(obj, 'content') and isinstance(obj.content, str):
                    found_texts.append(obj.content)
                elif hasattr(obj, 'text') and isinstance(obj.text, str):
                    found_texts.append(obj.text)
                elif hasattr(obj, 'data'):
                    found_texts.extend(hunt_for_text(obj.data))
                return found_texts

            # Extract everything and grab the very last block of text (The Architect's patch)
            all_text = hunt_for_text(result)
            if all_text:
                print(all_text[-1])
            else:
                # Absolute last resort fallback
                print("Could not parse text natively. Raw object dump:")
                print(result)
                
            print("\n" + f"{Colors.GREEN}{Colors.BOLD}================================================={Colors.RESET}\n")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n\033[91m\033[1mStitch encountered an error: {e}\033[0m")