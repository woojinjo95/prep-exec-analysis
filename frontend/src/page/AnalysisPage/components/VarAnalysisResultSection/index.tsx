import React from 'react'
import { Tabs } from '@global/ui'
import SetROIButton from './SetROIButton'

/**
 * 분석변수 설정 및 결과 영역
 */
const VarAnalysisResultSection: React.FC = () => {
  return (
    <section className="border-l border-[#37383E] row-span-3 bg-black text-white">
      <Tabs header={['Var/Analysis Results']} theme="dark" className="pl-5 pr-1 py-1">
        <div>
          <SetROIButton />
        </div>
      </Tabs>
    </section>
  )
}

export default VarAnalysisResultSection
