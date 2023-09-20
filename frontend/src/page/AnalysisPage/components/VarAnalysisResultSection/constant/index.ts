import { BootType, ResumeType } from '@global/api/entity'
import { FreezeType } from '@global/constant'

/**
 * AnalysisType - Resume의 Type 항목 라벨
 */
export const ResumeTypeLabel: { [key in ResumeType]: string } = {
  image_matching: 'Image Matching',
  screen_change_rate: 'Screen Change Rate',
} as const

/**
 * AnalysisType - Boot의 Type 항목 라벨
 */
export const BootTypeLabel: { [key in BootType]: string } = {
  image_matching: 'Image Matching',
} as const

/**
 * AnalysisType - Freeze의 Target 항목 라벨
 */
export const FreezeTypeLabel: { [key in keyof typeof FreezeType]: string } = {
  black: 'Black',
  default: 'Default',
  no_signal: 'No signal',
  one_colored: 'One colored',
  white: 'White',
}
