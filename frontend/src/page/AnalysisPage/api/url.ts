type ApiName = 'partial_video' | 'video' | 'analysis_config' | 'analysis_result_summary'

const apiUrls: {
  [key in ApiName]: string
} = {
  partial_video: '/api/v1/analysis_result/file/partial_video',
  video: '/api/v1/analysis_result/file/video',
  analysis_config: '/api/v1/analysis_config',
  analysis_result_summary: '/api/v1/analysis_result/summary',
}

export default apiUrls
