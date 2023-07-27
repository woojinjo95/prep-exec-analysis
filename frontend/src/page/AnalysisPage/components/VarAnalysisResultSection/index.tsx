import React from 'react'
import SetROIButton from './SetROIButton'

/**
 * 분석변수 설정 및 결과 영역
 */
const VarAnalysisResultSection: React.FC = () => {
  return (
    <section className="border-l border-[#37383E] row-span-3 bg-black text-white">
      VarAnalysisResultSection
      <SetROIButton />
    </section>
  )
}

export default VarAnalysisResultSection
