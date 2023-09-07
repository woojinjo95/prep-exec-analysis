import { AnalysisConfig } from '@page/AnalysisPage/api/entity'

/**
 * Analaysis(분석 시작) 버튼을 누르기 전 분석설정 UI 상태
 */
export interface UnsavedAnalysisConfig
  extends Pick<AnalysisConfig, 'loudness' | 'channel_change_time' | 'log_level_finder' | 'log_pattern_matching'> {
  // duration -> number로 변경 후 api call
  freeze?: Omit<NonNullable<AnalysisConfig['freeze']>, 'duration'> & { duration: string }
  resume?: Omit<NonNullable<AnalysisConfig['resume']>, 'frame'> & {
    frame?: NonNullable<AnalysisConfig['resume']>['frame']
  }
  boot?: Omit<NonNullable<AnalysisConfig['boot']>, 'frame'> & {
    frame?: NonNullable<AnalysisConfig['boot']>['frame']
  }
}
