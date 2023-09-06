import React, { useEffect, useState } from 'react'
import cx from 'classnames'
import { useNavigate } from 'react-router-dom'
import { AppURL } from '@global/constant'
import { Text } from '@global/ui'
import { useRecoilValue } from 'recoil'
import { isBlockRecordModeState } from '@global/atom'
import { useServiceState } from '@global/api/hook'
import { useWebsocket } from '@global/hook'
import HLSPlayer from './components/HLSPlayer'

/**
 * 모니터 영역
 */
const MonitorSection: React.FC = () => {
  const [isHovered, setIsHovered] = useState<boolean>(false)
  const navigate = useNavigate()

  const isBlockRecordMode = useRecoilValue(isBlockRecordModeState)

  const [isBorderVisible, setIsBorderVisible] = useState<boolean>(true)

  const { serviceState } = useServiceState()

  const { sendMessage } = useWebsocket()

  useEffect(() => {
    const timer = setInterval(() => {
      setIsBorderVisible((prev) => !prev)
    }, 2000)

    return () => {
      clearInterval(timer)
    }
  }, [])

  return (
    <section
      className={cx('w-full h-full relative aspect-video grid justify-center items-center bg-black', {
        'border-red border-l-4 border-t-4 border-r-4': isBlockRecordMode && isBorderVisible,
        'border-primary border-l-4 border-t-4 border-r-4': serviceState === 'playblock' && isBorderVisible,
      })}
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
          // analysis_mode message 전송 후 이동
          const date = new Date()
          const startDate = new Date(date)
          startDate.setMinutes(date.getMinutes() - 30)

          sendMessage({
            level: 'info',
            msg: 'analysis_mode_init',
            data: {
              start_time: startDate.getTime() / 1000,
              end_time: date.getTime() / 1000,
            },
          })
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
