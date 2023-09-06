import React from 'react'
import { Accordion, Text } from '@global/ui'
import { AnalysisResultSummary } from '@page/AnalysisPage/api/entity'
import { AnalysisTypeLabel } from '../../../constant'

interface LoudnessSummaryResultItemProps {
  loudness: NonNullable<AnalysisResultSummary['loudness']>
}

/**
 * loudness 분석결과 요약 아이템
 */
const LoudnessSummaryResultItem: React.FC<LoudnessSummaryResultItemProps> = ({ loudness }) => {
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

          <Text weight="medium">{loudness.lkfs} LKFS</Text>
        </div>
      }
    />
  )
}

export default LoudnessSummaryResultItem
