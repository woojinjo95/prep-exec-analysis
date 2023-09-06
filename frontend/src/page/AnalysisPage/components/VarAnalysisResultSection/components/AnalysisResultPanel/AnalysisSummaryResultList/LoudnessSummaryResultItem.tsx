import React from 'react'
import { Accordion, Text } from '@global/ui'
import { AnalysisTypeLabel } from '../../../constant'
import { AnalysisResultSummary } from '../../../api/entity'

interface LoudnessSummaryResultItemProps {
  result: NonNullable<AnalysisResultSummary['loudness']>[0]
}

/**
 * loudness 분석결과 요약 아이템
 */
const LoudnessSummaryResultItem: React.FC<LoudnessSummaryResultItemProps> = ({ result }) => {
  return (
    <Accordion
      header={
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-x-3">
            <div
              className="w-4 h-4"
              style={{
                // TODO:
                backgroundColor: 'white',
              }}
            />
            <Text size="sm" weight="medium">
              {AnalysisTypeLabel.loudness}
            </Text>
          </div>

          <Text weight="medium">{result.lkfs} LKFS</Text>
        </div>
      }
    />
  )
}

export default LoudnessSummaryResultItem
