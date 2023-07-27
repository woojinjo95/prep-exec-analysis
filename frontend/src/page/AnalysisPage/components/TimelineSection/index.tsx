import React from 'react'

import AreaChart from './components/AreaChart'

/**
 * 타임라인 차트 영역
 */
const TimelineSection: React.FC = () => {
  return (
    <section className="bg-black grid grid-cols-1 grid-rows-6 gap-y-2 p-2 text-white">
      <AreaChart />
    </section>
  )
}

export default TimelineSection
