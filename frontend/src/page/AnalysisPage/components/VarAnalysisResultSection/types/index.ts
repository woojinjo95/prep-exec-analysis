import { AnalysisConfig } from '../api/entity'

/**
 * Analaysis(분석 시작) 버튼을 누르기 전 분석설정 UI 상태
 */
export interface UnsavedAnalysisConfig
  extends Pick<
    AnalysisConfig,
    'freeze' | 'loudness' | 'channel_change_time' | 'log_level_finder' | 'log_pattern_matching'
  > {
  resume?: Omit<NonNullable<AnalysisConfig['resume']>, 'frame'> & {
    frame?: NonNullable<AnalysisConfig['resume']>['frame']
  }
  boot?: Omit<NonNullable<AnalysisConfig['boot']>, 'frame'> & {
    frame?: NonNullable<AnalysisConfig['boot']>['frame']
  }
}
