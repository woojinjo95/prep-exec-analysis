type ApiName =
  | 'scenario'
  | 'hardware_configuration'
  | 'connect'
  | 'disconnect'
  | 'log_connection_status'
  | 'tag'
  | 'testrun'
  | 'copy_scenario'

const apiUrls: {
  [key in ApiName]: string
} = {
  scenario: '/api/v1/scenario',
  hardware_configuration: '/api/v1/hardware_configuration',
  connect: '/api/v1/shell/connect',
  disconnect: '/api/v1/shell/disconnect',
  log_connection_status: '/api/v1/log_connection_status',
  tag: '/api/v1/scenario/tag',
  testrun: '/api/v1/scenario/testrun',
  copy_scenario: '/api/v1/copy_scenario',
}

export default apiUrls
