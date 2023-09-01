type ApiName = 'partial_video' | 'video'

const apiUrls: {
  [key in ApiName]: string
} = {
  partial_video: '/api/v1/analysis_result/file/partial_video',
  video: '/api/v1/analysis_result/file/video',
}

export default apiUrls
