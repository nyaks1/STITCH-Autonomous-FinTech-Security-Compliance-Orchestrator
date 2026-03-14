import os
from azure.mgmt.network import NetworkManagementClient
from azure.identity.aio import DefaultAzureCredential
from agent_framework import tool

@tool
async def check_azure_security_groups(resource_group: str) -> str:
    """
    Scans Azure Network Security Groups (NSGs) in a resource group 
    to find any rules that allow public internet access (Port 80/443/22/3389).
    """
    async with DefaultAzureCredential() as credential:
        network_client = NetworkManagementClient(credential, os.getenv("AZURE_SUBSCRIPTION_ID"))
        
        risks = []
        async for nsg in network_client.network_security_groups.list(resource_group):
            for rule in nsg.security_rules:
                if rule.access == "Allow" and rule.source_address_prefix in ["*", "0.0.0.0/0", "Internet"]:
                    risks.append(f"NSG: {nsg.name} | Rule: {rule.name} | Port: {rule.destination_port_range} is OPEN TO INTERNET")
        
        return "\n".join(risks) if risks else "No immediate public NSG risks found."