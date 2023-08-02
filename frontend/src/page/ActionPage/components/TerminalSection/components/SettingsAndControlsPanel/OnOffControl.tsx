import React from 'react'
import { ToggleButton } from '@global/ui'

const OnOffControl: React.FC = () => {
  return (
    <div className="bg-white h-fit">
      <h4>On/Off Control</h4>

      <ul>
        <li>
          <span>DUT Power</span>
          <ToggleButton isOn />
        </li>
        <li>
          <span>HDMI(HPD)</span>
          <ToggleButton isOn />
        </li>
        <li>
          <span>DUT WAN</span>
          <ToggleButton isOn />
        </li>
      </ul>
    </div>
  )
}

export default OnOffControl
