import React from 'react'
import { useHardwareConfiguration } from '../../api/hook'

const RemoteControl: React.FC = () => {
  const { hardwareConfiguration } = useHardwareConfiguration()

  return (
    <div className="bg-white">
      <h4>Remote Control</h4>
      <button type="button">
        <input type="radio" readOnly checked={hardwareConfiguration?.remote_control_type === 'ir'} />
        <span className="mr-4">IR</span>
      </button>

      <button type="button">
        <input type="radio" readOnly checked={hardwareConfiguration?.remote_control_type === 'bluetooth'} />
        <span>Bluetooth</span>
      </button>
    </div>
  )
}

export default RemoteControl
