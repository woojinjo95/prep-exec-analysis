import React, { useCallback, useEffect, useRef, useState } from 'react'
import { useRecoilValue } from 'recoil'
import { useNavigate } from 'react-router-dom'
import { ReactComponent as GoToFirstIcon } from '@assets/images/icon_go_to_first_w.svg'
import { ReactComponent as StepBackIcon } from '@assets/images/icon_step_back_1sec_w.svg'
import { ReactComponent as PlayIcon } from '@assets/images/icon_play.svg'
import { ReactComponent as StepForwardIcon } from '@assets/images/icon_step_forward_1sec_w.svg'
import { ReactComponent as GoToLastIcon } from '@assets/images/icon_go_to_last_w.svg'
import { ReactComponent as StopIcon } from '@assets/images/icon_stop.svg'
import { ReactComponent as RealTimeScreenIcon } from '@assets/images/icon_realtime_screen.svg'
import { IconButton, Skeleton, Text } from '@global/ui'
import { cursorDateTimeState, scenarioIdState, testRunIdState } from '@global/atom'
import { AppURL } from '@global/constant'
import apiUrls from '@page/AnalysisPage/api/url'
import { useVideoSummary } from '@global/api/hook'
import { delay } from '@global/usecase'
import { useWebsocket } from '@global/hook'

/**
 * 간격 시간을 표현하는 함수
 *
 * @param time 단위: s
 * @example 07:20.5
 */
const convertTime = (time: number) => {
  const minute = Math.floor(time / 60)
  const second = Math.floor(time % 60)
  const millisecond = Math.floor((time % 1) * 10)

  return `${minute < 10 ? `0${minute}` : minute}:${second < 10 ? `0${second}` : second}.${millisecond}`
}

/**
 * 결과영상 및 정보 영역
 */
const VideoDetailSection: React.FC = () => {
  const navigate = useNavigate()
  const videoRef = useRef<HTMLVideoElement | null>(null)
  const scenarioId = useRecoilValue(scenarioIdState)
  const testRunId = useRecoilValue(testRunIdState)
  const [isPlaying, setIsPlaying] = useState<boolean>(false)
  const [isVideoLoaded, setIsVideoLoaded] = useState<boolean>(false)
  const [currentTime, setCurrentTime] = useState<number>(0)
  const [duration, setDuration] = useState<number>(0)
  const cursorDateTime = useRecoilValue(cursorDateTimeState)
  const { videoSummary } = useVideoSummary()

  // 커서 시간이 변경될 경우 -> 비디오 엘리먼트에 시간 반영
  useEffect(() => {
    if (!videoSummary || !cursorDateTime || !videoRef.current) return

    const newCurrentTime = (cursorDateTime.getTime() - new Date(videoSummary.start_time).getTime()) / 1000
    setCurrentTime(newCurrentTime)
    videoRef.current.currentTime = newCurrentTime
  }, [cursorDateTime])

  const reloadVideo = useCallback(async () => {
    if (!videoRef.current) return

    await delay(2)
    videoRef.current.load()
  }, [])

  const { sendMessage } = useWebsocket()

  return (
    <section className="bg-black text-white grid grid-rows-1 grid-cols-[1fr_1.5fr_1fr]">
      <div className="flex flex-col justify-end py-5 px-6 gap-y-4">
        <button
          type="button"
          className="bg-[#FFFFFFCC] py-3 px-6 flex items-center justify-center absolute top-5 left-6 rounded-full border-2 border-primary cursor-pointer z-10 transition-opacity opacity-50 hover:opacity-100"
          onClick={() => {
            sendMessage({
              level: 'info',
              msg: 'action_mode',
            })
            navigate('/action')
          }}
        >
          <RealTimeScreenIcon className="w-[18px] h-[15px] mr-2" />
          <Text colorScheme="dark" weight="medium">
            Real-time Screen
          </Text>
        </button>

        <Text colorScheme="light" weight="medium">
          {convertTime(currentTime)} / {convertTime(duration)}
        </Text>
        <div className="flex flex-wrap items-center gap-2">
          <IconButton
            colorScheme="charcoal"
            icon={<GoToFirstIcon />}
            onClick={() => {
              if (!videoRef.current) return
              videoRef.current.currentTime = 0
            }}
            disabled={!isVideoLoaded}
          />
          <IconButton
            colorScheme="charcoal"
            icon={<StepBackIcon />}
            onClick={() => {
              if (!videoRef.current) return
              videoRef.current.currentTime = Math.max(videoRef.current.currentTime - 1, 0)
            }}
            disabled={!isVideoLoaded}
          />
          {isPlaying && (
            <IconButton
              colorScheme="charcoal"
              icon={<StopIcon />}
              onClick={() => {
                if (!videoRef.current) return
                videoRef.current.pause()
              }}
              disabled={!isVideoLoaded}
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
              disabled={!isVideoLoaded}
            />
          )}
          <IconButton
            colorScheme="charcoal"
            icon={<StepForwardIcon />}
            onClick={() => {
              if (!videoRef.current) return
              videoRef.current.currentTime = Math.min(videoRef.current.currentTime + 1, videoRef.current.duration)
            }}
            disabled={!isVideoLoaded}
          />
          <IconButton
            colorScheme="charcoal"
            icon={<GoToLastIcon />}
            onClick={() => {
              if (!videoRef.current) return
              videoRef.current.currentTime = videoRef.current.duration
            }}
            disabled={!isVideoLoaded}
          />
        </div>
      </div>

      <div className="aspect-video">
        {!isVideoLoaded && (
          <Skeleton className="h-full aspect-video" colorScheme="dark">
            <video className="h-full" />
          </Skeleton>
        )}

        {scenarioId && testRunId && (
          <video
            ref={videoRef}
            className="h-full aspect-video"
            src={`${AppURL.backendURL}${apiUrls.partial_video}?scenario_id=${scenarioId}&testrun_id=${testRunId}`}
            muted
            loop={false}
            onPlay={() => setIsPlaying(true)}
            onPause={() => setIsPlaying(false)}
            onLoadedData={() => {
              if (!videoRef.current) return
              setIsVideoLoaded(true)
              setCurrentTime(videoRef.current.currentTime)
              setDuration(videoRef.current.duration)
            }}
            onTimeUpdate={() => {
              if (!videoRef.current) return
              setCurrentTime(videoRef.current.currentTime)
            }}
            onError={() => {
              setIsVideoLoaded(false)
              reloadVideo()
            }}
          />
        )}
      </div>

      {/* FIXME: 타임라인 tick 부분에서 시간 크롭, 결과 export 기능. MVP2 에서 개발 */}
      <div className="ml-auto mt-auto py-4 px-3">
        {/* <Button colorScheme="charcoal" className="w-[132px]">
          Save
        </Button> */}
      </div>
    </section>
  )
}

export default VideoDetailSection
