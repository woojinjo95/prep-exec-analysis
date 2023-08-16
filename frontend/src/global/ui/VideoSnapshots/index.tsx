import React, { useMemo, useRef } from 'react'
import * as d3 from 'd3'

import { useCreateVideo } from '@global/ui/VideoSnapshots/hook'
import { VIDEO_SNAPSHOT_HEIGHT } from '@global/ui/VideoSnapshots/constant'
import VideoSnapshot from './components/VideoSnapshot'

interface VideoSnapshotsProps {
  src: string
  // TODO: startTime
  // TODO: endTime
}

/**
 * 비디오 스냅샷 리스트 컴포넌트
 *
 * @param src 비디오 주소
 */
const VideoSnapshots: React.FC<VideoSnapshotsProps> = ({ src }) => {
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

  return (
    <div ref={divRef} className="relative mt-1" style={{ height: VIDEO_SNAPSHOT_HEIGHT }}>
      {scaleX?.ticks(10).map((currentTime) => {
        return (
          <VideoSnapshot
            key={`snapshot-${currentTime}`}
            src={src}
            currentTime={currentTime}
            translateX={scaleX(currentTime)}
          />
        )
      })}
      {/* {range(0, 100, 10).map((num) => (
        <VideoSnapshot key={`snapshot-${num}`} src={src} translateX={num * 6} />
      ))} */}
    </div>
  )
}

export default VideoSnapshots
