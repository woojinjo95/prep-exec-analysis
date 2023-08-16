import React from 'react'
import AppURL from '@global/constant/appURL'
import HLSPlayer from './components/HLSPlayer'

/**
 * 모니터 영역
 */
const MonitorSection: React.FC = () => {
  return (
    <section className="w-full h-full border-b border-light-charcoal relative aspect-video grid justify-center items-center bg-black">
      <HLSPlayer autoPlay controls className="h-full aspect-video" src={AppURL.streamingURL} />
    </section>
  )
}

export default MonitorSection
