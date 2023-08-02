import React from 'react'
import RemoteControl from './RemoteControl'
import NetworkEmulation from './NetworkEmulation'
import DeviceInfo from './DeviceInfo'
import OnOffControl from './OnOffControl'
import { useHardwareConfiguration } from '../../api/hook'

/**
 * Settings & Controls 탭의 패널
 */
const SettingsAndControlsPanel: React.FC = () => {
  const { hardwareConfiguration } = useHardwareConfiguration()

  return (
    <div className="grid grid-rows-2 grid-cols-3 gap-4 h-full overflow-y-auto px-5">
      <RemoteControl />
      <NetworkEmulation />
      <DeviceInfo />
      <OnOffControl />
    </div>
  )
}

export default SettingsAndControlsPanel
