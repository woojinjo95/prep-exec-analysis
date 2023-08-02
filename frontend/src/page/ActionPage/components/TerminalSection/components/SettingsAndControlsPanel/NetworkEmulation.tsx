import React from 'react'
import { Input, ToggleButton } from '@global/ui'

const NetworkEmulation: React.FC = () => {
  return (
    <div className="bg-white row-span-2">
      <div>
        <h4>Network Emulation</h4>
        <ToggleButton isOn />
      </div>

      <div className="grid grid-cols-3 grid-rows-[auto_1fr] gap-2">
        <div className="col-span-3">
          <h6>Packet Contorl (Inbound)</h6>
        </div>
        <div>
          <p>Bandwidth</p>
          <Input />
        </div>
        <div>
          <p>Delay</p>
          <Input />
        </div>
        <div>
          <p>Loss</p>
          <Input />
        </div>
      </div>

      <div>
        <h6>Configuring IP Limit</h6>
        <div className="grid grid-cols-[80%_20%]">
          <div className="grid grid-cols-[45%_20%_30%] gap-x-1">
            <Input placeholder="IP" />
            <Input placeholder="Port" />
            <Input placeholder="All" />
          </div>
          <div>
            <button type="button">delete</button>
          </div>
        </div>

        <button type="button">Add Item</button>
      </div>
    </div>
  )
}

export default NetworkEmulation
