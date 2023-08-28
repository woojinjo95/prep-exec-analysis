import { AnalysisConfig } from '../api/entity'

/**
 * Analaysis(분석 시작) 버튼을 누르기 전 분석설정 UI 상태
 */
export interface UnsavedAnalysisConfig {
  freeze?: Partial<AnalysisConfig['freeze']>
  resume?: Partial<AnalysisConfig['resume']>
  boot?: Partial<AnalysisConfig['boot']>
  channel_change_time?: Partial<AnalysisConfig['channel_change_time']>
  log_level_finder?: Partial<AnalysisConfig['log_level_finder']>
  log_pattern_matching?: Partial<AnalysisConfig['log_pattern_matching']>
}
