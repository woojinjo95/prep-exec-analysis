type ApiName = 'analysis_config' | 'analysis_result_summary'

const apiUrls: {
  [key in ApiName]: string
} = {
  analysis_config: '/api/v1/analysis_config',
  analysis_result_summary: '/api/v1/analysis_result/summary',
}

export default apiUrls
