import React from 'react'
import { Accordion, Text } from '@global/ui'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import { dropDecimalPoint } from '@global/usecase'
import { AnalysisTypeLabel } from '@global/constant'

interface LoudnessSummaryItemProps {
  loudness: NonNullable<AnalysisResultSummary['loudness']>
}

/**
 * loudness 분석결과 요약 아이템
 */
const LoudnessSummaryItem: React.FC<LoudnessSummaryItemProps> = ({ loudness }) => {
  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-x-3">
            <div
              className="w-4 h-4"
              style={{
                backgroundColor: loudness.color,
              }}
            />
            <Text size="sm" weight="medium">
              {AnalysisTypeLabel.loudness}
            </Text>
          </div>

          <Text size="sm" weight="medium">
            {dropDecimalPoint(loudness.lkfs)} LKFS
          </Text>
        </div>
      }
    />
  )
}

export default LoudnessSummaryItem
