type ApiName = 'service_state'

const apiUrls: {
  [key in ApiName]: string
} = {
  service_state: '/api/v1/service_state',
}

export default apiUrls
