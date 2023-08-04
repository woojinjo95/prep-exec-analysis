type ApiName = 'remocon' | 'custom_key'

const apiUrls: {
  [key in ApiName]: string
} = {
  remocon: '/api/v1/remocon',
  custom_key: '/api/v1/remocon/custom_key',
}

export default apiUrls
