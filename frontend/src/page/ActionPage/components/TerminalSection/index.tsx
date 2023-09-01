import React from 'react'
import { Tabs } from '@global/ui'
import { useServiceState } from '@global/api/hook'
import SettingsAndControlsPanel from './components/SettingsAndControlsPanel'
import TerminalPanel from './components/TerminalPanel/TerminalPanel'

/**
 * 터미널 영역
 */
const TerminalSection: React.FC = () => {
  const { serviceState } = useServiceState()
  return (
    <section className="col-span-2 relative">
      <Tabs header={['Settings & Controls', 'Terminal']} className="py-3 px-6" colorScheme="dark">
        <SettingsAndControlsPanel />
        <TerminalPanel />
      </Tabs>
      {serviceState === 'playblock' && (
        <div className="absolute top-0 left-0 w-full h-full z-10 bg-black opacity-[0.6]" />
      )}
    </section>
  )
}

export default TerminalSection
