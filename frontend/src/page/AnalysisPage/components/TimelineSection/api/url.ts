type ApiName =
  | 'log_level_finder'
  | 'cpu_and_memory'
  | 'color_reference'
  | 'event_log'
  | 'video_analysis_result'
  | 'log_pattern_matching'
  | 'measurement'
  | 'process_lifecycle'
  | 'network_filter'

const apiUrls: {
  [key in ApiName]: string
} = {
  log_level_finder: '/api/v1/analysis_result/log_level_finder',
  cpu_and_memory: '/api/v1/analysis_result/cpu_and_memory',
  color_reference: '/api/v1/analysis_result/color_reference',
  event_log: '/api/v1/analysis_result/event_log',
  video_analysis_result: '/api/v1/analysis_result/video_analysis_result',
  log_pattern_matching: '/api/v1/analysis_result/log_pattern_matching',
  measurement: '/api/v1/analysis_result/measurement', // ???
  process_lifecycle: '/api/v1/analysis_result/process_lifecycle',
  network_filter: '/api/v1/analysis_result/network_filter',
}

export default apiUrls
