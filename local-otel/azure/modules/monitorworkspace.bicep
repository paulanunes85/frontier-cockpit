param location string
param name string
param tags object

resource monitorWorkspace 'Microsoft.Monitor/accounts@2023-04-03' = {
  name: name
  location: location
  tags: tags
  properties: {}
}

output id string = monitorWorkspace.id
output name string = monitorWorkspace.name
