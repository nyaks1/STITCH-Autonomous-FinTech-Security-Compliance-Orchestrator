param name string
param location string

// 1. Azure OpenAI Service
resource openAi 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: '${name}-openai'
  location: location
  kind: 'AIServices'
  sku: { name: 'S0' }
  properties: {
    customSubDomainName: '${name}-openai'
    publicNetworkAccess: 'Enabled'
  }
}

// 2. Deployment for GPT-4o
resource gpt4o 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = {
  parent: openAi
  name: 'gpt-4o'
  sku: { name: 'GlobalStandard', capacity: 10 }
  properties: {
    model: { format: 'OpenAI', name: 'gpt-4o', version: '2024-05-13' }
  }
}

// 3. Azure AI Search (For the Judge's Knowledge Base)
resource search 'Microsoft.Search/searchServices@2024-03-01-preview' = {
  name: '${name}-search'
  location: location
  sku: { name: 'basic' }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
  }
}

// 4. Foundry Hub & Project
resource aiHub 'Microsoft.MachineLearningServices/workspaces@2024-01-01-preview' = {
  name: '${name}-hub'
  location: location
  kind: 'hub'
  properties: { friendlyName: 'Stitch Hub' }
}

resource aiProject 'Microsoft.MachineLearningServices/workspaces@2024-01-01-preview' = {
  name: '${name}-project'
  location: location
  kind: 'project'
  properties: {
    hubResourceId: aiHub.id
    friendlyName: 'Stitch Security Project'
  }
}

output projectConnectionString string = '${aiProject.properties.discoveryUrl}/api/projects/${aiProject.name}'
output openAiEndpoint string = openAi.properties.endpoint