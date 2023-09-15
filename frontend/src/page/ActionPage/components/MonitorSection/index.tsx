import React, { useEffect, useState } from 'react'
import cx from 'classnames'
import { useNavigate } from 'react-router-dom'
import { AppURL } from '@global/constant'
import { Text } from '@global/ui'
import { useRecoilValue } from 'recoil'
import { isBlockRecordModeState, scenarioIdState } from '@global/atom'
import { useScenarioById, useServiceState } from '@global/api/hook'
import { useWebsocket } from '@global/hook'
import { ReactComponent as AnalysisIcon } from '@assets/images/icon_analysis.svg'
import HLSPlayer from './components/HLSPlayer'
import SaveBlocksModal from '../ActionSection/components/SaveBlocksModal'
import { LKFSPlayload } from './type'
import SoundBar from './components/SoundBar'

/**
 * 모니터 영역
 */
const MonitorSection: React.FC = () => {
  const [isHovered, setIsHovered] = useState<boolean>(false)
  const navigate = useNavigate()

  const isBlockRecordMode = useRecoilValue(isBlockRecordModeState)

  const [isBorderVisible, setIsBorderVisible] = useState<boolean>(true)

  const { serviceState } = useServiceState()

  const [lkfsPayload, setLkfsPayload] = useState<LKFSPlayload | null>(null)

  const { sendMessage } = useWebsocket({
    onMessage: (msg) => {
      // lkfs 관련 msg
      if (msg.service === 'media' && msg.I && msg.M) {
        setLkfsPayload({ I: msg.I, M: msg.M })
      }
    },
  })

  const scenarioId = useRecoilValue(scenarioIdState)

  const { scenario } = useScenarioById({ scenarioId })

  const [isSaveBlocksModalOpen, setIsSaveBlocksModalOpen] = useState<boolean>(false)

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
          'absolute top-5 left-1/2 -translate-x-1/2 bg-white/80 rounded-full border-2 border-primary py-3 px-10 cursor-pointer z-10 transition-opacity flex justify-center items-start gap-x-2',
          {
            'opacity-30': !isHovered,
            'opacity-100': isHovered,
          },
        )}
        type="button"
        onClick={() => {
          if (!scenario) return
          const date = new Date()
          const startDate = new Date(date)
          startDate.setMinutes(date.getMinutes() - 30)

          if (scenario.is_active === false) {
            if (window.confirm('Do you want to save the block?')) {
              // 블럭 저장 모달 실행
              setIsSaveBlocksModalOpen(true)
              return
            }
          }

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
        <AnalysisIcon className="w-[18px] mt-0.5" />
        <Text weight="medium" colorScheme="dark">
          Analysis
        </Text>
      </button>

      <HLSPlayer autoPlay controls className="h-full aspect-video" src={AppURL.streamingURL} />
      {isSaveBlocksModalOpen && (
        <SaveBlocksModal
          isOpen={isSaveBlocksModalOpen}
          close={() => {
            setIsSaveBlocksModalOpen(false)
          }}
          isMoveAnalysisPage
          isPlay={false}
        />
      )}
      {lkfsPayload && (
        <div className="absolute bottom-14 right-4 h-[200px] z-10 w-[26px]">
          <SoundBar value={lkfsPayload.M} />
        </div>
      )}
    </section>
  )
}

export default MonitorSection
