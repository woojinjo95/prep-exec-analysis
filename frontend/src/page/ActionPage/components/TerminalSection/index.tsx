import React from 'react'
import { Tabs } from '@global/ui'
import SettingsAndControlsPanel from './components/SettingsAndControlsPanel'
import TerminalPanel from './components/TerminalPanel'

/**
 * 터미널 영역
 */
const TerminalSection: React.FC = () => {
  return (
    <section className="col-span-2">
      <Tabs header={['Settings & Controls', 'Terminal']} className="py-3 px-6" colorScheme="dark">
        <SettingsAndControlsPanel />
        <TerminalPanel />
      </Tabs>
    </section>
  )
}

export default TerminalSection
