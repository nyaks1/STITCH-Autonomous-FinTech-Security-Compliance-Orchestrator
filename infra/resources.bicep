param name string
param location string

// Generate a unique suffix so your OpenAI endpoint is never taken
var uniqueSuffix = substring(uniqueString(resourceGroup().id), 0, 6)
var uniqueName = '${name}-${uniqueSuffix}'

// 1. Azure OpenAI Service
resource openAi 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: '${uniqueName}-openai'
  location: location
  kind: 'AIServices'
  sku: { name: 'S0' }
  properties: {
    customSubDomainName: '${uniqueName}-openai'
    publicNetworkAccess: 'Enabled'
  }
}

// 2. Deployment for GPT-4o
resource gpt4o 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = {
  parent: openAi
  name: 'gpt-4o'
  sku: { 
    name: 'Standard' // <-- Changed from GlobalStandard
    capacity: 5       // <-- Lowered to 5k Tokens Per Minute for the Free Tier
  }
  properties: {
    model: { format: 'OpenAI', name: 'gpt-4o', version: '2024-05-13' }
  }
}

// 3. Azure AI Search (For the Judge's Knowledge Base)
resource search 'Microsoft.Search/searchServices@2024-03-01-preview' = {
  name: '${uniqueName}-search'
  location: location
  sku: { name: 'basic' }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
  }
}

// 4. Foundry Hub
resource aiHub 'Microsoft.MachineLearningServices/workspaces@2024-01-01-preview' = {
  name: '${uniqueName}-hub'
  location: location
  kind: 'hub'
  identity: {
    type: 'SystemAssigned' // <-- This fixes the MSI error!
  }
  properties: { friendlyName: 'Stitch Hub' }
}

// 5. Foundry Project
resource aiProject 'Microsoft.MachineLearningServices/workspaces@2024-01-01-preview' = {
  name: '${uniqueName}-project'
  location: location
  kind: 'project'
  identity: {
    type: 'SystemAssigned' // <-- This fixes the MSI error!
  }
  properties: {
    hubResourceId: aiHub.id
    friendlyName: 'Stitch Security Project'
  }
}

output projectConnectionString string = '${aiProject.properties.discoveryUrl}/api/projects/${aiProject.name}'
output openAiEndpoint string = openAi.properties.endpoint
