import React from 'react'
import { Accordion, Text } from '@global/ui'
import { AnalysisTypeLabel } from '../../../constant'

/**
 * loudness 분석결과 요약 아이템
 */
const LoudnessSummaryResultItem: React.FC = () => {
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

          <Text weight="medium">- 24 LKFS</Text>
        </div>
      }
    />
  )
}

export default LoudnessSummaryResultItem
