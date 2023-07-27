import React from 'react'

import AreaChart from './components/AreaChart'

/**
 * 타임라인 차트 영역
 */
const TimelineSection: React.FC = () => {
  return (
    <section className="h-full bg-black grid grid-cols-1 grid-rows-[auto_1fr_auto] gap-1 p-1">
      <div className="text-white">time</div>

      <div className="grid grid-cols-1 gap-y-2 p-1 overflow-y-auto">
        <AreaChart />
        <AreaChart />
        <AreaChart />
        <AreaChart />
        <AreaChart />
        <AreaChart />
      </div>

      <div className="text-white">scroll</div>
    </section>
  )
}

export default TimelineSection
