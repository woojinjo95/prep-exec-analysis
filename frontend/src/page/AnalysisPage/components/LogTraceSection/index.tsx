import { Tabs } from '@global/ui'
import React from 'react'

/**
 * 로그 추적 영역
 */
const LogTraceSection: React.FC = () => {
  return (
    <section className="border-t border-b border-[#37383E] bg-black text-white">
      <Tabs header={['Logcat Trace', 'Network Trace']} theme="dark" className="pl-5 pr-1 py-1">
        <div />
      </Tabs>
    </section>
  )
}

export default LogTraceSection
