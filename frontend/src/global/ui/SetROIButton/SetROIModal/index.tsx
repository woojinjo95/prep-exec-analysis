import React, { useMemo, useRef, useState } from 'react'
import * as d3 from 'd3'
import { useRecoilValue } from 'recoil'
import { scenarioIdState, testRunIdState, videoBlobURLState } from '@global/atom'
import { Button, Modal, Text, VideoSnapshots } from '@global/ui'
import { AppURL } from '@global/constant'
import { useVideoSummary } from '@global/api/hook'
import { formatDateTo } from '@global/usecase'
import { AnalysisFrame } from '@global/api/entity'
import { useWebsocket } from '@global/hook'

import apiUrls from '@page/AnalysisPage/api/url'
import CropBox from './CropBox'
import VideoSnapshotsCursor from './VideoSnapshotsCursor'

interface SetROIModalProps {
  isOpen: boolean
  onClose: () => void
  onSave: (frame: AnalysisFrame) => void
  defaultCurrentTime?: number
  defaultROI?: AnalysisFrame['roi']
}

/**
 * ROI 설정 모달
 */
const SetROIModal: React.FC<SetROIModalProps> = ({ isOpen, onClose, onSave, defaultCurrentTime, defaultROI }) => {
  const { videoSummary } = useVideoSummary()
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const src = useRecoilValue(videoBlobURLState)

  const videoRef = useRef<HTMLVideoElement | null>(null)
  const [duration, setDuration] = useState<number | null>(null) // 단위: 초

  const [videoClientWidth, setVideoClientWidth] = useState<number | null>(null) // 비디오 크기에 맞는 비율 계산 시 사용
  const [videoClientHeight, setVideoClientHeight] = useState<number | null>(null) // 비디오 크기에 맞는 비율 계산 시 사용
  const [videoWidth, setVideoWidth] = useState<number | null>(null)
  const [videoHeight, setVideoHeight] = useState<number | null>(null)
  const [cropTwoPosX, setCropTwoPosX] = useState<[number, number] | null>(null)
  const [cropTwoPosY, setCropTwoPosY] = useState<[number, number] | null>(null)

  const { sendMessage } = useWebsocket<{ id: string; path: string; log: string }>({
    onMessage: (message) => {
      if (!videoSummary || !videoRef.current || !cropTwoPosX || !cropTwoPosY) return

      if (message.msg === 'video_snapshot_response' && message.level === 'info') {
        onSave({
          id: message.data.id,
          path: message.data.path,
          relative_time: videoRef.current.currentTime,
          roi: {
            x: cropTwoPosX[0],
            y: cropTwoPosY[0],
            w: Math.abs(cropTwoPosX[1] - cropTwoPosX[0]),
            h: Math.abs(cropTwoPosY[1] - cropTwoPosY[0]),
          },
        })
        onClose()
      }
    },
  })

  const timestampScaleX: d3.ScaleTime<number, number, never> | null = useMemo(() => {
    if (!videoSummary) return null
    return d3.scaleTime().domain([new Date(videoSummary.start_time), new Date(videoSummary.end_time)])
  }, [])

  const onClickSave = () => {
    if (!videoSummary || !videoRef.current) return

    sendMessage({
      msg: 'video_snapshot',
      data: {
        video_path: videoSummary.path,
        relative_time: videoRef.current.currentTime,
      },
    })
  }

  if (!isOpen || !videoSummary) return null
  return (
    <Modal isOpen={isOpen} close={onClose} title="Set ROI" className="w-[60vw]">
      <div className="flex flex-col items-center h-full">
        <div
          className="relative"
          ref={(ref) => {
            // video 렌더링 전
            if (!ref || videoWidth === null || videoHeight === null) return
            // 이미 넓이, 높이를 구했을 경우
            if (videoClientWidth !== null || cropTwoPosX !== null) return

            setVideoClientWidth(ref.clientWidth)
            setVideoClientHeight(ref.clientHeight)
            if (defaultROI) {
              setCropTwoPosX([defaultROI.x, defaultROI.x + defaultROI.w])
              setCropTwoPosY([defaultROI.y, defaultROI.y + defaultROI.h])
            } else {
              setCropTwoPosX([0, ref.clientWidth / 2])
              setCropTwoPosY([0, ref.clientHeight / 2])
            }
          }}
        >
          {scenarioId && testRunId && (
            <video
              className="w-[640px]"
              ref={videoRef}
              src={`${AppURL.backendURL}${apiUrls.partial_video}?scenario_id=${scenarioId}&testrun_id=${testRunId}`}
              onLoadedData={(e) => {
                setVideoWidth(e.currentTarget.videoWidth)
                setVideoHeight(e.currentTarget.videoHeight)
                setDuration(e.currentTarget.duration)
                if (defaultCurrentTime) {
                  videoRef.current!.currentTime = defaultCurrentTime
                }
              }}
            />
          )}

          {/* background 영역, brightness 1/4배 어둡게 */}
          <div className="absolute top-0 left-0 w-full h-full backdrop-brightness-[0.25]" />
          {/* crop 영역, brightness 4배 밝게 => 원본밝기 */}
          {videoClientWidth !== null && videoClientHeight !== null && cropTwoPosX !== null && cropTwoPosY !== null && (
            <CropBox
              clientWidth={videoClientWidth}
              clientHeight={videoClientHeight}
              cropTwoPosX={cropTwoPosX}
              cropTwoPosY={cropTwoPosY}
              setCropTwoPosX={setCropTwoPosX as Parameters<typeof CropBox>[0]['setCropTwoPosX']}
              setCropTwoPosY={setCropTwoPosY as Parameters<typeof CropBox>[0]['setCropTwoPosY']}
            />
          )}
        </div>

        <div className="pt-4 w-full grid grid-cols-1 grid-rows-[auto_1fr] gap-y-1">
          <div className="flex items-center justify-between">
            {timestampScaleX?.ticks(10).map((date) => (
              <Text key={`set-roi-modal-${date.toISOString()}`} colorScheme="grey" size="xs">
                {formatDateTo('HH:MM:SS', date)}
              </Text>
            ))}
          </div>
          <div className="w-full relative">
            <VideoSnapshots
              src={src}
              startMillisecond={0}
              endMillisecond={new Date(videoSummary.end_time).getTime() - new Date(videoSummary.start_time).getTime()}
              tickCount={12}
            />
            {duration && (
              <VideoSnapshotsCursor
                startDuration={0}
                endDuration={duration}
                defaultCurrentTime={defaultCurrentTime}
                changeVideoTimeCallback={(sec) => {
                  if (!videoRef.current) return
                  videoRef.current.currentTime = sec
                }}
              />
            )}
          </div>
        </div>

        <div className="mt-10 ml-auto flex items-center gap-x-3">
          <Button colorScheme="primary" onClick={onClickSave}>
            Save
          </Button>
          <Button colorScheme="grey" onClick={onClose}>
            Cancel
          </Button>
        </div>
      </div>
    </Modal>
  )
}

export default SetROIModal
