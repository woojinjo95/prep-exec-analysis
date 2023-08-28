type ApiName = 'scenario' | 'hardware_configuration' | 'connect' | 'disconnect'

const apiUrls: {
  [key in ApiName]: string
} = {
  scenario: '/api/v1/scenario',
  hardware_configuration: '/api/v1/hardware_configuration',
  connect: '/api/v1/shell/connect',
  disconnect: '/api/v1/shell/disconnect',
}

export default apiUrls
