import React from 'react'

import ScrollComponent from '@global/ui/ScrollComponent'
import RemoteControl from './RemoteControl'
import NetworkEmulation from './NetworkEmulation'
import DeviceInfo from './DeviceInfo'
import OnOffControl from './OnOffControl'

/**
 * Settings & Controls 탭의 패널
 */
const SettingsAndControlsPanel: React.FC = () => {
  return (
    <ScrollComponent>
      <div className="grid grid-rows-[auto_1fr] grid-cols-[auto_1.5fr_1fr] gap-4 h-full !text-black">
        <RemoteControl />
        <NetworkEmulation />
        <DeviceInfo />
        <OnOffControl />
      </div>
    </ScrollComponent>
  )
}

export default SettingsAndControlsPanel
