param location string
param name string
param tags object
param resourceGroupId string
param azureMonitorWorkspaceId string

resource grafana 'Microsoft.Dashboard/grafana@2023-09-01' = {
  name: name
  location: location
  tags: tags
  sku: {
    name: 'Standard'
  }
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    publicNetworkAccess: 'Enabled'
    apiKey: 'Enabled'
    deterministicOutboundIP: 'Disabled'
    zoneRedundancy: 'Disabled'
    grafanaIntegrations: {
      azureMonitorWorkspaceIntegrations: [
        {
          azureMonitorWorkspaceResourceId: azureMonitorWorkspaceId
        }
      ]
    }
  }
}

resource monitoringReaderRole 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(resourceGroupId, grafana.id, 'monitoring-reader')
  properties: {
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '43d0d8ad-25c7-4714-9337-8ba259a9fe05')
    principalId: grafana.identity.principalId
    principalType: 'ServicePrincipal'
  }
}

output id string = grafana.id
output name string = grafana.name
output endpoint string = grafana.properties.endpoint
output principalId string = grafana.identity.principalId
