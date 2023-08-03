import React from 'react'

const DeviceInfo: React.FC = () => {
  return (
    <div className="bg-white row-span-2">
      <h4>Device Info</h4>

      <select>
        <option>Type</option>
        <option>adb</option>
        <option>ssh</option>
      </select>
    </div>
  )
}

export default DeviceInfo
