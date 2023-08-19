import React, { useMemo, useRef } from 'react'
import * as d3 from 'd3'

import { useCreateVideo } from '@global/ui/VideoSnapshots/hook'
import { VIDEO_SNAPSHOT_HEIGHT } from '@global/ui/VideoSnapshots/constant'
import VideoSnapshot from './components/VideoSnapshot'

interface VideoSnapshotsProps {
  src: string | null
  // TODO: startTime
  // TODO: endTime
  tickCount?: number
}

/**
 * 비디오 스냅샷 리스트 컴포넌트
 *
 * @param src 비디오 주소
 */
const VideoSnapshots: React.FC<VideoSnapshotsProps> = ({ src, tickCount = 10 }) => {
  const divRef = useRef<HTMLDivElement | null>(null)
  const { isLoadedVideo, videoRef } = useCreateVideo({ src, currentTime: 0 })
  // 비디오 스냅샷 넓이
  const videoSnapshotWidth = useMemo(() => {
    if (!isLoadedVideo || !videoRef.current) return null
    return (VIDEO_SNAPSHOT_HEIGHT * videoRef.current.videoWidth) / videoRef.current.videoHeight
  }, [isLoadedVideo])
  const scaleX: d3.ScaleLinear<number, number, never> | null = useMemo(() => {
    if (!isLoadedVideo || !videoRef.current || !divRef.current || !videoSnapshotWidth) return null
    return d3
      .scaleLinear()
      .domain([0, Math.floor(videoRef.current?.duration)])
      .range([0, divRef.current.clientWidth - videoSnapshotWidth])
  }, [isLoadedVideo])

  if (!src) return <div />
  return (
    <div ref={divRef} className="relative" style={{ height: VIDEO_SNAPSHOT_HEIGHT }}>
      {isLoadedVideo &&
        scaleX?.ticks(tickCount).map((currentTime) => {
          return (
            <VideoSnapshot
              key={`snapshot-${currentTime}`}
              currentTime={currentTime}
              translateX={scaleX(currentTime)}
              videoRef={videoRef}
            />
          )
        })}
    </div>
  )
}

export default VideoSnapshots
