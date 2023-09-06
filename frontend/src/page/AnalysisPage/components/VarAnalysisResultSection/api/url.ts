type ApiName = 'analysis_config' | 'analysis_result_summary' | 'validate_regex'

const apiUrls: {
  [key in ApiName]: string
} = {
  analysis_config: '/api/v1/analysis_config',
  analysis_result_summary: '/api/v1/analysis_result/summary',
  validate_regex: '/api/v1/validate_regex',
}

export default apiUrls
