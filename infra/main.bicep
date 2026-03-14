targetScope = 'subscription'

param name string = 'stitch'
param location string = 'eastus2' // Recommended for latest GPT-4o models
param resourceGroupName string = 'rg-${name}'

resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: resourceGroupName
  location: location
}

module resources './resources.bicep' = {
  scope: rg
  name: 'stitch-resources'
  params: {
    name: name
    location: location
  }
}

output PROJECT_CONNECTION_STRING string = resources.outputs.projectConnectionString
output AZURE_OPENAI_ENDPOINT string = resources.outputs.openAiEndpoint