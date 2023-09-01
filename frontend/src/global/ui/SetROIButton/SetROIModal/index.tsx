import React, { useMemo, useRef, useState } from 'react'
import * as d3 from 'd3'
import { useRecoilValue } from 'recoil'
import { scenarioIdState, testRunIdState, videoBlobURLState } from '@global/atom'
import { Button, Modal, Text, VideoSnapshots } from '@global/ui'
import { AppURL } from '@global/constant'
import { useVideoTimestamp } from '@global/api/hook'

import apiUrls from '@page/AnalysisPage/api/url'
import { formatDateTo } from '@global/usecase'
import CropBox from './CropBox'
import VideoSnapshotsCursor from './VideoSnapshotsCursor'

interface SetROIModalProps {
  isOpen: boolean
  onClose: () => void
}

/**
 * ROI 설정 모달
 */
const SetROIModal: React.FC<SetROIModalProps> = ({ isOpen, onClose }) => {
  const { videoTimestamp } = useVideoTimestamp()
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const src = useRecoilValue(videoBlobURLState)

  const videoRef = useRef<HTMLVideoElement | null>(null)
  const [duration, setDuration] = useState<number | null>(null) // 단위: 초

  const [videoClientWidth, setVideoClientWidth] = useState<number | null>(null) // 비디오 크기에 맞는 비율 계산 시 사용
  const [videoClientHeight, setVideoClientHeight] = useState<number | null>(null) // 비디오 크기에 맞는 비율 계산 시 사용
  const [videoWidth, setVideoWidth] = useState<number | null>(null)
  const [videoHeight, setVideoHeight] = useState<number | null>(null)
  const [cropWidth, setCropWidth] = useState<number | null>(null)
  const [cropHeight, setCropHeight] = useState<number | null>(null)

  const timestampScaleX: d3.ScaleTime<number, number, never> | null = useMemo(() => {
    if (!videoTimestamp) return null
    return d3.scaleTime().domain([new Date(videoTimestamp.start_time), new Date(videoTimestamp.end_time)])
  }, [])

  if (!isOpen || !videoTimestamp) return null
  return (
    <Modal isOpen={isOpen} close={onClose} title="Set ROI" className="w-[60vw]">
      <div className="flex flex-col items-center h-full">
        <div
          className="relative"
          ref={(ref) => {
            // video 렌더링 전
            if (!ref || videoWidth === null || videoHeight === null) return
            // 이미 넓이, 높이를 구했을 경우
            if (videoClientWidth !== null || cropWidth !== null) return

            setVideoClientWidth(ref.clientWidth)
            setVideoClientHeight(ref.clientHeight)
            setCropWidth(ref.clientWidth / 2)
            setCropHeight(ref.clientHeight / 2)
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
              }}
            />
          )}

          {/* background 영역, brightness 1/4배 어둡게 */}
          <div className="absolute top-0 left-0 w-full h-full backdrop-brightness-[0.25]" />
          {/* crop 영역, brightness 4배 밝게 => 원본밝기 */}
          {cropWidth !== null && cropHeight !== null && videoClientWidth !== null && videoClientHeight !== null && (
            <CropBox
              clientWidth={videoClientWidth}
              clientHeight={videoClientHeight}
              cropTwoPosX={[0, cropWidth]}
              cropTwoPosY={[0, cropHeight]}
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
              endMillisecond={
                new Date(videoTimestamp.end_time).getTime() - new Date(videoTimestamp.start_time).getTime()
              }
              tickCount={12}
            />
            {duration && (
              <VideoSnapshotsCursor
                startDuration={0}
                endDuration={duration}
                changeVideoTimeCallback={(sec) => {
                  if (!videoRef.current) return
                  videoRef.current.currentTime = sec
                }}
              />
            )}
          </div>
        </div>

        <div className="mt-10 ml-auto flex items-center gap-x-3">
          {/* TODO: save 로직 */}
          <Button colorScheme="primary">Save</Button>
          <Button colorScheme="grey" onClick={onClose}>
            Cancel
          </Button>
        </div>
      </div>
    </Modal>
  )
}

export default SetROIModal
