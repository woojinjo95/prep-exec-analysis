import React from 'react'
import { Tabs } from '@global/ui'
import LogcatTrace from './components/LogcatTrace'
import NetworkTrace from './components/NetworkTrace'
import { useShells } from './api/hook'
import ShellLog from './components/ShellLog'

/**
 * 로그 추적 영역
 */
const LogTraceSection: React.FC = () => {
  const { shells } = useShells()

  return (
    <section className="border-t border-b border-[#37383E] bg-black text-white">
      <Tabs
        header={['Logcat Trace', 'Network Trace', ...(shells?.map(({ mode }) => mode) || [])]}
        colorScheme="dark"
        className="pl-5 pr-1 py-1 !gap-y-2"
      >
        <LogcatTrace />
        <NetworkTrace />
        {shells?.map(({ mode }, index) => <ShellLog key={`shell-logs-${mode}-${index}`} shell_mode={mode} />)}
      </Tabs>
    </section>
  )
}

export default LogTraceSection
