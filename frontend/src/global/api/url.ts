type ApiName = 'scenario' | 'hardware_configuration'

const apiUrls: {
  [key in ApiName]: string
} = {
  scenario: '/api/v1/scenario',
  hardware_configuration: '/api/v1/hardware_configuration',
}

export default apiUrls
