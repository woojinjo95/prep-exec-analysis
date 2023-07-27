import React from 'react'

import AreaChart from './components/AreaChart'

/**
 * 타임라인 차트 영역
 */
const TimelineSection: React.FC = () => {
  return (
    <section className="border border-black col-span-2 grid grid-cols-1 grid-rows-6 gap-y-2 p-2">
      <AreaChart />
    </section>
  )
}

export default TimelineSection
