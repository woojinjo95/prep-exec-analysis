import React, { useState } from 'react'
import { AnalysisTypeLabel } from '../../constant'
import Header from './Header'
import AnalysisItemList from './AnalysisItemList'

/**
 * 분석 아이템 설정 패널
 */
const SetAnalysisItemPanel: React.FC = () => {
  const [selectedAnalysisItems, setSelectedAnalysisItems] = useState<(keyof typeof AnalysisTypeLabel)[]>([])

  return (
    <div className="grid grid-cols-1 grid-rows-[auto_1fr] gap-y-2 h-full">
      <Header selectedAnalysisItems={selectedAnalysisItems} setSelectedAnalysisItems={setSelectedAnalysisItems} />
      <AnalysisItemList
        selectedAnalysisItems={selectedAnalysisItems}
        setSelectedAnalysisItems={setSelectedAnalysisItems}
      />
    </div>
  )
}

export default SetAnalysisItemPanel
