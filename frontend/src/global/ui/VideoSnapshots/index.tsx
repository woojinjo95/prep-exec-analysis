import React, { useMemo, useState } from 'react'
import * as d3 from 'd3'

import { VIDEO_SNAPSHOT_HEIGHT } from '@global/ui/VideoSnapshots/constant'
import VideoSnapshot from './components/VideoSnapshot'

interface VideoSnapshotsProps {
  startMillisecond: number | null
  endMillisecond: number | null
  tickCount?: number
  src: string | null
}

/**
 * 비디오 스냅샷 리스트 컴포넌트
 *
 * @param src 비디오 주소
 */
const VideoSnapshots: React.FC<VideoSnapshotsProps> = ({ startMillisecond, endMillisecond, tickCount = 10, src }) => {
  const [clientWidth, setClientWidth] = useState<number | null>(null)

  // video x축 scale
  const scaleX: d3.ScaleLinear<number, number, never> | null = useMemo(() => {
    if (startMillisecond === null || endMillisecond === null || !clientWidth) return null
    return d3
      .scaleLinear()
      .domain([startMillisecond / 1000, endMillisecond / 1000])
      .range([0, clientWidth])
  }, [startMillisecond, endMillisecond, clientWidth])

  return (
    <div
      ref={(ref) => {
        if (!ref || clientWidth !== null) return
        setClientWidth(ref.clientWidth)
      }}
      className="relative overflow-hidden"
      style={{ height: VIDEO_SNAPSHOT_HEIGHT }}
    >
      {src &&
        scaleX?.ticks(tickCount).map((currentTime) => {
          return (
            <VideoSnapshot
              key={`snapshot-${currentTime}`}
              currentTime={currentTime}
              translateX={scaleX(currentTime)}
              src={src}
            />
          )
        })}
    </div>
  )
}

export default VideoSnapshots
