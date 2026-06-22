param location string
param name string
param tags object
param logAnalyticsCustomerId string
@secure()
param logAnalyticsSharedKey string

resource managedEnvironment 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsCustomerId
        sharedKey: logAnalyticsSharedKey
      }
    }
  }
}

output id string = managedEnvironment.id
output name string = managedEnvironment.name
