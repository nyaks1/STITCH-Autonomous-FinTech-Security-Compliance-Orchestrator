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

async def main():
    print("..Stitch is waking up...")
    
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
            # Target 'main.py' to let Stitch audit its own structure!
            target = "vulnerable_sample.py"
            result = await stitch.run(target)
            
            print("\n" + "="*30)
            print("FINAL STITCH REPORT")
            print("="*30)
            print(f"FILE: {target}")
            print("-" * 30)
            print("VERDICT & PATCH PLAN:\n")
           
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
                
            print("\n" + "="*30)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Stitch encountered an error: {e}")