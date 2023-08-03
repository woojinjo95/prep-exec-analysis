import React from 'react'

const RemoteControl: React.FC = () => {
  return (
    <div className="bg-white">
      <h4>Remote Control</h4>
      <button type="button" className="mr-4">
        IR
      </button>
      <button type="button">Bluetooth</button>
    </div>
  )
}

export default RemoteControl
