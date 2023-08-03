import React from 'react'
import HLSPlayer from './components/HLSPlayer'

/**
 * 모니터 영역
 */
const MonitorSection: React.FC = () => {
  return (
    <section className="w-full h-full border border-black relative">
      <HLSPlayer
        autoPlay
        controls
        className="h-full aspect-video bg-black"
        src={import.meta.env.VITE_STREAMING_URL || `${window.location.protocol}//${window.location.hostname}:8888/live`}
      />
    </section>
  )
}

export default MonitorSection
