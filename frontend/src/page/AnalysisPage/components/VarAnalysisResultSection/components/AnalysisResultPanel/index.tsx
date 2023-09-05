import React from 'react'
import { Text } from '@global/ui'
import AnalysisSummaryResultList from './AnalysisSummaryResultList'

/**
 * 분석 결과(요약 데이터) 패널
 */
const AnalysisResultPanel: React.FC = () => {
  return (
    <div className="grid grid-cols-1 grid-rows-[auto_1fr] gap-y-2 h-full">
      {/* FIXME: 어떻게 알 수 있는지? */}
      <Text>Last Update : </Text>

      <AnalysisSummaryResultList />
    </div>
  )
}

export default AnalysisResultPanel
