type ApiName = 'hardware_configuration' | 'connect' | 'disconnect'

const apiUrls: {
  [key in ApiName]: string
} = {
  hardware_configuration: '/api/v1/hardware_configuration',
  connect: '/api/v1/shell/connect',
  disconnect: '/api/v1/shell/disconnect',
}

export default apiUrls
