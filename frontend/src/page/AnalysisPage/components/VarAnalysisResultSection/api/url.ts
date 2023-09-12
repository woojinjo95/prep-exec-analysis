type ApiName = 'analysis_config' | 'analysis' | 'validate_regex'

const apiUrls: {
  [key in ApiName]: string
} = {
  analysis_config: '/api/v1/analysis_config',
  analysis: '/api/v1/analysis',
  validate_regex: '/api/v1/validate_regex',
}

export default apiUrls
