type ApiName = 'video_snapshot'

const apiUrls: {
  [key in ApiName]: string
} = {
  video_snapshot: '/api/v1/analysis_result/file/video_snapshot',
}

export default apiUrls
