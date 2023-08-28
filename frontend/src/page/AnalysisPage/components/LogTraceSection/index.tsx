import { Tabs } from '@global/ui'
import React from 'react'
import LogcatTrace from './components/LogcatTrace'
import NetworkTrace from './components/NetworkTrace'

/**
 * 로그 추적 영역
 */
const LogTraceSection: React.FC = () => {
  return (
    <section className="border-t border-b border-[#37383E] bg-black text-white">
      <Tabs header={['Logcat Trace', 'Network Trace']} colorScheme="dark" className="pl-5 pr-1 py-1">
        <LogcatTrace />
        <NetworkTrace />
      </Tabs>
    </section>
  )
}

export default LogTraceSection
