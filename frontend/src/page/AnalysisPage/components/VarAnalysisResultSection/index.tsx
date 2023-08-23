import React from 'react'
import { Tabs } from '@global/ui'
import SetAnalysisItemPanel from './components/SetAnalysisItemPanel'
import AnalysisResultPanel from './components/AnalysisResultPanel'

/**
 * 분석변수 설정 및 결과 영역
 */
const VarAnalysisResultSection: React.FC = () => {
  return (
    <section className="border-l border-[#37383E] row-span-3 bg-black text-white">
      <Tabs header={['Set Analysis Items', 'Result']} colorScheme="dark" className="pl-5 pr-6 pt-3">
        <SetAnalysisItemPanel />
        <AnalysisResultPanel />
      </Tabs>
    </section>
  )
}

export default VarAnalysisResultSection
