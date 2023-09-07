type ApiName = 'analysis_config' | 'validate_regex'

const apiUrls: {
  [key in ApiName]: string
} = {
  analysis_config: '/api/v1/analysis_config',
  validate_regex: '/api/v1/validate_regex',
}

export default apiUrls
