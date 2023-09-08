type ApiName =
  | 'partial_video'
  | 'video'
  | 'analysis_config'
  | 'analysis_result_summary'
  | 'log_level_finder'
  | 'cpu'
  | 'memory'
  | 'color_reference'
  | 'event_log'
  | 'freeze'
  | 'log_pattern_matching'
  | 'measurement'
  | 'process_lifecycle'
  | 'network_filter'
  | 'loudness'
  | 'resume'
  | 'boot'

const apiUrls: {
  [key in ApiName]: string
} = {
  partial_video: '/api/v1/analysis_result/file/partial_video',
  video: '/api/v1/analysis_result/file/video',
  analysis_config: '/api/v1/analysis_config',
  analysis_result_summary: '/api/v1/analysis_result/summary',
  log_level_finder: '/api/v1/analysis_result/log_level_finder',
  cpu: '/api/v1/analysis_result/cpu',
  memory: '/api/v1/analysis_result/memory',
  color_reference: '/api/v1/analysis_result/color_reference',
  event_log: '/api/v1/analysis_result/event_log',
  freeze: '/api/v1/analysis_result/freeze',
  log_pattern_matching: '/api/v1/analysis_result/log_pattern_matching',
  measurement: '/api/v1/analysis_result/measurement', // ???
  process_lifecycle: '/api/v1/analysis_result/process_lifecycle',
  network_filter: '/api/v1/analysis_result/network_filter',
  loudness: '/api/v1/analysis_result/loudness',
  resume: '/api/v1/analysis_result/resume',
  boot: '/api/v1/analysis_result/boot',
}

export default apiUrls
