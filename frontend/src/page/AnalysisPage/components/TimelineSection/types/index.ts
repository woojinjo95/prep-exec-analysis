import { AnalysisType } from '@global/constant'

/**
 * 분석 완료 메시지 data 부분
 */
export type AnalysisResponseMessageBody = {
  measurement: keyof typeof AnalysisType | 'color_reference'
}
