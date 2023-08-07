import React from 'react'

import RemoteControl from './RemoteControl'
import NetworkEmulation from './NetworkEmulation'
import DeviceInfo from './DeviceInfo'
import OnOffControl from './OnOffControl'

/**
 * Settings & Controls 탭의 패널
 */
const SettingsAndControlsPanel: React.FC = () => {
  return (
    <div className="grid grid-rows-[auto_1fr] grid-cols-[auto_1fr_1fr] gap-4 h-full overflow-y-auto px-5 !text-black">
      <RemoteControl />
      <NetworkEmulation />
      <DeviceInfo />
      <OnOffControl />
    </div>
  )
}

export default SettingsAndControlsPanel
