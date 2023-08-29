import React, { useState } from 'react'
import cx from 'classnames'
import { useNavigate } from 'react-router-dom'
import AppURL from '@global/constant/appURL'
import { Text } from '@global/ui'
import HLSPlayer from './components/HLSPlayer'

/**
 * 모니터 영역
 */
const MonitorSection: React.FC = () => {
  const [isHovered, setIsHovered] = useState<boolean>(false)
  const navigate = useNavigate()

  return (
    <section
      className="w-full h-full relative aspect-video grid justify-center items-center bg-black"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onLostPointerCapture={() => setIsHovered(false)}
    >
      <button
        className={cx(
          'absolute top-5 left-1/2 -translate-x-1/2 bg-white/80 rounded-full border-2 border-primary py-3 px-10 cursor-pointer z-10 transition-opacity',
          {
            'opacity-30': !isHovered,
            'opacity-100': isHovered,
          },
        )}
        type="button"
        onClick={() => {
          navigate('/analysis')
        }}
      >
        <Text weight="medium" colorScheme="dark">
          Analysis
        </Text>
      </button>

      <HLSPlayer autoPlay controls className="h-full aspect-video" src={AppURL.streamingURL} />
    </section>
  )
}

export default MonitorSection
