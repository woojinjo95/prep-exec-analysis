import React from 'react'
import { Tabs } from '@global/ui'

/**
 * 결과영상 및 정보 영역
 */
const VideoDetailSection: React.FC = () => {
  return (
    <section className="bg-black text-white">
      <Tabs header={['Video']} colorScheme="dark" className="px-5 pb-5 pt-2">
        <div />
      </Tabs>
    </section>
  )
}

export default VideoDetailSection
