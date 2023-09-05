type ApiName = 'logcat' | 'network' | 'shell' | 'shell_log'

const apiUrls: {
  [key in ApiName]: string
} = {
  logcat: '/api/v1/trace/logcat',
  network: '/api/v1/trace/network',
  shell: '/api/v1/shell',
  shell_log: '/api/v1/shell/logs',
}

export default apiUrls
