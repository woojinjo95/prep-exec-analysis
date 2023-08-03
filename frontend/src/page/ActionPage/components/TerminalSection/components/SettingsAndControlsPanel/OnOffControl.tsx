import React from 'react'
import { ToggleButton } from '@global/ui'
import { useHardwareConfiguration } from '../../api/hook'

const OnOffControl: React.FC = () => {
  const { hardwareConfiguration } = useHardwareConfiguration()

  return (
    <div className="bg-white h-fit">
      <h4>On/Off Control</h4>

      <ul>
        <li>
          <span>DUT Power</span>
          <ToggleButton isOn={!!hardwareConfiguration?.enable_dut_power} />
        </li>
        <li>
          <span>HDMI(HPD)</span>
          <ToggleButton isOn={!!hardwareConfiguration?.enable_hdmi} />
        </li>
        <li>
          <span>DUT WAN</span>
          <ToggleButton isOn={!!hardwareConfiguration?.enable_dut_wan} />
        </li>
      </ul>
    </div>
  )
}

export default OnOffControl
