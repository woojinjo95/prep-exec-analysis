import React from 'react'
import FreezeSummaryResultItem from './FreezeSummaryResultItem'

/**
 * 분석 결과(요약 데이터) 리스트
 */
const AnalysisSummaryResultList: React.FC = () => {
  return (
    <div className="overflow-y-auto flex flex-col gap-y-1">
      <FreezeSummaryResultItem />
    </div>
  )
}

export default AnalysisSummaryResultList
