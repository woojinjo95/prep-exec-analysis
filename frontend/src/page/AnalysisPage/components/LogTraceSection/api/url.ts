type ApiName = 'logcat' | 'network'

const apiUrls: {
  [key in ApiName]: string
} = {
  logcat: '/api/v1/trace/logcat',
  network: '/api/v1/trace/network',
}

export default apiUrls
