import React, { useMemo, useRef, useState } from 'react'
import { ReactComponent as GoToFirstIcon } from '@assets/images/icon_go_to_first_w.svg'
import { ReactComponent as StepBackIcon } from '@assets/images/icon_step_back_1sec_w.svg'
import { ReactComponent as PlayIcon } from '@assets/images/icon_play.svg'
import { ReactComponent as StepForwardIcon } from '@assets/images/icon_step_forward_1sec_w.svg'
import { ReactComponent as GoToLastIcon } from '@assets/images/icon_go_to_last_w.svg'
import { ReactComponent as StopIcon } from '@assets/images/icon_stop.svg'
import { Button, IconButton, Text } from '@global/ui'
import AppURL from '@global/constant/appURL'
import { useScenarios } from '@global/api/hook'

/**
 * 결과영상 및 정보 영역
 */
const VideoDetailSection: React.FC = () => {
  const videoRef = useRef<HTMLVideoElement | null>(null)
  const [isPlaying, setIsPlaying] = useState<boolean>(false)
  const [currentTime, setCurrentTime] = useState<number>(0)
  const [scenarioId, setScenarioId] = useState<string | null>(null)
  /**
   * @example 07:20.5
   */
  const currentTimeLabel = useMemo(() => {
    const minute = Math.floor(currentTime / 60)
    const second = Math.floor(currentTime % 60)
    const millisecond = Math.floor((currentTime % 1) * 10)

    return `${minute < 10 ? `0${minute}` : minute}:${second < 10 ? `0${second}` : second}.${millisecond}`
  }, [currentTime])

  useScenarios({
    onSuccess: (res) => {
      if (res && res.items.length > 0) {
        setScenarioId(res.items[0].id)
      }
    },
  })

  return (
    <section className="bg-black text-white grid grid-rows-1 grid-cols-[1fr_1.5fr_1fr]">
      <div className="flex flex-col justify-end py-5 px-6 gap-y-4">
        <Text colorScheme="light" weight="medium">
          {currentTimeLabel}
        </Text>
        <div className="flex flex-wrap items-center gap-2">
          <IconButton
            colorScheme="charcoal"
            icon={<GoToFirstIcon />}
            onClick={() => {
              if (!videoRef.current) return
              videoRef.current.currentTime = 0
            }}
          />
          <IconButton
            colorScheme="charcoal"
            icon={<StepBackIcon />}
            onClick={() => {
              if (!videoRef.current) return
              videoRef.current.currentTime = Math.max(videoRef.current.currentTime - 1, 0)
            }}
          />
          {isPlaying && (
            <IconButton
              colorScheme="charcoal"
              icon={<StopIcon />}
              onClick={() => {
                if (!videoRef.current) return
                videoRef.current.pause()
              }}
            />
          )}
          {!isPlaying && (
            <IconButton
              colorScheme="charcoal"
              icon={<PlayIcon />}
              onClick={() => {
                if (!videoRef.current) return
                videoRef.current.play()
              }}
            />
          )}
          <IconButton
            colorScheme="charcoal"
            icon={<StepForwardIcon />}
            onClick={() => {
              if (!videoRef.current) return
              videoRef.current.currentTime = Math.min(videoRef.current.currentTime + 1, videoRef.current.duration)
            }}
          />
          <IconButton
            colorScheme="charcoal"
            icon={<GoToLastIcon />}
            onClick={() => {
              if (!videoRef.current) return
              videoRef.current.currentTime = videoRef.current.duration
            }}
          />
        </div>
      </div>

      <div className="aspect-video">
        {scenarioId && (
          <video
            ref={videoRef}
            className="h-full aspect-video"
            src={`${AppURL.backendURL}/api/v1/video?scenario_id=${scenarioId}`}
            muted
            controls
            loop={false}
            onPlay={() => setIsPlaying(true)}
            onPause={() => setIsPlaying(false)}
            onLoadedData={() => {
              if (!videoRef.current) return
              setCurrentTime(videoRef.current.currentTime)
            }}
            onTimeUpdate={() => {
              if (!videoRef.current) return
              setCurrentTime(videoRef.current.currentTime)
            }}
          />
        )}
      </div>

      {/* FIXME: 버튼의 의미(동영상 다운로드?) */}
      <div className="ml-auto mt-auto py-4 px-3">
        <Button colorScheme="charcoal">Save</Button>
      </div>
    </section>
  )
}

export default VideoDetailSection
